from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from ..schemas.llm import (
    ChatRequest,
    ChatResponse,
    SkillRecommendationRequest,
    SkillGapAnalysisRequest
)
from ..services.llm_client import llm_client

router = APIRouter(prefix="/api/llm", tags=["llm"])


@router.post("/chat", response_model=Dict[str, Any])
async def chat_completion(request: ChatRequest):
    """
    Generic LLM chat completion endpoint

    Sends a request to the LLM farm with configurable model, system, and user content.
    """
    try:
        response = await llm_client.chat_completion(
            user_content=request.user_content,
            system_content=request.system_content,
            model=request.model,
            max_tokens=request.max_tokens
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM request failed: {str(e)}")


@router.post("/skills/recommend")
async def recommend_skills(request: SkillRecommendationRequest):
    """
    Get AI-powered skill recommendations based on current skills and career goals
    """
    try:
        response = await llm_client.get_skill_recommendations(
            current_skills=request.current_skills,
            target_role=request.target_role,
            experience_level=request.experience_level
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skill recommendation failed: {str(e)}")


@router.post("/skills/gap-analysis")
async def analyze_skill_gap(request: SkillGapAnalysisRequest):
    """
    Analyze the gap between current skills and required skills for a target role
    """
    try:
        response = await llm_client.analyze_skill_gap(
            user_skills=request.user_skills,
            required_skills=request.required_skills
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skill gap analysis failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Check if LLM service is configured"""
    from ..core.config import settings

    return {
        "status": "configured" if settings.LLM_FARM_API_KEY else "not_configured",
        "base_url": settings.LLM_FARM_BASE_URL,
        "default_model": settings.LLM_DEFAULT_MODEL,
        "endpoint_example": f"{settings.LLM_FARM_BASE_URL}/publishers/anthropic/models/{settings.LLM_DEFAULT_MODEL}:rawPredict",
        "has_api_key": bool(settings.LLM_FARM_API_KEY)
    }
