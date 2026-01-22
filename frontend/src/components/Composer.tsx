import { useEffect, useRef, useState } from "react";

type Props = {
  onSend: (text: string) => void;
  disabled?: boolean;
};

export default function Composer({ onSend, disabled }: Props) {
  const [text, setText] = useState("");
  const inputRef = useRef<HTMLTextAreaElement | null>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  function send() {
    const trimmed = text.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setText("");
    inputRef.current?.focus();
  }

  return (
    <div style={styles.wrap}>
      <textarea
        ref={inputRef}
        value={text}
        placeholder="Type a message… (Enter to send, Shift+Enter for newline)"
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            if (!disabled) send();
          }
        }}
        disabled={disabled}
        rows={2}
        style={styles.textarea}
      />
      <button onClick={send} disabled={disabled || !text.trim()} style={styles.button}>
        Send
      </button>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  wrap: {
    display: "flex",
    gap: 10,
    padding: 12,
    borderTop: "1px solid rgba(0,0,0,0.12)",
  },
  textarea: {
    flex: 1,
    resize: "none",
    padding: "10px 12px",
    borderRadius: 12,
    border: "1px solid rgba(0,0,0,0.18)",
    fontSize: 14,
    lineHeight: 1.35,
    outline: "none",
  },
  button: {
    padding: "10px 14px",
    borderRadius: 12,
    border: "1px solid rgba(0,0,0,0.18)",
    cursor: "pointer",
    fontSize: 14,
  },
};
