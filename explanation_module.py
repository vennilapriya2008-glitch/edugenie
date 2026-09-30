import os

from ai_client import generate_text


def explain_concept(concept: str, level: str = "beginner") -> str:
    """
    Explain an educational concept at the requested difficulty level.

    Uses Gemini by default. If USE_LOCAL_EXPLAINER=true is configured,
    a local LaMini-Flan-T5 model can be used instead.
    """

    use_local = os.getenv("USE_LOCAL_EXPLAINER", "false").lower() == "true"

    if use_local:
        try:
            from transformers import pipeline

            model_name = os.getenv(
                "LOCAL_EXPLAINER_MODEL",
                "MBZUAI/LaMini-Flan-T5-783M"
            )

            generator = pipeline(
                "text2text-generation",
                model=model_name
            )

            prompt = (
                f"Explain the following concept for a {level} student. "
                f"Use simple language, examples, and important points.\n\n"
                f"Concept: {concept}"
            )

            result = generator(
                prompt,
                max_new_tokens=300,
                do_sample=False
            )

            return result[0]["generated_text"].strip()

        except Exception:
            # If the optional local model is unavailable,
            # fall back to Gemini.
            pass

    prompt = f"""
You are EduGenie, an educational tutor.

Explain the following concept to a {level} learner.

Concept:
{concept}

Requirements:
- Use simple and clear language.
- Start with a short definition.
- Explain the concept step by step.
- Give a practical or easy-to-understand example.
- Mention important points the student should remember.
- Avoid unnecessary technical jargon.
"""

    return generate_text(prompt)