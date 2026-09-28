<<<<<<< HEAD
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, Mail, ArrowRight, ShieldCheck } from 'lucide-react';
import { Button } from '../components/ui/Button';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = React.useState('admin@matrixflow.com');
  const [password, setPassword] = React.useState('••••••••');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    localStorage.setItem('matrixflow_token', 'mock_jwt_token_123');
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl p-8 border border-slate-800/20">
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-primary to-accent mx-auto flex items-center justify-center text-white font-black text-2xl shadow-lg shadow-primary/30 mb-3">
            M
          </div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">MATRIXFLOW ENTERPRISE</h2>
          <p className="text-xs text-slate-500 mt-1">Plataforma Empresarial de Análisis por Álgebra Lineal</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Correo Electrónico</label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs font-medium text-slate-800 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Contraseña</label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs font-medium text-slate-800 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
              />
            </div>
          </div>

          <div className="flex items-center justify-between text-xs pt-1">
            <label className="flex items-center gap-2 text-slate-600">
              <input type="checkbox" defaultChecked className="rounded border-slate-300 text-primary" />
              <span>Recordar sesión</span>
            </label>
            <a href="#" className="text-primary hover:underline font-medium">¿Olvidaste tu clave?</a>
          </div>

          <Button type="submit" variant="primary" className="w-full py-2.5 mt-2">
            <span>Iniciar Sesión en el Sistema</span>
            <ArrowRight size={16} />
          </Button>
        </form>

        <div className="mt-8 pt-4 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
          <div className="flex items-center gap-1.5">
            <ShieldCheck size={14} className="text-accent" />
            <span>JWT + RBAC Security</span>
          </div>
          <span>Versión 1.0</span>
        </div>
      </div>
    </div>
  );
};
=======
import {
  useState,
  type FormEvent,
} from "react";

import { Link, useNavigate }
  from "react-router-dom";

import axios from "axios";

import { useAuth }
  from "../context/AuthContext";


export default function LoginPage() {

  const navigate =
    useNavigate();

  const {
    loginPassword,
  } = useAuth();


  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [error, setError] =
    useState("");

  const [loading, setLoading] =
    useState(false);


  async function handleSubmit(
    event: FormEvent
  ) {

    event.preventDefault();

    setError("");
    setLoading(true);

    try {

      await loginPassword(
        email,
        password
      );

      navigate(
        "/dashboard",
        {
          replace: true,
        }
      );

    } catch (error) {

      if (axios.isAxiosError(error)) {

        setError(
          error.response?.data?.detail ||
          "No se pudo iniciar sesión."
        );

      } else {

        setError(
          "Ocurrió un error inesperado."
        );

      }

    } finally {

      setLoading(false);

    }
  }


  return (
    <main className="auth-page">

      <section className="auth-brand">

        <div className="brand-content">

          <span className="brand-badge">
            MatrixFlow
          </span>

          <h1>
            Gestiona tu empresa
            desde un solo lugar.
          </h1>

          <p>
            Plataforma empresarial para
            operaciones, análisis,
            cotizaciones e inventario.
          </p>

        </div>

      </section>


      <section className="auth-panel">

        <div className="login-card">

          <div className="mobile-logo">
            MatrixFlow
          </div>

          <p className="eyebrow">
            BIENVENIDO
          </p>

          <h2>
            Iniciar sesión
          </h2>

          <p className="subtitle">
            Accede a tu cuenta para
            continuar.
          </p>


          <form
            onSubmit={handleSubmit}
            className="login-form"
          >

            <label>
              Correo electrónico

              <input
                type="email"
                placeholder="nombre@empresa.com"
                value={email}
                onChange={(event) =>
                  setEmail(
                    event.target.value
                  )
                }
                autoComplete="email"
                required
              />
            </label>


            <label>
              Contraseña

              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(event) =>
                  setPassword(
                    event.target.value
                  )
                }
                autoComplete="current-password"
                required
              />
            </label>


            {error && (
              <div
                className="error-message"
                role="alert"
              >
                {error}
              </div>
            )}


            <button
              type="submit"
              className="primary-button"
              disabled={loading}
            >
              {loading
                ? "Ingresando..."
                : "Iniciar sesión"}
            </button>

          </form>


          <div className="separator">
            <span>
              o continúa con
            </span>
          </div>


          <Link
            to="/login/facial"
            className="face-button"
          >
            <span className="face-icon">
              ◉
            </span>

            Iniciar sesión con rostro
          </Link>


          <p className="register-link">
            ¿No tienes una cuenta?{" "}

            <Link to="/registro">
              Crear cuenta
            </Link>
          </p>

        </div>

      </section>

    </main>
  );
}
>>>>>>> 87884f86cb2298dcd4e88163aca4349d473a1149
