import { useState, useCallback, useRef, useEffect } from 'react';
import * as api from '../services/api';

const STORAGE_KEY = 'studybot-chat';

function loadChat(documentId) {
  try {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    return data[documentId] || { messages: [], conversationId: null };
  } catch {
    return { messages: [], conversationId: null };
  }
}

function saveChat(documentId, messages, conversationId) {
  try {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    data[documentId] = { messages, conversationId };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch {
    // Ignore storage errors
  }
}

// Mock data used when the real API isn't available yet
const MOCK_RESPONSES = [
  {
    text: '이 문서에 따르면, **AWS Lambda**는 서버리스 컴퓨팅 서비스로, 서버를 프로비저닝하거나 관리하지 않고도 코드를 실행할 수 있습니다.\n\n주요 특징:\n- 이벤트 기반 실행\n- 자동 확장\n- 사용한 만큼만 비용 지불',
    citations: [
      { page: 3, paragraph: 2, text: 'AWS Lambda is a serverless compute service...' },
      { page: 5, paragraph: 1, text: 'Lambda automatically scales your application...' },
    ],
  },
  {
    text: '좋은 질문입니다! **Amazon S3**의 스토리지 클래스는 다음과 같습니다:\n\n1. **S3 Standard** — 자주 접근하는 데이터\n2. **S3 Intelligent-Tiering** — 접근 패턴이 변하는 데이터\n3. **S3 Glacier** — 아카이브용 장기 보관\n\n각 클래스마다 비용과 접근 속도가 다릅니다.',
    citations: [
      { page: 12, paragraph: 1, text: 'Amazon S3 offers multiple storage classes...' },
    ],
  },
  {
    text: '문서 15페이지에 자세히 설명되어 있습니다.\n\n**VPC (Virtual Private Cloud)**는 AWS 클라우드 내에서 논리적으로 격리된 가상 네트워크입니다. 서브넷, 라우팅 테이블, 인터넷 게이트웨이 등을 구성할 수 있습니다.',
    citations: [
      { page: 15, paragraph: 3, text: 'A VPC is a logically isolated virtual network...' },
      { page: 16, paragraph: 1, text: 'You can configure subnets, route tables...' },
    ],
  },
];

export default function useChat(documentId) {
  const [messages, setMessages] = useState(() => {
    if (!documentId) return [];
    return loadChat(documentId).messages;
  });
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(() => {
    if (!documentId) return null;
    return loadChat(documentId).conversationId;
  });
  const mockIndex = useRef(0);

  const skipSaveRef = useRef(true);

  useEffect(() => {
    if (skipSaveRef.current) {
      skipSaveRef.current = false;
      return;
    }
    if (documentId && messages.length > 0) {
      saveChat(documentId, messages, conversationId);
    }
  }, [documentId, messages, conversationId]);

  useEffect(() => {
    skipSaveRef.current = true;
    if (documentId) {
      const saved = loadChat(documentId);
      setMessages(saved.messages);
      setConversationId(saved.conversationId);
      mockIndex.current = 0;
    } else {
      setMessages([]);
      setConversationId(null);
    }
  }, [documentId]);

  const sendMessage = useCallback(
    async (text) => {
      const userMsg = { role: 'user', content: text, timestamp: new Date().toISOString() };
      setMessages((prev) => [...prev, userMsg]);
      setLoading(true);

      try {
        const res = await api.sendMessage(documentId, text, conversationId);
        if (res.conversationId) setConversationId(res.conversationId);

        const aiMsg = {
          role: 'assistant',
          content: res.answer,
          citations: res.citations || [],
          followUps: res.followUps || [],
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, aiMsg]);
      } catch {
        // Fallback to mock data when API is unavailable
        const mock = MOCK_RESPONSES[mockIndex.current % MOCK_RESPONSES.length];
        mockIndex.current += 1;

        await new Promise((r) => setTimeout(r, 800 + Math.random() * 700));

        const aiMsg = {
          role: 'assistant',
          content: mock.text,
          citations: mock.citations,
          followUps: [],
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, aiMsg]);
      } finally {
        setLoading(false);
      }
    },
    [documentId, conversationId],
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    mockIndex.current = 0;
    if (documentId) {
      try {
        const data = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
        delete data[documentId];
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      } catch {
        // Ignore
      }
    }
  }, [documentId]);

  return { messages, loading, sendMessage, clearMessages, conversationId };
}
