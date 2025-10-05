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

  // Always fetch publications with abstract and summary when the app loads
  useEffect(() => {
    setLoading(true);
    fetch("/publications?include_abstract=true")
      .then(res => {
        if (res.status === 304) {
          setLoading(false);
          return;
        }
        const contentType = res.headers.get("content-type");
        if (!res.ok || !contentType || !contentType.includes("application/json")) {
          return res.text().then(text => {
            throw new Error(`Publications fetch failed: ${res.status} ${text}`);
          });
        }
        return res.json();
      })
      .then(data => {
        if (data && data.items) setPublications(data.items);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error loading publications", err);
        setLoading(false);
      });

    fetch("/knowledge-graph")
      .then(res => res.json())
      .then(data => setGraphData(data))
      .catch(err => {
        console.error("Error loading knowledge graph", err);
        setGraphData(null);
      });
  }, []);

  // Handle semantic search
  const handleSearch = () => {
    setLoading(true);
    fetch(`/search?query=${encodeURIComponent(searchQuery)}`)
      .then(res => {
        if (res.status === 304) {
          setLoading(false);
          return;
        }
        const contentType = res.headers.get("content-type");
        if (!res.ok || !contentType || !contentType.includes("application/json")) {
          return res.text().then(text => {
            throw new Error(`Search failed: ${res.status} ${text}`);
          });
        }
        return res.json();
      })
      .then(data => {
        if (data) setSearchResults(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error performing search", err);
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
