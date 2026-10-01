import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, Building2, MapPin, Package, ShoppingCart, 
  Boxes, Binary, Grid3X3, Calculator, Network, History, 
  BarChart3, Users, Settings, ChevronDown, LogOut 
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const Sidebar: React.FC = () => {
  const [empresaOpen, setEmpresaOpen] = React.useState(true);
  const [mathOpen, setMathOpen] = React.useState(true);
  const { user } = useAuth();

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all duration-200 ${
      isActive
        ? 'matrix-sidebar-link-active shadow-md'
        : 'matrix-sidebar-link'
    }`;

  const subLinkClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-semibold transition-all duration-200 ${
      isActive
        ? 'matrix-sidebar-link-active'
        : 'matrix-sidebar-link'
    }`;

  return (
    <aside className="matrix-sidebar w-64 flex flex-col h-screen fixed left-0 top-0 z-30 shadow-2xl">
      {/* Brand Header */}
      <div className="p-5 border-b border-brand-dark flex items-center gap-3 bg-brand-darker/50">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-teal to-brand-mint flex items-center justify-center text-brand-darkest font-black text-lg shadow-md shadow-brand-teal/30">
          M
        </div>
        <div>
          <h1 className="font-extrabold text-white tracking-tight text-base leading-none">MATRIXFLOW</h1>
          <span className="text-[10px] text-brand-mint font-bold tracking-wider uppercase">Enterprise v1.0</span>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 overflow-y-auto p-4 space-y-1.5 text-xs">
        <NavLink to="/dashboard" className={linkClass}>
          <LayoutDashboard size={17} />
          <span>Dashboard</span>
        </NavLink>

        {/* Empresa Group */}
        <div>
          <button
            onClick={() => setEmpresaOpen(!empresaOpen)}
            className="w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-slate-300 hover:text-white hover:bg-brand-dark/80 text-xs font-semibold transition-all"
          >
            <div className="flex items-center gap-3">
              <Building2 size={17} />
              <span>Empresa</span>
            </div>
            <ChevronDown size={14} className={`transition-transform duration-200 ${empresaOpen ? 'rotate-180' : ''}`} />
          </button>
          {empresaOpen && (
            <div className="ml-4 pl-3 border-l border-brand-dark/80 mt-1 space-y-1">
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
          <ShoppingCart size={17} />
          <span>Ventas</span>
        </NavLink>

        <NavLink to="/inventario" className={linkClass}>
          <Boxes size={17} />
          <span>Inventario</span>
        </NavLink>

        {/* Análisis Matemático Group */}
        <div className="pt-3">
          <div className="px-3 mb-1.5 text-[10px] font-extrabold text-brand-mint uppercase tracking-wider">
            Motor de Álgebra Lineal
          </div>
          <button
            onClick={() => setMathOpen(!mathOpen)}
            className="w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-slate-300 hover:text-white hover:bg-brand-dark/80 text-xs font-semibold transition-all"
          >
            <div className="flex items-center gap-3">
              <Binary size={17} className="text-brand-mint" />
              <span className="text-white font-bold">Análisis Matemático</span>
            </div>
            <ChevronDown size={14} className={`transition-transform duration-200 ${mathOpen ? 'rotate-180' : ''}`} />
          </button>

          {mathOpen && (
            <div className="ml-4 pl-3 border-l border-brand-dark/80 mt-1 space-y-1">
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
        <div className="pt-3">
          <div className="px-3 mb-1.5 text-[10px] font-extrabold text-brand-mint uppercase tracking-wider">
            Gestión & Reportes
          </div>
          <NavLink to="/historial" className={linkClass}>
            <History size={17} />
            <span>Historial y Auditoría</span>
          </NavLink>
          <NavLink to="/reportes" className={linkClass}>
            <BarChart3 size={17} />
            <span>Reportes & KPIs</span>
          </NavLink>
          <NavLink to="/usuarios" className={linkClass}>
            <Users size={17} />
            <span>Usuarios & Roles</span>
          </NavLink>
          <NavLink to="/configuracion" className={linkClass}>
            <Settings size={17} />
            <span>Configuración</span>
          </NavLink>
        </div>
      </nav>

      {/* User Footer Profile */}
      <div className="p-4 border-t border-brand-dark bg-brand-darker flex items-center justify-between">
        <div className="flex items-center gap-2.5 w-full">
          <div className="w-8 h-8 rounded-full bg-brand-teal border border-brand-mint flex items-center justify-center text-brand-mint font-extrabold text-xs shrink-0">
            {user?.nombre 
              ? user.nombre.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() 
              : 'U'}
          </div>
          <div className="overflow-hidden flex-1">
            <p className="text-xs font-bold text-white truncate">{user?.nombre || 'Usuario'}</p>
            <p className="text-[10px] text-brand-mint font-semibold truncate capitalize">{user?.rol || 'consulta'}</p>
          </div>
          <button 
            onClick={() => {
              localStorage.removeItem('matrixflow_token');
              localStorage.removeItem('matrixflow_user');
              window.location.href = '/login';
            }}
            className="text-slate-400 hover:text-red-400 transition-colors p-1"
            title="Cerrar sesión"
          >
            <LogOut size={16} />
          </button>
        </div>
      </div>
    </aside>
  );
};
