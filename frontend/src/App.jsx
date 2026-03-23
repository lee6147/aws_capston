import { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ToastProvider } from './components/Toast';
import Layout from './components/Layout';
import DashboardPage from './pages/DashboardPage';
import ChatPage from './pages/ChatPage';
import UploadPage from './pages/UploadPage';
import QuizPage from './pages/QuizPage';
import DocumentsPage from './pages/DocumentsPage';

/**
 * In development / demo mode we skip Cognito auth entirely.
 * Set VITE_SKIP_AUTH=true in .env to enable this.
 *
 * When Cognito is configured, we'll use the Amplify Authenticator.
 */
const SKIP_AUTH = import.meta.env.VITE_SKIP_AUTH !== 'false'; // demo mode by default, set VITE_SKIP_AUTH=false to require login

export default function App() {
  const [authenticated, setAuthenticated] = useState(SKIP_AUTH);

  const handleSignOut = () => {
    setAuthenticated(false);
  };

  if (!authenticated) {
    return (
      <BrowserRouter>
        <div className="login-page">
          <div className="login-page__brand">
            <h1>StudyBot Enhanced</h1>
            <p>AI 기반 학습 도우미</p>
          </div>
          <div className="login-page__form card">
            <h2>로그인</h2>
            <p className="muted">Cognito가 구성되면 여기에 로그인 화면이 표시됩니다.</p>
            <button className="btn btn--primary btn--lg" onClick={() => setAuthenticated(true)}>
              데모 모드로 시작
            </button>
          </div>
        </div>
      </BrowserRouter>
    );
  }

  return (
    <BrowserRouter>
      <ToastProvider>
        <Routes>
          <Route element={<Layout onSignOut={handleSignOut} />}>
            <Route index element={<DashboardPage />} />
            <Route path="chat" element={<ChatPage />} />
            <Route path="upload" element={<UploadPage />} />
            <Route path="quiz" element={<QuizPage />} />
            <Route path="documents" element={<DocumentsPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </ToastProvider>
    </BrowserRouter>
  );
}
