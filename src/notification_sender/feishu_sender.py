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


class FeishuSender:
    
    def __init__(self, config: Config):
        """
        初始化飞书配置

        Args:
            config: 配置对象
        """
        self._feishu_url = getattr(config, 'feishu_webhook_url', None)
        self._feishu_secret = (getattr(config, 'feishu_webhook_secret', None) or '').strip()
        self._feishu_keyword = (getattr(config, 'feishu_webhook_keyword', None) or '').strip()
        self._feishu_max_bytes = getattr(config, 'feishu_max_bytes', 20000)
        self._webhook_verify_ssl = getattr(config, 'webhook_verify_ssl', True)
        # API 模式配置（App ID + Secret + User Open ID）
        self._feishu_app_id = (getattr(config, 'feishu_app_id', None) or '').strip()
        self._feishu_app_secret = (getattr(config, 'feishu_app_secret', None) or '').strip()
        self._feishu_user_open_id = (getattr(config, 'feishu_user_open_id', None) or '').strip()
        self._tenant_access_token = None
        self._token_expires_at = 0  # token 过期时间戳

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
        if not self._feishu_user_open_id:
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
            payload = {
                "receive_id": self._feishu_user_open_id,
                "msg_type": "interactive",
                "content": json.dumps({
                    "type": "interactive",
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
                                    "content": content
                                }
                            }
                        ]
                    }
                }),
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
        if self._feishu_app_id and self._feishu_app_secret and self._feishu_user_open_id:
            logger.info("Webhook 未配置，使用 API 模式发送飞书消息")
            return self._send_feishu_api_chunked(content, timeout_seconds=timeout_seconds)

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
