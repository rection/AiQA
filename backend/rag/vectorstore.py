import chromadb
from config import settings


_client = None
_collection = None


def get_client() -> chromadb.PersistentClient:
    """获取 ChromaDB 客户端（单例）。"""
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
    return _client


def get_collection() -> chromadb.Collection:
    """获取文档向量集合（单例）。"""
    global _collection
    if _collection is None:
        client = get_client()
        _collection = client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def add_documents(
    document_id: str,
    chunks: list[str],
    embeddings: list[list[float]],
    filename: str,
) -> int:
    """将文档分块及其向量存入 ChromaDB。返回存储的块数。"""
    collection = get_collection()
    ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [
        {"document_id": document_id, "filename": filename, "chunk_index": i}
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    return len(chunks)


def query_documents(
    query_embedding: list[float],
    n_results: int = 5,
    document_ids: list[str] | None = None,
) -> list[dict]:
    """查询相似文档块。"""
    collection = get_collection()
    where_filter = None
    if document_ids:
        where_filter = {"document_id": {"$in": document_ids}}

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where_filter,
    )

    formatted = []
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = results.get("distances", [[]])[0] if results.get("distances") else [None] * len(docs)

    for i in range(len(docs)):
        formatted.append({
            "content": docs[i],
            "metadata": metas[i] if i < len(metas) else {},
            "distance": dists[i] if i < len(dists) else None,
        })
    return formatted


def delete_document(document_id: str) -> int:
    """删除指定文档的所有向量块。返回删除的块数。"""
    collection = get_collection()
    results = collection.get(where={"document_id": document_id})
    count = len(results["ids"])
    if count > 0:
        collection.delete(where={"document_id": document_id})
    return count
