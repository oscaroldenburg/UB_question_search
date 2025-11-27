from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    mock_items = [
        {"question": f"Vad tycker du om {q}?", "category": "Samhälle", "year": 2023},
        {"question": f"Hur ofta använder du {q} i vardagen?", "category": "Livsstil", "year": 2024},
        {"question": "Vilket parti skulle du rösta på idag?", "category": "Politik", "year": 2023},
        {"question": "Hur ser du på framtiden?", "category": "Framtid", "year": 2022},
    ]
    # Filter simple mock
    filtered = [i for i in mock_items if q.lower() in i["question"].lower()] if q else []
    print(filtered)
    
    return {"items": filtered if filtered else mock_items, "total": len(filtered) or len(mock_items)}
