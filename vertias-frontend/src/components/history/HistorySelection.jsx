import HistoryList from "./HIstoryList";


export default function HistorySection() {
  return (
    <aside className="history-section">
      <header>
        <h2>History</h2>
      </header>

      <HistoryList />
    </aside>
  );
}