const [query, setQuery] = useState("");
const [results, setResults] = useState([]);

const handleSearch = async () => {
  const res = await fetch(`/api/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  });
  setResults(await res.json());
};

return (
  <div>
    <input value={query} onChange={e => setQuery(e.target.value)} />
    <button onClick={handleSearch}>Search</button>
    <ul>
      {results.map(pub => (
        <li>
          <strong>{pub.title}</strong>
          <p>{pub.summary}</p>
          <span>{pub.impact}</span>
        </li>
      ))}
    </ul>
  </div>
);