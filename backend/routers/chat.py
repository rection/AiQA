import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session as DBSession
from database.session import get_db
from models.schemas import (
    ChatRequest,
    SessionInfo,
    SessionListResponse,
    MessageInfo,
    MessageListResponse,
    ToolCallInfo,
    DeleteResponse,
)
from services import chat_service
from agents.graph import agent_graph
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from prompts.system import get_system_prompt

router = APIRouter()


def sse_encode(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def generate_sse_stream(session_id: str, message: str, db: DBSession):
    """生成 SSE 事件流。"""
    session, created = chat_service.get_or_create_session(session_id, db)
    session_id = session.id

    chat_service.save_message(session_id, "user", message, None, db)

    yield sse_encode("session", {"session_id": session_id, "created": created})

    history_msgs, _ = chat_service.get_messages(session_id, db)

    messages = [SystemMessage(content=get_system_prompt())]
    for msg in history_msgs[:-1]:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            messages.append(AIMessage(content=msg.content))

    messages.append(HumanMessage(content=message))

    full_answer = ""
    tool_calls_collected = []

    try:
        async for event in agent_graph.astream_events(
            {"messages": messages, "session_id": session_id, "tool_call_count": 0, "max_tool_calls": 5},
            config={"configurable": {"session_id": session_id}},
            version="v2",
        ):
            kind = event["event"]

            if kind == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                if chunk.content:
                    full_answer += chunk.content
                    yield sse_encode("answer", {"content": chunk.content})

            elif kind == "on_tool_start":
                tool_name = event["name"]
                tool_input = event["data"].get("input", "")
                yield sse_encode("tool_call", {
                    "tool": tool_name,
                    "input": str(tool_input)[:200],
                    "status": "running",
                })

            elif kind == "on_tool_end":
                tool_name = event["name"]
                tool_output = event["data"].get("output", "")
                tool_calls_collected.append({
                    "tool": tool_name,
                    "input": "",
                    "output": str(tool_output)[:500],
                })
                yield sse_encode("tool_result", {
                    "tool": tool_name,
                    "output": str(tool_output)[:500],
                    "status": "success",
                })

    except Exception as e:
        yield sse_encode("error", {"code": "AGENT_ERROR", "message": str(e)})
        return

    msg = chat_service.save_message(
        session_id, "assistant", full_answer,
        tool_calls_collected if tool_calls_collected else None,
        db,
    )

    yield sse_encode("done", {"message_id": msg.id})


@router.post("/stream")
async def chat_stream(req: ChatRequest, db: DBSession = Depends(get_db)):
    """流式对话接口。"""
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="消息不能为空")

    return StreamingResponse(
        generate_sse_stream(req.session_id, req.message, db),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/sessions", response_model=SessionListResponse)
def list_sessions(page: int = 1, page_size: int = 20, db: DBSession = Depends(get_db)):
    sessions, total = chat_service.get_sessions(page, page_size, db)
    return SessionListResponse(
        total=total,
        page=page,
        page_size=page_size,
        sessions=[
            SessionInfo(
                session_id=s.id,
                title=s.title,
                created_at=s.created_at,
                updated_at=s.updated_at,
                message_count=chat_service.get_message_count(s.id, db),
            )
            for s in sessions
        ],
    )


@router.get("/sessions/{session_id}/messages", response_model=MessageListResponse)
def get_session_messages(session_id: str, db: DBSession = Depends(get_db)):
    messages, total = chat_service.get_messages(session_id, db)
    return MessageListResponse(
        session_id=session_id,
        total=total,
        messages=[
            MessageInfo(
                message_id=m.id,
                role=m.role,
                content=m.content,
                tool_calls=[ToolCallInfo(**tc) for tc in m.tool_calls] if m.tool_calls else None,
                created_at=m.created_at,
            )
            for m in messages
        ],
    )


@router.delete("/sessions/{session_id}", response_model=DeleteResponse)
def delete_session(session_id: str, db: DBSession = Depends(get_db)):
    deleted = chat_service.delete_session(session_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="会话不存在")
    return DeleteResponse(deleted=True)
