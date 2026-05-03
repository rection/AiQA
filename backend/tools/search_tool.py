from tavily import TavilyClient
from config import settings


_client: TavilyClient | None = None


def _get_client() -> TavilyClient:
    global _client
    if _client is None:
        _client = TavilyClient(api_key=settings.TAVILY_API_KEY)
    return _client


def search(query: str) -> str:
    """搜索互联网获取实时信息。"""
    client = _get_client()
    response = client.search(query, max_results=5)

    if not response.get("results"):
        return "未找到相关搜索结果。"

    parts = []
    for i, result in enumerate(response["results"], 1):
        parts.append(
            f"[{i}] {result['title']}\n"
            f"来源：{result['url']}\n"
            f"摘要：{result['content']}"
        )

    return "\n\n".join(parts)
