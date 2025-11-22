from app.services.retrieval import retrieval_service
from app.services.generation import evaluate_candidate
from app.models.database import Candidate, Evaluation, Job
from sqlalchemy.orm import Session
from typing import List
from app.models.schemas import EvaluationResponse


class RAGService:
    def __init__(self, db: Session):
        self.db = db
    
    def evaluate_job_candidates(self, job_id: int, top_k: int = 15) -> List[EvaluationResponse]:
        """
        Complete RAG pipeline: Retrieve top candidates and generate evaluations.
        
        Args:
            job_id: Job ID to evaluate candidates for
            top_k: Number of candidates to retrieve for evaluation
        
        Returns:
            List of top 5 evaluation responses
        """
        # Get job
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise ValueError(f"Job {job_id} not found")
        
        # RETRIEVAL: Get top K candidates using vector similarity
        matches = retrieval_service.retrieve_top_k(
            job_description=job.description,
            top_k=top_k
        )
        
        if not matches:
            return []
        
        # Get candidate IDs from matches
        candidate_ids = [match["candidate_id"] for match in matches if match.get("candidate_id")]
        
        # Get candidates from database
        candidates = self.db.query(Candidate).filter(
            Candidate.id.in_(candidate_ids),
            Candidate.job_id == job_id
        ).all()
        
        # GENERATION: Evaluate each retrieved candidate
        evaluations = []
        for candidate in candidates:
            try:
                # Generate evaluation using GPT-4
                evaluation_data = evaluate_candidate(
                    job_description=job.description,
                    resume_text=candidate.resume_text
                )
                
                # Save evaluation to database
                evaluation = Evaluation(
                    candidate_id=candidate.id,
                    overall_score=evaluation_data["overall_score"],
                    technical_score=evaluation_data["technical_score"],
                    experience_score=evaluation_data["experience_score"],
                    education_score=evaluation_data["education_score"],
                    strengths=evaluation_data["strengths"],
                    concerns=evaluation_data["concerns"],
                    recommendation=evaluation_data["recommendation"],
                    ai_analysis=evaluation_data.get("ai_analysis", "")
                )
                
                # Update or create evaluation
                existing = self.db.query(Evaluation).filter(
                    Evaluation.candidate_id == candidate.id
                ).first()
                
                if existing:
                    for key, value in evaluation_data.items():
                        if key != "ai_analysis":
                            setattr(existing, key, value)
                    existing.ai_analysis = evaluation_data.get("ai_analysis", "")
                else:
                    self.db.add(evaluation)
                
                self.db.commit()
                
                # Create response
                eval_response = EvaluationResponse(
                    candidate_id=candidate.id,
                    candidate_name=candidate.name or "Unknown",
                    overall_score=evaluation_data["overall_score"],
                    technical_score=evaluation_data["technical_score"],
                    experience_score=evaluation_data["experience_score"],
                    education_score=evaluation_data["education_score"],
                    strengths=evaluation_data["strengths"],
                    concerns=evaluation_data["concerns"],
                    recommendation=evaluation_data["recommendation"],
                    ai_analysis=evaluation_data.get("ai_analysis")
                )
                
                evaluations.append(eval_response)
                
            except Exception as e:
                print(f"Error evaluating candidate {candidate.id}: {e}")
                continue
        
        # RANKING: Sort by overall score and return top 5
        evaluations.sort(key=lambda x: x.overall_score, reverse=True)
        return evaluations[:5]

