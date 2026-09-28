import type { ReactNode }
  from "react";

import { Navigate }
  from "react-router-dom";

import { useAuth }
  from "../context/AuthContext";


interface Props {
  children: ReactNode;
}


export default function ProtectedRoute({
  children,
}: Props) {

  const {
    user,
    loading,
  } = useAuth();


  if (loading) {
    return (
      <div className="center-screen">
        <div className="loader" />

        <p>
          Verificando sesión...
        </p>
      </div>
    );
  }


  if (!user) {
    return (
      <Navigate
        to="/login"
        replace
      />
    );
  }


  return <>{children}</>;
}