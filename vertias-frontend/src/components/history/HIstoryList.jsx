import HistoryItem from "./HIstoryItem";

export default function HistoryList({
  isAuthenticated,
  history
}) {
  if (!isAuthenticated) {
    return (
      <div className="history-placeholder">
        Login or Signup to view history
      </div>
    );
  }

  return (
    <>
      {history.map(item => (
        <HistoryItem
          key={item._id}
          item={item}
        />
      ))}

    </>
  );
}