# -*- coding: utf-8 -*-
"""
飞书 发送提醒服务

职责：
1. 通过 webhook 发送飞书消息
2. 通过 API（App ID + Secret）发送飞书消息
"""
import base64
import hashlib
import hmac
import json
import logging
import time
import uuid as uuid_mod
from pathlib import Path
from typing import Any, Dict, Optional

import requests

from src.config import Config
from src.formatters import (
    MIN_MAX_BYTES,
    PAGE_MARKER_SAFE_BYTES,
    chunk_content_by_max_bytes,
    format_feishu_markdown,
)


logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# lark-oapi SDK availability
# ---------------------------------------------------------------------------

FEISHU_SDK_AVAILABLE = False
_lark: Any = None  # type: ignore[assignment]
FEISHU_DOMAIN = "feishu"
LARK_DOMAIN = "lark"
try:
    import lark_oapi as _lark
    from lark_oapi.api.im.v1 import (
        CreateMessageRequest,
        CreateMessageRequestBody,
    )
    from lark_oapi.core.const import FEISHU_DOMAIN as _SDK_FEISHU_DOMAIN
    from lark_oapi.core.const import LARK_DOMAIN as _SDK_LARK_DOMAIN

    FEISHU_DOMAIN = _SDK_FEISHU_DOMAIN
    LARK_DOMAIN = _SDK_LARK_DOMAIN
    FEISHU_SDK_AVAILABLE = True
except ImportError:
    pass

# File-upload SDK classes (isolated from the core messaging SDK availability
# so that an older lark-oapi without file support doesn't break App Bot text).
FEISHU_FILE_SDK_AVAILABLE = False
_CreateFileRequest: Any = None
_CreateFileRequestBody: Any = None
try:
    from lark_oapi.api.im.v1 import (
        CreateFileRequest as _CreateFileRequest,
        CreateFileRequestBody as _CreateFileRequestBody,
    )
    FEISHU_FILE_SDK_AVAILABLE = True
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_APP_SEND_RETRIES = 3
_APP_SEND_BACKOFF_SECONDS = (1.0, 2.0, 4.0)
_WEBHOOK_SEND_TIMEOUT_SECONDS = 30

# Sentinel for "client not yet initialised".
_NO_CLIENT = object()


class FeishuSender:
    
    def __init__(self, config: Config):
        """
        初始化飞书配置

        Args:
            config: 配置对象
        """
        # -- Webhook mode --
        self._feishu_url = getattr(config, "feishu_webhook_url", None)
        self._feishu_secret = (getattr(config, "feishu_webhook_secret", None) or "").strip()
        self._feishu_keyword = (getattr(config, "feishu_webhook_keyword", None) or "").strip()
        self._feishu_max_bytes = getattr(config, "feishu_max_bytes", 20000)
        self._feishu_send_as_file = getattr(config, "feishu_send_as_file", False)
        self._webhook_verify_ssl = getattr(config, "webhook_verify_ssl", True)

        # -- App Bot mode --
        self._feishu_app_id = (getattr(config, "feishu_app_id", None) or "").strip()
        self._feishu_app_secret = (getattr(config, "feishu_app_secret", None) or "").strip()
        self._feishu_chat_id = (getattr(config, "feishu_chat_id", None) or "").strip()
        self._feishu_receive_id_type = (
            getattr(config, "feishu_receive_id_type", None) or "chat_id"
        ).strip().lower()
        if self._feishu_receive_id_type not in ("chat_id", "open_id"):
            logger.warning(
                "无效的 FEISHU_RECEIVE_ID_TYPE=%s，回退为 chat_id",
                self._feishu_receive_id_type,
            )
            self._feishu_receive_id_type = "chat_id"
        # domain_name must be "feishu" or "lark"; anything else defaulted to feishu.
        raw_domain = (
            getattr(config, "feishu_domain", None) or os.getenv("FEISHU_DOMAIN", "feishu")
        ).strip().lower()
        if raw_domain not in ("feishu", "lark"):
            logger.warning(
                "无效的 FEISHU_DOMAIN=%s，回退为 feishu", raw_domain
            )
            raw_domain = "feishu"
        self._feishu_domain = FEISHU_DOMAIN if raw_domain == "feishu" else LARK_DOMAIN

        self._app_client: Any = _NO_CLIENT
        self._app_client_lock = threading.Lock()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_card_body(content: str) -> dict:
        """Build a Feishu interactive-card body (without the ``msg_type`` wrapper)."""
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "股票智能分析报告"},
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": content},
                }
            ],
        }

    # ------------------------------------------------------------------
    # Webhook helpers (unchanged legacy path)
    # ------------------------------------------------------------------

    def _get_keyword_prefix(self) -> str:
        """Return the keyword prefix required by Feishu webhook security settings."""
        if not self._feishu_keyword:
            return ""
        return f"{self._feishu_keyword}\n"

    def _apply_keyword_prefix(self, content: str) -> str:
        """Prepend the optional keyword so each webhook request passes keyword checks."""
        prefix = self._get_keyword_prefix()
        if not prefix:
            return content
        return f"{prefix}{content}" if content else self._feishu_keyword

    def _build_security_fields(self) -> Dict[str, str]:
        """Build optional signing fields required by Feishu custom robot security."""
        if not self._feishu_secret:
            return {}

        timestamp = str(int(time.time()))
        string_to_sign = f"{timestamp}\n{self._feishu_secret}"
        sign = base64.b64encode(
            hmac.new(
                string_to_sign.encode('utf-8'),
                digestmod=hashlib.sha256,
            ).digest()
        ).decode('utf-8')
        return {
            "timestamp": timestamp,
            "sign": sign,
        }
    
    def _get_tenant_access_token(self) -> Optional[str]:
        """获取 tenant_access_token，使用缓存避免频繁请求"""
        # 缓存未过期直接返回
        if self._tenant_access_token and time.time() < self._token_expires_at:
            return self._tenant_access_token

        if not self._feishu_app_id or not self._feishu_app_secret:
            logger.warning("飞书 APP_ID 或 APP_SECRET 未配置，无法获取 tenant_access_token")
            return None

        try:
            url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            payload = {
                "app_id": self._feishu_app_id,
                "app_secret": self._feishu_app_secret,
            }
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    self._tenant_access_token = result.get('tenant_access_token')
                    # 提前5分钟过期，留出缓冲时间
                    expire_in = result.get('expire', 7200) - 300
                    self._token_expires_at = time.time() + expire_in
                    logger.info("成功获取飞书 tenant_access_token")
                    return self._tenant_access_token
                else:
                    logger.error(f"获取 tenant_access_token 失败: {result}")
            else:
                logger.error(f"获取 tenant_access_token HTTP 错误: {response.status_code}")
        except Exception as e:
            logger.error(f"获取 tenant_access_token 异常: {e}")

        return None

    def _send_via_api(self, content: str, *, timeout_seconds: Optional[float] = None) -> bool:
        """
        通过飞书 API（App ID + Secret）发送单条消息

        Args:
            content: 消息内容（lark_md 格式）
            timeout_seconds: 超时秒数

        Returns:
            是否发送成功
        """
        if not self._feishu_chat_id:
            logger.warning("飞书 USER_OPEN_ID 未配置，无法通过 API 发送消息")
            return False

        token = self._get_tenant_access_token()
        if not token:
            return False

        try:
            url = "https://open.feishu.cn/open-apis/im/v1/messages"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
            # 使用 interactive 卡片（msg_type 指定），不需要外层 type/card 包装
            # 内部 div > lark_md 是支持的组合（实测通过）
            card_elements = []
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                card_elements.append({
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": para
                    }
                })

            payload = {
                "receive_id": self._feishu_chat_id,
                "msg_type": "interactive",
                "content": json.dumps({
                    "config": {"wide_screen_mode": True},
                    "header": {
                        "title": {
                            "tag": "plain_text",
                            "content": "📊 股票智能分析报告"
                        },
                        "template": "blue"
                    },
                    "elements": card_elements
                }, ensure_ascii=False),
            }
            params = {"receive_id_type": "open_id"}

            response = requests.post(url, headers=headers, json=payload, params=params, timeout=timeout_seconds or 30)

            if response.status_code == 200:
                result = response.json()
                code = result.get('code') if 'code' in result else result.get('StatusCode')
                if code == 0:
                    logger.info("飞书 API 消息发送成功")
                    return True
                else:
                    error_msg = result.get('msg') or '未知错误'
                    error_code = result.get('code', 'N/A')
                    logger.error(f"飞书 API 返回错误 [code={error_code}]: {error_msg}")
                    # 如果是 token 过期，清除缓存下次重试
                    if error_code == 99991663:
                        self._tenant_access_token = None
                        self._token_expires_at = 0
                    return False
            else:
                logger.error(f"飞书 API 请求失败: HTTP {response.status_code}")
                logger.error(f"响应内容: {response.text}")
                return False

        except Exception as e:
            logger.error(f"飞书 API 发送异常: {e}")
            return False

    def _send_feishu_api_chunked(self, content: str, *, timeout_seconds: Optional[float] = None) -> bool:
        """
        通过飞书 API 发送消息（支持分片）

        Args:
            content: 消息内容
            timeout_seconds: 超时秒数

        Returns:
            是否发送成功
        """
        # 格式化为飞书 Markdown
        formatted_content = format_feishu_markdown(content)
        
        # 如果内容超长，分片发送
        content_bytes = len(formatted_content.encode('utf-8'))
        max_bytes = self._feishu_max_bytes

        if content_bytes > max_bytes:
            logger.info(f"飞书 API 消息内容超长({content_bytes}字节)，将分片发送")
            try:
                chunks = chunk_content_by_max_bytes(formatted_content, max_bytes, add_page_marker=True)
            except ValueError as e:
                logger.error(f"飞书消息分片失败: {e}")
                return False

            success_count = 0
            total_chunks = len(chunks)
            for i, chunk in enumerate(chunks):
                if self._send_via_api(chunk, timeout_seconds=timeout_seconds):
                    success_count += 1
                    logger.info(f"飞书 API 第 {i+1}/{total_chunks} 片发送成功")
                else:
                    logger.error(f"飞书 API 第 {i+1}/{total_chunks} 片发送失败")
                if i < total_chunks - 1:
                    time.sleep(1)

            return success_count == total_chunks
        else:
            return self._send_via_api(formatted_content, timeout_seconds=timeout_seconds)

    def send_to_feishu(self, content: str, *, timeout_seconds: Optional[float] = None) -> bool:
        """
        推送消息到飞书机器人

        发送策略：
        1. 优先使用 Webhook（如果已配置）
        2. 回退使用 API 模式（App ID + Secret + User Open ID）

        Args:
            content: 消息内容（Markdown 会转为纯文本）
            timeout_seconds: 超时秒数

        Returns:
            是否发送成功
        """
        # 优先尝试 Webhook 模式
        if self._feishu_url:
            return self._send_feishu_webhook(content, timeout_seconds=timeout_seconds)

        # 回退到 API 模式
        if self._feishu_app_id and self._feishu_app_secret and self._feishu_chat_id:
            logger.info("Webhook 未配置，使用 API 模式发送飞书消息")
            return self._send_feishu_api_chunked(content, timeout_seconds=timeout_seconds)

    def send_feishu_file(self, file_path: str) -> bool:
        """
        Upload and send a file to the Feishu chat.

        .. note::

           * **App Bot mode** – uploads the file via the lark-oapi SDK and
             sends it as a file message.  This is the recommended path.
           * **Webhook mode** – reads the file content and sends it as a
             regular text/card message (webhooks do not support file upload).

        Args:
            file_path: Absolute or relative path to the local file.

        Returns:
            Whether the send succeeded.
        """
        path = Path(file_path)
        if not path.is_file():
            logger.error("send_feishu_file: 文件不存在: %s", file_path)
            return False

        if self._feishu_url:
            # Webhook mode: send file content as a message (best-effort).
            return self._send_file_via_webhook(path)

        # App Bot mode: upload file via SDK.
        return self._send_file_via_app_bot(path)

    def _send_file_via_app_bot(self, path: Path) -> bool:
        """Upload *path* to Feishu via App Bot SDK and send as file message."""
        if not FEISHU_FILE_SDK_AVAILABLE:
            logger.warning("lark-oapi SDK does not support file upload; upgrade lark-oapi")
            return False

        if not self._feishu_chat_id:
            logger.warning("FEISHU_CHAT_ID 未配置，跳过 App Bot 文件推送")
            return False

        client = self._ensure_app_client()
        if client is None:
            return False

        file_name = path.name
        # Determine file_type from extension; fall back to "stream" for unknown types.
        feishu_file_types = {
            ".opus": "opus", ".aac": "aac", ".amr": "amr", ".mp3": "mp3",
            ".wma": "wma", ".pcm": "pcm", ".wav": "wav",
            ".mp4": "mp4", ".gif": "gif",
            ".pdf": "pdf",
            ".doc": "doc", ".docx": "docx",
            ".xls": "xls", ".xlsx": "xlsx",
            ".ppt": "ppt", ".pptx": "pptx",
        }
        file_type = feishu_file_types.get(path.suffix.lower(), "stream")

        try:
            with path.open("rb") as f:
                body = (
                    _CreateFileRequestBody.builder()
                    .file_type(file_type)
                    .file_name(file_name)
                    .file(f)  # type: ignore[arg-type]
                    .build()
                )
                req = (
                    _CreateFileRequest.builder()
                    .request_body(body)
                    .build()
                )
                resp = client.im.v1.file.create(req)
        except Exception as e:
            logger.error("App Bot 文件上传异常: %s: %s", type(e).__name__, e)
            return False

        if not resp.success():
            try:
                log_id = resp.get_log_id()
            except (AttributeError, Exception):
                log_id = "N/A"
            logger.error(
                "App Bot 文件上传失败: code=%s, msg=%s, log_id=%s",
                resp.code, resp.msg, log_id,
            )
            return False

        file_key = resp.data.file_key if resp.data else None
        if not file_key:
            logger.error("App Bot 文件上传成功但未返回 file_key")
            return False

        logger.info("App Bot 文件上传成功: file_key=%s, file_name=%s", file_key, file_name)

        # Send a file message with the uploaded file_key.
        content_json = json.dumps({"file_key": file_key})
        return self._app_send_raw(client, "file", content_json)

    @staticmethod
    def _guess_mime_for_webhook(path: Path) -> str:
        """Determine a human-readable label for webhook fallback."""
        suffix = path.suffix.lower()
        labels = {".md": "Markdown", ".txt": "文本", ".pdf": "PDF", ".csv": "CSV"}
        return labels.get(suffix, suffix.lstrip(".").upper() or "文件")

    def _send_file_via_webhook(self, path: Path) -> bool:
        """Send file *content* as a Feishu message (webhook fallback)."""
        try:
            text = path.read_text("utf-8")
        except (OSError, UnicodeDecodeError) as e:
            logger.error("读取文件内容失败 (webhook fallback): %s: %s", type(e).__name__, e)
            return False

        file_label = self._guess_mime_for_webhook(path)
        header = f"**📄 {file_label} 文件内容: {path.name}**\n\n"
        content = header + text
        # Delegate to the existing webhook send path.
        return self._send_via_webhook(content)

    # ------------------------------------------------------------------
    # Webhook path (legacy, unchanged)
    # ------------------------------------------------------------------

        logger.warning("飞书 Webhook 和 API 均未配置，跳过推送")
        return False

    def _send_feishu_webhook(self, content: str, *, timeout_seconds: Optional[float] = None) -> bool:
        """通过 Webhook 发送飞书消息"""
        formatted_content = format_feishu_markdown(content)
        max_bytes = self._feishu_max_bytes
        keyword_overhead = len(self._get_keyword_prefix().encode('utf-8'))
        effective_max_bytes = max_bytes - keyword_overhead

        if effective_max_bytes <= 0:
            logger.error("飞书关键词过长，超过单条消息允许的最大字节数，无法发送")
            return False

        content_bytes = len(formatted_content.encode('utf-8')) + keyword_overhead
        if content_bytes > max_bytes:
            min_chunk_bytes = MIN_MAX_BYTES + PAGE_MARKER_SAFE_BYTES
            if effective_max_bytes < min_chunk_bytes:
                logger.error(
                    "飞书关键词过长，剩余分片预算(%s字节)不足以安全分页发送，至少需要 %s 字节",
                    effective_max_bytes,
                    min_chunk_bytes,
                )
                return False
            logger.info(f"飞书消息内容超长({content_bytes}字节/{len(content)}字符)，将分批发送")
            return self._send_feishu_webhook_chunked(formatted_content, effective_max_bytes)

        try:
            return self._send_feishu_message_webhook(formatted_content, timeout_seconds=timeout_seconds)
        except Exception as e:
            logger.error(f"发送飞书消息失败: {e}")
            return False

    def _send_feishu_webhook_chunked(self, content: str, max_bytes: int) -> bool:
        """分批发送长消息到飞书（Webhook 模式）"""
        try:
            chunks = chunk_content_by_max_bytes(content, max_bytes, add_page_marker=True)
        except ValueError as e:
            logger.error("飞书消息分片失败: %s", e)
            return False

        total_chunks = len(chunks)
        success_count = 0

        logger.info(f"飞书分批发送：共 {total_chunks} 批")

        for i, chunk in enumerate(chunks):
            try:
                if self._send_feishu_message_webhook(chunk):
                    success_count += 1
                    logger.info(f"飞书第 {i+1}/{total_chunks} 批发送成功")
                else:
                    logger.error(f"飞书第 {i+1}/{total_chunks} 批发送失败")
            except Exception as e:
                logger.error(f"飞书第 {i+1}/{total_chunks} 批发送异常: {e}")

            if i < total_chunks - 1:
                time.sleep(1)

        return success_count == total_chunks

    def _send_feishu_message_webhook(self, content: str, *, timeout_seconds: Optional[float] = None) -> bool:
        """发送单条飞书消息（Webhook 模式）"""
        prepared_content = self._apply_keyword_prefix(content)
        security_fields = self._build_security_fields()

        def _post_payload(payload: Dict[str, Any]) -> bool:
            request_payload = dict(payload)
            request_payload.update(security_fields)
            logger.debug(f"飞书请求 URL: {self._feishu_url}")
            logger.debug(f"飞书请求 payload 长度: {len(prepared_content)} 字符")

            response = requests.post(
                self._feishu_url,
                json=request_payload,
                timeout=timeout_seconds or 30,
                verify=self._webhook_verify_ssl
            )

            logger.debug(f"飞书响应状态码: {response.status_code}")
            logger.debug(f"飞书响应内容: {response.text}")

            if response.status_code == 200:
                result = response.json()
                code = result.get('code') if 'code' in result else result.get('StatusCode')
                if code == 0:
                    logger.info("飞书消息发送成功")
                    return True
                else:
                    error_msg = result.get('msg') or result.get('StatusMessage', '未知错误')
                    error_code = result.get('code') or result.get('StatusCode', 'N/A')
                    logger.error(f"飞书返回错误 [code={error_code}]: {error_msg}")
                    logger.error(f"完整响应: {result}")
                    return False
            else:
                logger.error(f"飞书请求失败: HTTP {response.status_code}")
                logger.error(f"响应内容: {response.text}")
                return False

        # 1) 优先使用交互卡片（支持 Markdown 渲染）
        card_payload = {
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True},
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": "股票智能分析报告"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": prepared_content
                        }
                    }
                ]
            }
        }

        if _post_payload(card_payload):
            return True

        # 2) 回退为普通文本消息
        text_payload = {
            "msg_type": "text",
            "content": {
                "text": prepared_content
            }
        }

        return _post_payload(text_payload)
