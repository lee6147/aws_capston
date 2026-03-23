import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Upload,
  MessageSquare,
  GraduationCap,
  FileText,
  TrendingUp,
  BookOpen,
} from 'lucide-react';
import useDocuments from '../hooks/useDocuments';
import DocumentCard from '../components/DocumentCard';
import * as api from '../services/api';

export default function DashboardPage() {
  const navigate = useNavigate();
  const { documents, loading } = useDocuments();
  const [stats, setStats] = useState({
    questionsAsked: 0,
    quizzesCompleted: 0,
    documentsUploaded: 0,
    avgScore: 0,
  });

  useEffect(() => {
    api.fetchDashboardStats()
      .then((data) => {
        setStats({
          questionsAsked: data.totalQuestions ?? 0,
          quizzesCompleted: data.quizzesCompleted ?? 5,
          documentsUploaded: data.totalDocuments ?? 0,
          avgScore: data.averageScore ?? 0,
        });
      })
      .catch(() => {
        // Fallback to mock stats
        setStats({
          questionsAsked: 47,
          quizzesCompleted: 5,
          documentsUploaded: 3,
          avgScore: 82,
        });
      });
  }, []);

  const recentDocs = documents.slice(0, 3);
  const hour = new Date().getHours();
  const greeting = hour < 12 ? '좋은 아침이에요! ☀️' : hour < 18 ? '안녕하세요! 📚' : '좋은 저녁이에요! 🌙';

  return (
    <div className="dashboard-page page">
      {/* Welcome */}
      <section className="dashboard-page__welcome">
        <h1>{greeting} 오늘도 열심히 공부해볼까요?</h1>
        <p>StudyBot이 학습을 도와드립니다. PDF를 업로드하고 AI에게 질문하세요.</p>
      </section>

      {/* Quick Actions */}
      <section className="dashboard-page__actions">
        <button className="action-card card" onClick={() => navigate('/upload')}>
          <Upload size={28} />
          <span>PDF 업로드</span>
        </button>
        <button className="action-card card" onClick={() => navigate('/chat')}>
          <MessageSquare size={28} />
          <span>AI 채팅</span>
        </button>
        <button className="action-card card" onClick={() => navigate('/quiz')}>
          <GraduationCap size={28} />
          <span>퀴즈 풀기</span>
        </button>
      </section>

      {/* Stats */}
      <section className="dashboard-page__stats">
        <h2 className="section-title">학습 통계</h2>
        <div className="stats-grid">
          <div className="stat-card card">
            <MessageSquare size={22} className="stat-card__icon" />
            <div>
              <p className="stat-card__value">{stats.questionsAsked}</p>
              <p className="stat-card__label">질문 수</p>
            </div>
          </div>
          <div className="stat-card card">
            <GraduationCap size={22} className="stat-card__icon" />
            <div>
              <p className="stat-card__value">{stats.quizzesCompleted}</p>
              <p className="stat-card__label">퀴즈 완료</p>
            </div>
          </div>
          <div className="stat-card card">
            <FileText size={22} className="stat-card__icon" />
            <div>
              <p className="stat-card__value">{stats.documentsUploaded}</p>
              <p className="stat-card__label">업로드 문서</p>
            </div>
          </div>
          <div className="stat-card card">
            <TrendingUp size={22} className="stat-card__icon" />
            <div>
              <p className="stat-card__value">{stats.avgScore}%</p>
              <p className="stat-card__label">평균 점수</p>
            </div>
          </div>
        </div>
      </section>

      {/* Recent documents */}
      <section className="dashboard-page__recent">
        <div className="section-header">
          <h2 className="section-title">최근 문서</h2>
          <button className="btn btn--ghost" onClick={() => navigate('/documents')}>
            <BookOpen size={16} /> 전체 보기
          </button>
        </div>

        {loading ? (
          <p className="muted">문서를 불러오는 중...</p>
        ) : recentDocs.length === 0 ? (
          <p className="muted">아직 업로드한 문서가 없습니다.</p>
        ) : (
          <div className="document-list">
            {recentDocs.map((doc) => (
              <DocumentCard key={doc.id} doc={doc} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
