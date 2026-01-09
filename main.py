from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from db import SessionLocal, engine
from models import Review, Base
from llm import call_llm


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- Schemas --------

class ReviewInput(BaseModel):
    rating: int
    review: str

# -------- API --------

@app.post("/submit-review")
def submit_review(data: ReviewInput):
    if not data.review.strip():
        raise HTTPException(status_code=400, detail="Review cannot be empty")

    if len(data.review) > 2000:
        raise HTTPException(status_code=400, detail="Review too long")

    user_prompt = f"""
User gave {data.rating} star rating and wrote:
{data.review}

Write a polite helpful response to the user.
"""

    summary_prompt = f"""
Summarize the following review in one sentence:
{data.review}
"""

    action_prompt = f"""
Based on this customer review, suggest one recommended business action:
{data.review}
"""

    try:
        ai_response = call_llm(user_prompt)
        ai_summary = call_llm(summary_prompt)
        ai_action = call_llm(action_prompt)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="LLM failure")

    db = SessionLocal()
    rec = Review(
        rating=data.rating,
        review_text=data.review,
        ai_response=ai_response,
        ai_summary=ai_summary,
        ai_action=ai_action
    )
    db.add(rec)
    db.commit()
    db.close()

    return {"message": "Submitted", "ai_response": ai_response}


@app.get("/admin/submissions")
def get_submissions():
    db = SessionLocal()
    data = db.query(Review).order_by(Review.id.desc()).all()
    db.close()

    return [
        {
            "rating": r.rating,
            "review": r.review_text,
            "summary": r.ai_summary,
            "action": r.ai_action
        }
        for r in data
    ]

