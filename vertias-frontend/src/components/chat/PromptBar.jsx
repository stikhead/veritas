import ModelSelector from "./ModelSelector";

export default function PromptBar() {
  return (
    <div className="prompt-bar">
      <ModelSelector />

      <input
        type="text"
        placeholder="Enter prompt..."
      />

      <button>Send</button>
    </div>
  );
}