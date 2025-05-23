import { useState } from 'react'

export default function GuessForm({ onResult }) {
  const [guess, setGuess] = useState(['', '', '', ''])

  const handleChange = (i, val) => {
    const g = [...guess]
    g[i] = val.toUpperCase().slice(0, 1)
    setGuess(g)
  }

  const handleSubmit = async e => {
    e.preventDefault()
    const res = await fetch('/api/guess', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ guess })
    })
    const data = await res.json()
    onResult({ guess, ...data })
  }

  return (
    <form onSubmit={handleSubmit}>
      {guess.map((c, i) => (
        <input key={i}
               value={c}
               onChange={e => handleChange(i, e.target.value)}
               placeholder="?" />
      ))}
      <button type="submit">Tester</button>
    </form>
  )
}