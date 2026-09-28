import React from 'react';
import { Bell, Search, ShieldCheck } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="h-16 bg-white border-b border-slate-200/80 px-6 flex items-center justify-between sticky top-0 z-20 shadow-xs">
      {/* Search Input */}
      <div className="relative w-72">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
        <input
          type="text"
          placeholder="Buscar vectores, matrices, operaciones..."
          className="w-full pl-9 pr-4 py-1.5 bg-slate-100/80 border-0 rounded-lg text-xs text-slate-700 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
        />
      </div>

      {/* Header Actions */}
      <div className="flex items-center gap-4">
        {/* Academic Status Badge */}
        <div className="hidden sm:flex items-center gap-2 px-3 py-1 bg-cyan-50 border border-cyan-200 rounded-full text-[11px] text-cyan-800 font-medium">
          <ShieldCheck size={14} className="text-cyan-600" />
          <span>Motor Matemático NumPy Activo</span>
        </div>

        {/* Notifications */}
        <button className="relative p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors">
          <Bell size={18} />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-primary rounded-full"></span>
        </button>

        <div className="h-6 w-px bg-slate-200"></div>

        {/* Status Period Badge */}
        <span className="text-xs text-slate-500 font-medium">
          Período: <strong className="text-slate-800">Setiembre 2026</strong>
        </span>
      </div>
    </header>
  );
};
