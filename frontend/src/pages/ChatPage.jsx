import { useState, useRef, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Send, GraduationCap, RotateCcw, PanelRightOpen, PanelRightClose, Download } from 'lucide-react';
import useChat from '../hooks/useChat';
import useDocuments from '../hooks/useDocuments';
import ChatMessage, { ChatMessageSkeleton } from '../components/ChatMessage';
import CitationHighlight from '../components/CitationHighlight';

export default function ChatPage() {
  const [searchParams] = useSearchParams();
  const docId = searchParams.get('doc') || null;
  const navigate = useNavigate();

  const { documents } = useDocuments();
  const [selectedDoc, setSelectedDoc] = useState(docId);
  const { messages, loading, sendMessage, clearMessages } = useChat(selectedDoc);

  const [input, setInput] = useState('');
  const [activeCitation, setActiveCitation] = useState(null);
  const [panelOpen, setPanelOpen] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = () => {
    const text = input.trim();
    if (!text || loading) return;
    setInput('');
    sendMessage(text);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleCitationClick = (citation) => {
    setActiveCitation(citation);
    setPanelOpen(true);
  };

  const handleFollowUp = (text) => {
    setInput(text);
    inputRef.current?.focus();
  };

  const handleExport = () => {
    if (messages.length === 0) return;
    const docName = documents.find((d) => d.id === selectedDoc)?.name || 'unknown';
    let text = `StudyBot 대화 기록\n문서: ${docName}\n날짜: ${new Date().toLocaleDateString('ko-KR')}\n${'─'.repeat(40)}\n\n`;

    messages.forEach((msg) => {
      const role = msg.role === 'user' ? '👤 나' : '🤖 AI';
      text += `${role}\n${msg.content}\n`;
      if (msg.citations?.length > 0) {
        text += `\n📌 출처: ${msg.citations.map((c) => `p.${c.page}`).join(', ')}\n`;
      }
      text += '\n' + '─'.repeat(40) + '\n\n';
    });

    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `studybot-chat-${new Date().toISOString().slice(0, 10)}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const readyDocs = documents.filter((d) => d.status === 'ready');

  return (
    <div className={`chat-page page ${panelOpen ? 'chat-page--panel-open' : ''}`}>
      {/* Chat column */}
      <div className="chat-page__main">
        {/* Top bar */}
        <div className="chat-page__topbar">
          <div className="chat-page__doc-select">
            <select
              value={selectedDoc || ''}
              onChange={(e) => {
                setSelectedDoc(e.target.value || null);
                clearMessages();
              }}
            >
              <option value="">문서를 선택하세요</option>
              {readyDocs.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.name}
                </option>
              ))}
            </select>
            {messages.length > 0 && (
              <span className="chat-page__msg-count">{messages.length}개 메시지</span>
            )}
          </div>

          <div className="chat-page__topbar-actions">
            <button className="icon-btn" onClick={clearMessages} title="대화 초기화">
              <RotateCcw size={18} />
            </button>
            <button
              className="icon-btn"
              onClick={handleExport}
              title="대화 내보내기"
              disabled={messages.length === 0}
            >
              <Download size={18} />
            </button>
            <button
              className="icon-btn"
              onClick={() => navigate('/quiz')}
              title="퀴즈 생성"
              disabled={messages.length < 2}
            >
              <GraduationCap size={18} />
            </button>
            <button
              className="icon-btn"
              onClick={() => setPanelOpen((o) => !o)}
              title="PDF 뷰어 토글"
            >
              {panelOpen ? <PanelRightClose size={18} /> : <PanelRightOpen size={18} />}
            </button>
          </div>
        </div>

        {/* Messages */}
        <div className="chat-page__messages">
          {messages.length === 0 && (
            <div className="chat-page__empty">
              <h2>AI에게 질문하세요</h2>
              <p>업로드한 문서에 대해 어떤 것이든 물어보세요.</p>
              <div className="chat-page__suggestions">
                {[
                  '📋 이 문서의 핵심 내용을 요약해줘',
                  '⚡ AWS Lambda가 뭔지 설명해줘',
                  '🔑 IAM 보안 모범 사례를 알려줘',
                  '🌐 VPC 네트워크 구성을 설명해줘',
                  '💾 S3 스토리지 클래스 비교해줘',
                  '🤖 RAG 아키텍처가 뭐야?',
                ].map((s) => (
                  <button
                    key={s}
                    className="suggestion-chip"
                    onClick={() => {
                      setInput(s);
                      inputRef.current?.focus();
                    }}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <ChatMessage key={i} message={msg} onCitationClick={handleCitationClick} onFollowUp={handleFollowUp} />
          ))}
          {loading && <ChatMessageSkeleton />}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="chat-page__input-area">
          <textarea
            ref={inputRef}
            className="chat-page__input"
            rows={1}
            placeholder={selectedDoc ? '메시지를 입력하세요...' : '먼저 문서를 선택하세요'}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={!selectedDoc}
          />
          <button
            className="chat-page__send btn btn--primary"
            onClick={handleSend}
            disabled={!input.trim() || loading}
          >
            <Send size={18} />
          </button>
          {/* Input hint */}
          {selectedDoc && messages.length === 0 && (
            <div className="chat-page__hint">
              Enter로 전송 · Shift+Enter로 줄바꿈
            </div>
          )}
        </div>
      </div>

      {/* PDF panel */}
      {panelOpen && (
        <div className="chat-page__panel">
          <CitationHighlight
            citation={activeCitation}
            onClose={() => {
              setActiveCitation(null);
              setPanelOpen(false);
            }}
          />
        </div>
      )}
    </div>
  );
}
