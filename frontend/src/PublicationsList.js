import React, { useState } from "react";
import { Card, CardContent, Typography, FormControl, InputLabel, Select, MenuItem } from "@mui/material";

const sectionOptions = [
  "Abstract",
  "Main",
  "Results",
  "Discussion",
  "Methods",
  "Acknowledgements",
  "Author contributions",
  "Peer review",
  "Data availability",
  "Code availability",
  "Competing interests",
  "Footnotes",
  "References",
  "Associated Data"
];

function PublicationsList({ publications }) {
  // Optional: maintain selected section for each publication
  const [selectedSections, setSelectedSections] = useState({});

  const handleDropdownChange = (idx, value) => {
    setSelectedSections(prev => ({ ...prev, [idx]: value }));
  };

  return (
    <div>
      {publications.map((pub, idx) => (
        <Card key={idx} style={{ marginBottom: 16 }}>
          <CardContent>
            <Typography variant="h6">{pub.Title}</Typography>
            <Typography variant="body2">{pub.summary}</Typography>
            <Typography variant="body2" color="textSecondary">{pub.abstract}</Typography>
            <FormControl fullWidth variant="outlined" style={{ marginTop: 8 }}>
              <InputLabel>Section</InputLabel>
              <Select
                label="Section"
                value={selectedSections[idx] || "Abstract"}
                onChange={e => handleDropdownChange(idx, e.target.value)}
              >
                {sectionOptions.map((option, i) => (
                  <MenuItem key={i} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

export default PublicationsList;
