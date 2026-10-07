from pathlib import Path
import sys

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel


# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


# ============================================================
# IMPORTS
# ============================================================

from backend.chatbot.chatbot import chatbot_response


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Yojana Mitra API",
    description="Personalized multilingual government scheme assistant",
    version="1.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# MASTER CSV
# ============================================================

CSV_PATH = BASE_DIR / "data" / "csv" / "yojana_mitra_master.csv"

schemes_df = pd.read_csv(CSV_PATH)


# ============================================================
# DATA MODELS
# ============================================================

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


# ============================================================
# API HOME
# ============================================================

@app.get("/api")
def api_home():

    return {
        "message": "Yojana Mitra API is running"
    }


# ============================================================
# GET SCHEMES
# ============================================================

@app.get("/api/schemes")
def get_schemes(state: str = None):

    if state:

        state_schemes = schemes_df[
            schemes_df["state"]
            .fillna("")
            .astype(str)
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


# ============================================================
# GET SINGLE SCHEME
# ============================================================

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

    return scheme.iloc[0].fillna("").to_dict()


# ============================================================
# OLD GEMINI / RAG API
#
# KEEPING THIS UNTOUCHED
# ============================================================

@app.post("/api/ask")
def ask_yojana_mitra(request: AskRequest):

    profile = request.profile.model_dump()

    try:

        from backend.rag.rag_pipeline import generate_answer

        answer = generate_answer(
            user_profile=profile,
            question=request.question,
            language=request.language,
            top_k=3
        )

        return {
            "question": request.question,
            "language": request.language,
            "answer": answer
        }

    except Exception as e:

        import traceback

        print("\n========== RAG ERROR ==========")
        print(repr(e))
        traceback.print_exc()
        print("================================\n")

        return {
            "question": request.question,
            "language": request.language,
            "answer": "Sorry, I couldn't get an answer right now. Please try again."
        }


# ============================================================
# YOJANALM API
#
# NEW CLEAN PATH
# ============================================================

@app.post("/api/ask-yojanalm")
def ask_yojanalm(request: AskRequest):

    try:

        # ------------------------------------------------------
        # Convert profile to dictionary
        # ------------------------------------------------------

        profile = request.profile.model_dump()


        # ------------------------------------------------------
        # Build a natural-language query
        # ------------------------------------------------------

        profile_text = (
            f"I am {profile['age']} years old, "
            f"from {profile['state']}, "
            f"working as a {profile['occupation']}, "
            f"with an annual income of {profile['income']}, "
            f"gender {profile['gender']}, "
            f"social category {profile['social_category']}. "
        )

        query = profile_text + request.question


        # ------------------------------------------------------
        # Call YojanaLM
        # ------------------------------------------------------

        answer = chatbot_response(query)


        # ------------------------------------------------------
        # Return ONLY the clean answer
        # ------------------------------------------------------

        return {
            "question": request.question,
            "language": request.language,
            "answer": answer
        }


    except Exception as e:

        import traceback

        print("\n========== YOJANALM API ERROR ==========")
        print(repr(e))
        traceback.print_exc()
        print("=========================================\n")

        return {
            "question": request.question,
            "language": request.language,
            "answer": "Sorry, I couldn't get an answer right now. Please try again."
        }


# ============================================================
# REACT FRONTEND
# ============================================================

FRONTEND_DIST = BASE_DIR / "frontend" / "dist"


if FRONTEND_DIST.exists():

    assets_path = FRONTEND_DIST / "assets"

    if assets_path.exists():

        from fastapi.staticfiles import StaticFiles

        app.mount(
            "/assets",
            StaticFiles(
                directory=str(assets_path)
            ),
            name="assets"
        )


# ============================================================
# FRONTEND FALLBACK
# ============================================================

@app.get("/{full_path:path}")
def serve_frontend(full_path: str):

    requested_file = FRONTEND_DIST / full_path

    if (
        requested_file.exists()
        and requested_file.is_file()
    ):

        return FileResponse(requested_file)


    index_file = FRONTEND_DIST / "index.html"

    if index_file.exists():

        return FileResponse(index_file)


    return {
        "message": "Yojana Mitra API is running"
    }