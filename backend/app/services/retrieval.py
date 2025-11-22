from pinecone import Pinecone
from app.config import settings
from app.services.embedding import get_embedding
from typing import List, Dict
import uuid


class RetrievalService:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self.index_name = settings.pinecone_index_name
        self._ensure_index()
    
    def _ensure_index(self):
        """Ensure Pinecone index exists, create if not."""
        try:
            # Check if index exists
            existing_indexes = [idx.name for idx in self.pc.list_indexes()]
            if self.index_name not in existing_indexes:
                # Create index with dimension 1536 (text-embedding-3-small)
                self.pc.create_index(
                    name=self.index_name,
                    dimension=1536,
                    metric="cosine"
                )
        except Exception as e:
            print(f"Warning: Could not ensure index exists: {e}")
    
    def upsert_resume(self, candidate_id: int, resume_text: str, metadata: Dict = None) -> str:
        """
        Store resume embedding in Pinecone.
        
        Args:
            candidate_id: Database candidate ID
            resume_text: Resume text content
            metadata: Additional metadata to store
        
        Returns:
            Pinecone ID for the vector
        """
        try:
            # Generate embedding
            embedding = get_embedding(resume_text)
            
            # Create unique ID
            pinecone_id = f"candidate_{candidate_id}_{uuid.uuid4().hex[:8]}"
            
            # Prepare metadata
            vector_metadata = {
                "candidate_id": candidate_id,
                "resume_text": resume_text[:1000]  # Store first 1000 chars for reference
            }
            if metadata:
                vector_metadata.update(metadata)
            
            # Upsert to Pinecone
            index = self.pc.Index(self.index_name)
            index.upsert(
                vectors=[{
                    "id": pinecone_id,
                    "values": embedding,
                    "metadata": vector_metadata
                }]
            )
            
            return pinecone_id
        except Exception as e:
            raise Exception(f"Error upserting resume to Pinecone: {str(e)}")
    
    def retrieve_top_k(self, job_description: str, top_k: int = 15) -> List[Dict]:
        """
        Retrieve top K candidates using vector similarity search.
        
        Args:
            job_description: Job description text
            top_k: Number of top candidates to retrieve
        
        Returns:
            List of candidate matches with scores and metadata
        """
        try:
            # Generate embedding for job description
            job_embedding = get_embedding(job_description)
            
            # Query Pinecone
            index = self.pc.Index(self.index_name)
            results = index.query(
                vector=job_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Format results
            matches = []
            for match in results.matches:
                matches.append({
                    "pinecone_id": match.id,
                    "candidate_id": match.metadata.get("candidate_id"),
                    "score": match.score,
                    "metadata": match.metadata
                })
            
            return matches
        except Exception as e:
            raise Exception(f"Error retrieving candidates from Pinecone: {str(e)}")
    
    def delete_resume(self, pinecone_id: str):
        """Delete a resume vector from Pinecone."""
        try:
            index = self.pc.Index(self.index_name)
            index.delete(ids=[pinecone_id])
        except Exception as e:
            print(f"Warning: Could not delete from Pinecone: {e}")


retrieval_service = RetrievalService()

