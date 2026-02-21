const API_BASE_URL = "http://localhost:8001";

export interface SourceDocument {
    title: string;
    source_url: string;
    score: number;
}

export interface SearchResponse {
    answer: string;
    sources: SourceDocument[];
    query: string;
}

export async function searchQuery(
    query: string,
    topK: number = 5
): Promise<SearchResponse> {
    const response = await fetch(`${API_BASE_URL}/api/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, top_k: topK }),
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: "Unknown error" }));
        throw new Error(error.detail || `Search failed: ${response.status}`);
    }

    return response.json();
}

export async function healthCheck(): Promise<boolean> {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        return response.ok;
    } catch {
        return false;
    }
}
