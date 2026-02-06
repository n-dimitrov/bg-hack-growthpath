from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    user_content: str = Field(..., description="The user's message or prompt")
    system_content: Optional[str] = Field(None, description="Optional system prompt to guide the model")
    model: Optional[str] = Field(None, description="Model name (defaults to claude-sonnet-4-5@20250929)")
    max_tokens: Optional[int] = Field(None, ge=1, le=8192, description="Maximum tokens in response (defaults to env LLM_DEFAULT_MAX_TOKENS)")


class ChatResponse(BaseModel):
    response: str
    model: str
    usage: Optional[dict] = None


class SkillRecommendationRequest(BaseModel):
    current_skills: list[str] = Field(..., description="List of current skills")
    target_role: str = Field(..., description="Desired job role or position")
    experience_level: str = Field(..., description="Current experience level (junior, mid, senior, etc.)")


class SkillGapAnalysisRequest(BaseModel):
    user_skills: list[dict] = Field(..., description="User's current skills with proficiency levels")
    required_skills: list[dict] = Field(..., description="Required skills for target role")
