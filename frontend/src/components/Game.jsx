import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function Game() {
  const { pseudo } = useParams();
  const playerId = pseudo;
  const [socket, setSocket] = useState(null);
  const [gameState, setGameState] = useState(null);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // Connexion au WebSocket du backend (port 8000)
    const ws = new WebSocket(`ws://localhost:8000/ws/${playerId}`);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages(msgs => [...msgs, data]);

      switch (data.type) {
        case 'request_secret':
          // Prompt pour que le joueur définisse son code secret (4 chiffres)
          const code = prompt('Définis ton code secret (4 chiffres)');
          ws.send(JSON.stringify({ type: 'set_secret', game_id: data.game_id, code }));
          break;
        case 'your_turn':
          setGameState(data.game_state);
          break;
        case 'guess_result':
          alert(`Feedback: ${data.result[0]} pions noirs, ${data.result[1]} blancs`);
          break;
        case 'game_over':
          alert(data.winner === playerId ? 'Tu as gagné !' : 'Tu as perdu.');
          break;
        default:
          break;
      }
    };
    setSocket(ws);
    return () => ws.close();
  }, [playerId]);

  const handleGuess = () => {
    if (socket && gameState && gameState.current_turn === playerId) {
      socket.send(JSON.stringify({ type: 'guess', game_id: gameState.game_id, guess: input }));
      setInput('');
    } else {
      alert("Attends ton tour...");
    }
  };

  return (
    <div>
      <h2>Mastermind 1v1</h2>
      <p>Joueur : {playerId}</p>
      {gameState ? (
        <div>
          <p>C'est à {gameState.current_turn} de jouer</p>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Proposition (4 chiffres)"
          />
          <button onClick={handleGuess}>Proposer</button>
          <h3>Historique des messages</h3>
          <ul>
            {messages.map((m, i) => <li key={i}>{JSON.stringify(m)}</li>)}
          </ul>
        </div>
      ) : (
        <p>En attente de partie...</p>
      )}
    </div>
  );
}

export default Game;
