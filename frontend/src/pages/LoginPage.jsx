import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import { Bot } from 'lucide-react';

const formFields = {
  signUp: {
    email: { label: '이메일', placeholder: 'you@example.com', order: 1 },
    password: { label: '비밀번호', placeholder: '비밀번호를 입력하세요', order: 2 },
    confirm_password: { label: '비밀번호 확인', placeholder: '비밀번호를 다시 입력하세요', order: 3 },
  },
};

export default function LoginPage({ onAuth }) {
  return (
    <div className="login-page">
      <div className="login-page__brand">
        <Bot size={48} />
        <h1>StudyBot Enhanced</h1>
        <p>AI 기반 학습 도우미</p>
      </div>

      <Authenticator formFields={formFields} variation="modal">
        {({ signOut, user }) => {
          // Once authenticated, notify parent
          if (user) {
            onAuth?.(user);
          }
          return null;
        }}
      </Authenticator>
    </div>
  );
}
