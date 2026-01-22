type Props = {
  title?: string;
  subtitle?: string;
};

export default function ChatHeader({
  title = "Chatbot",
  subtitle = "Frontend only (TypeScript + SWC)",
}: Props) {
  return (
    <header style={styles.header}>
      <div>
        <h1 style={styles.title}>{title}</h1>
        <p style={styles.subtitle}>{subtitle}</p>
      </div>
      <span style={styles.badge}>Local</span>
    </header>
  );
}

const styles: Record<string, React.CSSProperties> = {
  header: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "16px 18px",
    borderBottom: "1px solid rgba(0,0,0,0.12)",
  },
  title: { margin: 0, fontSize: 18 },
  subtitle: { margin: "4px 0 0", fontSize: 12, opacity: 0.7 },
  badge: {
    fontSize: 12,
    padding: "6px 10px",
    borderRadius: 999,
    border: "1px solid rgba(0,0,0,0.12)",
  },
};
