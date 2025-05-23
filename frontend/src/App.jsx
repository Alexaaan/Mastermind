import { useState, useEffect } from 'react'
import GuessForm from './components/GuessForm.jsx'
import History from './components/History.jsx'

export default function App() {
  const [attempts, setAttempts] = useState([])
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetch('ht /api/start')
      .then(res => res.json())
      .then(data => setMessage(data.message))
  }, [])

  const handleResult = result => {
    setAttempts(prev => [...prev, result])
  }

  return (
    <div style={{ padding: 20, fontFamily: 'sans-serif' }}>
      <h1>Masterminder</h1>
      <p>{message}</p>
      <GuessForm onResult={handleResult} />
      <History attempts={attempts} />
    </div>
  )
}