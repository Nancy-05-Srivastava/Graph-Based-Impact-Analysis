const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function getGraph() {
  const res = await fetch(`${API}/api/graph`);
  if (!res.ok) throw new Error("Unable to load graph");
  return res.json();
}

export async function analyzePdf(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API}/api/analyze-pdf`, { method: "POST", body: form });
  const body = await res.json();
  if (!res.ok) throw new Error(body.detail || "Analysis failed");
  return body;
}

export { API };
