export default function History({ attempts }) {
  if (!attempts.length) return <p>Aucune tentative.</p>
  return (
    <ul>
      {attempts.map((a, i) => (
        <li key={i}>
          {a.guess.join(' ')} → {a.well_placed} bien placés, {a.misplaced} mal placés
        </li>
      ))}
    </ul>
  )
}