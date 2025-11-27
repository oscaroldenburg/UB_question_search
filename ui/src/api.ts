const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export interface SearchResultItem {
  question: string;
  category?: string;
  year?: number;
  [key: string]: any;
}

export interface SearchResponse {
  items: SearchResultItem[];
  total: number;
}

export async function searchQuestions(q: string): Promise<SearchResponse> {
  const url = new URL("/search", API_BASE);
  url.searchParams.set("q", q);

  const res = await fetch(url.toString());

  if (!res.ok) {
    throw new Error("API error");
  }

  return await res.json();
}
