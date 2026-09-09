import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


class GeminiClient:
    """Centralized Gemini API client."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Add it to your .env file."
            )

        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        )

        self.client = genai.Client(api_key=api_key)

    def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> str:
        """Generate a response using Gemini."""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
        )

        return response.text or ""