import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import {
  getCurrentUser,
  loginWithPassword,
} from "../api/authApi";

import { tokenService }
  from "../services/tokenService";

import type { User }
  from "../types/auth";


interface AuthContextType {
  user: User | null;
  loading: boolean;

  loginPassword: (
    email: string,
    password: string
  ) => Promise<void>;

  saveSession: (
    token: string,
    user: User
  ) => void;

  logout: () => void;
}


const AuthContext =
  createContext<AuthContextType | undefined>(
    undefined
  );


interface AuthProviderProps {
  children: ReactNode;
}


export function AuthProvider({
  children,
}: AuthProviderProps) {

  const [user, setUser] =
    useState<User | null>(null);

  const [loading, setLoading] =
    useState(true);


  useEffect(() => {

    async function restoreSession() {

      const token =
        tokenService.get();

      if (!token) {
        setLoading(false);
        return;
      }

      try {

        const currentUser =
          await getCurrentUser();

        setUser(currentUser);

      } catch {

        tokenService.remove();
        setUser(null);

      } finally {

        setLoading(false);

      }
    }

    restoreSession();

  }, []);


  async function loginPassword(
    email: string,
    password: string
  ) {

    const response =
      await loginWithPassword(
        email,
        password
      );

    tokenService.set(
      response.access_token
    );

    setUser(
      response.usuario
    );
  }


  function saveSession(
    token: string,
    authenticatedUser: User
  ) {

    tokenService.set(token);

    setUser(
      authenticatedUser
    );
  }


  function logout() {

    tokenService.remove();

    setUser(null);
  }


  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        loginPassword,
        saveSession,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}


export function useAuth() {

  const context =
    useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth debe utilizarse dentro de AuthProvider"
    );
  }

  return context;
}