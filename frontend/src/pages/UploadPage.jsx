import { useState, useRef } from 'react';
import { CheckCircle, Loader, Clock } from 'lucide-react';
import FileUpload from '../components/FileUpload';
import { useToast } from '../components/Toast';
import useDocuments from '../hooks/useDocuments';

const PROCESSING_STEPS = [
  { label: 'PDF 텍스트 추출', icon: CheckCircle },
  { label: '텍스트 청크 분할', icon: CheckCircle },
  { label: '임베딩 생성 (Bedrock)', icon: Loader },
  { label: 'Knowledge Base 인덱싱', icon: Clock },
];

export default function UploadPage() {
  const { upload } = useDocuments();
  const toast = useToast();
  const [recentUpload, setRecentUpload] = useState(null);
  const [processingStep, setProcessingStep] = useState(-1);
  const cancelledRef = useRef(false);

  const handleUpload = async (file, onProgress) => {
    cancelledRef.current = false;
    const result = await upload(file, onProgress);
    setRecentUpload(result);
    // Simulate step-functions progress
    for (let i = 0; i < PROCESSING_STEPS.length; i++) {
      if (cancelledRef.current) return;
      setProcessingStep(i);
      await new Promise((r) => setTimeout(r, 1500));
    }
    if (cancelledRef.current) return;
    setProcessingStep(PROCESSING_STEPS.length);
    toast?.('문서 처리가 완료되었습니다! 채팅에서 질문할 수 있습니다.', 'success');
  };

  return (
    <div className="upload-page page">
      <h1 className="page-title">문서 업로드</h1>
      <p className="page-desc">
        PDF 파일을 업로드하면 AI가 내용을 분석하고, 질문에 답하거나 퀴즈를 만들어 드립니다.
      </p>

      <FileUpload onUpload={handleUpload} />

      {/* Processing progress */}
      {recentUpload && processingStep >= 0 && (
        <div className="upload-page__progress card">
          <h3>문서 처리 현황</h3>
          <p className="muted">{recentUpload.name}</p>

          <div className="processing-steps">
            {PROCESSING_STEPS.map((step, i) => {
              let status = 'pending';
              if (i < processingStep) status = 'done';
              else if (i === processingStep && processingStep < PROCESSING_STEPS.length) status = 'active';
              else if (processingStep >= PROCESSING_STEPS.length) status = 'done';

              return (
                <div key={i} className={`processing-step processing-step--${status}`}>
                  <div className="processing-step__icon">
                    {status === 'done' && <CheckCircle size={18} />}
                    {status === 'active' && <Loader size={18} className="spin" />}
                    {status === 'pending' && <Clock size={18} />}
                  </div>
                  <span>{step.label}</span>
                </div>
              );
            })}
          </div>

          {processingStep >= PROCESSING_STEPS.length && (
            <p className="upload-page__done text-green">
              문서 처리가 완료되었습니다! 이제 채팅에서 질문할 수 있습니다.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
