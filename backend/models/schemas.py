from datetime import datetime
from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str = ""
    message: str
    stream: bool = True


class SessionInfo(BaseModel):
    session_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int


class ToolCallInfo(BaseModel):
    tool: str
    input: str
    output: str


class MessageInfo(BaseModel):
    message_id: str
    role: str
    content: str
    tool_calls: list[ToolCallInfo] | None = None
    created_at: datetime


class DocumentInfo(BaseModel):
    document_id: str
    filename: str
    file_size: int
    file_type: str
    chunk_count: int
    status: str
    created_at: datetime


class SessionListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    sessions: list[SessionInfo]


class MessageListResponse(BaseModel):
    session_id: str
    total: int
    messages: list[MessageInfo]


class DocumentListResponse(BaseModel):
    total: int
    documents: list[DocumentInfo]


class DeleteResponse(BaseModel):
    deleted: bool
