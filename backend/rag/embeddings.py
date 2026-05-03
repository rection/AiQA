from langchain_openai import OpenAIEmbeddings
from config import settings


def get_embedding_model() -> OpenAIEmbeddings:
    """获取 DeepSeek Embedding 模型（兼容 OpenAI 格式）。"""
    return OpenAIEmbeddings(
        model=settings.DEEPSEEK_EMBEDDING_MODEL,
        openai_api_key=settings.DEEPSEEK_API_KEY,
        openai_api_base=settings.DEEPSEEK_BASE_URL,
    )
