interface ScoreCardProps {
  title: string;
  score: number;
  max: number;
  color: string;
  delay?: number;
}

function ScoreCard({ title, score, max, color, delay = 0 }: ScoreCardProps) {
  const percentage = (score / max) * 100;
  
  return (
    <div 
      className="score-card animate-in"
      style={{ 
        '--delay': `${delay * 0.1}s`,
        '--card-color': color 
      } as React.CSSProperties}
    >
      <div className="score-card-header">
        <span className="score-card-title">{title}</span>
        <span className="score-card-value" style={{ color }}>
          {score}/{max}
        </span>
      </div>
      <div className="score-card-bar">
        <div 
          className="score-card-fill" 
          style={{ width: `${percentage}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}

export default ScoreCard;
