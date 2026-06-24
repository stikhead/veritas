export default function HistoryItem({ item }) {
  return (
    <div className="history-item">
      <h4>{item.prediction.label}</h4>

      <p>
        {item.input.slice(0, 100)}
      </p>

      <small>
        {new Date(item.createdAt)
          .toLocaleString()}
      </small>
    </div>
  );
}