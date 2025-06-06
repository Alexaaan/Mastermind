import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [pseudo, setPseudo] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!pseudo) return;

    // Envoi d'un POST /login avec JSON { pseudo: "..." }
    const res = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pseudo })
    });

    if (res.ok) {
      // Redirige vers /jeu/<pseudo> si la création/récupération a fonctionné
      navigate(`/jeu/${pseudo}`);
    } else {
      alert('Impossible de se connecter');
    }
  };

  return (
    <div>
      <h2>Connecte-toi</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Ton pseudo"
          value={pseudo}
          onChange={e => setPseudo(e.target.value)}
        />
        <button type="submit">Jouer</button>
      </form>
    </div>
  );
}

export default Login;
