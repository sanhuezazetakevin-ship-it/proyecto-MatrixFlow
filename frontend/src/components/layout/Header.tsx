import React from 'react';
import { Bell, Search, ShieldCheck, Sun, Moon } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

export const Header: React.FC = () => {
  const [showNotifications, setShowNotifications] = React.useState(false);
  const { theme, toggleTheme } = useTheme();

  // Mock sessions para visualización rápida de últimos logins
  const recentSessions = [
    { id: 1, user: 'Gabriel Cerna Bustamante', role: 'ADMINISTRADOR', time: 'Hace 5 min' },
    { id: 2, user: 'Ana López', role: 'OPERADOR', time: 'Hace 1 hora' },
    { id: 3, user: 'Carlos Ruiz', role: 'CONSULTA', time: 'Hace 3 horas' },
  ];

  return (
    <header className="matrix-header h-16 px-6 flex items-center justify-between sticky top-0 z-20 shadow-xs transition-colors duration-300">
      {/* Search Input */}
      <div className="relative w-80">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 opacity-60" size={16} />
        <input
          type="text"
          placeholder="Buscar vectores, matrices, operaciones..."
          className="matrix-input w-full pl-9 pr-4 py-2 rounded-xl text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-brand-teal transition-all shadow-inner"
        />
      </div>

      {/* Header Actions */}
      <div className="flex items-center gap-4">
        {/* Dark Mode Toggle Button */}
        <button
          onClick={toggleTheme}
          title="Cambiar modo visual"
          className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-slate-200 dark:bg-brand-dark hover:bg-slate-300 dark:hover:bg-brand-teal/40 text-slate-900 dark:text-brand-mint border border-slate-300 dark:border-brand-dark text-xs font-bold transition-all duration-200 active:scale-95 shadow-xs"
        >
          {theme === 'dark' ? (
            <>
              <Sun size={15} className="text-amber-400" />
              <span>Modo Claro</span>
            </>
          ) : (
            <>
              <Moon size={15} className="text-brand-teal" />
              <span>Modo Oscuro</span>
            </>
          )}
        </button>

        {/* Academic Status Badge */}
        <div className="hidden sm:flex items-center gap-2 px-3.5 py-1.5 bg-brand-mint/20 dark:bg-brand-mint/15 border border-brand-teal/40 rounded-full text-[11px] text-brand-dark dark:text-brand-mint font-extrabold">
          <ShieldCheck size={14} className="text-brand-teal dark:text-brand-mint" />
          <span>Motor Matemático NumPy Activo</span>
        </div>

        {/* Notifications */}
        <div className="relative">
          <button 
            onClick={() => setShowNotifications(!showNotifications)}
            className="relative p-2 opacity-80 hover:opacity-100 hover:bg-slate-100 dark:hover:bg-brand-dark rounded-xl transition-colors"
          >
            <Bell size={18} />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-brand-teal dark:bg-brand-mint rounded-full animate-pulse"></span>
          </button>

          {/* Notifications Dropdown */}
          {showNotifications && (
            <div className="absolute right-0 mt-2 w-72 bg-white dark:bg-brand-darker border border-slate-200 dark:border-brand-dark rounded-2xl shadow-xl overflow-hidden animate-fade-in z-50">
              <div className="p-3 border-b border-slate-200 dark:border-brand-dark bg-slate-50 dark:bg-brand-darkest">
                <h3 className="text-xs font-bold text-slate-800 dark:text-white">Sesiones Recientes</h3>
                <p className="text-[10px] text-slate-500 dark:text-slate-400">Últimos accesos biométricos al sistema</p>
              </div>
              <div className="max-h-64 overflow-y-auto">
                {recentSessions.map(session => (
                  <div key={session.id} className="p-3 border-b border-slate-100 dark:border-brand-dark/50 hover:bg-slate-50 dark:hover:bg-brand-dark/30 transition-colors cursor-pointer">
                    <p className="text-xs font-bold text-slate-700 dark:text-slate-200">{session.user}</p>
                    <div className="flex items-center justify-between mt-1">
                      <span className="text-[10px] font-semibold text-brand-teal dark:text-brand-mint">{session.role}</span>
                      <span className="text-[10px] text-slate-400 dark:text-slate-500">{session.time}</span>
                    </div>
                  </div>
                ))}
              </div>
              <div className="p-2 bg-slate-50 dark:bg-brand-darkest text-center border-t border-slate-200 dark:border-brand-dark">
                <button className="text-[10px] font-bold text-brand-teal dark:text-brand-mint hover:underline">Ver todo el historial de auditoría</button>
              </div>
            </div>
          )}
        </div>

        <div className="h-6 w-px bg-slate-300 dark:bg-brand-dark"></div>

        {/* Status Period Badge */}
        <span className="text-xs font-semibold opacity-80">
          Período: <strong className="font-extrabold opacity-100">Setiembre 2026</strong>
        </span>
      </div>
    </header>
  );
};
