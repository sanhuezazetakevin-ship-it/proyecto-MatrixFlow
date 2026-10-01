import React from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

export const MainLayout: React.FC = () => {
  return (
    <div className="min-h-screen flex transition-colors duration-300">
      {/* Fixed Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="flex-1 ml-64 flex flex-col min-h-screen">
        <Header />
        
        <main className="flex-1 p-6 max-w-7xl w-full mx-auto animate-fade-in">
          <Outlet />
        </main>

        <footer className="py-4 px-6 border-t border-slate-200 dark:border-brand-dark text-center text-xs font-semibold opacity-75 bg-white dark:bg-brand-darker transition-colors duration-300">
          MatrixFlow Enterprise v1.0 — Sistema Web de Análisis de Ventas, Inventario e Indicadores mediante Álgebra Lineal &copy; 2026
        </footer>
      </div>
    </div>
  );
};
