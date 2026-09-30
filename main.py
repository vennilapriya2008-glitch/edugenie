from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_concept
from learning_path import generate_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000,
        description="User input text",
    )
    level: str = Field(
        default="beginner",
        description="Learner level",
    )


def clean_input(text: str) -> str:
    cleaned = text.strip()

    if not cleaned:
        raise HTTPException(
            status_code=422,
            detail="Please enter some text.",
        )

    return cleaned


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "application": "EduGenie",
        "version": "1.0.0",
    }


@app.post("/qa")
async def qa(payload: TextRequest):
    text = clean_input(payload.text)

    try:
        result = answer_question(
            question=text,
            level=payload.level,
        )

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to answer the question: {exc}",
        ) from exc


@app.post("/explain")
async def explain(payload: TextRequest):
    text = clean_input(payload.text)

    try:
        result = explain_concept(
            concept=text,
            level=payload.level,
        )

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to generate explanation: {exc}",
        ) from exc


@app.post("/quiz")
async def quiz(payload: TextRequest):
    text = clean_input(payload.text)

    try:
        result = generate_quiz(
            topic=text,
            level=payload.level,
        )

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to generate quiz: {exc}",
        ) from exc


@app.post("/summarize")
async def summarize(payload: TextRequest):
    text = clean_input(payload.text)

    try:
        result = summarize_text(
            text=text,
            level=payload.level,
        )

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to summarize text: {exc}",
        ) from exc


@app.post("/learn/recommendations")
async def learning_recommendations(payload: TextRequest):
    text = clean_input(payload.text)

    try:
        result = generate_learning_recommendations(
            topic=text,
            level=payload.level,
        )

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to generate learning recommendations: {exc}",
        ) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )