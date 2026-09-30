import json
import re
from typing import Any, Dict

from ai_client import generate_text


def _clean_json(text: str) -> str:
    text = text.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"^```\s*",
        "",
        text,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    return text.strip()


def generate_learning_recommendations(
    topic: str,
    level: str = "beginner",
) -> Dict[str, Any]:

    prompt = f"""
You are EduGenie, a personalized learning-path generator.

Create a structured learning path for:

Topic:
{topic}

Current learner level:
{level}

Return ONLY valid JSON.

Use this structure:

{{
  "topic": "Topic name",
  "level": "Learner level",
  "goal": "Overall learning goal",
  "estimated_timeline": "Estimated timeline",
  "stages": [
    {{
      "stage": 1,
      "title": "Stage title",
      "objectives": [
        "Objective 1",
        "Objective 2"
      ],
      "activities": [
        "Activity 1",
        "Activity 2"
      ],
      "project": "Small practical project"
    }}
  ],
  "recommended_resource_types": [
    "Resource type 1",
    "Resource type 2"
  ],
  "final_project": "Suggested final project"
}}

Create a progression from beginner concepts toward more advanced concepts.

Keep the plan practical and suitable for the learner level.
"""

    raw = generate_text(
        prompt,
        temperature=0.5,
        json_output=True,
    )

    cleaned = _clean_json(raw)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Gemini returned invalid learning-path JSON."
        ) from exc