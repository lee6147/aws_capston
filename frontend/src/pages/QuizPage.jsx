import { useState, useEffect } from 'react';
import { Trophy, RotateCcw, BookOpen, Loader } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import QuizCard from '../components/QuizCard';
import * as api from '../services/api';
import useDocuments from '../hooks/useDocuments';

const FALLBACK_QUIZ = [
  {
    question: 'AWS Lambda의 최대 실행 시간 제한은?',
    choices: ['5분', '15분', '30분', '60분'],
    correctIndex: 1,
    explanation: 'AWS Lambda 함수의 최대 실행 시간은 15분(900초)입니다.',
    sourcePage: 8,
  },
  {
    question: 'Amazon S3의 객체 최대 크기는?',
    choices: ['5GB', '5TB', '50TB', '제한 없음'],
    correctIndex: 1,
    explanation: 'S3 단일 객체의 최대 크기는 5TB입니다. 멀티파트 업로드를 사용하면 대용량 파일을 업로드할 수 있습니다.',
    sourcePage: 12,
  },
  {
    question: 'VPC에서 인터넷 게이트웨이의 역할은?',
    choices: [
      'VPC 내부 트래픽 라우팅',
      'VPC와 인터넷 간의 통신',
      'VPC 간 피어링',
      'DNS 해석',
    ],
    correctIndex: 1,
    explanation: '인터넷 게이트웨이는 VPC와 인터넷 간의 통신을 가능하게 합니다.',
    sourcePage: 15,
  },
  {
    question: 'Amazon DynamoDB의 기본 키 유형이 아닌 것은?',
    choices: ['파티션 키', '복합 키 (파티션 + 정렬)', '보조 인덱스 키', '글로벌 키'],
    correctIndex: 3,
    explanation: 'DynamoDB는 파티션 키 또는 파티션 키 + 정렬 키 조합의 기본 키를 사용합니다. 글로벌 키라는 개념은 없습니다.',
    sourcePage: 22,
  },
  {
    question: 'CloudFormation 템플릿에서 반드시 포함해야 하는 섹션은?',
    choices: ['Parameters', 'Resources', 'Outputs', 'Mappings'],
    correctIndex: 1,
    explanation: 'Resources 섹션은 CloudFormation 템플릿에서 유일한 필수 섹션입니다.',
    sourcePage: 30,
  },
];

function mapApiQuiz(apiQuestions) {
  return apiQuestions.map((q) => ({
    question: q.question,
    choices: q.options || q.choices,
    correctIndex: q.correctAnswer ?? q.correctIndex,
    explanation: q.explanation,
    sourcePage: q.sourcePage || null,
  }));
}

export default function QuizPage() {
  const navigate = useNavigate();
  const { documents } = useDocuments();
  const [quiz, setQuiz] = useState(FALLBACK_QUIZ);
  const [loadingQuiz, setLoadingQuiz] = useState(false);
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState('');

  const readyDocs = documents.filter((d) => d.status === 'ready');

  const handleGenerate = async () => {
    if (!selectedDoc) return;
    setLoadingQuiz(true);
    setAnswers({});
    setShowResults(false);
    try {
      const data = await api.generateQuiz(selectedDoc);
      if (data.questions?.length > 0) {
        setQuiz(mapApiQuiz(data.questions));
      }
    } catch {
      setQuiz(FALLBACK_QUIZ);
    } finally {
      setLoadingQuiz(false);
    }
  };

  const handleAnswer = (qIndex, choiceIndex) => {
    setAnswers((prev) => ({ ...prev, [qIndex]: choiceIndex }));
  };

  const score = Object.entries(answers).reduce(
    (acc, [qi, ci]) => acc + (quiz[qi].correctIndex === ci ? 1 : 0),
    0,
  );

  const allAnswered = Object.keys(answers).length === quiz.length;

  const handleSubmit = () => {
    setShowResults(true);
  };

  const handleRetry = () => {
    setAnswers({});
    setShowResults(false);
  };

  return (
    <div className="quiz-page page">
      <h1 className="page-title">퀴즈</h1>
      <p className="page-desc">
        문서를 선택하고 퀴즈를 생성하세요. AI가 문서 내용을 바탕으로 문제를 만들어 드립니다.
      </p>

      {/* Document selector + generate */}
      <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '1.5rem', alignItems: 'center' }}>
        <select
          className="chat-page__input"
          style={{ maxWidth: '320px', padding: '0.5rem 0.75rem' }}
          value={selectedDoc}
          onChange={(e) => setSelectedDoc(e.target.value)}
        >
          <option value="">문서를 선택하세요</option>
          {readyDocs.map((d) => (
            <option key={d.id} value={d.id}>{d.name}</option>
          ))}
        </select>
        <button
          className="btn btn--primary"
          onClick={handleGenerate}
          disabled={!selectedDoc || loadingQuiz}
        >
          {loadingQuiz ? <><Loader size={16} className="spin" /> 생성 중...</> : '퀴즈 생성'}
        </button>
      </div>

      {/* Score banner */}
      {showResults && (
        <div className={`quiz-page__score card ${score === quiz.length ? 'quiz-page__score--perfect' : ''}`}>
          <Trophy size={32} />
          <div>
            <h2>
              {score} / {quiz.length} 정답
            </h2>
            <p>
              {score === quiz.length
                ? '완벽합니다! 모든 문제를 맞혔습니다!'
                : score >= quiz.length * 0.8
                  ? '훌륭합니다! 거의 다 맞혔어요.'
                  : '틀린 문제를 복습해보세요.'}
            </p>
          </div>
        </div>
      )}

      {/* Questions */}
      <div className="quiz-page__questions">
        {quiz.map((q, i) => (
          <QuizCard
            key={i}
            question={q}
            index={i}
            onAnswer={handleAnswer}
            showResult={showResults}
          />
        ))}
      </div>

      {/* Actions */}
      <div className="quiz-page__actions">
        {!showResults ? (
          <button
            className="btn btn--primary btn--lg"
            disabled={!allAnswered}
            onClick={handleSubmit}
          >
            제출하기
          </button>
        ) : (
          <>
            <button className="btn btn--primary btn--lg" onClick={handleRetry}>
              <RotateCcw size={18} /> 다시 풀기
            </button>
            <button className="btn btn--outline btn--lg" onClick={() => navigate('/chat')}>
              <BookOpen size={18} /> 오답 복습하기
            </button>
          </>
        )}
      </div>
    </div>
  );
}
