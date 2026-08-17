import { useEffect, useRef } from "react";
import cytoscape from "cytoscape";

const COLORS = {
  Regulation: "#0b65c2",
  "Internal Policy": "#1597b8",
  "Business Process": "#3c82f6",
  API: "#0ea5e9",
  Microservice: "#6366f1",
  Database: "#0f766e",
  "Compliance Control": "#0891b2",
  "Business Unit": "#64748b",
  "Audit Artifact": "#475569"
};

export default function GraphView({ graph, selected, onSelect, impactedIds = [] }) {
  const ref = useRef(null);
  const cyRef = useRef(null);

  useEffect(() => {
    if (!ref.current || !graph) return;

    const elements = [
      ...graph.nodes.map(n => ({ data: { id:n.id, label:n.label, type:n.type, risk:n.risk } })),
      ...graph.edges.map((e,i) => ({ data: { id:`e-${i}`, source:e.source, target:e.target, relation:e.relation } }))
    ];

    const cy = cytoscape({
      container: ref.current,
      elements,
      layout: { name:"cose", animate:true, fit:true, padding:35, nodeRepulsion:8500, idealEdgeLength:135 },
      style: [
        { selector:"node", style:{
          "background-color": e => COLORS[e.data("type")] || "#0f172a",
          label:"data(label)", color:"#0f172a", "font-size":9,
          "text-wrap":"wrap", "text-max-width":90, "text-valign":"bottom",
          "text-margin-y":8, width:e => 18 + Math.min(18,e.data("risk")/6),
          height:e => 18 + Math.min(18,e.data("risk")/6),
          "border-width":2, "border-color":"#fff"
        }},
        { selector:"edge", style:{
          width:1.5, "line-color":"#9bd9ee", "target-arrow-color":"#4aa9c7",
          "target-arrow-shape":"triangle", "curve-style":"bezier", opacity:.65
        }},
        { selector:".dim", style:{ opacity:.12 }},
        { selector:".impact", style:{ "border-color":"#f59e0b", "border-width":4, "background-color":"#f59e0b" }},
        { selector:".selected", style:{ "border-color":"#ef4444", "border-width":5 }}
      ]
    });

    cy.on("tap", "node", evt => onSelect(evt.target.id()));
    cyRef.current = cy;
    return () => cy.destroy();
  }, [graph, onSelect]);

  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    cy.elements().removeClass("dim impact selected");
    if (selected) {
      cy.getElementById(selected).addClass("selected");
      cy.nodes().forEach(n => {
        if (n.id() !== selected && !impactedIds.includes(n.id())) n.addClass("dim");
      });
      impactedIds.forEach(id => cy.getElementById(id).addClass("impact"));
    }
  }, [selected, impactedIds]);

  return <div className="graph-canvas" ref={ref} />;
}
