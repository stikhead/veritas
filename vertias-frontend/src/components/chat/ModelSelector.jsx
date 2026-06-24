export default function ModelSelector(isAuthenticated) {
    {
  !isAuthenticated && (
    <div>
      Login required to switch models
    </div>
  );
}
  return (

    <select>
      <option value="spam">
        Spam Detection
      </option>

      <option value="emotion">
        Emotion Detection
      </option>
    </select>
  );
}