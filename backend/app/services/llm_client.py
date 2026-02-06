"""
LLM Farm Client Service
Handles communication with the Bosch LLM Farm (Google Vertex AI format)
"""
import httpx
from typing import Optional, List, Dict, Any
from ..core.config import settings


class LLMClient:
    """Client for interacting with the Bosch LLM farm"""

    def __init__(self):
        self.base_url = settings.LLM_FARM_BASE_URL
        self.api_key = settings.LLM_FARM_API_KEY
        self.default_model = settings.LLM_DEFAULT_MODEL
        self.default_max_tokens = settings.LLM_DEFAULT_MAX_TOKENS

    def _build_endpoint_url(self, model: str) -> str:
        """Build the full endpoint URL for a specific model"""
        return f"{self.base_url}/publishers/anthropic/models/{model}:rawPredict"

    async def chat_completion(
        self,
        user_content: str,
        system_content: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to the Bosch LLM farm

        Args:
            user_content: The user's message/prompt
            system_content: Optional system prompt to guide the model
            model: Model name (defaults to claude-sonnet-4-5@20250929)
            max_tokens: Maximum tokens in response

        Returns:
            Dict containing the LLM response
        """
        if not self.api_key:
            raise ValueError("LLM_FARM_API_KEY is not configured")

        # Use specified model or default
        model_name = model or self.default_model
        endpoint_url = self._build_endpoint_url(model_name)

        # Use specified max_tokens or default
        tokens_limit = max_tokens or self.default_max_tokens

        # Build messages array (Anthropic format)
        messages = []
        messages.append({
            "role": "user",
            "content": user_content
        })

        # Prepare request payload (Anthropic Messages API format)
        payload = {
            "anthropic_version": "vertex-2023-10-16",
            "messages": messages,
            "max_tokens": tokens_limit
        }

        # Add system prompt if provided
        if system_content:
            payload["system"] = system_content

        # Make request to Bosch LLM farm
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                endpoint_url,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()

    async def get_skill_recommendations(
        self,
        current_skills: List[str],
        target_role: str,
        experience_level: str
    ) -> Dict[str, Any]:
        """
        Get AI-powered skill recommendations based on current skills and goals
        """
        system_prompt = """You are an expert career development advisor specializing in technology skills.
Your task is to provide personalized skill recommendations based on the user's current skills and career goals.
Provide specific, actionable recommendations with reasoning."""

        user_prompt = f"""
I currently have these skills: {', '.join(current_skills)}
My target role is: {target_role}
My experience level: {experience_level}

Please recommend:
1. Top 5 skills I should focus on developing
2. Skills I already have that are valuable for my target role
3. Learning path priorities (which skills to learn first and why)

Format your response as structured JSON with keys: recommended_skills, valuable_current_skills, learning_path
"""

        return await self.chat_completion(
            user_content=user_prompt,
            system_content=system_prompt
        )

    async def analyze_skill_gap(
        self,
        user_skills: List[Dict[str, Any]],
        required_skills: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze the gap between user's skills and required skills for a role
        """
        system_prompt = """You are a skills gap analysis expert. Analyze the difference between
current competencies and required competencies, providing actionable insights."""

        user_prompt = f"""
Current Skills: {user_skills}
Required Skills: {required_skills}

Analyze the gap and provide:
1. Critical gaps that need immediate attention
2. Partial matches where upskilling is needed
3. Strengths that already meet requirements
4. Estimated timeline to close the gap
5. Recommended learning resources or approaches

Format as structured JSON.
"""

        return await self.chat_completion(
            user_content=user_prompt,
            system_content=system_prompt
        )


# Global instance
llm_client = LLMClient()
