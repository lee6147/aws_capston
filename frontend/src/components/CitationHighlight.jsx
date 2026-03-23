import { useState } from 'react';
import { FileText, ChevronLeft, ChevronRight, X } from 'lucide-react';

/**
 * PDF citation viewer panel.
 * Uses a simple placeholder when react-pdf isn't configured with a worker.
 * When the backend serves real PDF URLs, swap in <Document>/<Page> from react-pdf.
 */
export default function CitationHighlight({ citation, onClose }) {
  const [currentPage, setCurrentPage] = useState(citation?.page || 1);

  if (!citation) {
    return (
      <div className="citation-panel citation-panel--empty">
        <FileText size={48} strokeWidth={1} />
        <p>인용을 클릭하면 해당 페이지가 여기에 표시됩니다</p>
      </div>
    );
  }

  return (
    <div className="citation-panel">
      <div className="citation-panel__header">
        <span className="citation-panel__title">
          PDF 뷰어 — {currentPage}페이지
        </span>
        <button className="icon-btn" onClick={onClose} title="닫기">
          <X size={16} />
        </button>
      </div>

      {/* Simulated PDF page */}
      <div className="citation-panel__page">
        <div className="citation-panel__placeholder">
          <FileText size={64} strokeWidth={0.8} />
          <h3>{currentPage}페이지</h3>
          {citation.text && (
            <blockquote className="citation-panel__excerpt">
              "{citation.text}"
            </blockquote>
          )}
          <p className="citation-panel__hint">
            실제 PDF가 연결되면 해당 페이지가 렌더링됩니다
          </p>
        </div>
      </div>

      {/* Page controls */}
      <div className="citation-panel__controls">
        <button
          className="icon-btn"
          disabled={currentPage <= 1}
          onClick={() => setCurrentPage((p) => p - 1)}
        >
          <ChevronLeft size={18} />
        </button>
        <span>{currentPage}페이지</span>
        <button className="icon-btn" onClick={() => setCurrentPage((p) => p + 1)}>
          <ChevronRight size={18} />
        </button>
      </div>
    </div>
  );
}
