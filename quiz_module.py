import json
import re
from typing import Any, Dict, List

from ai_client import generate_text


def _remove_markdown_fences(text: str) -> str:
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


def _validate_quiz(data: Any) -> List[Dict[str, Any]]:

    if not isinstance(data, list):
        raise ValueError(
            "Quiz response must be a JSON list."
        )

    if len(data) != 3:
        raise ValueError(
            "Quiz must contain exactly 3 questions."
        )

    required_fields = {
        "question",
        "options",
        "correct_answer",
        "explanation",
    }

    for index, item in enumerate(data, start=1):

        if not isinstance(item, dict):
            raise ValueError(
                f"Question {index} is invalid."
            )

        missing = required_fields - set(item.keys())

        if missing:
            raise ValueError(
                f"Question {index} is missing: "
                f"{', '.join(sorted(missing))}"
            )

        options = item["options"]

        if not isinstance(options, dict):
            raise ValueError(
                f"Question {index} options must be an object."
            )

        expected = {"A", "B", "C", "D"}

        if set(options.keys()) != expected:
            raise ValueError(
                f"Question {index} must have "
                "A, B, C and D options."
            )

        if item["correct_answer"] not in expected:
            raise ValueError(
                f"Question {index} has an invalid "
                "correct answer."
            )

    return data


def generate_quiz(
    topic: str,
    level: str = "beginner",
) -> List[Dict[str, Any]]:

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create a multiple-choice quiz for this topic:

Topic:
{topic}

Student level:
{level}

Create exactly 3 questions.

Every question must contain:

- question
- options
- correct_answer
- explanation

The options must contain exactly:

A
B
C
D

The correct_answer must be one of:

A
B
C
D

Return ONLY valid JSON.

Required format:

[
  {{
    "question": "Question text",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "correct_answer": "A",
    "explanation": "Explanation of the answer"
  }}
]
"""

    raw = generate_text(
        prompt,
        temperature=0.5,
        json_output=True,
    )

    cleaned = _remove_markdown_fences(raw)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Gemini returned invalid quiz JSON."
        ) from exc

    return _validate_quiz(data)