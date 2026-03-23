const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

let getAuthToken = () => Promise.resolve(null);

export function setAuthTokenProvider(fn) {
  getAuthToken = fn;
}

async function request(path, options = {}) {
  const token = await getAuthToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.message || `API Error ${res.status}`);
  }

  return res.json();
}

// ── Documents ──────────────────────────────────────────────
export async function fetchDocuments() {
  return request('/documents');
}

export async function uploadDocument(file, onProgress) {
  // Step 1: get presigned URL
  const { uploadUrl, documentId } = await request('/documents/upload', {
    method: 'POST',
    body: JSON.stringify({ fileName: file.name, fileType: file.type }),
  });

  // Step 2: upload to S3 via presigned URL
  await new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('PUT', uploadUrl);
    xhr.setRequestHeader('Content-Type', file.type);
    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable && onProgress) {
        onProgress(Math.round((e.loaded / e.total) * 100));
      }
    };
    xhr.onload = () => (xhr.status < 400 ? resolve() : reject(new Error('Upload failed')));
    xhr.onerror = () => reject(new Error('Upload failed'));
    xhr.send(file);
  });

  // Step 3: confirm upload
  return request(`/documents/${documentId}/confirm`, { method: 'POST' });
}

export async function deleteDocument(documentId) {
  return request(`/documents/${documentId}`, { method: 'DELETE' });
}

export async function getDocumentStatus(documentId) {
  return request(`/documents/${documentId}/status`);
}

// ── Chat ───────────────────────────────────────────────────
export async function sendMessage(documentId, message, conversationId) {
  return request('/chat', {
    method: 'POST',
    body: JSON.stringify({ documentId, message, conversationId }),
  });
}

export async function getChatHistory(conversationId) {
  return request(`/chat/${conversationId}/history`);
}

// ── Quiz ───────────────────────────────────────────────────
export async function generateQuiz(documentId, conversationId) {
  return request('/quiz/generate', {
    method: 'POST',
    body: JSON.stringify({ documentId, conversationId }),
  });
}

export async function submitQuizAnswer(quizId, questionIndex, answer) {
  return request('/quiz/answer', {
    method: 'POST',
    body: JSON.stringify({ quizId, questionIndex, answer }),
  });
}

// ── Dashboard stats ────────────────────────────────────────
export async function fetchDashboardStats() {
  return request('/dashboard/stats');
}

// ── Text-to-speech (Polly) ─────────────────────────────────
export async function synthesizeSpeech(text) {
  return request('/tts', {
    method: 'POST',
    body: JSON.stringify({ text }),
  });
}
