import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, Building2, MapPin, Package, ShoppingCart, 
  Boxes, Binary, Grid3X3, Calculator, Network, History, 
  BarChart3, Users, Settings, ChevronDown 
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const [empresaOpen, setEmpresaOpen] = React.useState(true);
  const [mathOpen, setMathOpen] = React.useState(true);

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium transition-all ${
      isActive
        ? 'bg-primary text-white font-semibold shadow-sm'
        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
    }`;

  const subLinkClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-2.5 px-3 py-1.5 rounded-lg text-xs transition-all ${
      isActive
        ? 'text-accent font-semibold bg-slate-800/80 border-l-2 border-accent pl-2'
        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
    }`;

  return (
    <aside className="w-64 bg-sidebar text-slate-300 flex flex-col h-screen fixed left-0 top-0 z-30 shadow-xl border-r border-slate-800">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-800/80 flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-primary to-accent flex items-center justify-center text-white font-black text-lg shadow-md shadow-primary/30">
          M
        </div>
        <div>
          <h1 className="font-bold text-white tracking-tight text-base leading-none">MATRIXFLOW</h1>
          <span className="text-[10px] text-accent font-semibold tracking-wider uppercase">Enterprise v1.0</span>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 overflow-y-auto p-4 space-y-1.5 text-xs">
        <NavLink to="/dashboard" className={linkClass}>
          <LayoutDashboard size={16} />
          <span>Dashboard</span>
        </NavLink>

        {/* Empresa Group */}
        <div>
          <button
            onClick={() => setEmpresaOpen(!empresaOpen)}
            className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 text-xs font-medium transition-all"
          >
            <div className="flex items-center gap-3">
              <Building2 size={16} />
              <span>Empresa</span>
            </div>
            <ChevronDown size={14} className={`transition-transform duration-200 ${empresaOpen ? 'rotate-180' : ''}`} />
          </button>
          {empresaOpen && (
            <div className="ml-4 pl-3 border-l border-slate-800 mt-1 space-y-1">
              <NavLink to="/empresa" className={subLinkClass}>
                <span>Información Corporativa</span>
              </NavLink>
              <NavLink to="/sucursales" className={subLinkClass}>
                <MapPin size={14} />
                <span>Sucursales</span>
              </NavLink>
              <NavLink to="/productos" className={subLinkClass}>
                <Package size={14} />
                <span>Productos</span>
              </NavLink>
            </div>
          )}
        </div>

        <NavLink to="/ventas" className={linkClass}>
          <ShoppingCart size={16} />
          <span>Ventas</span>
        </NavLink>

        <NavLink to="/inventario" className={linkClass}>
          <Boxes size={16} />
          <span>Inventario</span>
        </NavLink>

        {/* Análisis Matemático Group */}
        <div className="pt-2">
          <div className="px-3 mb-1 text-[10px] font-semibold text-slate-500 uppercase tracking-wider">
            Motor de Álgebra Lineal
          </div>
          <button
            onClick={() => setMathOpen(!mathOpen)}
            className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 text-xs font-medium transition-all"
          >
            <div className="flex items-center gap-3">
              <Binary size={16} className="text-accent" />
              <span className="text-slate-200">Análisis Matemático</span>
            </div>
            <ChevronDown size={14} className={`transition-transform duration-200 ${mathOpen ? 'rotate-180' : ''}`} />
          </button>

          {mathOpen && (
            <div className="ml-4 pl-3 border-l border-slate-800 mt-1 space-y-1">
              <NavLink to="/vectores" className={subLinkClass}>
                <Binary size={14} />
                <span>Vectores</span>
              </NavLink>
              <NavLink to="/matrices" className={subLinkClass}>
                <Grid3X3 size={14} />
                <span>Matrices</span>
              </NavLink>
              <NavLink to="/operaciones" className={subLinkClass}>
                <Calculator size={14} />
                <span>Operaciones</span>
              </NavLink>
              <NavLink to="/combinaciones" className={subLinkClass}>
                <Network size={14} />
                <span>Combinaciones Lineales</span>
              </NavLink>
            </div>
          )}
        </div>

        {/* General Management */}
        <div className="pt-2">
          <div className="px-3 mb-1 text-[10px] font-semibold text-slate-500 uppercase tracking-wider">
            Gestión & Reportes
          </div>
          <NavLink to="/historial" className={linkClass}>
            <History size={16} />
            <span>Historial y Auditoría</span>
          </NavLink>
          <NavLink to="/reportes" className={linkClass}>
            <BarChart3 size={16} />
            <span>Reportes & KPIs</span>
          </NavLink>
          <NavLink to="/usuarios" className={linkClass}>
            <Users size={16} />
            <span>Usuarios & Roles</span>
          </NavLink>
          <NavLink to="/configuracion" className={linkClass}>
            <Settings size={16} />
            <span>Configuración</span>
          </NavLink>
        </div>
      </nav>

      {/* User Footer Profile */}
      <div className="p-4 border-t border-slate-800/80 bg-slate-900/60 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-full bg-primary/20 border border-primary/40 flex items-center justify-center text-primary font-bold text-xs">
            GA
          </div>
          <div className="overflow-hidden">
            <p className="text-xs font-medium text-white truncate">Gabriel Admin</p>
            <p className="text-[10px] text-slate-400">ADMINISTRADOR</p>
          </div>
        </div>
      </div>
    </aside>
  );
};
