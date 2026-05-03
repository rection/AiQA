import os
import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session as DBSession
from config import settings
from database.models import Document
from rag.loader import load_document
from rag.splitter import split_text
from rag.embeddings import get_embedding_model
from rag.vectorstore import add_documents


ALLOWED_EXTENSIONS = {"pdf", "docx", "md", "txt", "csv"}


def get_file_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


async def process_upload(
    file: UploadFile,
    session_id: str,
    db: DBSession,
) -> Document:
    """处理文档上传：保存文件 → 解析 → 分块 → 向量化 → 存储。"""
    ext = get_file_extension(file.filename or "")
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"不支持的文件格式: {ext}")

    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise ValueError(f"文件大小超过限制 ({settings.MAX_FILE_SIZE // 1024 // 1024}MB)")

    doc_id = str(uuid.uuid4())
    save_filename = f"{doc_id}.{ext}"
    save_path = os.path.join(settings.UPLOAD_DIR, save_filename)
    with open(save_path, "wb") as f:
        f.write(content)

    doc = Document(
        id=doc_id,
        session_id=session_id or None,
        filename=file.filename or save_filename,
        file_path=save_path,
        file_size=len(content),
        file_type=ext,
        chunk_count=0,
        status="processing",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    try:
        text = load_document(save_path, ext)
        if not text.strip():
            raise ValueError("文档内容为空")

        chunks = split_text(text)
        embedding_model = get_embedding_model()
        embeddings = embedding_model.embed_documents(chunks)

        add_documents(
            document_id=doc_id,
            chunks=chunks,
            embeddings=embeddings,
            filename=file.filename or save_filename,
        )

        doc.chunk_count = len(chunks)
        doc.status = "indexed"
        db.commit()
        db.refresh(doc)

    except Exception:
        doc.status = "failed"
        db.commit()
        raise

    return doc


def list_documents(
    session_id: str | None,
    page: int,
    page_size: int,
    db: DBSession,
) -> tuple[list[Document], int]:
    query = db.query(Document)
    if session_id:
        query = query.filter(Document.session_id == session_id)

    total = query.count()
    documents = (
        query.order_by(Document.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return documents, total


def delete_document(document_id: str, db: DBSession) -> int:
    from rag.vectorstore import delete_document as delete_vec

    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise ValueError("文档不存在")

    chunks_deleted = delete_vec(document_id)

    if os.path.exists(doc.file_path):
        os.unlink(doc.file_path)

    db.delete(doc)
    db.commit()

    return chunks_deleted
