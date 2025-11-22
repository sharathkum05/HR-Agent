from openai import OpenAI
from app.config import settings
from typing import Dict
import json

client = OpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """You are an expert HR recruiter with 15+ years of experience in technical hiring. 
Your task is to evaluate candidates objectively and provide detailed, actionable insights.

Guidelines:
- Be thorough but concise
- Focus on evidence from the resume
- Identify both strengths and potential concerns
- Provide specific examples when possible
- Use a consistent scoring rubric
- Be fair and unbiased"""


def evaluate_candidate(job_description: str, resume_text: str) -> Dict:
    """
    Evaluate a candidate using GPT-4.
    
    Args:
        job_description: Job description text
        resume_text: Candidate resume text
    
    Returns:
        Dictionary with evaluation scores and analysis
    """
    try:
        prompt = f"""Evaluate the following candidate for this job opening:

=== JOB DESCRIPTION ===
{job_description}

=== CANDIDATE RESUME ===
{resume_text[:4000]}  # Limit resume text to avoid token limits

=== EVALUATION TASK ===
Provide a comprehensive evaluation in the following JSON format:

{{
  "technical_score": <0-100>,
  "technical_analysis": "<brief analysis>",
  "experience_score": <0-100>,
  "experience_analysis": "<brief analysis>",
  "education_score": <0-100>,
  "education_analysis": "<brief analysis>",
  "overall_score": <0-100>,
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "concerns": ["<concern 1>", "<concern 2>"],
  "recommendation": "<Strong Match | Good Match | Moderate Match | Weak Match>",
  "summary": "<2-3 sentence summary>"
}}

Scoring Guidelines:
- Technical Skills: 0-40 (missing critical skills), 41-60 (some gaps), 61-80 (good match), 81-100 (excellent match)
- Experience: 0-40 (<1 year relevant), 41-60 (1-3 years), 61-80 (3-5 years), 81-100 (5+ years or exceptional)
- Education: 0-40 (doesn't meet requirements), 41-60 (meets minimum), 61-80 (exceeds minimum), 81-100 (significantly exceeds)
- Overall: Weighted average (Technical: 30%, Experience: 40%, Education: 15%, Cultural: 15% estimated)

Recommendation Guidelines:
- Strong Match: Overall score 80+, all critical requirements met
- Good Match: Overall score 65-79, most requirements met
- Moderate Match: Overall score 50-64, some gaps but potential
- Weak Match: Overall score <50, significant gaps
"""

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        # Parse JSON response
        content = response.choices[0].message.content
        evaluation = json.loads(content)
        
        # Validate and structure response
        return {
            "technical_score": float(evaluation.get("technical_score", 0)),
            "technical_analysis": evaluation.get("technical_analysis", ""),
            "experience_score": float(evaluation.get("experience_score", 0)),
            "experience_analysis": evaluation.get("experience_analysis", ""),
            "education_score": float(evaluation.get("education_score", 0)),
            "education_analysis": evaluation.get("education_analysis", ""),
            "overall_score": float(evaluation.get("overall_score", 0)),
            "strengths": evaluation.get("strengths", []),
            "concerns": evaluation.get("concerns", []),
            "recommendation": evaluation.get("recommendation", "Moderate Match"),
            "summary": evaluation.get("summary", ""),
            "ai_analysis": content  # Store full analysis
        }
    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing GPT-4 JSON response: {str(e)}")
    except Exception as e:
        raise Exception(f"Error evaluating candidate with GPT-4: {str(e)}")

