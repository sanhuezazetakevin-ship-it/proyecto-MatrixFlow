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