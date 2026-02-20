import { useState } from "react";
import { SearchBar } from "./components/SearchBar";
import { ResultView } from "./components/ResultView";
import { searchQuery, type SearchResponse } from "./api";
import "./App.css";

function App() {
  const [result, setResult] = useState<SearchResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (query: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await searchQuery(query);
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "検索に失敗しました");
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <svg
              width="28"
              height="28"
              viewBox="0 0 24 24"
              fill="none"
              stroke="url(#logoGradient)"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <defs>
                <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#6366f1" />
                  <stop offset="100%" stopColor="#a855f7" />
                </linearGradient>
              </defs>
              <circle cx="11" cy="11" r="8" />
              <path d="M21 21l-4.35-4.35" />
              <path d="M11 8v6" />
              <path d="M8 11h6" />
            </svg>
            <h1>Cosense RAG</h1>
          </div>
          <p className="subtitle">Cosense の知識を AI で検索</p>
        </div>
      </header>

      <main className="app-main">
        <SearchBar onSearch={handleSearch} isLoading={isLoading} />

        {error && (
          <div className="error-message fade-in">
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <circle cx="12" cy="12" r="10" />
              <line x1="15" y1="9" x2="9" y2="15" />
              <line x1="9" y1="9" x2="15" y2="15" />
            </svg>
            <span>{error}</span>
          </div>
        )}

        {isLoading && (
          <div className="loading-state fade-in">
            <div className="loading-dots">
              <span />
              <span />
              <span />
            </div>
            <p>検索中...</p>
          </div>
        )}

        {result && !isLoading && <ResultView result={result} />}

        {!result && !isLoading && !error && (
          <div className="empty-state fade-in">
            <svg
              width="48"
              height="48"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              opacity="0.3"
            >
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
            <p>質問を入力して、Cosense のナレッジベースから回答を取得しましょう</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
