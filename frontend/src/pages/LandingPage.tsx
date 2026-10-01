import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, ShieldCheck, Activity, BarChart3, Database } from 'lucide-react';
import { Button } from '../components/ui/Button';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-brand-darkest text-slate-100 flex flex-col font-sans selection:bg-brand-teal selection:text-brand-darkest">
      
      {/* Navbar */}
      <header className="border-b border-brand-dark/50 bg-brand-darker/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-teal to-brand-mint flex items-center justify-center text-brand-darkest font-black text-lg shadow-lg shadow-brand-teal/20">
              M
            </div>
            <span className="font-bold text-white tracking-tight text-sm">MATRIXFLOW ENTERPRISE</span>
          </div>
          <div className="flex items-center gap-4">
            <Link to="/login" className="text-xs font-semibold text-slate-300 hover:text-white transition-colors">
              Portal de Acceso
            </Link>
            <Link to="/registro">
              <Button variant="accent" className="py-1.5 px-4 text-xs">
                Alta de Usuario
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center relative overflow-hidden px-6 py-20">
        
        {/* Background Gradients */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[500px] bg-brand-teal/10 rounded-full blur-[120px] pointer-events-none"></div>
        <div className="absolute top-0 right-0 w-[400px] h-[400px] bg-brand-mint/5 rounded-full blur-[100px] pointer-events-none"></div>

        <div className="max-w-4xl w-full mx-auto text-center relative z-10 space-y-8 animate-fade-in">
          
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-dark/60 border border-brand-dark text-[11px] font-bold text-brand-mint tracking-widest uppercase mb-4 shadow-sm">
            <ShieldCheck size={14} />
            Arquitectura de Nivel Empresarial
          </div>

          <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight text-white leading-tight">
            Análisis de datos potenciado por <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-teal to-brand-mint">Álgebra Lineal</span>
          </h1>

          <p className="text-base md:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed font-medium">
            Plataforma corporativa para la gestión centralizada de ventas e inventario. Transforma la información de tus sucursales en vectores y matrices para generar indicadores analíticos precisos.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-8">
            <Link to="/login" className="w-full sm:w-auto">
              <Button variant="accent" className="w-full sm:w-auto py-3 px-8 text-sm font-bold flex items-center justify-center gap-2 group">
                <span>Ingresar al Sistema</span>
                <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
              </Button>
            </Link>
            <Link to="/registro" className="w-full sm:w-auto">
              <Button variant="outline" className="w-full sm:w-auto py-3 px-8 text-sm font-bold bg-brand-dark/40 border-brand-teal/30 hover:border-brand-teal hover:bg-brand-dark text-slate-200">
                Registrar Nuevo Usuario
              </Button>
            </Link>
          </div>

          {/* Feature highlights */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-20 text-left border-t border-brand-dark/50 mt-12">
            <div className="space-y-3 p-6 bg-brand-darker/50 rounded-2xl border border-brand-dark/50 hover:border-brand-teal/30 transition-colors">
              <div className="w-10 h-10 rounded-xl bg-brand-dark flex items-center justify-center text-brand-mint border border-brand-teal/20">
                <Database size={20} />
              </div>
              <h3 className="text-sm font-bold text-slate-200">Gestión Centralizada</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Administración integral de empresas, sucursales y catálogo de productos estructurada en PostgreSQL.
              </p>
            </div>
            
            <div className="space-y-3 p-6 bg-brand-darker/50 rounded-2xl border border-brand-dark/50 hover:border-brand-teal/30 transition-colors">
              <div className="w-10 h-10 rounded-xl bg-brand-dark flex items-center justify-center text-brand-mint border border-brand-teal/20">
                <Activity size={20} />
              </div>
              <h3 className="text-sm font-bold text-slate-200">Motor Matemático</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Procesamiento de datos a través de operaciones vectoriales y matriciales ejecutadas en NumPy.
              </p>
            </div>

            <div className="space-y-3 p-6 bg-brand-darker/50 rounded-2xl border border-brand-dark/50 hover:border-brand-teal/30 transition-colors">
              <div className="w-10 h-10 rounded-xl bg-brand-dark flex items-center justify-center text-brand-mint border border-brand-teal/20">
                <BarChart3 size={20} />
              </div>
              <h3 className="text-sm font-bold text-slate-200">Seguridad Biométrica</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Autenticación por reconocimiento facial, Liveness Detection y control de acceso basado en roles (RBAC).
              </p>
            </div>
          </div>

        </div>
      </main>
      
      <footer className="py-6 text-center border-t border-brand-dark/50 text-[11px] font-semibold text-slate-500 bg-brand-darkest">
        &copy; {new Date().getFullYear()} MatrixFlow Enterprise. Todos los derechos reservados.
      </footer>
    </div>
  );
};

export default LandingPage;
