<<<<<<< HEAD
import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { DollarSign, TrendingUp, ShoppingBag, Binary, ArrowUpRight } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const salesData = [
  { name: 'Lima', Ventas: 48500, Meta: 52000 },
  { name: 'Arequipa', Ventas: 32100, Meta: 35000 },
  { name: 'Trujillo', Ventas: 24900, Meta: 26000 },
  { name: 'Cusco', Ventas: 19800, Meta: 20000 },
  { name: 'Piura', Ventas: 15400, Meta: 16000 },
];

export const DashboardPage: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Title Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Dashboard Ejecutivo</h1>
        <p className="text-xs text-slate-500 mt-1">Indicadores corporativos y analítica de ventas impulsada por Álgebra Lineal</p>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="border-l-4 border-l-primary">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-500">Ventas Totales (Producto Escalar)</p>
              <h3 className="text-2xl font-bold text-slate-900 mt-1">S/ 140,700</h3>
              <p className="text-[11px] text-emerald-600 font-medium mt-1 flex items-center gap-1">
                <ArrowUpRight size={12} /> +12.4% vs mes anterior
              </p>
            </div>
            <div className="p-3 bg-primary/10 text-primary rounded-xl">
              <DollarSign size={22} />
            </div>
          </div>
        </Card>

        <Card className="border-l-4 border-l-accent">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-500">Cumplimiento de Metas (Resta Matricial)</p>
              <h3 className="text-2xl font-bold text-slate-900 mt-1">94.4%</h3>
              <p className="text-[11px] text-slate-500 mt-1">Brecha: - S/ 8,300</p>
            </div>
            <div className="p-3 bg-accent/10 text-accent rounded-xl">
              <TrendingUp size={22} />
            </div>
          </div>
        </Card>

        <Card className="border-l-4 border-l-emerald-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-500">Sucursales Activas</p>
              <h3 className="text-2xl font-bold text-slate-900 mt-1">5 Sedes</h3>
              <p className="text-[11px] text-slate-500 mt-1">Lima, AQP, TRU, CUS, PIU</p>
            </div>
            <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl">
              <ShoppingBag size={22} />
            </div>
          </div>
        </Card>

        <Card className="border-l-4 border-l-indigo-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-500">Operaciones Ejecutadas</p>
              <h3 className="text-2xl font-bold text-slate-900 mt-1">148 Cálculos</h3>
              <p className="text-[11px] text-indigo-600 font-medium mt-1">Trazabilidad 100% NumPy</p>
            </div>
            <div className="p-3 bg-indigo-50 text-indigo-600 rounded-xl">
              <Binary size={22} />
            </div>
          </div>
        </Card>
      </div>

      {/* Main Bar Chart */}
      <Card>
        <CardHeader 
          title="Ventas Reales vs Metas por Sucursal" 
          subtitle="Representación vectorial de ingresos por ciudad (Matriz de Ventas Q_Real vs Q_Meta)"
          action={<Badge variant="info">Actualizado hoy</Badge>}
        />
        <div className="h-72 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={salesData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
              <XAxis dataKey="name" tickLine={false} axisLine={false} tick={{ fontSize: 12 }} />
              <YAxis tickLine={false} axisLine={false} tick={{ fontSize: 12 }} />
              <Tooltip formatter={(val) => `S/ ${Number(val).toLocaleString()}`} />
              <Bar dataKey="Ventas" fill="#2563EB" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Meta" fill="#06B6D4" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  );
};
=======
import { useNavigate }
  from "react-router-dom";

import { useAuth }
  from "../context/AuthContext";


export default function DashboardPage() {

  const navigate =
    useNavigate();

  const {
    user,
    logout,
  } = useAuth();


  function handleLogout() {

    logout();

    navigate(
      "/login",
      {
        replace: true,
      }
    );
  }


  return (
    <main className="dashboard-page">

      <div className="dashboard-card">

        <p className="eyebrow">
          MATRIXFLOW
        </p>

        <h1>
          Bienvenido, {user?.nombre}
        </h1>

        <p>
          Tu autenticación funciona
          correctamente.
        </p>


        <div className="user-data">

          <div>
            <span>Correo</span>
            <strong>
              {user?.email}
            </strong>
          </div>

          <div>
            <span>Rol</span>
            <strong>
              {user?.rol}
            </strong>
          </div>

        </div>


        <button
          className="secondary-button"
          onClick={handleLogout}
        >
          Cerrar sesión
        </button>

      </div>

    </main>
  );
}
>>>>>>> 87884f86cb2298dcd4e88163aca4349d473a1149
