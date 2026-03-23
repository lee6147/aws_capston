import { useState, useRef, useCallback } from 'react';
import { Upload, File, CheckCircle, AlertCircle } from 'lucide-react';

const MAX_SIZE = 10 * 1024 * 1024; // 10 MB

export default function FileUpload({ onUpload }) {
  const [dragOver, setDragOver] = useState(false);
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(null); // null | 0-100 | 'done' | 'error'
  const [errorMsg, setErrorMsg] = useState('');
  const inputRef = useRef();

  const validate = (f) => {
    if (!f) return false;
    if (f.type !== 'application/pdf') {
      setErrorMsg('PDF 파일만 업로드할 수 있습니다.');
      return false;
    }
    if (f.size > MAX_SIZE) {
      setErrorMsg('파일 크기는 10MB 이하여야 합니다.');
      return false;
    }
    setErrorMsg('');
    return true;
  };

  const handleFile = useCallback(
    async (f) => {
      if (!validate(f)) return;
      setFile(f);
      setProgress(0);
      try {
        await onUpload(f, (p) => setProgress(p));
        setProgress('done');
      } catch (err) {
        setErrorMsg(err.message || '업로드 실패');
        setProgress('error');
      }
    },
    [onUpload],
  );

  const onDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const f = e.dataTransfer.files?.[0];
    handleFile(f);
  };

  const reset = () => {
    setFile(null);
    setProgress(null);
    setErrorMsg('');
  };

  return (
    <div className="file-upload-wrapper">
      <div
        className={`file-upload ${dragOver ? 'file-upload--drag' : ''} ${progress === 'error' ? 'file-upload--error' : ''}`}
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        onClick={() => !file && inputRef.current?.click()}
        role="button"
        tabIndex={0}
      >
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          hidden
          onChange={(e) => handleFile(e.target.files?.[0])}
        />

        {!file && (
          <>
            <Upload size={48} strokeWidth={1.2} className="file-upload__icon" />
            <p className="file-upload__text">PDF 파일을 드래그하거나 클릭하여 업로드하세요</p>
            <p className="file-upload__hint">최대 10MB</p>
          </>
        )}

        {file && progress !== null && progress !== 'done' && progress !== 'error' && (
          <div className="file-upload__progress">
            <File size={32} />
            <p className="file-upload__filename">{file.name}</p>
            <div className="progress-bar">
              <div className="progress-bar__fill" style={{ width: `${progress}%` }} />
            </div>
            <span className="file-upload__percent">{progress}%</span>
          </div>
        )}

        {progress === 'done' && (
          <div className="file-upload__done">
            <CheckCircle size={48} className="text-green" />
            <p>{file.name}</p>
            <p className="file-upload__hint">업로드 완료! 문서 처리가 시작되었습니다.</p>
            <button className="btn btn--outline" onClick={(e) => { e.stopPropagation(); reset(); }}>
              다른 파일 업로드
            </button>
          </div>
        )}

        {progress === 'error' && (
          <div className="file-upload__done">
            <AlertCircle size={48} className="text-red" />
            <p>{errorMsg}</p>
            <button className="btn btn--outline" onClick={(e) => { e.stopPropagation(); reset(); }}>
              다시 시도
            </button>
          </div>
        )}
      </div>

      {errorMsg && progress !== 'error' && (
        <p className="file-upload__error">{errorMsg}</p>
      )}
    </div>
  );
}
