import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot, Volume2, VolumeX, BookOpen, Copy, Check, ThumbsUp, ThumbsDown } from 'lucide-react';

export default function ChatMessage({ message, onCitationClick, onFollowUp }) {
  const [speaking, setSpeaking] = useState(false);
  const [copied, setCopied] = useState(false);
  const [rating, setRating] = useState(null); // 'up' | 'down' | null
  const isUser = message.role === 'user';

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.content);
    } catch {
      // Fallback for insecure contexts (HTTP)
      const textarea = document.createElement('textarea');
      textarea.value = message.content;
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleReadAloud = () => {
    if (speaking) {
      window.speechSynthesis.cancel();
      setSpeaking(false);
      return;
    }
    // Use browser SpeechSynthesis as fallback; real app would call Polly API
    const utterance = new SpeechSynthesisUtterance(message.content.replace(/[*#_`]/g, ''));
    utterance.lang = 'ko-KR';
    utterance.onend = () => setSpeaking(false);
    window.speechSynthesis.speak(utterance);
    setSpeaking(true);
  };

  return (
    <div className={`chat-message ${isUser ? 'chat-message--user' : 'chat-message--ai'}`}>
      <div className="chat-message__avatar">
        {isUser ? <User size={18} /> : <Bot size={18} />}
      </div>

      <div className="chat-message__body">
        <div className="chat-message__content">
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>

        {/* Citations */}
        {!isUser && message.citations?.length > 0 && (
          <div className="chat-message__citations">
            <span className="chat-message__citations-label">
              <BookOpen size={14} /> 참고 출처:
            </span>
            {message.citations.map((c, i) => (
              <button
                key={i}
                className="citation-badge"
                onClick={() => onCitationClick?.(c)}
                title={c.text}
              >
                p.{c.page}
                {c.paragraph != null && ` - ${c.paragraph}단락`}
              </button>
            ))}
          </div>
        )}

        {/* Follow-up suggestions */}
        {!isUser && message.followUps?.length > 0 && (
          <div className="chat-message__followups">
            <span className="chat-message__followups-label">💡 추가 질문:</span>
            {message.followUps.map((q, i) => (
              <button
                key={i}
                className="followup-chip"
                onClick={() => onFollowUp?.(q)}
              >
                {q}
              </button>
            ))}
          </div>
        )}

        {/* Actions */}
        {!isUser && (
          <div className="chat-message__actions">
            <button
              className="icon-btn"
              onClick={handleCopy}
              title={copied ? '복사됨!' : '복사'}
            >
              {copied ? <Check size={16} /> : <Copy size={16} />}
              <span>{copied ? '복사됨' : '복사'}</span>
            </button>
            <button
              className="icon-btn"
              onClick={handleReadAloud}
              title={speaking ? '읽기 중지' : '읽어주기'}
            >
              {speaking ? <VolumeX size={16} /> : <Volume2 size={16} />}
              <span>{speaking ? '중지' : '읽어주기'}</span>
            </button>
            <div className="chat-message__rating">
              <button
                className={`icon-btn ${rating === 'up' ? 'icon-btn--active' : ''}`}
                onClick={() => setRating(rating === 'up' ? null : 'up')}
                title="도움이 됐어요"
              >
                <ThumbsUp size={14} />
              </button>
              <button
                className={`icon-btn ${rating === 'down' ? 'icon-btn--active' : ''}`}
                onClick={() => setRating(rating === 'down' ? null : 'down')}
                title="도움이 안 됐어요"
              >
                <ThumbsDown size={14} />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export function ChatMessageSkeleton() {
  return (
    <div className="chat-message chat-message--ai">
      <div className="chat-message__avatar">
        <Bot size={18} />
      </div>
      <div className="chat-message__body">
        <div className="chat-message__loading">
          <div className="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <span>AI가 문서를 분석하고 있습니다...</span>
        </div>
      </div>
    </div>
  );
}
