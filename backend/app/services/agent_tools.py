from langchain.tools import tool
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from app.services.retrieval import retrieval_service
from app.services.generation import evaluate_candidate
from app.services.rag_service import RAGService
from app.models.database import Job, Candidate, Evaluation


@tool
def search_candidates(job_id: int, query: str = None, top_k: int = 15) -> str:
    """Search for candidates using vector similarity search.
    
    Use this tool to find candidates that match a job description.
    
    Args:
        job_id: The job ID to search candidates for (required)
        query: Optional search query. If not provided, uses the job description
        top_k: Number of top candidates to retrieve (default: 15, max: 50)
    
    Returns:
        JSON string with candidate IDs, names, and similarity scores
    """
    try:
        # Limit top_k to prevent abuse
        top_k = min(top_k, 50)
        
        # Get job description
        # Note: In real implementation, we'd pass db session
        # For now, we'll use the retrieval service which already has job context
        
        # Use retrieval service to find candidates
        if query:
            matches = retrieval_service.retrieve_top_k(query, top_k=top_k)
        else:
            # Default to job description - this would need job from DB
            matches = retrieval_service.retrieve_top_k("", top_k=top_k)
        
        result = {
            "candidates": [
                {
                    "candidate_id": match.get("candidate_id"),
                    "score": match.get("score", 0),
                    "metadata": match.get("metadata", {})
                }
                for match in matches
            ],
            "count": len(matches)
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error searching candidates: {str(e)}"})


@tool
def evaluate_candidate(candidate_id: int, job_id: int, focus_areas: Optional[List[str]] = None) -> str:
    """Perform detailed evaluation of a candidate against a job.
    
    Use this tool to get comprehensive evaluation scores and analysis for a candidate.
    
    Args:
        candidate_id: ID of the candidate to evaluate (required)
        job_id: Job ID for evaluation context (required)
        focus_areas: Optional list of areas to focus on, e.g., ['technical', 'experience', 'education']
    
    Returns:
        JSON string with detailed evaluation scores, strengths, concerns, and recommendation
    """
    try:
        # This would need db session - simplified for now
        # In actual implementation, we'd get job and candidate from DB
        # For now, using the generation service directly
        
        # Get job and candidate from database (would need db session)
        # job = db.query(Job).filter(Job.id == job_id).first()
        # candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        
        # For tool interface, we'll return a message indicating this needs DB context
        # In full implementation, this would be:
        # evaluation = evaluate_candidate(job.description, candidate.resume_text)
        
        result = {
            "candidate_id": candidate_id,
            "job_id": job_id,
            "message": "Evaluation requires database session. Use RAGService for full evaluation.",
            "note": "This tool will evaluate the candidate when called with proper DB context"
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error evaluating candidate: {str(e)}"})


@tool
def compare_candidates(candidate_ids: List[int], job_id: int) -> str:
    """Compare multiple candidates side by side.
    
    Use this tool to see how candidates stack up against each other.
    
    Args:
        candidate_ids: List of candidate IDs to compare (2-10 candidates)
        job_id: Job ID for comparison context
    
    Returns:
        JSON string with side-by-side comparison of scores and key metrics
    """
    try:
        # Limit comparison count
        candidate_ids = candidate_ids[:10]
        
        if len(candidate_ids) < 2:
            return json.dumps({"error": "Need at least 2 candidates to compare"})
        
        # This would fetch evaluations from DB and compare
        # Simplified for tool interface
        
        result = {
            "job_id": job_id,
            "candidate_ids": candidate_ids,
            "message": "Comparison requires database session. Use RAGService for full comparison.",
            "comparison": "This will show side-by-side scores, strengths, and weaknesses when fully implemented"
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error comparing candidates: {str(e)}"})


@tool
def get_job_details(job_id: int) -> str:
    """Get detailed information about a job posting.
    
    Use this tool to retrieve job title, description, and requirements.
    
    Args:
        job_id: The job ID to get details for
    
    Returns:
        JSON string with job title, description, requirements, and metadata
    """
    try:
        # This would query the database
        # For now, return a template response
        
        result = {
            "job_id": job_id,
            "message": "Job details require database session. Use DB query in full implementation.",
            "fields": ["title", "description", "requirements", "created_at"]
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error getting job details: {str(e)}"})


@tool
def filter_candidates(
    job_id: int,
    min_score: Optional[float] = None,
    skills: Optional[List[str]] = None,
    min_experience: Optional[int] = None
) -> str:
    """Filter candidates based on criteria.
    
    Use this tool to narrow down candidates by score, skills, or experience.
    
    Args:
        job_id: Job ID to filter candidates for
        min_score: Minimum overall score (0-100)
        skills: List of required skills
        min_experience: Minimum years of experience
    
    Returns:
        JSON string with filtered candidate list
    """
    try:
        result = {
            "job_id": job_id,
            "filters": {
                "min_score": min_score,
                "skills": skills,
                "min_experience": min_experience
            },
            "message": "Filtering requires database session and evaluation data."
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error filtering candidates: {str(e)}"})


# Helper function to create tools with DB session
def create_tools_with_db(db: Session):
    """Create tools with database session context."""
    
    @tool
    def search_candidates_db(job_id: int, query: str = None, top_k: int = 15) -> str:
        """Search candidates with DB context."""
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return json.dumps({"error": f"Job {job_id} not found"})
        
        search_query = query if query else job.description
        matches = retrieval_service.retrieve_top_k(search_query, top_k=min(top_k, 50))
        
        result = {
            "job_id": job_id,
            "job_title": job.title,
            "candidates": [
                {
                    "candidate_id": match.get("candidate_id"),
                    "score": round(match.get("score", 0), 3),
                    "metadata": match.get("metadata", {})
                }
                for match in matches
            ],
            "count": len(matches)
        }
        return json.dumps(result, indent=2)
    
    @tool
    def get_job_details_db(job_id: int) -> str:
        """Get job details with DB context."""
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return json.dumps({"error": f"Job {job_id} not found"})
        
        result = {
            "job_id": job.id,
            "title": job.title,
            "description": job.description,
            "created_at": job.created_at.isoformat() if job.created_at else None
        }
        return json.dumps(result, indent=2)
    
    @tool
    def evaluate_candidate_db(candidate_id: int, job_id: int) -> str:
        """Evaluate candidate with DB context."""
        job = db.query(Job).filter(Job.id == job_id).first()
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        
        if not job:
            return json.dumps({"error": f"Job {job_id} not found"})
        if not candidate:
            return json.dumps({"error": f"Candidate {candidate_id} not found"})
        
        evaluation_data = evaluate_candidate(job.description, candidate.resume_text)
        
        result = {
            "candidate_id": candidate_id,
            "candidate_name": candidate.name or "Unknown",
            "job_id": job_id,
            "job_title": job.title,
            **evaluation_data
        }
        return json.dumps(result, indent=2)
    
    @tool
    def compare_candidates_db(candidate_ids: List[int], job_id: int) -> str:
        """Compare multiple candidates side by side with DB context."""
        if len(candidate_ids) < 2:
            return json.dumps({"error": "Need at least 2 candidates to compare"})
        
        if len(candidate_ids) > 10:
            candidate_ids = candidate_ids[:10]
        
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return json.dumps({"error": f"Job {job_id} not found"})
        
        candidates = db.query(Candidate).filter(
            Candidate.id.in_(candidate_ids),
            Candidate.job_id == job_id
        ).all()
        
        if len(candidates) < 2:
            return json.dumps({"error": "Not enough candidates found for comparison"})
        
        # Get or create evaluations
        comparisons = []
        for candidate in candidates:
            # Check if evaluation exists
            evaluation = db.query(Evaluation).filter(
                Evaluation.candidate_id == candidate.id
            ).first()
            
            if not evaluation:
                # Create evaluation
                eval_data = evaluate_candidate(job.description, candidate.resume_text)
                evaluation = Evaluation(
                    candidate_id=candidate.id,
                    overall_score=eval_data["overall_score"],
                    technical_score=eval_data["technical_score"],
                    experience_score=eval_data["experience_score"],
                    education_score=eval_data["education_score"],
                    strengths=eval_data["strengths"],
                    concerns=eval_data["concerns"],
                    recommendation=eval_data["recommendation"],
                    ai_analysis=eval_data.get("ai_analysis", "")
                )
                db.add(evaluation)
                db.commit()
            
            comparisons.append({
                "candidate_id": candidate.id,
                "candidate_name": candidate.name or "Unknown",
                "overall_score": evaluation.overall_score,
                "technical_score": evaluation.technical_score,
                "experience_score": evaluation.experience_score,
                "education_score": evaluation.education_score,
                "recommendation": evaluation.recommendation,
                "strengths": evaluation.strengths or [],
                "concerns": evaluation.concerns or []
            })
        
        # Sort by overall score
        comparisons.sort(key=lambda x: x["overall_score"], reverse=True)
        
        result = {
            "job_id": job_id,
            "job_title": job.title,
            "comparisons": comparisons,
            "summary": f"Compared {len(comparisons)} candidates. Top ranked: {comparisons[0]['candidate_name']} (Score: {comparisons[0]['overall_score']:.1f})"
        }
        
        return json.dumps(result, indent=2)
    
    return [search_candidates_db, get_job_details_db, evaluate_candidate_db, compare_candidates_db]

