import { useCallback, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { ArrowLeft, Camera, ShieldCheck, UserCheck } from "lucide-react";
import CameraCapture from "../components/CameraCapture";
import { loginWithFace } from "../api/authApi";
import { useAuth } from "../context/AuthContext";
import { Button } from "../components/ui/Button";

export default function FacialLoginPage() {
  const navigate = useNavigate();
  const { saveSession } = useAuth();

  const [dni, setDni] = useState("");
  const [capturing, setCapturing] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("Ingresa tu DNI para comenzar.");

  const handleCameraError = useCallback((message: string) => {
    setError(message);
    setCapturing(false);
    setProcessing(false);
  }, []);

  function startVerification() {
    setError("");
    const cleanDni = dni.trim();

    if (cleanDni.length !== 8 || !/^\d{8}$/.test(cleanDni)) {
      setError("Ingresa un DNI válido de 8 dígitos.");
      return;
    }

    setStatus("Mira a la cámara y mueve ligeramente la cabeza.");
    setCapturing(true);
  }

  const handleFramesCaptured = useCallback(
    async (frames: Blob[]) => {
      setCapturing(false);
      setProcessing(true);
      setError("");
      setStatus("Verificando identidad con IA...");

      try {
        const result = await loginWithFace(dni.trim(), frames);
        saveSession(result.access_token, result.usuario);
        setStatus("Identidad verificada exitosamente.");
        navigate("/dashboard", { replace: true });
      } catch (error) {
        console.error(error);
        if (axios.isAxiosError(error)) {
          const detail = error.response?.data?.detail;
          setError(typeof detail === "string" ? detail : "No se pudo verificar la identidad.");
        } else {
          setError("Ocurrió un error durante la verificación.");
        }
        setStatus("Puedes intentarlo nuevamente.");
      } finally {
        setProcessing(false);
      }
    },
    [dni, navigate, saveSession]
  );

  const busy = capturing || processing;

  return (
    <main className="min-h-screen bg-brand-darkest text-slate-100 p-6 flex flex-col justify-between transition-colors duration-300">
      <div className="max-w-6xl w-full mx-auto animate-fade-in">
        {/* Top Header Navigation */}
        <div className="flex items-center justify-between pb-8">
          <div></div>

          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-brand-teal flex items-center justify-center text-white font-bold text-sm">
              M
            </div>
            <span className="font-bold text-white tracking-tight text-sm">MATRIXFLOW</span>
          </div>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center pt-4">
          <section className="space-y-6">
            <span className="px-3 py-1 bg-brand-mint/15 border border-brand-teal/30 rounded-full text-[11px] font-bold text-brand-mint tracking-wider uppercase inline-flex items-center gap-1.5">
              <ShieldCheck size={14} /> Acceso Biométrico por Rostro
            </span>

            <h1 className="text-4xl lg:text-5xl font-bold tracking-tight text-white leading-tight">
              Inicia sesión con tu rostro en segundos.
            </h1>

            <p className="text-sm text-slate-400 max-w-md leading-relaxed">
              Ingresa tu documento de identidad (DNI) y realiza una verificación facial instantánea segura.
            </p>

            <div className="space-y-4 pt-2">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-brand-dark border border-brand-teal flex items-center justify-center text-brand-mint font-bold text-xs">
                  01
                </div>
                <p className="text-xs font-semibold text-slate-200">Ingresa tu número de DNI</p>
              </div>

              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-brand-dark border border-brand-teal flex items-center justify-center text-brand-mint font-bold text-xs">
                  02
                </div>
                <p className="text-xs font-semibold text-slate-200">Permite la cámara y posiciona tu rostro</p>
              </div>

              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-brand-dark border border-brand-teal flex items-center justify-center text-brand-mint font-bold text-xs">
                  03
                </div>
                <p className="text-xs font-semibold text-slate-200">Verificamos biometría y te redirigimos</p>
              </div>
            </div>
          </section>

          {/* Camera & Form Card */}
          <section className="bg-brand-darker border border-brand-dark rounded-2xl p-6 shadow-2xl relative">
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Número de DNI
                </label>
                <input
                  type="text"
                  inputMode="numeric"
                  maxLength={8}
                  placeholder="Ingresa 8 dígitos"
                  value={dni}
                  disabled={busy}
                  onChange={(e) => {
                    const value = e.target.value.replace(/\D/g, "").slice(0, 8);
                    setDni(value);
                  }}
                  className="w-full px-4 py-2.5 bg-brand-dark/60 border border-brand-dark rounded-lg text-sm font-semibold text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-brand-teal tracking-widest"
                />
              </div>

              <CameraCapture
                capturing={capturing}
                totalFrames={3}
                captureInterval={700}
                onFramesCaptured={handleFramesCaptured}
                onError={handleCameraError}
              />

              <div className="flex items-center gap-2 p-3 bg-brand-dark/50 border border-brand-dark rounded-lg text-xs text-slate-300">
                {processing && <div className="w-4 h-4 border-2 border-brand-mint border-t-transparent rounded-full animate-spin"></div>}
                <span>{status}</span>
              </div>

              {error && (
                <div className="p-3 bg-red-950/60 border border-red-800 rounded-lg text-xs text-red-300">
                  {error}
                </div>
              )}

              <Button
                type="button"
                variant="accent"
                className="w-full py-3"
                disabled={busy}
                onClick={startVerification}
              >
                <UserCheck size={16} />
                <span>
                  {capturing
                    ? "Capturando rostro..."
                    : processing
                    ? "Verificando identidad..."
                    : "Verificar mi identidad"}
                </span>
              </Button>

              <p className="text-[11px] text-center text-slate-500 pt-1">
                La cámara se utiliza únicamente durante el proceso de validación biométrica.
              </p>
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}