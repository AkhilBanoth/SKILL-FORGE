
import time

from google import genai
from google.genai import errors
from app.config import settings

api_key = settings.GEMINI_API_KEY
client = genai.Client(api_key=api_key) if api_key else None


def generate_response(prompt: str) -> str:
    """Generate text with Gemini and retry temporary service failures."""

    if not api_key or client is None:
        return (
            "AI generation is not configured because GEMINI_API_KEY is missing. "
            "Add a valid key in the backend .env file to enable Gemini responses."
        )

    model = settings.GEMINI_MODEL
    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            if not response.text:
                raise RuntimeError("Gemini returned an empty response.")

            return response.text.strip()

        except errors.ServerError as exc:
            # Retry only temporary server errors, such as HTTP 503.
            if exc.code not in (500, 502, 503, 504):
                raise

            if attempt == max_attempts - 1:
                raise

            time.sleep(2 ** attempt)

    raise RuntimeError("Gemini could not generate a response.")
