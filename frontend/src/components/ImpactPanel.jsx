export default function ImpactPanel({ analysis }) {
  if (!analysis) return (
    <aside className="panel impact-panel empty">
      <div className="panel-title">Impact Summary</div>
      <p>Select a regulation node or upload a regulatory PDF to generate an explainable impact analysis.</p>
    </aside>
  );

  const metrics = [
    ["Policies", analysis.counts["Internal Policy"] || 0],
    ["APIs", analysis.counts.API || 0],
    ["Processes", analysis.counts["Business Process"] || 0],
    ["Controls", analysis.counts["Compliance Control"] || 0],
    ["Business Units", analysis.counts["Business Unit"] || 0],
    ["Audit Artifacts", analysis.counts["Audit Artifact"] || 0]
  ];

  return (
    <aside className="panel impact-panel">
      <div className="panel-title">Impact Summary</div>
      <div className="source-pill">{analysis.source_label}</div>

      <div className="risk-card">
        <span>Operational Impact Risk</span>
        <strong>{Math.round(analysis.risk_score)}/100</strong>
        <div className="risk-track"><i style={{width:`${Math.min(100,analysis.risk_score)}%`}} /></div>
      </div>

      <div className="metric-grid">
        {metrics.map(([label,value]) => (
          <div className="metric" key={label}><strong>{value}</strong><span>{label}</span></div>
        ))}
      </div>

      <div className="summary-box">
        <b>AI Impact Explanation</b><p>{analysis.summary}</p>
      </div>

      <div className="section">
        <div className="section-title">Dependency Trace</div>
        {analysis.evidence_paths.slice(0,5).map((path,i) => (
          <div className="trace" key={i}>{path.join("  →  ")}</div>
        ))}
      </div>

      <div className="section">
        <div className="section-title">Recommended Actions</div>
        {analysis.recommendations.map(r => <div className="recommendation" key={r}>✓ {r}</div>)}
      </div>

      {analysis.extracted_obligations?.length > 0 && (
        <div className="section">
          <div className="section-title">Extracted Obligations</div>
          {analysis.extracted_obligations.slice(0,5).map(x => <div className="obligation" key={x}>{x}</div>)}
        </div>
      )}
    </aside>
  );
}
