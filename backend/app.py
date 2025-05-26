from fastapi import FastAPI
from pydantic import BaseModel
from game.mastermind import generate_code, check_guess
from fastapi.staticfiles import StaticFiles

app = FastAPI()

class Guess(BaseModel):
    guess: list[str]

SECRET = generate_code()

@app.get("/api/start")
def start_game():
    global SECRET
    SECRET = generate_code()
    return {"message": "new game started"}

@app.post("/api/guess")
def post_guess(g: Guess):
    return check_guess(SECRET, g.guess)

# _______________________________
# Monture des fichiers statiques
app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="static"
)
