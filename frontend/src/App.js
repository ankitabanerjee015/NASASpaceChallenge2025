import React, { useState, useEffect } from "react";
import { Container, Typography, TextField, Button, CircularProgress } from "@mui/material";
import PublicationsList from "./PublicationsList";
import KnowledgeGraph from "./KnowledgeGraph";
import SearchResults from "./SearchResults";

function App() {
  const [publications, setPublications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [graphData, setGraphData] = useState(null);

  // Fetch publications on mount
  useEffect(() => {
    setLoading(true);
    fetch("/publications")
      .then(res => res.json())
      .then(data => {
        setPublications(data);
        setLoading(false);
      });
    fetch("/knowledge-graph")
      .then(res => res.json())
      .then(data => setGraphData(data));
  }, []);

  // Handle semantic search
  const handleSearch = () => {
    setLoading(true);
    fetch(`/search?query=${encodeURIComponent(searchQuery)}`)
      .then(res => res.json())
      .then(data => {
        setSearchResults(data);
        setLoading(false);
      });
  };

  return (
    <Container maxWidth="lg">
      <Typography variant="h3" gutterBottom align="center">
        NASA Bioscience Publications Dashboard
      </Typography>
      <TextField
        label="Semantic Search"
        variant="outlined"
        fullWidth
        value={searchQuery}
        onChange={e => setSearchQuery(e.target.value)}
        margin="normal"
      />
      <Button variant="contained" color="primary" onClick={handleSearch} disabled={loading}>
        Search
      </Button>
      {loading && <CircularProgress />}
      {searchResults.length > 0 ? (
        <SearchResults results={searchResults} />
      ) : (
        <PublicationsList publications={publications} />
      )}
      {graphData && <KnowledgeGraph data={graphData} />}
    </Container>
  );
}

export default App;