from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json

app = FastAPI()

# CORS – så att din Vue-app får prata med API:et lokalt och från Azure
origins = [
    "http://localhost:5173",  # Vite dev
    # lägg till din frontend-URL i Azure här sen, t.ex:
    # "https://dinapp.azurestaticapps.net",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/search")
def search(q: str):
    # Mock data for UI development
    # Load questions.json located next to this file
    questions_path = "questions.json"
    try:
        with open(questions_path, "r", encoding="utf-8") as f:
            questions = json.load(f)
    except Exception:
        questions = []
        

    # Filter simple mock
    filtered = [i for i in questions if q and q.lower() in i.get("question", "").lower()] if q else []
    
    return {"items": filtered if filtered else questions, "total": len(filtered) or len(questions)}
