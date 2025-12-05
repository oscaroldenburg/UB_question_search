const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export interface QuestionItem {
  question: string;
  category?: string;
  refference_used?: string;
  year?: number;
  Answer_alternatives?: string[];
  [key: string]: any;
}

export interface SearchResponse {
  items: QuestionItem[];
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

export async function getQuestion(id: string): Promise<QuestionItem> {
  const url = new URL('/get_question_by_varname', API_BASE);
  url.searchParams.set("var_name", id);

  const res = await fetch(url.toString());
  const data = await res.json();
  if (!res.ok) {
    throw new Error("API error");
  }

  return data.item;
}
