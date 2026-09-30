from ai_client import generate_text


def summarize_text(
    text: str,
    level: str = "beginner",
) -> str:

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following material for a {level} learner.

Material:
{text}

Create a useful study summary.

Use this structure:

# Summary

## Main Idea
Give the central idea.

## Important Points
List the most important facts or concepts.

## Key Terms
Explain important terminology.

## Quick Revision
Give a short revision section.

## Key Takeaway
Give the most important thing the student should remember.

Do not add information that is not supported by the supplied material.
"""

    return generate_text(
        prompt,
        temperature=0.3,
    )