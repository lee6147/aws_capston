export default function LoadingSpinner({ size = 24, className = '' }) {
  return (
    <div
      className={`loading-spinner ${className}`}
      style={{ width: size, height: size }}
      role="status"
      aria-label="로딩 중"
    >
      <svg viewBox="0 0 24 24" fill="none" style={{ width: '100%', height: '100%' }}>
        <circle
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="3"
          strokeLinecap="round"
          opacity="0.25"
        />
        <path
          d="M12 2a10 10 0 0 1 10 10"
          stroke="currentColor"
          strokeWidth="3"
          strokeLinecap="round"
          className="spinner-arc"
        />
      </svg>
    </div>
  );
}
