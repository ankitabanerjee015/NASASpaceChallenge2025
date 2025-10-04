import React, { useRef, useEffect } from "react";
import * as d3 from "d3";

// Simple force-directed graph for publication-keyword relationships
const KnowledgeGraph = ({ data }) => {
  const ref = useRef();

  useEffect(() => {
    if (!data) return;
    const svg = d3.select(ref.current);
    svg.selectAll("*").remove();
    const width = 800, height = 400;

    // Setup simulation
    const simulation = d3.forceSimulation(data.nodes)
      .force("link", d3.forceLink(data.edges).id(d => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-200))
      .force("center", d3.forceCenter(width/2, height/2));

    svg.attr("width", width).attr("height", height);

    // Draw links
    const link = svg.append("g")
      .selectAll("line")
      .data(data.edges)
      .enter().append("line")
      .attr("stroke", "#aaa");

    // Draw nodes
    const node = svg.append("g")
      .selectAll("circle")
      .data(data.nodes)
      .enter().append("circle")
      .attr("r", 12)
      .attr("fill", d => d.type === "publication" ? "#1976d2" : "#43a047")
      .call(d3.drag()
        .on("start", (event, d) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x; d.fy = d.y;
        })
        .on("drag", (event, d) => {
          d.fx = event.x; d.fy = event.y;
        })
        .on("end", (event, d) => {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null; d.fy = null;
        })
      );

    // Draw labels
    const label = svg.append("g")
      .selectAll("text")
      .data(data.nodes)
      .enter().append("text")
      .text(d => d.label)
      .attr("font-size", 12)
      .attr("dx", 15)
      .attr("dy", 5);

    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
      label
        .attr("x", d => d.x)
        .attr("y", d => d.y);
    });

  }, [data]);

  return (
    <div style={{ marginTop: 40 }}>
      <h3>Knowledge Graph</h3>
      <svg ref={ref} />
    </div>
  );
};

export default KnowledgeGraph;