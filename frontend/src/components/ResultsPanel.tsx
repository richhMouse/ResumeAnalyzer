interface ResultsPanelProps {
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
}

function ResultsPanel({ strengths, weaknesses, suggestions }: ResultsPanelProps) {
  return (
    <div className="results-panel">
      <div className="result-section">
        <h3 className="result-title strengths">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="20 6 9 17 4 12" />
          </svg>
          Factual Strengths
        </h3>
        <ul className="result-list">
          {strengths.map((strength, index) => (
            <li key={index} className="result-item">{strength}</li>
          ))}
        </ul>
      </div>

      <div className="result-section">
        <h3 className="result-title weaknesses">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="15" y1="9" x2="9" y2="15" />
            <line x1="9" y1="9" x2="15" y2="15" />
          </svg>
          Factual Weaknesses
        </h3>
        <ul className="result-list">
          {weaknesses.map((weakness, index) => (
            <li key={index} className="result-item">{weakness}</li>
          ))}
        </ul>
      </div>

      <div className="result-section suggestions-section">
        <h3 className="result-title suggestions">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
            <line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
          Actionable Improvements
        </h3>
        <ul className="result-list suggestions-list">
          {suggestions.map((suggestion, index) => (
            <li key={index} className="result-item suggestion-item">
              <span className="suggestion-number">{index + 1}</span>
              {suggestion}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default ResultsPanel;
