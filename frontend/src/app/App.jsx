import { useState } from "react";

import { fetchHealth } from "../api/health.js";

export default function App() {
  const [backendHealth, setBackendHealth] = useState("not checked");

  async function handleHealthCheck() {
    setBackendHealth("loading");

    try {
      const health = await fetchHealth();
      setBackendHealth(health.status);
    } catch {
      setBackendHealth("error");
    }
  }

  return (
    <main>
      <h1>Pathwise</h1>
      <p>Frontend foundation is running.</p>
      <button
        type="button"
        onClick={handleHealthCheck}
        disabled={backendHealth === "loading"}
      >
        Check backend health
      </button>
      <p>Backend health: {backendHealth}</p>
    </main>
  );
}
