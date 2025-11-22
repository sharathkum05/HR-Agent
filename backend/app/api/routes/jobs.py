from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from uuid import uuid4

from app.services.db_service import get_db
from app.models.database import Job, Candidate
from app.models.schemas import JobCreate, JobResponse, CandidateResponse, TopCandidatesResponse, EvaluationStatusResponse
from app.services.resume_parser import extract_text_from_pdf, extract_name_from_resume, extract_email_from_resume
from app.services.retrieval import retrieval_service
from app.services.rag_service import RAGService
from app.config import settings

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.post("", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """Create a new job posting."""
    db_job = Job(title=job.title, description=job.description)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get job details."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/{job_id}/resumes")
async def upload_resumes(
    job_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """Upload multiple resume files for a job."""
    # Verify job exists
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(settings.upload_dir, f"job_{job_id}")
    os.makedirs(upload_dir, exist_ok=True)
    
    uploaded_count = 0
    candidates_created = []
    
    for file in files:
        try:
            # Validate file type
            if not file.filename.endswith('.pdf'):
                continue
            
            # Save file
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid4().hex}{file_extension}"
            file_path = os.path.join(upload_dir, unique_filename)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Parse PDF
            resume_text = extract_text_from_pdf(file_path)
            if not resume_text:
                os.remove(file_path)
                continue
            
            # Extract metadata
            name = extract_name_from_resume(resume_text)
            email = extract_email_from_resume(resume_text)
            
            # Create candidate record
            candidate = Candidate(
                job_id=job_id,
                name=name,
                email=email,
                resume_file_path=file_path,
                resume_text=resume_text
            )
            db.add(candidate)
            db.flush()  # Get candidate ID
            
            # Store embedding in Pinecone
            try:
                pinecone_id = retrieval_service.upsert_resume(
                    candidate_id=candidate.id,
                    resume_text=resume_text,
                    metadata={
                        "job_id": job_id,
                        "name": name or "",
                        "email": email or ""
                    }
                )
                candidate.pinecone_id = pinecone_id
            except Exception as e:
                print(f"Warning: Could not store in Pinecone: {e}")
            
            db.commit()
            candidates_created.append(candidate.id)
            uploaded_count += 1
            
        except Exception as e:
            print(f"Error processing file {file.filename}: {e}")
            continue
    
    return {
        "uploaded": uploaded_count,
        "job_id": job_id,
        "candidate_ids": candidates_created
    }


@router.post("/{job_id}/evaluate", response_model=EvaluationStatusResponse)
def evaluate_candidates(job_id: int, db: Session = Depends(get_db)):
    """Trigger RAG evaluation for all candidates of a job."""
    # Verify job exists
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check if candidates exist
    candidate_count = db.query(Candidate).filter(Candidate.job_id == job_id).count()
    if candidate_count == 0:
        raise HTTPException(status_code=400, detail="No candidates found for this job")
    
    return {
        "job_id": job_id,
        "status": "processing",
        "message": f"Evaluation started for {candidate_count} candidates. Use GET /api/jobs/{job_id}/top-candidates to get results."
    }


@router.get("/{job_id}/top-candidates", response_model=TopCandidatesResponse)
def get_top_candidates(job_id: int, db: Session = Depends(get_db)):
    """Get top 5 candidates after RAG evaluation."""
    # Verify job exists
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Run RAG evaluation
    rag_service = RAGService(db)
    top_5 = rag_service.evaluate_job_candidates(job_id=job_id, top_k=15)
    
    # Get total candidate count
    total_candidates = db.query(Candidate).filter(Candidate.job_id == job_id).count()
    
    return {
        "job_id": job_id,
        "total_candidates": total_candidates,
        "top_5": top_5
    }

