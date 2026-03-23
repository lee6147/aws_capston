const awsConfig = {
  Auth: {
    Cognito: {
      userPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID || 'ap-northeast-2_PLACEHOLDER',
      userPoolClientId: import.meta.env.VITE_COGNITO_CLIENT_ID || 'placeholder_client_id',
      loginWith: {
        email: true,
      },
    },
  },
  API: {
    REST: {
      StudyBotAPI: {
        endpoint: import.meta.env.VITE_API_URL || 'http://localhost:3001/api',
      },
    },
  },
};

export default awsConfig;
