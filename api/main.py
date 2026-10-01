from pathlib import Path
import sys

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from backend.rag.rag_pipeline import generate_answer


# -----------------------------------------
# FastAPI application
# -----------------------------------------

app = FastAPI(
    title="Yojana Mitra API",
    description="Personalized multilingual government scheme assistant",
    version="1.0"
)


# -----------------------------------------
# CORS
# -----------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------
# Load scheme data
# -----------------------------------------

CSV_PATH = (
    BASE_DIR
    / "data"
    / "csv"
    / "yojana_mitra_master.csv"
)

schemes_df = pd.read_csv(CSV_PATH)


# -----------------------------------------
# Request models
# -----------------------------------------

class Profile(BaseModel):
    age: int
    state: str
    occupation: str
    income: float
    gender: str
    social_category: str


class AskRequest(BaseModel):
    profile: Profile
    question: str
    language: str = "English"


# -----------------------------------------
# Home endpoint
# -----------------------------------------

@app.get("/")
def home():
    return {
        "message": "Yojana Mitra API is running"
    }


# -----------------------------------------
# Get schemes
# -----------------------------------------

@app.get("/api/schemes")
def get_schemes(state: str = None):

    if state:
        state_schemes = schemes_df[
            schemes_df["state"]
            .fillna("")
            .str.contains(
                state,
                case=False,
                na=False
            )
        ]
    else:
        state_schemes = schemes_df

    schemes = (
        state_schemes
        .head(50)
        .fillna("")
        .to_dict(orient="records")
    )

    return {
        "state": state,
        "count": len(state_schemes),
        "schemes": schemes
    }


# -----------------------------------------
# Get one scheme
# -----------------------------------------

@app.get("/api/schemes/{scheme_id}")
def get_scheme_by_id(scheme_id: str):

    scheme = schemes_df[
        schemes_df["scheme_id"]
        .astype(str)
        == str(scheme_id)
    ]

    if scheme.empty:
        return {
            "error": "Scheme not found"
        }

    return (
        scheme
        .iloc[0]
        .fillna("")
        .to_dict()
    )


# -----------------------------------------
# Ask Yojana Mitra
# -----------------------------------------

@app.post("/api/ask")
def ask_yojana_mitra(request: AskRequest):

    profile = request.profile.model_dump()

    answer = generate_answer(
        user_profile=profile,
        question=request.question,
        language=request.language,
        top_k=5
    )

    return {
        "question": request.question,
        "language": request.language,
        "answer": answer
    }