import { useState } from 'react';

function App() {
  const [name, setName] = useState('');
  const [character, setCharacter] = useState(null);
  const [error, setError] = useState('');

  const searchCharacter = async () => {
    setError('');
    setCharacter(null);
    try {
      const res = await fetch(`http://localhost:5000/api/character/${name}`);
      if (!res.ok) throw new Error('Character not found');
      const data = await res.json();
      setCharacter(data);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Rick and Morty Character Search</h1>
      <input
        type="text"
        placeholder="Enter character name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <button onClick={searchCharacter}>Search</button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {character && (
        <div style={{ marginTop: '1rem' }}>
          <h2>{character.name}</h2>
          <img src={character.image} alt={character.name} />

          <p>Total Episodes: {character.total_episodes}</p>
          <ul>
            {character.episodes.map((ep, idx) => (
              <li key={idx}>{ep}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
