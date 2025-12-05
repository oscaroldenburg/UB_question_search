from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI
import os

import json
import numpy as np

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

load_dotenv()

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
)
EMBEDDING_DEPLOYMENT = os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"]
def embed_text(text: str):
    """Skapa embedding för en text med Azure OpenAI."""
    response = client.embeddings.create(
        model=EMBEDDING_DEPLOYMENT,
        input=text,
    )
    print(f"Number of tokens: {response.usage.prompt_tokens}")
    return response.data[0].embedding


def cosine_similarity(a, b):
    """Cosine similarity mellan två vektorer."""
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


@app.get("/search")
def search(q: str, limit: int = 10):
    """
    Sök i frågebanken med semantisk likhet.
    - q embed:as
    - jämförs med embedded_question för varje fråga
    - returnerar top 'limit' frågor sorterade på likhet
    """
    questions_path = "questions_with_embeddings.json"
    try:
        with open(questions_path, "r", encoding="utf-8") as f:
            questions = json.load(f)
    except Exception:
        questions = []
        
    if not q:
        # Inget query → returnera allt (ev. ändra om du hellre vill returnera tom lista)
        return {"items": questions, "total": len(questions)}

    if len(questions) == 0:
        return {"items": [], "total": 0}

    # 1. Embedda sökfrågan
    query_vec = embed_text(q)

    scored_items = []

    for item in questions:
        emb = item.get("embedded_question")
        if not emb:
            # Hoppa över om det inte finns embedding (eller embedda on-the-fly om du vill)
            continue

        score = cosine_similarity(query_vec, emb)

        # Kopiera objektet + lägg till similarity-score (bra för debugging/UI)
        scored_items.append({
            **item,
            "similarity": score,
        })

    # 2. Sortera på similarity (högst först)
    scored_items.sort(key=lambda x: x["similarity"], reverse=True)

    # 3. Begränsa antal träffar
    top_items = []
    for item in scored_items:
        if item.get("similarity"):  # just for testing
            print("Similarity:", item.get("similarity"))
            top_items.append(item)
        if len(top_items) >= limit-1:
            break
    #top_items = scored_items[:limit]

    return {
        "items": top_items,
        "total": len(top_items),
    }

""" 
@app.get("/search")
def search(q: str):
    # Mock data for UI development
    # Load questions.json located next to this file
    questions_path = "questions_with_embeddings.json"
    try:
        with open(questions_path, "r", encoding="utf-8") as f:
            questions = json.load(f)
    except Exception:
        questions = []
        

    # Filter simple mock
    filtered = [i for i in questions if q and q.lower() in i.get("embedded_question", "").lower()] if q else []
    
    return {"items": filtered if filtered else questions, "total": len(filtered) or len(questions)}
 """