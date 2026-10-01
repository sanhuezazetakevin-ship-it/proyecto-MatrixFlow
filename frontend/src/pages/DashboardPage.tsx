import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { DollarSign, TrendingUp, ShoppingBag, Binary, ArrowUpRight, User as UserIcon } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

const salesData = [
  { name: 'Lima', Ventas: 48500, Meta: 52000 },
  { name: 'Arequipa', Ventas: 32100, Meta: 35000 },
  { name: 'Trujillo', Ventas: 24900, Meta: 26000 },
  { name: 'Cusco', Ventas: 19800, Meta: 20000 },
  { name: 'Piura', Ventas: 15400, Meta: 16000 },
];

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const { theme } = useTheme();
  const isDark = theme === 'dark';

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Title Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="matrix-card-title text-2xl font-extrabold tracking-tight">
            Dashboard Ejecutivo {user?.nombre ? `— Bienvenido, ${user.nombre}` : ''}
          </h1>
          <p className="matrix-card-subtitle text-xs font-semibold mt-1">
            Indicadores corporativos y analítica de ventas impulsada por Álgebra Lineal
          </p>
        </div>
        {user && (
          <div className="flex items-center gap-2 px-3.5 py-1.5 bg-slate-200 dark:bg-brand-dark rounded-xl text-xs font-bold text-slate-800 dark:text-brand-mint border border-slate-300 dark:border-brand-teal/40">
            <UserIcon size={14} className="text-brand-teal dark:text-brand-mint" />
            <span>{user.email} ({user.rol || 'ADMINISTRADOR'})</span>
          </div>
        )}
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="border-l-4 border-l-brand-teal">
          <div className="flex items-center justify-between">
            <div>
              <p className="matrix-card-subtitle text-xs font-bold">Ventas Totales (Producto Escalar)</p>
              <h3 className="matrix-card-title text-2xl font-black mt-1">S/ 140,700</h3>
              <p className="text-[11px] text-emerald-600 dark:text-emerald-400 font-bold mt-1 flex items-center gap-1">
                <ArrowUpRight size={13} /> +12.4% vs mes anterior
              </p>
            </div>
            <div className="p-3 bg-brand-teal/15 dark:bg-brand-teal/30 text-brand-teal dark:text-brand-mint rounded-xl">
              <DollarSign size={22} />
            </div>
          </div>
        </Card>

        <Card className="border-l-4 border-l-cyan-600 dark:border-l-brand-mint">
          <div className="flex items-center justify-between">
            <div>
              <p className="matrix-card-subtitle text-xs font-bold">Cumplimiento (Resta Matricial)</p>
              <h3 className="matrix-card-title text-2xl font-black mt-1">94.4%</h3>
              <p className="matrix-card-subtitle text-[11px] font-semibold mt-1">Brecha: - S/ 8,300</p>
            </div>
            <div className="p-3 bg-cyan-100 dark:bg-brand-mint/20 text-cyan-700 dark:text-brand-mint rounded-xl">
              <TrendingUp size={22} />
            </div>
          </div>
        </Card>

        <Card className="border-l-4 border-l-emerald-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="matrix-card-subtitle text-xs font-bold">Sucursales Activas</p>
              <h3 className="matrix-card-title text-2xl font-black mt-1">5 Sedes</h3>
              <p className="matrix-card-subtitle text-[11px] font-semibold mt-1">Lima, AQP, TRU, CUS, PIU</p>
            </div>
            <div className="p-3 bg-emerald-100 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-400 rounded-xl">
              <ShoppingBag size={22} />
            </div>
          </div>
        </Card>

        <Card className="border-l-4 border-l-indigo-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="matrix-card-subtitle text-xs font-bold">Operaciones Ejecutadas</p>
              <h3 className="matrix-card-title text-2xl font-black mt-1">148 Cálculos</h3>
              <p className="text-[11px] text-indigo-600 dark:text-indigo-400 font-bold mt-1">Trazabilidad 100% NumPy</p>
            </div>
            <div className="p-3 bg-indigo-100 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 rounded-xl">
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
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke={isDark ? "#0F3A3F" : "#CBD5E1"} />
              <XAxis dataKey="name" tickLine={false} axisLine={false} tick={{ fontSize: 12, fill: isDark ? '#E2E8F0' : '#071014', fontWeight: 700 }} />
              <YAxis tickLine={false} axisLine={false} tick={{ fontSize: 12, fill: isDark ? '#E2E8F0' : '#071014', fontWeight: 700 }} />
              <Tooltip 
                formatter={(val) => `S/ ${Number(val).toLocaleString()}`}
                contentStyle={{ 
                  backgroundColor: isDark ? '#0A1F24' : '#FFFFFF', 
                  borderColor: isDark ? '#0F3A3F' : '#CBD5E1',
                  borderRadius: '12px',
                  color: isDark ? '#FFFFFF' : '#071014',
                  fontWeight: 700
                }}
              />
              <Bar dataKey="Ventas" fill="#1C6B6A" radius={[4, 4, 0, 0]} name="Ventas Reales" />
              <Bar dataKey="Meta" fill={isDark ? "#B8F2E6" : "#0F3A3F"} radius={[4, 4, 0, 0]} name="Meta Planificada" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  );
};

export default DashboardPage;
