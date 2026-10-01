import { useCallback, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { ArrowLeft, UserPlus, ShieldCheck } from "lucide-react";
import CameraCapture from "../components/CameraCapture";
import { registerWithFace } from "../api/authApi";
import { useAuth } from "../context/AuthContext";
import { Button } from "../components/ui/Button";

export default function RegisterPage() {
  const navigate = useNavigate();
  const { saveSession } = useAuth();

  const [dni, setDni] = useState("");
  const [nombre, setNombre] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [capturing, setCapturing] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("Completa tus datos para continuar.");

  const handleCameraError = useCallback((message: string) => {
    setError(message);
    setCapturing(false);
    setProcessing(false);
  }, []);

  function validateForm(): boolean {
    setError("");
    const cleanDni = dni.trim();
    const cleanName = nombre.trim();
    const cleanEmail = email.trim();

    if (cleanDni.length !== 8 || !/^\d{8}$/.test(cleanDni)) {
      setError("Ingresa un DNI válido de 8 dígitos.");
      return false;
    }

    if (cleanName.length < 3) {
      setError("Ingresa tu nombre completo.");
      return false;
    }

    if (!cleanEmail) {
      setError("Ingresa tu correo electrónico.");
      return false;
    }

    if (password.length < 8) {
      setError("La contraseña debe tener al menos 8 caracteres.");
      return false;
    }

    if (password !== confirmPassword) {
      setError("Las contraseñas no coinciden.");
      return false;
    }

    return true;
  }

  function startRegistration() {
    if (!validateForm()) {
      return;
    }

    setStatus("Mira a la cámara mientras realizamos las capturas.");
    setCapturing(true);
  }

  const handleFramesCaptured = useCallback(
    async (frames: Blob[]) => {
      setCapturing(false);
      setProcessing(true);
      setError("");
      setStatus("Creando tu cuenta y registrando tu rostro...");

      try {
        const result = await registerWithFace(
          dni.trim(),
          nombre.trim(),
          email.trim().toLowerCase(),
          password,
          frames
        );

        saveSession(result.access_token, result.usuario);
        setStatus("Registro completado correctamente.");
        navigate("/dashboard", { replace: true });
      } catch (error) {
        console.error(error);
        if (axios.isAxiosError(error)) {
          const detail = error.response?.data?.detail;
          setError(typeof detail === "string" ? detail : "No se pudo completar el registro.");
        } else {
          setError("Ocurrió un error durante el registro.");
        }
        setStatus("Puedes corregir los datos e intentarlo nuevamente.");
      } finally {
        setProcessing(false);
      }
    },
    [dni, nombre, email, password, navigate, saveSession]
  );

  const busy = capturing || processing;

  return (
    <main className="min-h-screen bg-brand-darkest text-slate-100 p-6 flex flex-col justify-between transition-colors duration-300">
      <div className="max-w-6xl w-full mx-auto animate-fade-in">
        {/* Header */}
        <div className="flex items-center justify-between pb-8">
          <Link
            to="/login"
            className="flex items-center gap-2 text-xs font-semibold text-brand-mint hover:text-white transition-colors"
          >
            <ArrowLeft size={16} />
            <span>Volver al Login</span>
          </Link>

          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-brand-teal flex items-center justify-center text-white font-bold text-sm">
              M
            </div>
            <span className="font-bold text-white tracking-tight text-sm">MATRIXFLOW</span>
          </div>
        </div>

        {/* Form and Camera Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start pt-2">
          {/* Form */}
          <section className="space-y-5">
            <span className="px-3 py-1 bg-brand-mint/15 border border-brand-teal/30 rounded-full text-[11px] font-bold text-brand-mint tracking-wider uppercase inline-flex items-center gap-1.5">
              <UserPlus size={14} /> Alta de Nuevo Usuario
            </span>

            <h1 className="text-3xl lg:text-4xl font-bold tracking-tight text-white leading-tight">
              Regístrate en MatrixFlow Enterprise
            </h1>

            <p className="text-xs text-slate-400">
              Registra tus datos y tu rostro para habilitar la autenticación biométrica de alta seguridad.
            </p>

            <div className="space-y-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">DNI</label>
                <input
                  type="text"
                  inputMode="numeric"
                  maxLength={8}
                  placeholder="8 dígitos"
                  value={dni}
                  disabled={busy}
                  onChange={(e) => setDni(e.target.value.replace(/\D/g, "").slice(0, 8))}
                  className="w-full px-4 py-2 bg-brand-dark/50 border border-brand-dark rounded-lg text-xs font-semibold text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-brand-teal"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Nombre Completo</label>
                <input
                  type="text"
                  placeholder="Nombre y apellidos"
                  value={nombre}
                  disabled={busy}
                  onChange={(e) => setNombre(e.target.value)}
                  className="w-full px-4 py-2 bg-brand-dark/50 border border-brand-dark rounded-lg text-xs font-medium text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-brand-teal"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Correo Electrónico</label>
                <input
                  type="email"
                  placeholder="nombre@correo.com"
                  value={email}
                  disabled={busy}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-2 bg-brand-dark/50 border border-brand-dark rounded-lg text-xs font-medium text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-brand-teal"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Contraseña</label>
                  <input
                    type="password"
                    placeholder="Mínimo 8 caracteres"
                    value={password}
                    disabled={busy}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full px-4 py-2 bg-brand-dark/50 border border-brand-dark rounded-lg text-xs font-medium text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-brand-teal"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Confirmar Contraseña</label>
                  <input
                    type="password"
                    placeholder="Repite la contraseña"
                    value={confirmPassword}
                    disabled={busy}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full px-4 py-2 bg-brand-dark/50 border border-brand-dark rounded-lg text-xs font-medium text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-brand-teal"
                  />
                </div>
              </div>
            </div>
          </section>

          {/* Camera Card */}
          <section className="bg-brand-darker border border-brand-dark rounded-2xl p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-[10px] font-bold text-brand-mint uppercase tracking-wider">Identidad Facial</p>
                <h2 className="text-xl font-bold text-white">Registra tu rostro</h2>
              </div>
              <span className="px-2.5 py-1 rounded-full bg-brand-dark text-brand-mint text-[11px] font-bold border border-brand-teal/40">
                3 capturas requeridas
              </span>
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
              onClick={startRegistration}
            >
              <ShieldCheck size={16} />
              <span>
                {capturing
                  ? "Capturando rostro..."
                  : processing
                  ? "Creando cuenta..."
                  : "Crear cuenta y registrar rostro"}
              </span>
            </Button>

            <p className="text-[11px] text-center text-slate-500">
              Tus capturas se procesan de forma segura para generar el perfil biométrico de acceso.
            </p>
          </section>
        </div>
      </div>
    </main>
  );
}