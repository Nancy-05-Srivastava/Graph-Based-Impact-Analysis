import { useRef, useState } from "react";
import { FileUp, LoaderCircle } from "lucide-react";

export default function UploadPanel({ onAnalyze }) {
  const input = useRef(null);
  const [loading,setLoading] = useState(false);
  const [name,setName] = useState("");

  async function handle(file) {
    if (!file) return;
    setName(file.name);
    setLoading(true);
    try { await onAnalyze(file); } finally { setLoading(false); }
  }

  return (
    <div className="upload-card">
      <div className="upload-icon"><FileUp size={25}/></div>
      <div>
        <div className="upload-title">Upload Regulatory Circular</div>
        <div className="upload-sub">PDF → clause extraction → dependency impact</div>
      </div>
      <button onClick={() => input.current?.click()} disabled={loading}>
        {loading ? <><LoaderCircle className="spin" size={16}/> Analyzing…</> : "Choose PDF"}
      </button>
      <input ref={input} type="file" accept=".pdf,application/pdf" hidden
        onChange={e => handle(e.target.files?.[0])}/>
      {name && <div className="filename">{name}</div>}
    </div>
  );
}
