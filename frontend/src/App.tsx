import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { MainLayout } from './components/layout/MainLayout';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { EmpresaPage } from './pages/EmpresaPage';
import { SucursalesPage } from './pages/SucursalesPage';
import { ProductosPage } from './pages/ProductosPage';
import { VentasPage } from './pages/VentasPage';
import { InventarioPage } from './pages/InventarioPage';
import { VectoresPage } from './pages/VectoresPage';
import { MatricesPage } from './pages/MatricesPage';
import { OperacionesPage } from './pages/OperacionesPage';
import { CombinacionesPage } from './pages/CombinacionesPage';
import { HistorialPage } from './pages/HistorialPage';
import { ReportesPage } from './pages/ReportesPage';
import { UsuariosPage } from './pages/UsuariosPage';
import { ConfiguracionPage } from './pages/ConfiguracionPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="empresa" element={<EmpresaPage />} />
          <Route path="sucursales" element={<SucursalesPage />} />
          <Route path="productos" element={<ProductosPage />} />
          <Route path="ventas" element={<VentasPage />} />
          <Route path="inventario" element={<InventarioPage />} />
          <Route path="vectores" element={<VectoresPage />} />
          <Route path="matrices" element={<MatricesPage />} />
          <Route path="operaciones" element={<OperacionesPage />} />
          <Route path="combinaciones" element={<CombinacionesPage />} />
          <Route path="historial" element={<HistorialPage />} />
          <Route path="reportes" element={<ReportesPage />} />
          <Route path="usuarios" element={<UsuariosPage />} />
          <Route path="configuracion" element={<ConfiguracionPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
