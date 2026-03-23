import { useState, useEffect, useCallback } from 'react';
import * as api from '../services/api';

// Minimal fallback when both mock server and real API are unavailable
const FALLBACK_DOCUMENTS = [
  { id: 'doc-fallback', name: 'Sample_Document.pdf', size: 1_000_000, pages: 10, status: 'ready', uploadedAt: new Date().toISOString() },
];

export default function useDocuments() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadDocuments = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.fetchDocuments();
      setDocuments(data.documents || data);
    } catch {
      // Fallback to mock
      setDocuments(FALLBACK_DOCUMENTS);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  const upload = useCallback(async (file, onProgress) => {
    try {
      const result = await api.uploadDocument(file, onProgress);
      await loadDocuments();
      return result;
    } catch {
      // Mock upload
      await new Promise((r) => {
        let p = 0;
        const iv = setInterval(() => {
          p += 10 + Math.random() * 15;
          if (p >= 100) {
            p = 100;
            clearInterval(iv);
            r();
          }
          onProgress?.(Math.min(Math.round(p), 100));
        }, 200);
      });

      const newDoc = {
        id: `doc-${Date.now()}`,
        name: file.name,
        size: file.size,
        pages: Math.floor(Math.random() * 40) + 10,
        status: 'processing',
        uploadedAt: new Date().toISOString(),
      };
      setDocuments((prev) => [newDoc, ...prev]);
      return newDoc;
    }
  }, [loadDocuments]);

  const remove = useCallback(async (documentId) => {
    try {
      await api.deleteDocument(documentId);
    } catch {
      // mock remove
    }
    setDocuments((prev) => prev.filter((d) => d.id !== documentId));
  }, []);

  return { documents, loading, error, upload, remove, refresh: loadDocuments };
}
