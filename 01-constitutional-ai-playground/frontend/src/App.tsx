import { useState } from "react";

interface Rule {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
}

const DEFAULT_RULES: Rule[] = [
  { id: "1", name: "Be Helpful", description: "Always try to help the user accomplish their goal", enabled: true },
  { id: "2", name: "Avoid Harm", description: "Refuse requests that could cause harm to others", enabled: true },
  { id: "3", name: "Be Honest", description: "Never provide false or misleading information", enabled: true },
];

export default function App() {
  const [rules, setRules] = useState<Rule[]>(DEFAULT_RULES);
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState<{ unconstrained: string; constrained: string } | null>(null);
  const [loading, setLoading] = useState(false);

  const testPrompt = async () => {
    setLoading(true);
    const res = await fetch("http://localhost:8000/api/test", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, rules }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 20, fontFamily: "sans-serif" }}>
      <h1>Constitutional AI Playground</h1>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
        <div>
          <h2>Constitutional Rules</h2>
          {rules.map(rule => (
            <div key={rule.id} style={{ border: "1px solid #ccc", padding: 10, marginBottom: 10, borderRadius: 4 }}>
              <label>
                <input type="checkbox" checked={rule.enabled} onChange={e =>
                  setRules(rules.map(r => r.id === rule.id ? { ...r, enabled: e.target.checked } : r))
                } /> <strong>{rule.name}</strong>
              </label>
              <p style={{ margin: "4px 0 0", color: "#666", fontSize: 14 }}>{rule.description}</p>
            </div>
          ))}
        </div>
        <div>
          <h2>Test Prompt</h2>
          <textarea
            value={prompt}
            onChange={e => setPrompt(e.target.value)}
            placeholder="Enter a prompt to test..."
            style={{ width: "100%", height: 120, padding: 8, boxSizing: "border-box" }}
          />
          <button onClick={testPrompt} disabled={loading || !prompt}
            style={{ marginTop: 8, padding: "8px 20px", background: "#0066cc", color: "white", border: "none", borderRadius: 4, cursor: "pointer" }}>
            {loading ? "Testing..." : "Run Test"}
          </button>
        </div>
      </div>
      {result && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginTop: 20 }}>
          <div>
            <h3>Without Constitution</h3>
            <pre style={{ background: "#f5f5f5", padding: 12, borderRadius: 4, whiteSpace: "pre-wrap" }}>{result.unconstrained}</pre>
          </div>
          <div>
            <h3>With Constitution</h3>
            <pre style={{ background: "#f0fff0", padding: 12, borderRadius: 4, whiteSpace: "pre-wrap" }}>{result.constrained}</pre>
          </div>
        </div>
      )}
    </div>
  );
}
