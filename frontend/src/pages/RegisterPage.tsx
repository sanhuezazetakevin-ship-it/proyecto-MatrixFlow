import {
  useCallback,
  useState,
} from "react";

import {
  Link,
  useNavigate,
} from "react-router-dom";

import axios from "axios";

import CameraCapture
  from "../components/CameraCapture";

import { registerWithFace }
  from "../api/authApi";

import { useAuth }
  from "../context/AuthContext";

export default function RegisterPage() {

  const navigate =
    useNavigate();

  const {
    saveSession,
  } = useAuth();

  const [dni, setDni] =
    useState("");

  const [nombre, setNombre] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [
    confirmPassword,
    setConfirmPassword,
  ] = useState("");

  const [capturing, setCapturing] =
    useState(false);

  const [processing, setProcessing] =
    useState(false);

  const [error, setError] =
    useState("");

  const [status, setStatus] =
    useState(
      "Completa tus datos para continuar."
    );

  // ========================================================
  // ERROR DE CÁMARA
  // ========================================================

  const handleCameraError =
    useCallback(
      (message: string) => {

        setError(message);
        setCapturing(false);
        setProcessing(false);

      },
      []
    );

  // ========================================================
  // VALIDAR FORMULARIO
  // ========================================================

  function validateForm():
  boolean {

    setError("");

    const cleanDni =
      dni.trim();

    const cleanName =
      nombre.trim();

    const cleanEmail =
      email.trim();

    if (
      cleanDni.length !== 8 ||
      !/^\d{8}$/.test(cleanDni)
    ) {

      setError(
        "Ingresa un DNI válido de 8 dígitos."
      );

      return false;
    }

    if (cleanName.length < 3) {

      setError(
        "Ingresa tu nombre completo."
      );

      return false;
    }

    if (!cleanEmail) {

      setError(
        "Ingresa tu correo electrónico."
      );

      return false;
    }

    if (password.length < 8) {

      setError(
        "La contraseña debe tener al menos 8 caracteres."
      );

      return false;
    }

    if (
      password !==
      confirmPassword
    ) {

      setError(
        "Las contraseñas no coinciden."
      );

      return false;
    }

    return true;
  }

  // ========================================================
  // INICIAR REGISTRO FACIAL
  // ========================================================

  function startRegistration() {

    if (!validateForm()) {
      return;
    }

    setStatus(
      "Mira a la cámara mientras realizamos las capturas."
    );

    setCapturing(true);
  }

  // ========================================================
  // CAPTURAS TERMINADAS
  // ========================================================

  const handleFramesCaptured =
    useCallback(
      async (frames: Blob[]) => {

        setCapturing(false);
        setProcessing(true);
        setError("");

        setStatus(
          "Creando tu cuenta y registrando tu rostro..."
        );

        try {

          const result =
            await registerWithFace(
              dni.trim(),
              nombre.trim(),
              email.trim().toLowerCase(),
              password,
              frames
            );

          saveSession(
            result.access_token,
            result.usuario
          );

          setStatus(
            "Registro completado correctamente."
          );

          navigate(
            "/dashboard",
            {
              replace: true,
            }
          );

        } catch (error) {

          console.error(error);

          if (
            axios.isAxiosError(error)
          ) {

            const detail =
              error.response
                ?.data
                ?.detail;

            setError(
              typeof detail === "string"
                ? detail
                : "No se pudo completar el registro."
            );

          } else {

            setError(
              "Ocurrió un error durante el registro."
            );

          }

          setStatus(
            "Puedes corregir los datos e intentarlo nuevamente."
          );

        } finally {

          setProcessing(false);

        }

      },
      [
        dni,
        nombre,
        email,
        password,
        navigate,
        saveSession,
      ]
    );

  const busy =
    capturing || processing;

  return (
    <main className="register-page">

      <div className="register-container">

        <header className="register-header">

          <Link
            to="/login"
            className="back-link"
          >
            ← Volver
          </Link>

          <div className="facial-brand">
            MatrixFlow
          </div>

        </header>

        <div className="register-grid">

          {/* ===============================================
              FORMULARIO
              =============================================== */}

          <section className="register-form-section">

            <p className="eyebrow">
              CREAR CUENTA
            </p>

            <h1>
              Comienza con
              MatrixFlow.
            </h1>

            <p className="register-description">
              Registra tus datos y tu rostro
              para habilitar el acceso facial.
            </p>

            <div className="register-form">

              <label>
                DNI

                <input
                  type="text"
                  inputMode="numeric"
                  maxLength={8}
                  placeholder="8 dígitos"
                  value={dni}
                  disabled={busy}
                  onChange={(event) => {

                    const value =
                      event.target.value
                        .replace(
                          /\D/g,
                          ""
                        )
                        .slice(
                          0,
                          8
                        );

                    setDni(value);

                  }}
                />

              </label>

              <label>
                Nombre completo

                <input
                  type="text"
                  placeholder="Nombre y apellidos"
                  value={nombre}
                  disabled={busy}
                  onChange={(event) =>
                    setNombre(
                      event.target.value
                    )
                  }
                />

              </label>

              <label>
                Correo electrónico

                <input
                  type="email"
                  placeholder="nombre@correo.com"
                  value={email}
                  disabled={busy}
                  onChange={(event) =>
                    setEmail(
                      event.target.value
                    )
                  }
                />

              </label>

              <div className="password-grid">

                <label>
                  Contraseña

                  <input
                    type="password"
                    placeholder="Mínimo 8 caracteres"
                    value={password}
                    disabled={busy}
                    onChange={(event) =>
                      setPassword(
                        event.target.value
                      )
                    }
                  />

                </label>

                <label>
                  Confirmar contraseña

                  <input
                    type="password"
                    placeholder="Repite la contraseña"
                    value={
                      confirmPassword
                    }
                    disabled={busy}
                    onChange={(event) =>
                      setConfirmPassword(
                        event.target.value
                      )
                    }
                  />

                </label>

              </div>

            </div>

          </section>

          {/* ===============================================
              CÁMARA
              =============================================== */}

          <section className="register-camera-card">

            <div className="register-camera-title">

              <div>
                <p className="eyebrow">
                  IDENTIDAD FACIAL
                </p>

                <h2>
                  Registra tu rostro
                </h2>
              </div>

              <span className="camera-status-badge">
                3 capturas
              </span>

            </div>

            <CameraCapture
              capturing={capturing}
              totalFrames={3}
              captureInterval={700}
              onFramesCaptured={
                handleFramesCaptured
              }
              onError={
                handleCameraError
              }
            />

            <div className="verification-status">

              {processing && (
                <div
                  className="small-loader"
                />
              )}

              <span>
                {status}
              </span>

            </div>

            {error && (
              <div
                className="error-message"
                role="alert"
              >
                {error}
              </div>
            )}

            <button
              type="button"
              className="primary-button register-submit"
              disabled={busy}
              onClick={
                startRegistration
              }
            >

              {capturing
                ? "Capturando rostro..."
                : processing
                ? "Creando cuenta..."
                : "Crear cuenta y registrar rostro"}

            </button>

            <p className="privacy-note">
              Tus capturas se procesan para
              generar la representación
              biométrica utilizada por el
              sistema de autenticación.
            </p>

          </section>

        </div>

      </div>

    </main>
  );
}