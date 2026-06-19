# -*- coding: utf-8 -*-
"""
===================================
东方财富妙想 MCP 接口
===================================

提供金融数据查询、智能选股、金融问答、资讯搜索、宏观数据等 API。
"""

import logging
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field

from api.v1.errors import api_error

logger = logging.getLogger(__name__)

router = APIRouter()


# ============================================================
# 请求/响应模型
# ============================================================


class MCPQueryRequest(BaseModel):
    query: str = Field(..., description="自然语言查询")
    indicators: Optional[str] = Field(None, description="限定指标关键词（可选）")


class MCPScreenRequest(BaseModel):
    query: str = Field(..., description="自然语言选股条件")
    select_type: str = Field("A股", description="筛选类型: A股/港股/美股/ETF/可转债/板块")


class MCPAskRequest(BaseModel):
    question: str = Field(..., description="自然语言问题")
    deep_research: bool = Field(False, description="是否启用深度研究")


class MCPNewsRequest(BaseModel):
    query: str = Field(..., description="搜索关键词")
    days: int = Field(3, description="搜索时间范围（天）")


class MCPPingResponse(BaseModel):
    status: str
    stats: dict
    api_key_prefix: str


# ============================================================
# 依赖
# ============================================================


def _get_mcp_service():
    """获取 MCP 服务实例"""
    from src.config import get_config
    from src.eastmoney_mcp_service import get_mcp_service

    config = get_config()
    if not config.mcp_enabled:
        raise HTTPException(status_code=503, detail="MCP 服务未启用")
    return get_mcp_service(
        api_key=config.em_api_key,
        timeout=config.mcp_timeout,
    )


# ============================================================
# 接口
# ============================================================


@router.get("/ping", response_model=MCPPingResponse, summary="MCP 服务状态检查")
async def ping():
    """检查 MCP 服务状态和调用统计"""
    service = _get_mcp_service()
    stats = service.get_stats()
    return MCPPingResponse(
        status="ok",
        stats=stats,
        api_key_prefix=service._api_key[:8] + "...",
    )


@router.post("/query", summary="金融数据查询")
async def query_finance_data(req: MCPQueryRequest):
    """
    通过自然语言查询金融数据（财务报表/估值/技术指标/资金流向）

    示例:
    - "贵州茅台近一年营收和净利润"
    - "宁德时代最新PE和PB"
    - "比亚迪近30日涨跌幅"
    """
    try:
        service = _get_mcp_service()
        result = service.query_finance_data(req.query, req.indicators)
        return result
    except Exception as e:
        logger.error("[MCP API] query 失败: %s", e)
        raise api_error(500, f"查询失败: {e}")


@router.post("/screen", summary="智能选股")
async def screen_stocks(req: MCPScreenRequest):
    """
    通过自然语言筛选股票

    示例:
    - "股价大于500元的A股"
    - "ROE大于15%且市盈率低于20的消费股"
    - "最近5日涨幅超过10%的科创板股票"
    """
    try:
        service = _get_mcp_service()
        result = service.screen_stocks(req.query, req.select_type)
        return result
    except Exception as e:
        logger.error("[MCP API] screen 失败: %s", e)
        raise api_error(500, f"选股失败: {e}")


@router.post("/ask", summary="金融问答")
async def ask_question(req: MCPAskRequest):
    """
    金融问答（七大能力：条件选股/个股分析/对比分析/资讯问答/机构观点/翻译转换/比价信息）

    示例:
    - "贵州茅台和五粮液哪个更值得投资"
    - "光伏行业未来前景如何"
    - "ROE大于15%的消费股有哪些"
    """
    try:
        service = _get_mcp_service()
        result = service.ask_question(req.question, req.deep_research)
        return result
    except Exception as e:
        logger.error("[MCP API] ask 失败: %s", e)
        raise api_error(500, f"问答失败: {e}")


@router.post("/news", summary="财经资讯搜索")
async def search_news(req: MCPNewsRequest):
    """
    搜索财经新闻、公告、研报

    示例:
    - "贵州茅台最新公告"
    - "光伏行业研报"
    - "央行降息相关新闻"
    """
    try:
        service = _get_mcp_service()
        result = service.search_news(req.query, req.days)
        return result
    except Exception as e:
        logger.error("[MCP API] news 失败: %s", e)
        raise api_error(500, f"资讯搜索失败: {e}")


@router.post("/macro", summary="宏观经济数据")
async def query_macro_data(req: MCPQueryRequest):
    """
    查询宏观经济数据

    示例:
    - "中国2025年GDP增速"
    - "美国最新CPI"
    - "中国制造业PMI近一年走势"
    """
    try:
        service = _get_mcp_service()
        result = service.query_macro_data(req.query)
        return result
    except Exception as e:
        logger.error("[MCP API] macro 失败: %s", e)
        raise api_error(500, f"宏观数据查询失败: {e}")


@router.post("/entity", summary="实体识别")
async def query_entity(
    content: str = Body(..., embed=True, description="待识别文本"),
    entity_type: str = Body("A股", embed=True, description="实体类型: A股/港股/基金/美股/指数"),
):
    """
    从文本中识别金融实体（股票/基金/指数等）

    示例:
    - content="贵州茅台", entity_type="A股" → 600519.SH
    - content="沪深300ETF", entity_type="基金"
    """
    try:
        service = _get_mcp_service()
        result = service.query_entity(content, entity_type)
        return {"entities": result}
    except Exception as e:
        logger.error("[MCP API] entity 失败: %s", e)
        raise api_error(500, f"实体识别失败: {e}")
