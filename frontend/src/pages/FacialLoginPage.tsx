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

import { loginWithFace }
  from "../api/authApi";

import { useAuth }
  from "../context/AuthContext";


export default function FacialLoginPage() {

  const navigate =
    useNavigate();

  const {
    saveSession,
  } = useAuth();


  const [dni, setDni] =
    useState("");

  const [capturing, setCapturing] =
    useState(false);

  const [processing, setProcessing] =
    useState(false);

  const [error, setError] =
    useState("");

  const [status, setStatus] =
    useState(
      "Ingresa tu DNI para comenzar."
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
  // COMENZAR VERIFICACIÓN
  // ========================================================

  function startVerification() {

    setError("");


    const cleanDni =
      dni.trim();


    if (
      cleanDni.length !== 8 ||
      !/^\d{8}$/.test(cleanDni)
    ) {

      setError(
        "Ingresa un DNI válido de 8 dígitos."
      );

      return;
    }


    setStatus(
      "Mira a la cámara y mueve ligeramente la cabeza."
    );

    setCapturing(true);
  }


  // ========================================================
  // FRAMES CAPTURADOS
  // ========================================================

  const handleFramesCaptured =
    useCallback(
      async (frames: Blob[]) => {

        setCapturing(false);
        setProcessing(true);
        setError("");

        setStatus(
          "Verificando identidad..."
        );


        try {

          const result =
            await loginWithFace(
              dni.trim(),
              frames
            );


          saveSession(
            result.access_token,
            result.usuario
          );


          setStatus(
            "Identidad verificada."
          );


          navigate(
            "/dashboard",
            {
              replace: true,
            }
          );

        } catch (error) {

          console.error(error);


          if (axios.isAxiosError(error)) {

            const detail =
              error.response
                ?.data
                ?.detail;


            setError(
              typeof detail === "string"
                ? detail
                : "No se pudo verificar la identidad."
            );

          } else {

            setError(
              "Ocurrió un error durante la verificación."
            );

          }


          setStatus(
            "Puedes intentarlo nuevamente."
          );

        } finally {

          setProcessing(false);

        }

      },
      [
        dni,
        navigate,
        saveSession,
      ]
    );


  const busy =
    capturing || processing;


  return (
    <main className="facial-page">

      <div className="facial-container">

        <div className="facial-header">

          <Link
            to="/login"
            className="back-link"
          >
            ← Volver
          </Link>


          <div className="facial-brand">
            MatrixFlow
          </div>

        </div>


        <div className="facial-grid">

          <section className="facial-info">

            <p className="eyebrow">
              ACCESO BIOMÉTRICO
            </p>

            <h1>
              Inicia sesión
              con tu rostro.
            </h1>

            <p className="facial-description">
              Introduce tu DNI y realiza una
              breve verificación frente a la
              cámara.
            </p>


            <div className="facial-steps">

              <div>
                <span>01</span>

                <p>
                  Ingresa tu DNI
                </p>
              </div>


              <div>
                <span>02</span>

                <p>
                  Mira a la cámara
                </p>
              </div>


              <div>
                <span>03</span>

                <p>
                  Verificamos tu identidad
                </p>
              </div>

            </div>

          </section>


          <section className="facial-card">

            <label
              className="dni-field"
            >
              DNI

              <input
                type="text"
                inputMode="numeric"
                maxLength={8}
                placeholder="Ingresa 8 dígitos"
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


            <CameraCapture
  capturing={capturing}
  totalFrames={5}
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
              className="primary-button facial-submit"
              disabled={busy}
              onClick={
                startVerification
              }
            >
              {capturing
                ? "Capturando..."
                : processing
                ? "Verificando..."
                : "Verificar mi identidad"}
            </button>


            <p className="privacy-note">
              La cámara se utiliza únicamente
              durante el proceso de
              verificación.
            </p>

          </section>

        </div>

      </div>

    </main>
  );
}