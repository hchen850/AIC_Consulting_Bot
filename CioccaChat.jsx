import { useState, useRef, useEffect } from "react";

const API_URL = "http://localhost:8000";

// ── Colors & theme ────────────────────────────────────────────────────────────
const COLORS = {
  scuRed: "#862633",
  scuGold: "#C4A052",
  bg: "#f8f9fa",
  white: "#ffffff",
  border: "#dee2e6",
  textDark: "#212529",
  textMuted: "#6c757d",
  bubbleUser: "#862633",
  bubbleBot: "#ffffff",
};

// ── Source Card ───────────────────────────────────────────────────────────────
function SourceCard({ source }) {
  const [open, setOpen] = useState(false);
  return (
    <div
      style={{
        border: `1px solid ${COLORS.border}`,
        borderRadius: 8,
        marginTop: 6,
        fontSize: 12,
        overflow: "hidden",
      }}
    >
      <button
        onClick={() => setOpen(!open)}
        style={{
          width: "100%",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "6px 10px",
          background: "#f1f3f5",
          border: "none",
          cursor: "pointer",
          color: COLORS.scuRed,
          fontWeight: 600,
          textAlign: "left",
        }}
      >
        <span>📄 {source.title}</span>
        <span>{open ? "▲" : "▼"}</span>
      </button>
      {open && (
        <div style={{ padding: "8px 10px", background: COLORS.white }}>
          <p style={{ margin: "0 0 4px", color: COLORS.textMuted }}>{source.snippet}</p>
          <a
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: COLORS.scuRed, fontSize: 11 }}
          >
            🔗 View Source →
          </a>
        </div>
      )}
    </div>
  );
}

// ── Message Bubble ─────────────────────────────────────────────────────────────
function MessageBubble({ msg }) {
  const isUser = msg.role === "user";
  const [sourcesOpen, setSourcesOpen] = useState(false);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: isUser ? "flex-end" : "flex-start",
        marginBottom: 12,
      }}
    >
      <div
        style={{
          maxWidth: "75%",
          padding: "10px 14px",
          borderRadius: isUser ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
          background: isUser ? COLORS.bubbleUser : COLORS.bubbleBot,
          color: isUser ? COLORS.white : COLORS.textDark,
          boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
          border: isUser ? "none" : `1px solid ${COLORS.border}`,
          whiteSpace: "pre-wrap",
          lineHeight: 1.5,
        }}
      >
        {msg.content}
      </div>

      {/* Sources dropdown */}
      {!isUser && msg.sources && msg.sources.length > 0 && (
        <div style={{ maxWidth: "75%", marginTop: 4 }}>
          <button
            onClick={() => setSourcesOpen(!sourcesOpen)}
            style={{
              background: "none",
              border: `1px solid ${COLORS.scuGold}`,
              borderRadius: 12,
              padding: "2px 10px",
              fontSize: 11,
              color: COLORS.scuGold,
              cursor: "pointer",
              fontWeight: 600,
            }}
          >
            {sourcesOpen ? "▲" : "▼"} {msg.sources.length} Source{msg.sources.length > 1 ? "s" : ""}
          </button>
          {sourcesOpen && (
            <div style={{ marginTop: 4 }}>
              {msg.sources.map((s, i) => (
                <SourceCard key={i} source={s} />
              ))}
            </div>
          )}
        </div>
      )}

      {/* Fallback notice */}
      {!isUser && msg.used_fallback && (
        <div
          style={{
            maxWidth: "75%",
            marginTop: 4,
            padding: "4px 10px",
            background: "#fff3cd",
            border: "1px solid #ffc107",
            borderRadius: 8,
            fontSize: 11,
            color: "#856404",
          }}
        >
          ⚠️ No matching policy found — please contact the Ciocca Center directly.
        </div>
      )}
    </div>
  );
}

// ── Quick Prompts ─────────────────────────────────────────────────────────────
const QUICK_PROMPTS = [
  "What is BEACH?",
  "How do I apply as a client?",
  "Is BEACH free?",
  "Can BEACH help with IP questions?",
  "What is the Bronco Ventures Accelerator?",
  "How do I contact the Ciocca Center?",
];

// ── Main Chat Component ────────────────────────────────────────────────────────
export default function CioccaChat() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "👋 Hi! I'm the Ciocca Center / BEACH assistant.\n\n" +
        "I can answer questions about the BEACH program, Ciocca Center programs, " +
        "how to apply, what BEACH can help with, and more.\n\n" +
        "How can I help you today?",
      sources: [],
      used_fallback: false,
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [category, setCategory] = useState("auto");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (text) => {
    const userText = text || input.trim();
    if (!userText || loading) return;
    setInput("");

    const userMsg = { role: "user", content: userText };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/bot`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userText,
          category: category === "auto" ? null : category,
        }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.reply,
          sources: data.sources || [],
          used_fallback: data.used_fallback || false,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `❌ Error connecting to the server. Make sure the FastAPI backend is running on port 8000.\n\nError: ${err.message}`,
          sources: [],
          used_fallback: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        fontFamily: "'Segoe UI', sans-serif",
        background: COLORS.bg,
      }}
    >
      {/* Header */}
      <div
        style={{
          background: COLORS.scuRed,
          color: COLORS.white,
          padding: "14px 20px",
          display: "flex",
          alignItems: "center",
          gap: 12,
          boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
        }}
      >
        <div style={{ fontSize: 28 }}>🌊</div>
        <div>
          <div style={{ fontWeight: 700, fontSize: 18 }}>Ciocca Center / BEACH Assistant</div>
          <div style={{ fontSize: 12, opacity: 0.85 }}>
            Santa Clara University · Bronco Entrepreneurs' Applied Collaboration Hub
          </div>
        </div>
        {/* Category selector */}
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          style={{
            marginLeft: "auto",
            padding: "4px 8px",
            borderRadius: 6,
            border: "none",
            background: "rgba(255,255,255,0.2)",
            color: COLORS.white,
            fontSize: 12,
            cursor: "pointer",
          }}
        >
          <option value="auto">Auto-detect</option>
          <option value="ciocca">Force: Ciocca/BEACH</option>
          <option value="general">Force: General</option>
        </select>
      </div>

      {/* Messages */}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "16px 20px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {messages.map((msg, i) => (
          <MessageBubble key={i} msg={msg} />
        ))}
        {loading && (
          <div style={{ alignSelf: "flex-start", padding: "10px 14px", color: COLORS.textMuted, fontStyle: "italic" }}>
            ⏳ Searching Ciocca knowledge base...
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Quick Prompts */}
      <div
        style={{
          padding: "6px 16px",
          display: "flex",
          gap: 6,
          flexWrap: "wrap",
          borderTop: `1px solid ${COLORS.border}`,
          background: COLORS.white,
        }}
      >
        {QUICK_PROMPTS.map((p, i) => (
          <button
            key={i}
            onClick={() => sendMessage(p)}
            disabled={loading}
            style={{
              padding: "4px 10px",
              borderRadius: 14,
              border: `1px solid ${COLORS.scuRed}`,
              background: "white",
              color: COLORS.scuRed,
              fontSize: 12,
              cursor: "pointer",
              whiteSpace: "nowrap",
            }}
          >
            {p}
          </button>
        ))}
      </div>

      {/* Input */}
      <div
        style={{
          display: "flex",
          gap: 10,
          padding: "12px 16px",
          background: COLORS.white,
          borderTop: `1px solid ${COLORS.border}`,
        }}
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
          placeholder="Ask about BEACH, Ciocca Center programs, how to apply..."
          disabled={loading}
          style={{
            flex: 1,
            padding: "10px 14px",
            borderRadius: 22,
            border: `1.5px solid ${COLORS.border}`,
            fontSize: 14,
            outline: "none",
          }}
        />
        <button
          onClick={() => sendMessage()}
          disabled={loading || !input.trim()}
          style={{
            padding: "10px 20px",
            background: COLORS.scuRed,
            color: COLORS.white,
            border: "none",
            borderRadius: 22,
            fontWeight: 700,
            cursor: loading || !input.trim() ? "not-allowed" : "pointer",
            opacity: loading || !input.trim() ? 0.6 : 1,
            fontSize: 14,
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}
