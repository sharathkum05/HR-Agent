from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import jobs, chat
from app.services.db_service import init_db
import os

app = FastAPI(
    title="HR Agent API",
    description="Autonomous AI Agent with LangChain for intelligent resume screening - RAG + Multi-step Reasoning + Conversational Interface",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Next.js default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(jobs.router)
app.include_router(chat.router)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    # Create uploads directory
    os.makedirs("uploads", exist_ok=True)
    # Initialize database
    init_db()


@app.get("/")
def root():
    return {"message": "HR Agent API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

