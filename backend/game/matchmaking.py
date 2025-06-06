from collections import deque
from game.mastermind import check  # Logique de validation (retourne (black_pins, white_pins))

waiting_players = deque()
active_games = {}

# Structure d'une partie :
# {
#   "players": [player1, player2],
#   "current_turn": player_id,
#   "secret_codes": {player1: str or None, player2: str or None},
#   "guesses": {player1: [(guess, (black, white)), ...], player2: [...]},
#   "round": int,
#   "status": "waiting" | "playing" | "finished"
# }

def add_player_to_queue(player_id):
    """
    Ajoute un joueur à la file d'attente. Si deux joueurs sont disponibles,
    crée une nouvelle partie et renvoie (game_id, [player1, player2]).
    Sinon renvoie (None, None).
    """
    if player_id not in waiting_players:
        waiting_players.append(player_id)
    if len(waiting_players) >= 2:
        p1 = waiting_players.popleft()
        p2 = waiting_players.popleft()
        game_id = f"{p1}_{p2}"
        active_games[game_id] = {
            "players": [p1, p2],
            "current_turn": None,
            "secret_codes": {p1: None, p2: None},
            "guesses": {p1: [], p2: []},
            "round": 1,
            "status": "waiting"
        }
        return game_id, [p1, p2]
    return None, None

def set_secret(game_id, player_id, code):
    """
    Stocke le code secret du joueur. Si les deux codes sont définis,
    passe au statut 'playing' et défini le current_turn.
    """
    game = active_games.get(game_id)
    if not game or game["status"] != "waiting":
        return None
    game["secret_codes"][player_id] = code
    # Dès que les deux codes sont posés
    if all(game["secret_codes"].values()):
        # Démarrer la partie
        game["status"] = "playing"
        # Le premier joueur est le premier de la liste
        game["current_turn"] = game["players"][0]
        return True
    return False

def make_guess(game_id, player_id, guess):
    """
    Effectue une proposition de code pour le joueur. Retourne le feedback (black, white)
    ou 'not_your_turn', 'not_started', 'error'.
    """
    game = active_games.get(game_id)
    if not game:
        return "error"
    if game["status"] != "playing":
        return "not_started"
    if game["current_turn"] != player_id:
        return "not_your_turn"

    opponent = [p for p in game["players"] if p != player_id][0]
    secret = game["secret_codes"][opponent]
    # Calcul du feedback
    black, white = check(secret, guess)
    # Sauvegarde de la tentative
    game["guesses"][player_id].append((guess, (black, white)))

    # Vérifier fin de partie
    if black == len(secret):
        game["status"] = "finished"
        return {"result": (black, white), "winner": player_id}

    # Passer le tour à l'adversaire
    game["current_turn"] = opponent
    return {"result": (black, white), "next_turn": opponent}

def get_game_state(game_id):
    """
    Renvoie l'état de la partie pour affichage (sans révéler les codes secrets).
    """
    game = active_games.get(game_id)
    if not game:
        return None
    return {
        "players": game["players"],
        "current_turn": game["current_turn"],
        "guesses": game["guesses"],
        "round": game["round"],
        "status": game["status"],
        "game_id": game_id
    }
