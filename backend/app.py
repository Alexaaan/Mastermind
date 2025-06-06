from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # Pour servir le build React en prod
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine, Base
from db.models import User, Game
from websocket_manager import router as websocket_router
from pydantic import BaseModel
from typing import List

# Créer les tables en base si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(websocket_router)

# Dans le cas d'un build React en production, on monte le dossier "static"
# (contenant index.html + JS/CSS générés par npm run build)
# ici on sert tout depuis /backend/static
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Autoriser le frontend React en dev (port 5173) à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modèle Pydantic pour la route /login, pour recevoir { "pseudo": "..." }
class LoginRequest(BaseModel):
    pseudo: str

@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    pseudo = request.pseudo
    user = db.query(User).filter(User.pseudo == pseudo).first()
    if not user:
        # Si l'utilisateur n'existe pas, on le crée
        user = User(pseudo=pseudo)
        db.add(user)
        db.commit()
        db.refresh(user)
    return {"id": user.id, "pseudo": user.pseudo, "elo": user.elo}

@app.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.elo.desc()).limit(100).all()
    return [
        {
            "pseudo": u.pseudo,
            "elo": u.elo,
            "winrate": (u.victories / u.total_games if u.total_games > 0 else 0)
        }
        for u in users
    ]

@app.get("/history/{pseudo}")
def get_history(pseudo: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.pseudo == pseudo).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    games = db.query(Game).filter(
        (Game.player1_id == user.id) | (Game.player2_id == user.id)
    ).all()
    result = []
    for g in games:
        if g.player1.pseudo == pseudo:
            opponent = g.player2.pseudo
        else:
            opponent = g.player1.pseudo
        win = (g.winner.pseudo == pseudo) if g.winner else None
        result.append({
            "date": g.date,
            "opponent": opponent,
            "result": "win" if win else "loss",
            "moves": g.moves_count
        })
    return result

# Facultatif : renvoie un message si on appelle GET / (évite le 404)
@app.get("/")
def read_root():
    return {"message": "API Mastermind.io en ligne 🎉"}
