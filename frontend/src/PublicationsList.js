import React from "react";
import { Card, CardContent, Typography, Link, Grid } from "@mui/material";

const PublicationsList = ({ publications }) => (
  <Grid container spacing={2} sx={{ mt: 2 }}>
    {publications.map((pub, idx) => (
      <Grid item xs={12} md={6} key={idx}>
        <Card>
          <CardContent>
            <Typography variant="h6">{pub.Title}</Typography>
            <Link href={pub.Link} target="_blank" rel="noopener">
              {pub.Link}
            </Link>
            <Typography variant="body2" sx={{ mt: 1 }}>
              <b>Summary:</b> {pub.summary}
            </Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              <b>Abstract:</b> {pub.abstract}
            </Typography>
          </CardContent>
        </Card>
      </Grid>
    ))}
  </Grid>
);

export default PublicationsList;