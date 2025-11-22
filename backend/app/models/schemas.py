from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class JobCreate(BaseModel):
    title: str
    description: str


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class CandidateResponse(BaseModel):
    id: int
    job_id: int
    name: Optional[str]
    email: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class EvaluationResponse(BaseModel):
    candidate_id: int
    candidate_name: str
    overall_score: float
    technical_score: float
    experience_score: float
    education_score: float
    strengths: List[str]
    concerns: List[str]
    recommendation: str
    ai_analysis: Optional[str] = None


class TopCandidatesResponse(BaseModel):
    job_id: int
    total_candidates: int
    top_5: List[EvaluationResponse]


class EvaluationRequest(BaseModel):
    job_id: int


class EvaluationStatusResponse(BaseModel):
    job_id: int
    status: str
    message: str


# Chat schemas
class ChatMessageRequest(BaseModel):
    message: str
    job_id: Optional[int] = None
    session_id: Optional[str] = None


class ReasoningStep(BaseModel):
    tool: str
    input: Dict[str, Any]
    output: str


class ChatMessageResponse(BaseModel):
    response: str
    reasoning: List[ReasoningStep]
    tools_used: List[str]
    success: bool
    session_id: str
    error: Optional[str] = None


class ChatSessionResponse(BaseModel):
    session_id: str
    job_id: Optional[int]
    created_at: datetime
    message_count: int
    
    class Config:
        from_attributes = True


class ChatHistoryMessage(BaseModel):
    id: int
    role: str
    content: str
    reasoning: Optional[List[Dict[str, Any]]] = None  # List of reasoning steps
    tools_used: Optional[List[str]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    session_id: str
    messages: List[ChatHistoryMessage]
