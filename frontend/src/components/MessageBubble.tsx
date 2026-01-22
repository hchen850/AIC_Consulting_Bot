import type { ChatMessage } from "../types/chat";

type Props = {
  msg: ChatMessage;
};

export default function MessageBubble({ msg }: Props) {
  const isUser = msg.role === "user";

  return (
    <div style={{ ...styles.row, justifyContent: isUser ? "flex-end" : "flex-start" }}>
      <div style={{ ...styles.bubble, ...(isUser ? styles.user : styles.assistant) }}>
        <div style={styles.role}>{isUser ? "You" : "Bot"}</div>
        <div style={styles.content}>{msg.content}</div>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  row: {
    display: "flex",
    padding: "6px 12px",
  },
  bubble: {
    maxWidth: 720,
    width: "fit-content",
    padding: "10px 12px",
    borderRadius: 14,
    border: "1px solid rgba(0,0,0,0.12)",
    whiteSpace: "pre-wrap",
    wordBreak: "break-word",
  },
  user: {
    borderTopRightRadius: 6,
  },
  assistant: {
    borderTopLeftRadius: 6,
    opacity: 0.95,
  },
  role: {
    fontSize: 11,
    opacity: 0.7,
    marginBottom: 6,
  },
  content: {
    fontSize: 14,
    lineHeight: 1.35,
  },
};
