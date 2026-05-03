from rag.embeddings import get_embedding_model
from rag.vectorstore import query_documents


def search(query: str, document_ids: list[str] | None = None) -> str:
    """在已上传的文档中搜索相关内容。"""
    embedding_model = get_embedding_model()
    query_embedding = embedding_model.embed_query(query)

    results = query_documents(
        query_embedding=query_embedding,
        n_results=5,
        document_ids=document_ids,
    )

    if not results:
        return "未在文档中找到相关内容。"

    parts = []
    for i, r in enumerate(results, 1):
        filename = r["metadata"].get("filename", "未知文档")
        parts.append(f"[{i}] 来源：{filename}\n{r['content']}")

    return "\n\n---\n\n".join(parts)
