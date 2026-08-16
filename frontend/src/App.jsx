import { useEffect, useMemo, useState } from "react";
import { Activity, Database, ShieldCheck, Sparkles } from "lucide-react";
import { getGraph, analyzePdf } from "./api";
import GraphView from "./components/GraphView";
import ImpactPanel from "./components/ImpactPanel";
import UploadPanel from "./components/UploadPanel";

export default function App() {
  const [graph,setGraph] = useState(null);
  const [selected,setSelected] = useState("reg_cross_border");
  const [analysis,setAnalysis] = useState(null);
  const [error,setError] = useState("");

  useEffect(() => {
    getGraph().then(setGraph).catch(e => setError(e.message));
  }, []);

  const selectedNode = useMemo(
    () => graph?.nodes?.find(n => n.id === selected), [graph,selected]
  );

  async function runSelected(id) {
    setSelected(id);
    setError("");
    const node = graph.nodes.find(n => n.id === id);
    if (!node || node.type !== "Regulation") return;

    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL || "http://localhost:8000"}/api/analyze-text`,
        {
          method:"POST",
          headers:{"Content-Type":"application/json"},
          body:JSON.stringify({
            text:`Regulatory requirement for ${node.label}. Financial institutions shall verify, monitor, report and maintain appropriate controls for ${node.label}.`,
            source_label:node.label
          })
        }
      );
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Analysis failed");
      setAnalysis(data);
    } catch(e) { setError(e.message); }
  }

  async function handleAnalyze(file) {
    try {
      setError("");
      const data = await analyzePdf(file);
      setAnalysis(data);
      setSelected(data.source_id);
    } catch(e) { setError(e.message); }
  }

  const impactedIds = analysis?.impacted?.map(x => x.node_id) || [];

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark"><ShieldCheck size={22}/></div>
          <div>
            <b>Graph-Based Operational Compliance Intelligence</b>
            <span>Financial Regulatory Dependency Graph • FRDG</span>
          </div>
        </div>
        <div className="status"><span/> Operational Compliance</div>
      </header>

      <main>
        <section className="hero-row">
          <div>
            <h1>Regulatory Impact Command Center</h1>
            <p>Trace regulatory change across the enterprise — from clause to policy, process, API, control and audit evidence.</p>
          </div>
          <div className="hero-metrics">
            <div><Activity size={18}/><b>{graph?.nodes?.length || "—"}</b><span>Graph Nodes</span></div>
            <div><Database size={18}/><b>{graph?.edges?.length || "—"}</b><span>Dependencies</span></div>
            <div><Sparkles size={18}/><b>AI</b><span>Explainable</span></div>
          </div>
        </section>

        <UploadPanel onAnalyze={handleAnalyze}/>
        {error && <div className="error">{error}</div>}

        <section className="workspace">
          <div className="panel graph-panel">
            <div className="panel-header">
              <div>
                <div className="panel-title">Financial Regulatory Dependency Graph</div>
                <div className="panel-sub">{selectedNode ? `Selected: ${selectedNode.label}` : "Select a node"}</div>
              </div>
              <div className="live"><span/> Live graph</div>
            </div>
            {graph && <GraphView graph={graph} selected={selected} impactedIds={impactedIds} onSelect={runSelected}/>}
            <div className="legend">
              <span><i className="dot regulation"/> Regulation</span>
              <span><i className="dot policy"/> Policy</span>
              <span><i className="dot process"/> Process</span>
              <span><i className="dot tech"/> Technology</span>
              <span><i className="dot control"/> Control</span>
            </div>
          </div>
          <ImpactPanel analysis={analysis}/>
        </section>
      </main>

      <footer>Prototype • SyntheticBank-360 • Decision-support only • Human compliance review required</footer>
    </div>
  );
}
