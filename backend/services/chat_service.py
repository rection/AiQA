import uuid
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session as DBSession
from database.models import Session as ChatSession, Message


def get_or_create_session(session_id: str, db: DBSession) -> tuple[ChatSession, bool]:
    if session_id:
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            return session, False

    session = ChatSession(id=str(uuid.uuid4()), title="", created_at=datetime.utcnow())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session, True


def save_message(
    session_id: str,
    role: str,
    content: str,
    tool_calls: list[dict] | None,
    db: DBSession,
) -> Message:
    msg = Message(
        id=str(uuid.uuid4()),
        session_id=session_id,
        role=role,
        content=content,
        tool_calls=tool_calls,
    )
    db.add(msg)

    if role == "user":
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session and not session.title:
            session.title = content[:50]
            session.updated_at = datetime.utcnow()
        elif session:
            session.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(msg)
    return msg


def get_sessions(page: int, page_size: int, db: DBSession) -> tuple[list[ChatSession], int]:
    total = db.query(func.count(ChatSession.id)).scalar()
    sessions = (
        db.query(ChatSession)
        .order_by(ChatSession.updated_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return sessions, total


def get_messages(session_id: str, db: DBSession) -> tuple[list[Message], int]:
    messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at.asc())
        .all()
    )
    return messages, len(messages)


def delete_session(session_id: str, db: DBSession) -> bool:
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        return False
    db.delete(session)
    db.commit()
    return True


def get_message_count(session_id: str, db: DBSession) -> int:
    return db.query(func.count(Message.id)).filter(Message.session_id == session_id).scalar()
