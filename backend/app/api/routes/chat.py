from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import uuid4
from datetime import datetime
import json

from app.services.db_service import get_db
from app.models.database import ChatSession, ChatMessage
from app.models.schemas import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatSessionResponse,
    ChatHistoryResponse,
    ChatHistoryMessage
)
from app.services.agent_service import create_agent

router = APIRouter(prefix="/api/chat", tags=["chat"])

# In-memory storage for agent instances (in production, use Redis or similar)
agent_sessions = {}


@router.post("", response_model=ChatMessageResponse)
def chat_with_agent(
    request: ChatMessageRequest,
    db: Session = Depends(get_db)
):
    """
    Chat with the autonomous HR agent.
    
    The agent can:
    - Make independent decisions
    - Use tools (search, evaluate, compare candidates)
    - Plan multi-step workflows
    - Reason about candidate evaluation
    """
    # Get or create session
    session_id = request.session_id
    if not session_id:
        session_id = str(uuid4())
    
    # Get or create chat session in DB
    chat_session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id
    ).first()
    
    if not chat_session:
        chat_session = ChatSession(
            session_id=session_id,
            job_id=request.job_id
        )
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)
    
    # Get or create agent instance
    if session_id not in agent_sessions:
        agent_sessions[session_id] = create_agent(
            db=db,
            job_id=request.job_id
        )
    
    agent = agent_sessions[session_id]
    
    # Save user message
    user_message = ChatMessage(
        session_id=session_id,
        role="user",
        content=request.message
    )
    db.add(user_message)
    
    # Get agent response
    result = agent.chat(request.message)
    
    # Save agent response
    agent_message = ChatMessage(
        session_id=session_id,
        role="agent",
        content=result["response"],
        reasoning=result.get("reasoning"),
        tools_used=result.get("tools_used", [])
    )
    db.add(agent_message)
    
    # Update session
    chat_session.updated_at = datetime.utcnow()
    
    db.commit()
    
    return ChatMessageResponse(
        response=result["response"],
        reasoning=result.get("reasoning", []),
        tools_used=result.get("tools_used", []),
        success=result.get("success", True),
        session_id=session_id,
        error=result.get("error")
    )


@router.get("/sessions/{session_id}", response_model=ChatHistoryResponse)
def get_chat_history(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get chat history for a session."""
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at).all()
    
    return ChatHistoryResponse(
        session_id=session_id,
        messages=[
            ChatHistoryMessage(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                reasoning=msg.reasoning,
                tools_used=msg.tools_used,
                created_at=msg.created_at
            )
            for msg in messages
        ]
    )


@router.post("/sessions/{session_id}/clear")
def clear_chat_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Clear chat session memory."""
    # Clear agent memory
    if session_id in agent_sessions:
        agent_sessions[session_id].clear_memory()
    
    # Optionally delete messages from DB
    # db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
    # db.commit()
    
    return {"status": "cleared", "session_id": session_id}


@router.get("/sessions", response_model=List[ChatSessionResponse])
def list_chat_sessions(
    job_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """List all chat sessions, optionally filtered by job_id."""
    query = db.query(ChatSession)
    if job_id:
        query = query.filter(ChatSession.job_id == job_id)
    
    sessions = query.order_by(ChatSession.updated_at.desc()).all()
    
    result = []
    for session in sessions:
        message_count = db.query(ChatMessage).filter(
            ChatMessage.session_id == session.session_id
        ).count()
        
        result.append(ChatSessionResponse(
            session_id=session.session_id,
            job_id=session.job_id,
            created_at=session.created_at,
            message_count=message_count
        ))
    
    return result

