import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Download, FileSpreadsheet, FileText } from 'lucide-react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts';
import { useTheme } from '../context/ThemeContext';

const productPieData = [
  { name: 'Workstation Pro', value: 45000 },
  { name: 'Desktop PC', value: 32000 },
  { name: 'Monitor 34"', value: 24000 },
  { name: 'Teclado RGB', value: 15000 },
  { name: 'Mouse Wireless', value: 12000 },
];

const COLORS = ['#1C6B6A', '#0F3A3F', '#10B981', '#F59E0B', '#8B5CF6'];

export const ReportesPage: React.FC = () => {
  const { theme } = useTheme();
  const isDark = theme === 'dark';

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Reportes Empresariales</h1>
          <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mt-1">Exportación de resultados y distribución porcentual de ventas</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline"><FileText size={16} /> Exportar PDF</Button>
          <Button variant="primary"><FileSpreadsheet size={16} /> Exportar Excel</Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader title="Distribución de Ingresos por Producto" subtitle="Derivado del Producto Escalar (Cantidades × Precios)" />
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={productPieData} cx="50%" cy="50%" outerRadius={80} dataKey="value" label={({ name }) => name}>
                  {productPieData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(val) => `S/ ${Number(val).toLocaleString()}`} 
                  contentStyle={{ 
                    backgroundColor: isDark ? '#0A1F24' : '#FFFFFF', 
                    borderColor: isDark ? '#0F3A3F' : '#CBD5E1',
                    borderRadius: '12px',
                    color: isDark ? '#FFFFFF' : '#071014',
                    fontWeight: 600
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card className="space-y-4">
          <CardHeader title="Informes Analíticos Disponibles" />
          <div className="space-y-3 text-xs">
            <div className="p-3.5 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-xl flex items-center justify-between">
              <div>
                <p className="font-bold text-slate-900 dark:text-white">Informe de Ventas por Sucursal</p>
                <p className="text-[11px] font-semibold text-slate-600 dark:text-slate-400">Formato vectorial consolidado</p>
              </div>
              <Button size="sm" variant="secondary"><Download size={14} /> Generar</Button>
            </div>

            <div className="p-3.5 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-xl flex items-center justify-between">
              <div>
                <p className="font-bold text-slate-900 dark:text-white">Informe de Brechas de Rendimiento</p>
                <p className="text-[11px] font-semibold text-slate-600 dark:text-slate-400">Matriz Reales − Metas</p>
              </div>
              <Button size="sm" variant="secondary"><Download size={14} /> Generar</Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
