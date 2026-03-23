import { useNavigate } from 'react-router-dom';
import { Upload, FileUp } from 'lucide-react';
import useDocuments from '../hooks/useDocuments';
import DocumentCard from '../components/DocumentCard';
import LoadingSpinner from '../components/LoadingSpinner';

export default function DocumentsPage() {
  const navigate = useNavigate();
  const { documents, loading, remove } = useDocuments();

  const handleDelete = (id) => {
    if (window.confirm('이 문서를 삭제하시겠습니까?')) {
      remove(id);
    }
  };

  return (
    <div className="documents-page page">
      <div className="section-header">
        <h1 className="page-title">내 문서</h1>
        <button className="btn btn--primary" onClick={() => navigate('/upload')}>
          <Upload size={16} /> 업로드
        </button>
      </div>
      <p className="page-desc">업로드한 PDF 문서 목록입니다.</p>

      {loading ? (
        <div className="center-block">
          <LoadingSpinner size={36} />
          <p className="muted">문서를 불러오는 중...</p>
        </div>
      ) : documents.length === 0 ? (
        <div className="center-block" style={{ padding: '3rem 1rem', textAlign: 'center' }}>
          <FileUp size={48} style={{ color: 'var(--text-muted)', marginBottom: '1rem' }} />
          <h3 style={{ marginBottom: '0.5rem' }}>아직 업로드한 문서가 없습니다</h3>
          <p className="muted" style={{ marginBottom: '1.5rem' }}>
            PDF 파일을 업로드하면 AI가 문서 내용을 분석하고,<br />
            질문에 답하거나 퀴즈를 만들어 드립니다.
          </p>
          <button className="btn btn--primary" onClick={() => navigate('/upload')}>
            <Upload size={16} /> PDF 업로드하기
          </button>
        </div>
      ) : (
        <div className="document-list">
          {documents.map((doc) => (
            <DocumentCard key={doc.id} doc={doc} onDelete={handleDelete} />
          ))}
        </div>
      )}
    </div>
  );
}
