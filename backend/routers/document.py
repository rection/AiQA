from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session as DBSession
from database.session import get_db
from models.schemas import DocumentInfo, DocumentListResponse, DeleteResponse
from services import document_service

router = APIRouter()


@router.post("/upload", response_model=DocumentInfo)
async def upload_document(
    file: UploadFile = File(...),
    session_id: str = Form(""),
    db: DBSession = Depends(get_db),
):
    try:
        doc = await document_service.process_upload(file, session_id, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return DocumentInfo(
        document_id=doc.id,
        filename=doc.filename,
        file_size=doc.file_size,
        file_type=doc.file_type,
        chunk_count=doc.chunk_count,
        status=doc.status,
        created_at=doc.created_at,
    )


@router.get("", response_model=DocumentListResponse)
def list_documents(
    session_id: str | None = None,
    page: int = 1,
    page_size: int = 20,
    db: DBSession = Depends(get_db),
):
    documents, total = document_service.list_documents(session_id, page, page_size, db)
    return DocumentListResponse(
        total=total,
        documents=[
            DocumentInfo(
                document_id=d.id,
                filename=d.filename,
                file_size=d.file_size,
                file_type=d.file_type,
                chunk_count=d.chunk_count,
                status=d.status,
                created_at=d.created_at,
            )
            for d in documents
        ],
    )


@router.delete("/{document_id}", response_model=DeleteResponse)
def delete_document(document_id: str, db: DBSession = Depends(get_db)):
    try:
        document_service.delete_document(document_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return DeleteResponse(deleted=True)
