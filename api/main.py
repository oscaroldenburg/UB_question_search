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
    # TODO: koppla till din söklogik/Typesense/Postgres
    return {"items": q*2, "total": 0}