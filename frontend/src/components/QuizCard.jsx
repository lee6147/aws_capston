import { useState } from 'react';
import { CheckCircle, XCircle } from 'lucide-react';

export default function QuizCard({ question, index, onAnswer, showResult }) {
  const [selected, setSelected] = useState(null);

  const handleSelect = (choiceIndex) => {
    if (showResult) return; // already answered
    setSelected(choiceIndex);
    onAnswer?.(index, choiceIndex);
  };

  const isCorrect = (ci) => showResult && ci === question.correctIndex;
  const isWrong = (ci) => showResult && ci === selected && ci !== question.correctIndex;

  return (
    <div className="quiz-card card">
      <div className="quiz-card__header">
        <span className="quiz-card__number">Q{index + 1}</span>
        <p className="quiz-card__question">{question.question}</p>
      </div>

      <div className="quiz-card__choices">
        {question.choices.map((choice, ci) => (
          <button
            key={ci}
            className={`quiz-card__choice
              ${selected === ci ? 'quiz-card__choice--selected' : ''}
              ${isCorrect(ci) ? 'quiz-card__choice--correct' : ''}
              ${isWrong(ci) ? 'quiz-card__choice--wrong' : ''}
            `}
            onClick={() => handleSelect(ci)}
          >
            <span className="quiz-card__choice-label">
              {String.fromCharCode(65 + ci)}
            </span>
            <span>{choice}</span>
            {isCorrect(ci) && <CheckCircle size={18} className="text-green" />}
            {isWrong(ci) && <XCircle size={18} className="text-red" />}
          </button>
        ))}
      </div>

      {showResult && selected !== question.correctIndex && question.explanation && (
        <div className="quiz-card__explanation">
          <strong>해설:</strong> {question.explanation}
          {question.sourcePage && (
            <span className="quiz-card__source"> (p.{question.sourcePage})</span>
          )}
        </div>
      )}
    </div>
  );
}
