import os
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash",
).strip()

if not GEMINI_API_KEY:
    client: Optional[genai.Client] = None
else:
    client = genai.Client(api_key=GEMINI_API_KEY)


def generate_text(
    prompt: str,
    temperature: float = 0.4,
    json_output: bool = False,
) -> str:

    if client is None:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Create a .env file and add your Gemini API key."
        )

    config_kwargs = {
        "temperature": temperature,
    }

    if json_output:
        config_kwargs["response_mime_type"] = "application/json"

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            **config_kwargs
        ),
    )

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()