import {
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import LoginPage
  from "./pages/LoginPage";

import FacialLoginPage
  from "./pages/FacialLoginPage";

import RegisterPage
  from "./pages/RegisterPage";

import DashboardPage
  from "./pages/DashboardPage";

import ProtectedRoute
  from "./components/ProtectedRoute";


export default function App() {

  return (
    <Routes>

      <Route
        path="/"
        element={
          <Navigate
            to="/login"
            replace
          />
        }
      />

      <Route
        path="/login"
        element={<LoginPage />}
      />

      <Route
        path="/login/facial"
        element={<FacialLoginPage />}
      />

      <Route
        path="/registro"
        element={<RegisterPage />}
      />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="*"
        element={
          <Navigate
            to="/login"
            replace
          />
        }
      />

    </Routes>
  );
}