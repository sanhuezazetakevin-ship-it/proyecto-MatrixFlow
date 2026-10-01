import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { LockKeyhole, ScanFace, ShieldCheck } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { Button } from "../components/ui/Button";

export function LoginPage() {
  const navigate = useNavigate();
  const { loginPassword } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (loading) return;
    setError("");
    setLoading(true);
    try {
      await loginPassword(email.trim(), password);
      navigate("/dashboard", { replace: true });
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;
        setError(typeof detail === "string" ? detail : "No se pudo iniciar sesión. Verifica tus credenciales.");
      } else {
        setError("No se pudo iniciar sesión. Inténtalo nuevamente.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-brand-darkest text-slate-100 p-6 flex items-center justify-center">
      <div className="w-full max-w-md bg-brand-darker border border-brand-dark rounded-2xl p-7 shadow-2xl space-y-6">
        <div className="flex items-center justify-center gap-2">
          <div className="w-9 h-9 rounded-lg bg-brand-teal flex items-center justify-center text-white font-bold">M</div>
          <span className="font-bold text-white tracking-tight">MATRIXFLOW</span>
        </div>
        <div className="text-center space-y-2">
          <div className="inline-flex items-center gap-2 text-brand-mint text-xs font-semibold uppercase tracking-wider">
            <ShieldCheck size={15} /> Acceso seguro
          </div>
          <h1 className="text-3xl font-bold text-white">Iniciar sesión</h1>
          <p className="text-sm text-slate-400">Ingresa con tu correo y contraseña o utiliza el reconocimiento facial.</p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1">
            <label htmlFor="email" className="block text-xs font-semibold text-slate-300">Correo electrónico</label>
            <input id="email" type="email" autoComplete="username" required value={email} disabled={loading}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="correo@ejemplo.com"
              className="w-full px-4 py-3 bg-brand-dark/60 border border-brand-dark rounded-lg text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-brand-teal" />
          </div>
          <div className="space-y-1">
            <label htmlFor="password" className="block text-xs font-semibold text-slate-300">Contraseña</label>
            <input id="password" type="password" autoComplete="current-password" required value={password} disabled={loading}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Ingresa tu contraseña"
              className="w-full px-4 py-3 bg-brand-dark/60 border border-brand-dark rounded-lg text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-brand-teal" />
          </div>
          {error && <div role="alert" className="p-3 bg-red-950/60 border border-red-800 rounded-lg text-xs text-red-300">{error}</div>}
          <Button type="submit" variant="accent" className="w-full py-3" disabled={loading}>
            <LockKeyhole size={16} /> {loading ? "Ingresando..." : "Ingresar con correo"}
          </Button>
        </form>
        <div className="flex items-center gap-3 text-slate-500 text-xs">
          <div className="h-px bg-brand-dark flex-1" /> O también <div className="h-px bg-brand-dark flex-1" />
        </div>
        <Link to="/login/facial" className="flex items-center justify-center gap-2 w-full py-3 border border-brand-teal text-brand-mint rounded-lg text-sm font-semibold hover:bg-brand-teal/10 transition-colors">
          <ScanFace size={18} /> Ingresar con DNI y reconocimiento facial
        </Link>
        <p className="text-center text-xs text-slate-400">¿No tienes una cuenta? <Link to="/registro" className="text-brand-mint hover:underline">Regístrate</Link></p>
      </div>
    </main>
  );
}
export default LoginPage;
