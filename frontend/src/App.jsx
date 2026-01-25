import { useMemo, useState } from "react";

function classifyLocal(text) {
  const t = text.toLowerCase();

  const legalWords = [
    "llc",
    "incorporate",
    "inc",
    "contract",
    "nda",
    "ip",
    "patent",
    "trademark",
    "terms",
    "privacy",
    "liability",
    "equity",
    "shares",
    "founder",
    "c-corp",
    "corp",
    "employment",
  ];
  const businessWords = [
    "pricing",
    "revenue",
    "business model",
    "customer",
    "market",
    "competition",
    "strategy",
    "go-to-market",
    "sales",
    "marketing",
    "unit economics",
    "mvp",
    "product",
  ];
  const cioccaWords = [
    "ciocca",
    "mentor",
    "accelerator",
    "incubator",
    "program",
    "funding",
    "pitch",
    "workshop",
    "application",
    "venture",
  ];

  const score = (words) =>
    words.reduce((acc, w) => acc + (t.includes(w) ? 1 : 0), 0);

  const legal = score(legalWords);
  const business = score(businessWords);
  const ciocca = score(cioccaWords);

  const max = Math.max(legal, business, ciocca);
  if (max === 0) {
    return {
      category: "unknown",
      confidence: 0.35,
      reply:
        "Got it. I can help route this—could you share a bit more detail about what you’re trying to do and what’s blocking you?",
      followups: [
        "What stage is your startup in (idea/MVP/launched)?",
        "What outcome are you hoping for from BEACH?",
        "Any deadlines coming up?",
      ],
    };
  }

  let category = "legal";
  if (max === business) category = "business";
  if (max === ciocca) category = "ciocca";

  // very simple confidence heuristic
  const confidence = Math.min(0.95, 0.55 + 0.15 * max);

  if (category === "legal") {
    return {
      category,
      confidence,
      reply:
        "This looks primarily like a **legal** question. I can collect a few details so the legal team can help efficiently.",
      followups: [
        "Is this about forming an entity (LLC/C-Corp) or a contract/IP issue?",
        "Which state is your startup based in (jurisdiction)?",
        "Do you have a deadline (fundraising, launch, signing date)?",
      ],
    };
  }

  if (category === "business") {
    return {
      category,
      confidence,
      reply:
        "This looks primarily like a **business** question. I’ll ask a few targeted questions to clarify your model and constraints.",
      followups: [
        "Who is your target customer and what problem are you solving?",
        "How are you thinking about pricing or revenue?",
        "What traction do you have so far (users, pilots, revenue)?",
      ],
    };
  }

  return {
    category,
    confidence,
    reply:
      "This looks like a **Ciocca / program** question. I can help route you to the right resources and next steps.",
    followups: [
      "Are you asking about programs, mentorship, funding, or pitch events?",
      "What is your startup stage (idea/MVP/launched)?",
      "What’s your timeline for applying or presenting?",
    ],
  };
}

function Badge({ label }) {
  const cls = useMemo(() => {
    const base =
      "display:inline-block;padding:2px 10px;border-radius:999px;border:1px solid #ddd;font-size:12px";
    if (label === "legal") return `${base};background:#fff1f2;color:#9f1239;border-color:#fecdd3`;
    if (label === "business")
      return `${base};background:#eff6ff;color:#1d4ed8;border-color:#bfdbfe`;
    if (label === "ciocca")
      return `${base};background:#ecfdf5;color:#047857;border-color:#a7f3d0`;
    return `${base};background:#f8fafc;color:#334155;border-color:#e2e8f0`;
  }, [label]);

  return <span style={{ cssText: cls }}>{label}</span>;
}

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Hi! I’m the BEACH consulting bot. Tell me what you’re working on and what you need help with.",
      meta: { category: "intake", confidence: 0.8 },
    },
  ]);
  const [input, setInput] = useState("");

  function addMessage(m) {
    setMessages((prev) => [...prev, m]);
  }

  function sendMessage(e) {
    e.preventDefault();
    const text = input.trim();
    if (!text) return;

    addMessage({ role: "user", text });
    setInput("");

    // Local “backend” mock
    const result = classifyLocal(text);

    addMessage({
      role: "bot",
      text: result.reply,
      meta: {
        category: result.category,
        confidence: result.confidence,
        followups: result.followups,
      },
    });
  }

  function clickFollowup(q) {
    setInput(q);
  }

  return (
    <div style={{ maxWidth: 860, margin: "32px auto", fontFamily: "Arial, sans-serif" }}>
      <div style={{ display: "flex", gap: 16, alignItems: "flex-start" }}>
        {/* Chat */}
        <div style={{ flex: 1, background: "white", border: "1px solid #e5e7eb", borderRadius: 16 }}>
          <div style={{ padding: 16, borderBottom: "1px solid #e5e7eb" }}>
            <div style={{ fontWeight: 700, fontSize: 18 }}>BEACH Intake Chat (Demo)</div>
            <div style={{ fontSize: 12, color: "#64748b" }}>
              Demo routing: business • legal • Ciocca
            </div>
          </div>

          <div style={{ padding: 16, height: 420, overflowY: "auto" }}>
            {messages.map((m, i) => {
              const isUser = m.role === "user";
              return (
                <div key={i} style={{ display: "flex", justifyContent: isUser ? "flex-end" : "flex-start", marginBottom: 12 }}>
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
          </div>

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
        </div>
      </div>
    </div>
  );
}