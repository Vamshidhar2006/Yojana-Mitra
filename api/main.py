from pathlib import Path
import sys

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))


app = FastAPI(
    title="Yojana Mitra API",
    description="Personalized multilingual government scheme assistant",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


CSV_PATH = BASE_DIR / "data" / "csv" / "yojana_mitra_master.csv"

schemes_df = pd.read_csv(CSV_PATH)


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


@app.get("/api")
def api_home():
    return {
        "message": "Yojana Mitra API is running"
    }


@app.get("/api/schemes")
def get_schemes(state: str = None):

    if state:
        state_schemes = schemes_df[
            schemes_df["state"].fillna("").str.contains(
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


@app.get("/api/schemes/{scheme_id}")
def get_scheme_by_id(scheme_id: str):

    scheme = schemes_df[
        schemes_df["scheme_id"].astype(str) == str(scheme_id)
    ]

    if scheme.empty:
        return {
            "error": "Scheme not found"
        }

    return scheme.iloc[0].fillna("").to_dict()


@app.post("/api/ask")
def ask_yojana_mitra(request: AskRequest):

    print("========== CHAT REQUEST RECEIVED ==========")
    print("PROFILE:", request.profile.model_dump())
    print("QUESTION:", request.question)
    print("LANGUAGE:", request.language)
    print("===========================================")

    return {
        "question": request.question,
        "language": request.language,
        "answer": "Test response from Yojana Mitra backend."
    }


# --------------------------------------------------
# Serve React frontend
# --------------------------------------------------

FRONTEND_DIST = BASE_DIR / "frontend" / "dist"


if FRONTEND_DIST.exists():

    assets_path = FRONTEND_DIST / "assets"

    if assets_path.exists():

        from fastapi.staticfiles import StaticFiles

        app.mount(
            "/assets",
            StaticFiles(directory=str(assets_path)),
            name="assets"
        )


@app.get("/{full_path:path}")
def serve_frontend(full_path: str):

    requested_file = FRONTEND_DIST / full_path

    if requested_file.exists() and requested_file.is_file():
        return FileResponse(requested_file)

    index_file = FRONTEND_DIST / "index.html"

    if index_file.exists():
        return FileResponse(index_file)

    return {
        "message": "Yojana Mitra API is running"
    }