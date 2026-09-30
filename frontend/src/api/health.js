export async function fetchHealth() {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

  if (typeof apiBaseUrl !== "string" || apiBaseUrl.trim() === "") {
    throw new Error("VITE_API_BASE_URL is required");
  }

  const response = await fetch(new URL("/health", apiBaseUrl), {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error(`Health request failed with status ${response.status}`);
  }

  const health = await response.json();
  if (health.status !== "ok") {
    throw new Error("Backend returned an unexpected health status");
  }

  return health;
}
