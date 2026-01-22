import { useEffect, useMemo, useRef, useState } from "react";
import ChatHeader from "./components/ChatHeader";
import Composer from "./components/Composer";
import MessageBubble from "./components/MessageBubble";
import type { ChatMessage } from "./types/chat";
import { sendToBot } from "./api/chat";


function uid() {
  return Math.random().toString(16).slice(2) + Date.now().toString(16);
}

function makeMsg(role: ChatMessage["role"], content: string): ChatMessage {
  return { id: uid(), role, content, createdAt: Date.now() };
}

export default function App() {
  const [messages, setMessages] = useState<ChatMessage[]>(() => [
    makeMsg("assistant", "Hi! I’m your chatbot UI.\n\nI’m not connected to a backend yet."),
    makeMsg("assistant", "Type a message below and I’ll echo it like a placeholder."),
  ]);

  const scrollRef = useRef<HTMLDivElement | null>(null);

  const sorted = useMemo(
    () => [...messages].sort((a, b) => a.createdAt - b.createdAt),
    [messages]
  );

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [sorted.length]);

  async function handleSend(text: string) {
    // Add the user's message immediately
    setMessages((prev) => [...prev, makeMsg("user", text)]);

    // Add a temporary assistant message while waiting
    const typingId = uid();
    setMessages((prev) => [
      ...prev,
      { id: typingId, role: "assistant", content: "Typing…", createdAt: Date.now() },
    ]);

    try {
      // Call your FastAPI backend (which calls Ollama)
      const data = await sendToBot(text);

      // Replace "Typing…" with the real reply
      setMessages((prev) =>
        prev.map((m) => (m.id === typingId ? { ...m, content: data.reply } : m))
      );
    } catch (err) {
      // Replace "Typing…" with an error message
      const msg = err instanceof Error ? err.message : "Unknown error";
      setMessages((prev) =>
        prev.map((m) => (m.id === typingId ? { ...m, content: `Error: ${msg}` } : m))
      );
    }
  }



  function clearChat() {
    setMessages([makeMsg("assistant", "Chat cleared. Send a message!")]);
  }

  return (
    <div style={styles.page}>
      <div style={styles.shell}>
        <ChatHeader title="My Chatbot" subtitle="React + TypeScript + SWC (frontend-only)" />

        <main style={styles.main}>
          <div style={styles.toolbar}>
            <button onClick={clearChat} style={styles.toolbarBtn}>
              Clear
            </button>
            <span style={styles.hint}>Tip: Enter = send, Shift+Enter = newline</span>
          </div>

          <div style={styles.messages}>
            {sorted.map((m) => (
              <MessageBubble key={m.id} msg={m} />
            ))}
            <div ref={scrollRef} />
          </div>
        </main>

        <Composer onSend={handleSend} />
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  page: {
    minHeight: "100vh",
    display: "grid",
    placeItems: "center",
    padding: 18,
  },
  shell: {
    width: "min(980px, 100%)",
    height: "min(78vh, 820px)",
    display: "flex",
    flexDirection: "column",
    border: "1px solid rgba(0,0,0,0.12)",
    borderRadius: 16,
    overflow: "hidden",
  },
  main: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    minHeight: 0,
  },
  toolbar: {
    display: "flex",
    alignItems: "center",
    gap: 12,
    padding: "10px 12px",
    borderBottom: "1px solid rgba(0,0,0,0.08)",
  },
  toolbarBtn: {
    padding: "6px 10px",
    borderRadius: 10,
    border: "1px solid rgba(0,0,0,0.18)",
    cursor: "pointer",
    fontSize: 13,
  },
  hint: { fontSize: 12, opacity: 0.7 },
  messages: {
    flex: 1,
    overflow: "auto",
    padding: "8px 0",
  },
};

