import { useMemo, useState } from "react";

const API_BASE = "https://beach-consulting-backend.onrender.com";

const GATE_QUESTION = "Do you have any inquiries related to:\n- Taxes\n- Rental/Property Issues/Evictions\n- Litigations";
const GATE_REDIRECT_MESSAGE = "We do not address these areas, but we can help you with the topics below.";

const TOPIC_OPTIONS = [
  "Legal Structure & Business Formation",
  "Business Strategy & Growth Plan",
  "Licensing and Regulatory Compliance",
  "Marketing & Positioning",
  "Intellectual Property & IP Protection",
  "Funding, Investment, & Equity",
];

async function sendToBackend(message, history, collected, category, confidence, stage) {
  const res = await fetch(`${API_BASE}/bot`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history, collected, category, confidence, stage }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Backend error ${res.status}: ${text}`);
  }

  return res.json();
}

function Badge({ label }) {
  const colors = useMemo(() => {
    if (label === "legal")
      return { background: "#fff1f2", color: "#9f1239", borderColor: "#fecdd3" };
    if (label === "business")
      return { background: "#eff6ff", color: "#1d4ed8", borderColor: "#bfdbfe" };
    if (label === "other")
      return { background: "#ecfdf5", color: "#047857", borderColor: "#a7f3d0" };
    if (label === "loading")
      return { background: "#f1f5f9", color: "#334155", borderColor: "#e2e8f0" };
    if (label === "error")
      return { background: "#fef2f2", color: "#b91c1c", borderColor: "#fecaca" };
    return { background: "#f8fafc", color: "#334155", borderColor: "#e2e8f0" };
  }, [label]);

  return (
    <span
      style={{
        padding: "2px 10px",
        borderRadius: 999,
        border: `1px solid ${colors.borderColor}`,
        background: colors.background,
        color: colors.color,
        fontSize: 12,
      }}
    >
      {label}
    </span>
  );
}

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: GATE_QUESTION,
      meta: { category: "intake", confidence: 0.8 },
    },
  ]);
  const [input, setInput] = useState("");
  const [collected, setCollected] = useState({});
  const [history, setHistory] = useState([]);
  const [category, setCategory] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [stage, setStage] = useState("problem");
  const [progress, setProgress] = useState({ answered: 0, total: 0, remaining: 0, done: false, tracked: false });

  // New: controls which UI is shown — gate question, topic dropdown, or the normal chat box
  const [uiStage, setUiStage] = useState("gate"); // "gate" -> "dropdown" -> "chat"
  const [selectedTopics, setSelectedTopics] = useState([]);
  const [otherChecked, setOtherChecked] = useState(false);
  const [otherText, setOtherText] = useState("");

  function addMessage(m) {
    setMessages((prev) => [...prev, m]);
  }

  function toggleTopic(topic) {
    setSelectedTopics((prev) =>
      prev.includes(topic) ? prev.filter((t) => t !== topic) : [...prev, topic]
    );
  }

  function handleGateAnswer(answer) {
    addMessage({ role: "user", text: answer });
    if (answer === "Yes") {
      addMessage({ role: "bot", text: GATE_REDIRECT_MESSAGE, meta: { category: "intake", confidence: 0.8 } });
    }
    setUiStage("dropdown");
  }

  async function submitTopics() {
    const parts = [...selectedTopics];
    if (otherChecked && otherText.trim()) {
      parts.push(`Other: ${otherText.trim()}`);
    }
    if (parts.length === 0) return;

    const combinedMessage = parts.join(", ");
    setUiStage("chat");
    await sendChatMessage(combinedMessage);
  }

  async function sendChatMessage(text) {
    addMessage({ role: "user", text });

    const typingId = crypto.randomUUID();
    addMessage({
      id: typingId,
      role: "bot",
      text: "…",
      meta: { category: "loading", confidence: null },
    });

    try {
      const data = await sendToBackend(text, history, collected, category, confidence, stage);

      setMessages((prev) => prev.filter((m) => m.id !== typingId));

      setHistory(data.history ?? history);
      setCollected(data.collected ?? {});
      setCategory(data.category ?? category);
      setConfidence(data.classification?.confidence ?? confidence);
      setProgress(data.progress ?? progress);
      setStage(data.stage ?? stage);

      addMessage({
        role: "bot",
        text: data.reply,
        meta: {
          category: data.classification?.category ?? "unknown",
          confidence: data.classification?.confidence ?? 0,
          followups: data.classification?.followups ?? [],
        },
      });
    } catch (err) {
      setMessages((prev) => prev.filter((m) => m.id !== typingId));
      addMessage({
        role: "bot",
        text: `Backend error: ${err.message}`,
        meta: { category: "error", confidence: 0 },
      });
    }
  }

  async function sendMessage(e) {
    e.preventDefault();
    const text = input.trim();
    if (!text) return;
    setInput("");
    await sendChatMessage(text);
  }

  function clickFollowup(q) {
    setInput(q);
  }

  return (
    <div style={{minHeight: "100vh", width: "100vw", fontFamily: "Arial, sans-serif", background: "#f8fafc",
                padding: 24, boxSizing: "border-box",}}>
      <div style={{ display: "flex", gap: 16, alignItems: "flex-start" }}>
        <div style={{flex: 1, height: "calc(100vh - 48px)", background: "white",
                    border: "1px solid #e5e7eb", borderRadius: 16, display: "flex",
                    flexDirection: "column",}}>
          <div style={{ padding: 16, borderBottom: "1px solid #e5e7eb" }}>
            <div style={{ fontWeight: 700, fontSize: 18 }}>BEACH Intake Chat</div>
            <div style={{ fontSize: 12, color: "#64748b" }}>
              Backend routing: business • legal • other
            </div>

            {progress.tracked && (
              <div style={{ marginTop: 12 }}>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12,
                              color: "#64748b", marginBottom: 6 }}>
                  <span>Progress</span>
                  <span>
                    {progress.done
                      ? (progress.is_summary ? "Ready to copy into HubSpot" : "0 questions left")
                      : `${progress.remaining} question${progress.remaining === 1 ? "" : "s"} left`}
                  </span>
                </div>

                <div style={{ width: "100%", height: 10, background: "#e5e7eb", borderRadius: 999 }}>
                  <div
                    style={{
                      width: `${progress.total ? Math.min(100, (progress.answered / progress.total) * 100) : 0}%`,
                      height: "100%",
                      background: progress.done ? "#059669" : "#111827",
                      borderRadius: 999,
                      transition: "width 0.3s ease",
                    }}
                  />
                </div>
              </div>
            )}

            {progress.tracked && progress.done && progress.is_summary && (
              <button
                type="button"
                onClick={() => navigator.clipboard.writeText(messages[messages.length - 1]?.text ?? "")}
                style={{ marginTop: 10, padding: "8px 12px", borderRadius: 8, border: "1px solid #059669", color: "#059669", background: "white", cursor: "pointer", fontSize: 13 }}
              >
                Copy summary
              </button>
            )}
          </div>

          <div style={{ padding: 16, flex: 1, overflowY: "auto" }}>
            {messages.map((m, i) => {
              const isUser = m.role === "user";
              return (
                <div
                  key={m.id ?? i}
                  style={{
                    display: "flex",
                    justifyContent: isUser ? "flex-end" : "flex-start",
                    marginBottom: 12,
                  }}
                >
                  <div style={{ maxWidth: "80%" }}>
                    <div
                      style={{
                        padding: "10px 12px",
                        borderRadius: 16,
                        border: "1px solid",
                        borderColor: isUser ? "#111827" : "#e5e7eb",
                        background: isUser ? "#111827" : "white",
                        color: isUser ? "white" : "#0f172a",
                        lineHeight: 1.4,
                        fontSize: 14,
                        whiteSpace: "pre-wrap",
                      }}
                    >
                      {m.text}
                    </div>

                    {!isUser && m.meta && (
                      <div style={{ marginTop: 6, display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
                        <Badge label={m.meta.category ?? "unknown"} />
                        {typeof m.meta.confidence === "number" && (
                          <span style={{ fontSize: 12, color: "#64748b" }}>
                            confidence: {Math.round(m.meta.confidence * 100)}%
                          </span>
                        )}
                      </div>
                    )}

                    {!isUser && m.meta?.followups?.length > 0 && (
                      <div style={{ marginTop: 8 }}>
                        <div style={{ fontSize: 12, color: "#64748b", marginBottom: 6 }}>
                          Suggested follow-ups:
                        </div>
                        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                          {m.meta.followups.slice(0, 5).map((q, idx) => (
                            <button
                              key={idx}
                              type="button"
                              onClick={() => clickFollowup(q)}
                              style={{
                                fontSize: 12,
                                padding: "6px 10px",
                                borderRadius: 999,
                                border: "1px solid #e5e7eb",
                                background: "#f8fafc",
                                cursor: "pointer",
                              }}
                            >
                              {q}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}

            {uiStage === "dropdown" && (
              <div style={{ marginTop: 8, padding: 16, border: "1px solid #e5e7eb", borderRadius: 12, background: "#f8fafc" }}>
                <div style={{ fontWeight: 600, marginBottom: 10, fontSize: 14, color: "#0f172a" }}>
                  Please select all areas where you are seeking guidance:
                </div>
                {TOPIC_OPTIONS.map((topic) => (
                  <label key={topic} style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8, fontSize: 14, cursor: "pointer", color: "#0f172a" }}>
                    <input
                      type="checkbox"
                      checked={selectedTopics.includes(topic)}
                      onChange={() => toggleTopic(topic)}
                    />
                    {topic}
                  </label>
                ))}
                <label style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8, fontSize: 14, cursor: "pointer", color: "#0f172a" }}>
                    type="checkbox"
                    checked={otherChecked}
                    onChange={() => setOtherChecked((v) => !v)}
                  />
                  Other...
                </label>
                {otherChecked && (
                  <input
                    type="text"
                    value={otherText}
                    onChange={(e) => setOtherText(e.target.value)}
                    placeholder="Tell us what you need help with"
                    style={{ width: "100%", padding: 8, borderRadius: 8, border: "1px solid #e5e7eb", marginBottom: 10, boxSizing: "border-box" }}
                  />
                )}
                <button
                  type="button"
                  onClick={submitTopics}
                  disabled={selectedTopics.length === 0 && !(otherChecked && otherText.trim())}
                  style={{
                    padding: "8px 14px",
                    borderRadius: 8,
                    border: "1px solid #111827",
                    background: "#111827",
                    color: "white",
                    cursor: "pointer",
                    fontSize: 13,
                    opacity: selectedTopics.length === 0 && !(otherChecked && otherText.trim()) ? 0.5 : 1,
                  }}
                >
                  Submit
                </button>
              </div>
            )}
          </div>

          {uiStage === "gate" && (
            <div style={{ padding: 12, borderTop: "1px solid #e5e7eb", display: "flex", gap: 8, justifyContent: "center" }}>
              <button
                type="button"
                onClick={() => handleGateAnswer("Yes")}
                style={{ padding: "10px 20px", borderRadius: 12, border: "1px solid #111827", background: "white", color: "#111827", cursor: "pointer" }}
              >
                Yes
              </button>
              <button
                type="button"
                onClick={() => handleGateAnswer("No")}
                style={{ padding: "10px 20px", borderRadius: 12, border: "1px solid #111827", background: "#111827", color: "white", cursor: "pointer" }}
              >
                No
              </button>
            </div>
          )}

          {uiStage === "chat" && (
            <form onSubmit={sendMessage} style={{ padding: 12, borderTop: "1px solid #e5e7eb", display: "flex", gap: 8 }}>
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your question…"
                style={{
                  flex: 1,
                  padding: 10,
                  borderRadius: 12,
                  border: "1px solid #e5e7eb",
                  outline: "none",
                }}
              />
              <button
                type="submit"
                style={{
                  padding: "10px 14px",
                  borderRadius: 12,
                  border: "1px solid #111827",
                  background: "#111827",
                  color: "white",
                  cursor: "pointer",
                }}
              >
                Send
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}