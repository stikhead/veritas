import ResponseCard from "../chat/ResponseCard";
import QueryCard from "../chat/QueryCard"
import PromptBar from "../chat/PromptBar"

export default function ChatSection() {
  return (
    <section className="chat-section">
      <QueryCard />
      <ResponseCard />
      <PromptBar />
    </section>
  );
}