from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from typing import Dict
from game.matchmaking import (
    add_player_to_queue,
    set_secret,
    make_guess,
    get_game_state
)
from db.database import SessionLocal
from db.models import User, Game as GameModel


router = APIRouter()
# Dans ce dictionnaire, on stocke { pseudo: WebSocket }
connections: Dict[str, WebSocket] = {}
# Pour savoir à quelle partie appartient chaque joueur : { pseudo: game_id }
user_game_map: Dict[str, str] = {}

def get_db_ws():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str, db: Session = Depends(get_db_ws)):
    await websocket.accept()
    connections[player_id] = websocket

    # Vérifier que l'utilisateur existe en base
    db_user = db.query(User).filter(User.pseudo == player_id).first()
    if not db_user:
        await websocket.close(code=1008)
        return

    # Ajout dans la file d'attente et création de la partie si possible
    game_id, players = add_player_to_queue(player_id)
    if game_id:
        # On crée un enregistrement Game en base avec player1 et player2
        player1 = db.query(User).filter(User.pseudo == players[0]).first()
        player2 = db.query(User).filter(User.pseudo == players[1]).first()
        new_game = GameModel(player1_id=player1.id, player2_id=player2.id, moves_count=0)
        db.add(new_game)
        db.commit()
        db.refresh(new_game)

        # On mémorise à quelle partie correspond chaque pseudo
        user_game_map[players[0]] = game_id
        user_game_map[players[1]] = game_id

        # On demande aux deux joueurs de définir leur code secret
        for pid in players:
            await connections[pid].send_json({
                "type": "request_secret",
                "game_id": game_id,
                "opponent": [p for p in players if p != pid][0]
            })

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")
            game_id = data.get("game_id")

            if msg_type == "set_secret":
                # Le joueur envoie son code secret
                ready = set_secret(game_id, player_id, data.get("code"))
                if ready:
                    # Dès que les deux codes sont reçus, on envoie le tour au premier joueur
                    state = get_game_state(game_id)
                    await connections[state["current_turn"]].send_json({
                        "type": "your_turn",
                        "game_state": state
                    })

            elif msg_type == "guess":
                # Le joueur envoie une proposition de code
                res = make_guess(game_id, player_id, data.get("guess"))

                # On incrémente moves_count en base
                db_game = db.query(GameModel).filter(GameModel.id == new_game.id).first()
                if db_game:
                    db_game.moves_count += 1
                    db.commit()

                if res == "not_your_turn":
                    await websocket.send_json({
                        "type": "error",
                        "message": "Ce n'est pas ton tour."
                    })
                elif res == "error":
                    await websocket.send_json({
                        "type": "error",
                        "message": "Partie introuvable."
                    })
                else:
                    # On envoie le feedback au joueur qui vient de jouer
                    await websocket.send_json({
                        "type": "guess_result",
                        "result": res["result"]
                    })

                    if res.get("winner"):
                        # La partie est terminée, on met à jour les stats en base
                        winner_user = db.query(User).filter(User.pseudo == res["winner"]).first()
                        loser = [p for p in players if p != res["winner"]][0]
                        loser_user = db.query(User).filter(User.pseudo == loser).first()

                        # Victoire / Défaite / Total parties
                        winner_user.victories += 1
                        winner_user.total_games += 1
                        loser_user.defeats += 1
                        loser_user.total_games += 1

                        # (Optionnel) calcul ELO simplifié ici

                        db.commit()

                        # On notifie les deux joueurs de la fin de partie
                        for pid in players:
                            await connections[pid].send_json({
                                "type": "game_over",
                                "winner": res["winner"]
                            })
                    else:
                        # Sinon on envoie le tour au prochain joueur
                        next_p = res["next_turn"]
                        state = get_game_state(game_id)
                        await connections[next_p].send_json({
                            "type": "your_turn",
                            "game_state": state
                        })

    except WebSocketDisconnect:
        # Si un joueur se déconnecte, on le supprime de la liste des connexions
        del connections[player_id]
