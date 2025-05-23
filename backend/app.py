#Backend Python (FastAPI)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path

app = FastAPI()



# Autorise le front local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre plus tard en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI"}

# Sert le frontend buildé statiquement (après build React)
app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)