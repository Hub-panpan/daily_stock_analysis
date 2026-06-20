# -*- coding: utf-8 -*-
"""
===================================
东方财富妙想 MCP 平台服务
===================================

通过东方财富 AI SaaS MCP 平台获取金融数据，提供：
1. 实体识别（股票/基金/指数代码解析）
2. 金融数据查询（财务报表/估值/技术指标/资金流向）
3. 智能选股（自然语言筛选 A/港/美/ETF/可转债/板块）
4. 金融问答（七大能力：选股/诊股/对比/资讯/观点/翻译/比价）
5. 财经资讯搜索（新闻/公告/研报）
6. 宏观经济数据（GDP/CPI/PMI/利率等）

数据来源：东方财富 Choice + 妙想 AI 平台
认证方式：EM_API_KEY（默认内置，可通过环境变量覆盖）

文档参考：https://ai.eastmoney.com/mxClaw
"""

import asyncio
import logging
import time
import uuid
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Dict, List, Optional, Tuple, Union

import httpx

logger = logging.getLogger(__name__)

# ============================================================
# 常量
# ============================================================

_BASE_URL = "https://ai-saas.eastmoney.com/proxy"

# MCP 工具接口
_URL_SEARCH_DATA = f"{_BASE_URL}/b/mcp/tool/searchData"
_URL_SEARCH_MACRO_DATA = f"{_BASE_URL}/b/mcp/tool/searchMacroData"
_URL_SELECT_SECURITY = f"{_BASE_URL}/b/mcp/tool/selectSecurity"
_URL_SEARCH_NEWS = f"{_BASE_URL}/b/mcp/tool/searchNews"
_URL_ASK = f"{_BASE_URL}/app-robo-advisor-api/assistant/ask"

# 实体识别
_URL_ENTITY_SaaS = f"{_BASE_URL}/entity/saas"

# 默认内置 Key（东方财富妙想平台公开测试 Key）
_DEFAULT_API_KEY = "em_1DCIJNVsxTjTSeb7ZfX0aocU02jiR5tL"

# 实体类型映射（参考 mx-finance-data SKILL.md）
_ENTITY_TYPE_MAP = {
    "A股": "002",
    "港股": "003",
    "基金": "001",
    "美股": "004",
    "期货": "005",
    "债券": "006",
    "指数": "007",
}

# 选股类型映射
_SELECT_TYPE_MAP = {
    "A股": "70",
    "港股": "71",
    "美股": "72",
    "ETF": "80",
    "可转债": "74",
    "板块": "75",
}

# ============================================================
# 异常
# ============================================================


class MCPError(Exception):
    """MCP 服务调用异常"""


class MCPAuthError(MCPError):
    """认证失败"""


class MCPTimeoutError(MCPError):
    """请求超时"""


class MCPDataError(MCPError):
    """数据解析异常"""


# ============================================================
# 核心服务
# ============================================================


class EastmoneyMCPService:
    """
    东方财富妙想 MCP 平台客户端

    线程安全，支持同步和异步调用。

    用法：
        service = EastmoneyMCPService()  # 使用默认内置 Key
        service = EastmoneyMCPService(api_key="your_key")  # 使用自定义 Key

        # 同步调用
        result = service.query_finance_data("贵州茅台近一年营收")

        # 异步调用
        result = await service.async_query_finance_data("贵州茅台近一年营收")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 2,
    ):
        self._api_key = api_key or _DEFAULT_API_KEY
        self._timeout = timeout
        self._max_retries = max_retries
        self._lock = Lock()

        # 统计
        self._call_count = 0
        self._error_count = 0
        self._total_latency_ms = 0

        logger.info(
            "[MCP] 东方财富妙想服务已初始化 | key_prefix=%s... | timeout=%ds",
            self._api_key[:8],
            self._timeout,
        )

    # ============================================================
    # 公共 API —— 同步
    # ============================================================

    def query_entity(self, content: str, entity_type: str = "A股") -> List[Dict[str, Any]]:
        """
        实体识别：从文本中提取金融实体（股票/基金/指数等）

        Args:
            content: 待识别文本，如 "贵州茅台"、"600519"、"沪深300ETF"
            entity_type: 实体类型（A股/港股/基金/美股/期货/债券/指数）

        Returns:
            实体列表，每个元素包含 entityId, secuCode, marketChar, fullName 等
        """
        type_code = _ENTITY_TYPE_MAP.get(entity_type, "002")
        body = {"content": content, "typeCodes": type_code}
        resp = self._request(_URL_ENTITY_SaaS, body)

        # ── DEBUG: 打印原始返回 ──
        logger.debug("[MCP] query_entity 原始返回 | content=%s | resp=%s", content, resp)

        entity_list = resp.get("data", {}).get("entityList", [])
        logger.info("[MCP] 实体识别 '%s' → %d 个实体", content, len(entity_list))
        return entity_list

    def query_finance_data(
        self,
        query: str,
        indicators: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        金融数据查询：通过自然语言获取财务/行情/技术指标数据

        Args:
            query: 自然语言查询，如 "贵州茅台近一年营收和净利润"
            indicators: 限定指标关键词（可选），如 "营收,净利润,ROE"

        Returns:
            {
                "query_rewrite": str,      # AI 理解后的查询意图
                "tables": [                # 数据表列表
                    {
                        "title": str,
                        "table": {...},      # 原始表格数据
                        "markdown": str,     # Markdown 格式表格
                    }
                ],
                "entity_list": [           # 涉及的实体
                    {"name": str, "code": str, "market": str}
                ],
                "raw": dict,               # 原始 API 响应
            }
        """
        body = {
            "query": query,
            "toolContext": self._make_tool_context(),
        }
        resp = self._request(_URL_SEARCH_DATA, body)

        # ── DEBUG: 打印原始返回 ──
        logger.debug("[MCP] query_finance_data 原始返回 | query=%s | resp=%s", query, resp)

        return self._parse_data_response(resp)

    def screen_stocks(
        self,
        query: str,
        select_type: str = "A股",
    ) -> Dict[str, Any]:
        """
        智能选股：通过自然语言筛选股票

        Args:
            query: 自然语言选股条件，如 "股价大于500元的A股"
            select_type: 筛选类型（A股/港股/美股/ETF/可转债/板块）

        Returns:
            {
                "security_count": int,     # 命中证券数量
                "columns": list,           # 列定义
                "data_list": list,         # 证券数据列表
                "partial_results": str,    # Markdown 格式结果
                "raw": dict,               # 原始 API 响应
            }
        """
        select_code = _SELECT_TYPE_MAP.get(select_type, "70")
        body = {
            "query": query,
            "selectType": select_type,
            "toolContext": self._make_tool_context(),
        }
        resp = self._request(_URL_SELECT_SECURITY, body, timeout=60.0)
        return self._parse_select_response(resp)

    def ask_question(
        self,
        question: str,
        deep_research: bool = False,
        models: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        金融问答：七大能力

        能力类型（自动识别，无需指定）：
        1. 条件选股：条件+结果，数据可回测
        2. 个股分析：基本面/技术面/消息面
        3. 对比分析：多只股票/基金/指数对比
        4. 资讯问答：公司/行业/大盘相关资讯
        5. 机构观点：研报总结
        6. 翻译转换：自然语言 ↔ 公式
        7. 比价信息：各交易所/币种价格

        Args:
            question: 自然语言问题
            deep_research: 是否启用深度研究（会搜索更全面的资料）
            models: 指定模型列表（可选）

        Returns:
            {
                "answer": str,             # AI 回答（含溯源标注 [1][2]...）
                "references": list,        # 溯源参考列表（标题/URL）
                "request_id": str,         # 请求 ID
                "raw": dict,               # 原始 API 响应
            }
        """
        body: Dict[str, Any] = {"question": question}
        if deep_research:
            body["extra"] = {"mode": "deep_research", "thinkingProcess": True}
        if models:
            body["extra"] = body.get("extra", {})
            body["extra"]["models"] = models

        resp = self._request(_URL_ASK, body, timeout=90.0)

        # ── DEBUG: 打印原始返回 ──
        logger.debug("[MCP] ask_question 原始返回 | question=%s | resp=%s", question, resp)

        return self._parse_ask_response(resp)

    def search_news(
        self,
        query: str,
        days: int = 3,
    ) -> Dict[str, Any]:
        """
        财经资讯搜索

        Args:
            query: 搜索关键词，如 "贵州茅台最新公告"
            days: 搜索时间范围（天）

        Returns:
            {
                "results": list,           # 资讯列表（标题/内容/来源/日期/URL）
                "count": int,              # 结果数量
                "raw": dict,               # 原始 API 响应
            }
        """
        body = {
            "query": query,
            "days": days,
            "toolContext": self._make_tool_context(),
        }
        resp = self._request(_URL_SEARCH_NEWS, body, timeout=60.0)

        # ── DEBUG: 打印原始返回 ──
        logger.debug("[MCP] search_news 原始返回 | query=%s | days=%d | resp=%s", query, days, resp)

        return self._parse_news_response(resp)

    def query_macro_data(self, query: str) -> Dict[str, Any]:
        """
        宏观经济数据查询

        Args:
            query: 自然语言查询，如 "中国2025年GDP增速"

        Returns:
            {
                "results": list,           # 数据列表（按频率分组：年度/季度/月度）
                "query_rewrite": str,      # AI 理解后的查询
                "raw": dict,               # 原始 API 响应
            }
        """
        body = {
            "query": query,
            "toolContext": self._make_tool_context(),
        }
        resp = self._request(_URL_SEARCH_MACRO_DATA, body, timeout=60.0)
        return self._parse_macro_response(resp)

    # ============================================================
    # 公共 API —— 异步包装
    # ============================================================

    async def async_query_entity(self, content: str, entity_type: str = "A股") -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self.query_entity, content, entity_type)

    async def async_query_finance_data(self, query: str, indicators: Optional[str] = None) -> Dict[str, Any]:
        return await asyncio.to_thread(self.query_finance_data, query, indicators)

    async def async_screen_stocks(self, query: str, select_type: str = "A股") -> Dict[str, Any]:
        return await asyncio.to_thread(self.screen_stocks, query, select_type)

    async def async_ask_question(self, question: str, deep_research: bool = False) -> Dict[str, Any]:
        return await asyncio.to_thread(self.ask_question, question, deep_research)

    async def async_search_news(self, query: str, days: int = 3) -> Dict[str, Any]:
        return await asyncio.to_thread(self.search_news, query, days)

    async def async_query_macro_data(self, query: str) -> Dict[str, Any]:
        return await asyncio.to_thread(self.query_macro_data, query)

    # ============================================================
    # 统计
    # ============================================================

    def get_stats(self) -> Dict[str, Any]:
        """返回调用统计"""
        with self._lock:
            avg_latency = (
                self._total_latency_ms / self._call_count
                if self._call_count > 0
                else 0
            )
            return {
                "call_count": self._call_count,
                "error_count": self._error_count,
                "avg_latency_ms": round(avg_latency, 1),
                "error_rate": (
                    round(self._error_count / self._call_count * 100, 1)
                    if self._call_count > 0
                    else 0
                ),
            }

    # ============================================================
    # 内部方法
    # ============================================================

    def _make_tool_context(self) -> Dict[str, Any]:
        """生成工具上下文"""
        return {
            "callId": f"call_{uuid.uuid4().hex[:8]}",
            "userInfo": {"userId": f"user_{uuid.uuid4().hex[:8]}"},
        }

    def _request(
        self,
        url: str,
        body: Dict[str, Any],
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        统一 HTTP POST 请求层

        内置重试、超时、错误处理。
        """
        timeout = timeout or self._timeout
        headers = {
            "Content-Type": "application/json",
            "em_api_key": self._api_key,
        }

        last_error = None
        for attempt in range(1, self._max_retries + 1):
            start_ms = time.monotonic_ns()
            try:
                with httpx.Client(timeout=timeout) as client:
                    resp = client.post(url, json=body, headers=headers)
                    elapsed_ms = (time.monotonic_ns() - start_ms) / 1e6

                    with self._lock:
                        self._call_count += 1
                        self._total_latency_ms += elapsed_ms

                    data = resp.json()
                    code = data.get("code")

                    if code == 401 or code == 403:
                        raise MCPAuthError(f"认证失败: {data.get('message', '')}")

                    if code != 200 and code != 0:
                        # code=0 也是成功（selectSecurity 等接口）
                        if attempt < self._max_retries:
                            logger.warning(
                                "[MCP] 请求失败 attempt=%d/%d code=%s url=%s",
                                attempt, self._max_retries, code, url,
                            )
                            time.sleep(1.0 * attempt)
                            continue
                        raise MCPDataError(f"接口返回异常: code={code}, msg={data.get('message', '')}")

                    logger.debug(
                        "[MCP] 请求成功 url=%s elapsed=%.0fms",
                        url.split("/")[-1], elapsed_ms,
                    )
                    return data

            except httpx.TimeoutException as e:
                elapsed_ms = (time.monotonic_ns() - start_ms) / 1e6
                with self._lock:
                    self._call_count += 1
                    self._error_count += 1
                    self._total_latency_ms += elapsed_ms
                last_error = MCPTimeoutError(f"请求超时 ({timeout}s): {url.split('/')[-1]}")
                if attempt < self._max_retries:
                    logger.warning("[MCP] 超时重试 attempt=%d/%d", attempt, self._max_retries)
                    time.sleep(1.0 * attempt)
                    continue

            except (httpx.HTTPError, httpx.RequestError) as e:
                elapsed_ms = (time.monotonic_ns() - start_ms) / 1e6
                with self._lock:
                    self._call_count += 1
                    self._error_count += 1
                    self._total_latency_ms += elapsed_ms
                last_error = MCPError(f"HTTP 错误: {e}")
                if attempt < self._max_retries:
                    logger.warning("[MCP] HTTP 错误重试 attempt=%d/%d: %s", attempt, self._max_retries, e)
                    time.sleep(1.0 * attempt)
                    continue

        raise last_error or MCPError("未知错误")

    # ============================================================
    # 响应解析
    # ============================================================

    @staticmethod
    def _parse_data_response(resp: Dict[str, Any]) -> Dict[str, Any]:
        """解析查数接口响应"""
        data = resp.get("data", {})
        if data is None:
            return {"query_rewrite": "", "tables": [], "entity_list": [], "raw": resp}

        query_rewrite = data.get("queryRewriteDTO", {}).get("query", "")
        entity_list_raw = data.get("entityList", [])
        entity_list = [
            {
                "name": e.get("name", ""),
                "code": e.get("code", ""),
                "market": e.get("marketChar", ""),
            }
            for e in entity_list_raw
        ]

        tables = []
        for dto in data.get("searchDataResultDTO", {}).get("dataTableDTOList", []):
            table_data = dto.get("table", {})
            title = dto.get("title", "")

            # 构建 Markdown 表格
            markdown = _build_markdown_table(table_data)

            tables.append({
                "title": title,
                "table": table_data,
                "markdown": markdown,
            })

        return {
            "query_rewrite": query_rewrite,
            "tables": tables,
            "entity_list": entity_list,
            "raw": resp,
        }

    @staticmethod
    def _parse_select_response(resp: Dict[str, Any]) -> Dict[str, Any]:
        """解析选股接口响应"""
        data = resp.get("data", {})
        if data is None:
            return {"security_count": 0, "columns": [], "data_list": [], "partial_results": "", "raw": resp}

        all_results = data.get("allResults", {})
        result = all_results.get("result", {}) if all_results else {}
        data_list = result.get("dataList", [])
        columns = result.get("columns", [])
        partial_results = data.get("partialResults", "")
        security_count = data.get("securityCount", 0)

        return {
            "security_count": security_count,
            "columns": columns,
            "data_list": data_list,
            "partial_results": partial_results,
            "raw": resp,
        }

    @staticmethod
    def _parse_ask_response(resp: Dict[str, Any]) -> Dict[str, Any]:
        """解析问答接口响应"""
        data = resp.get("data", {})
        if data is None:
            return {"answer": "", "references": [], "request_id": "", "raw": resp}

        display_data = data.get("displayData", "")
        ref_list = data.get("refIndexList", [])
        request_id = data.get("requestId", "")

        references = []
        for ref in ref_list:
            references.append({
                "title": ref.get("title", ""),
                "url": ref.get("url", ""),
                "source": ref.get("source", ""),
                "date": ref.get("date", ""),
            })

        return {
            "answer": display_data,
            "references": references,
            "request_id": request_id,
            "raw": resp,
        }

    @staticmethod
    def _parse_news_response(resp: Dict[str, Any]) -> Dict[str, Any]:
        """解析资讯搜索响应"""
        data = resp.get("data", {})
        if data is None:
            return {"results": [], "count": 0, "raw": resp}

        # 实际数据路径: data.llmSearchResponse.data
        llm_data = data.get("llmSearchResponse", {}).get("data", [])
        results = []
        for item in llm_data:
            results.append({
                "title": item.get("title", ""),
                "content": item.get("content", "")[:500],
                "source": item.get("source", ""),
                "date": item.get("date", ""),
                "url": item.get("jumpUrl", ""),
                "type": item.get("informationType", ""),
            })

        return {
            "results": results,
            "count": len(results),
            "raw": resp,
        }

    @staticmethod
    def _parse_macro_response(resp: Dict[str, Any]) -> Dict[str, Any]:
        """解析宏观数据响应"""
        data = resp.get("data", {})
        if data is None:
            return {"results": [], "query_rewrite": "", "raw": resp}

        query_rewrite = data.get("queryRewriteDTO", {}).get("query", "")
        results = []
        for dto in data.get("searchMacroDataResultDTO", {}).get("macroDataDTOList", []):
            results.append({
                "title": dto.get("title", ""),
                "frequency": dto.get("frequency", ""),
                "unit": dto.get("unit", ""),
                "data": dto.get("data", []),
                "table": dto.get("table", {}),
            })

        return {
            "results": results,
            "query_rewrite": query_rewrite,
            "raw": resp,
        }


# ============================================================
# 工具函数
# ============================================================


def _build_markdown_table(table_data: Dict[str, Any]) -> str:
    """
    将 MCP 返回的表格数据转为 Markdown 格式

    table_data 格式示例：
    {
        "columns": ["日期", "营收", "净利润"],
        "data": [
            ["2025-12-31", "1234亿", "567亿"],
            ...
        ]
    }
    """
    columns = table_data.get("columns", [])
    rows = table_data.get("data", [])

    if not columns or not rows:
        return ""

    lines = []
    # 表头
    lines.append("| " + " | ".join(str(c) for c in columns) + " |")
    lines.append("| " + " | ".join("---" for _ in columns) + " |")
    # 数据行
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")

    return "\n".join(lines)


# ============================================================
# 单例（模块级）
# ============================================================

_service_instance: Optional[EastmoneyMCPService] = None
_service_lock = Lock()


def get_mcp_service(
    api_key: Optional[str] = None,
    timeout: int = 30,
) -> EastmoneyMCPService:
    """
    获取 MCP 服务单例

    首次调用时创建实例，后续调用返回同一实例。
    """
    global _service_instance
    if _service_instance is None:
        with _service_lock:
            if _service_instance is None:
                _service_instance = EastmoneyMCPService(
                    api_key=api_key,
                    timeout=timeout,
                )
    return _service_instance
