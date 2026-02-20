import type { SearchResponse } from "../api";

interface ResultViewProps {
    result: SearchResponse;
}

export function ResultView({ result }: ResultViewProps) {
    return (
        <div className="result-view fade-in">
            <div className="result-query">
                <span className="query-label">Q.</span>
                <span className="query-text">{result.query}</span>
            </div>

            <div className="result-answer">
                <div className="answer-header">
                    <svg
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    >
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                    </svg>
                    <span>回答</span>
                </div>
                <div className="answer-body">
                    {result.answer.split("\n").map((line, i) => (
                        <p key={i}>{line || "\u00A0"}</p>
                    ))}
                </div>
            </div>

            {result.sources.length > 0 && (
                <div className="result-sources">
                    <div className="sources-header">
                        <svg
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        >
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                            <polyline points="14 2 14 8 20 8" />
                        </svg>
                        <span>参照ソース ({result.sources.length})</span>
                    </div>
                    <div className="sources-list">
                        {result.sources.map((source, i) => (
                            <a
                                key={i}
                                className="source-card"
                                href={source.source_url}
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                <span className="source-index">{i + 1}</span>
                                <span className="source-title">{source.title}</span>
                                <span className="source-score">
                                    {(source.score).toFixed(1)}
                                </span>
                            </a>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
