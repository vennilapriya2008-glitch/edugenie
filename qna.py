from ai_client import generate_text


def answer_question(
    question: str,
    level: str = "beginner",
) -> str:

    prompt = f"""
You are EduGenie, an educational AI tutor.

Answer the student's question accurately and clearly.

Student level:
{level}

Question:
{question}

Instructions:

1. Explain the answer in a student-friendly way.
2. Start with the direct answer.
3. Explain important concepts.
4. Use simple examples where useful.
5. Avoid unnecessary complexity.
6. If the question involves a technical concept, explain terminology.
7. If there are multiple steps, use numbered steps.
8. Do not invent facts.
9. End with a short "Key Takeaway" section.

Return only the educational answer.
"""

    return generate_text(
        prompt,
        temperature=0.3,
    )