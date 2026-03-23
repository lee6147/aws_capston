import { FileText, Trash2, MessageSquare, Loader } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
}

export default function DocumentCard({ doc, onDelete }) {
  const navigate = useNavigate();
  const isReady = doc.status === 'ready';

  return (
    <div className="document-card card">
      <div className="document-card__icon">
        <FileText size={28} />
      </div>

      <div className="document-card__info">
        <h4 className="document-card__name" title={doc.name}>{doc.name}</h4>
        <div className="document-card__meta">
          <span>{formatSize(doc.size)}</span>
          {doc.pages && <span>{doc.pages}페이지</span>}
          <span>{formatDate(doc.uploadedAt)}</span>
        </div>
        {!isReady && (
          <div className="document-card__status">
            <Loader size={14} className="spin" />
            <span>처리 중...</span>
          </div>
        )}
      </div>

      <div className="document-card__actions">
        <button
          className="icon-btn"
          disabled={!isReady}
          onClick={() => navigate(`/chat?doc=${doc.id}`)}
          title="채팅 시작"
        >
          <MessageSquare size={18} />
        </button>
        <button
          className="icon-btn icon-btn--danger"
          onClick={() => onDelete?.(doc.id)}
          title="삭제"
        >
          <Trash2 size={18} />
        </button>
      </div>
    </div>
  );
}
