from langchain_core.tools import tool
from tools import rag_tool, search_tool, db_tool


@tool
def rag_search(query: str, document_ids: list[str] | None = None) -> str:
    """在已上传的文档中搜索相关内容。当用户问题可能在已上传文档中有答案时使用此工具。
    Args:
        query: 搜索查询语句
        document_ids: 限定搜索的文档 ID 列表，不传则搜索所有文档
    """
    return rag_tool.search(query, document_ids)


@tool
def web_search(query: str) -> str:
    """搜索互联网获取实时信息。当用户问题涉及实时信息、新闻、或文档中没有的信息时使用。
    Args:
        query: 搜索关键词
    """
    return search_tool.search(query)


@tool
def mysql_query(natural_language: str) -> str:
    """将自然语言描述转换为 SQL 并查询 MySQL 数据库。当用户需要查询或统计数据库中的数据时使用。
    Args:
        natural_language: 用自然语言描述要查询的内容
    """
    return db_tool.query(natural_language)


ALL_TOOLS = [rag_search, web_search, mysql_query]
TOOL_MAP = {
    "rag_search": rag_tool.search,
    "web_search": search_tool.search,
    "mysql_query": db_tool.query,
}
