// frontend/src/api/apiClient.ts
// API client — configure backend base URL here

// For local development:
const BASE_URL = "http://localhost:8000";

// Later for deployment (HuggingFace Space):
// const BASE_URL = "https://your-hf-space-url.hf.space";

// ----------------------
// Fetch matched jobs
// ----------------------
export async function getMatchedJobs(formData: FormData) {
  const response = await fetch(`${BASE_URL}/match`, {
    method: "POST",
    body: formData,
  });
  const data = await response.json();
  return data.results || [];
}

// ----------------------
// Fetch /match/more
// ----------------------
export async function getMoreJobs() {
  const response = await fetch(`${BASE_URL}/match/more`);
  const data = await response.json();
  return data.results || [];
}

// ----------------------
// Fetch random jobs for homepage
// ----------------------
export async function getRandomJobs() {
  const response = await fetch(`${BASE_URL}/jobs/random`);
  const data = await response.json();
  return data.results || [];
}
