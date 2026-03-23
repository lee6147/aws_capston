import { useState, useEffect, useCallback, createContext, useContext } from 'react';
import { fetchAuthSession, signOut as amplifySignOut, getCurrentUser } from 'aws-amplify/auth';
import { setAuthTokenProvider } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadUser = useCallback(async () => {
    try {
      const currentUser = await getCurrentUser();
      setUser(currentUser);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  // Wire up the API auth-token provider
  useEffect(() => {
    setAuthTokenProvider(async () => {
      try {
        const session = await fetchAuthSession();
        return session.tokens?.idToken?.toString() ?? null;
      } catch {
        return null;
      }
    });
  }, []);

  const signOut = useCallback(async () => {
    await amplifySignOut();
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, signOut, refreshUser: loadUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export default function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
}
