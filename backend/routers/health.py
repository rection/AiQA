from fastapi import APIRouter
from config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    services = {}

    services["deepseek_api"] = "ok" if settings.DEEPSEEK_API_KEY else "not_configured"

    try:
        from rag.vectorstore import get_client
        get_client()
        services["chromadb"] = "ok"
    except Exception:
        services["chromadb"] = "error"

    try:
        from database.session import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        services["mysql"] = "ok"
    except Exception:
        services["mysql"] = "error"

    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "services": services,
    }
