const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function searchQuestions(q) {
  const url = new URL("/search", API_BASE);
  url.searchParams.set("q", q);

  const res = await fetch(url.toString());

  if (!res.ok) {
    throw new Error("API error");
  }

  return await res.json();
}