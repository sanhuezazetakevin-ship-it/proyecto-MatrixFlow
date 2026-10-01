import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { mockSales } from '../services/mockData';
import { Plus, Calendar } from 'lucide-react';

export const VentasPage: React.FC = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-extrabold">Registro de Ventas</h1>
          <p className="text-xs font-bold mt-1 text-muted-custom">Histórico transaccional utilizado como fuente para la matriz Q_Real</p>
        </div>
        <Button variant="primary"><Plus size={16} /> Registrar Venta</Button>
      </div>

      <Card>
        <CardHeader title="Ventas por Comprobante" />
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="matrix-table-head">
              <tr>
                <th className="p-3">ID Venta</th>
                <th className="p-3">Sucursal</th>
                <th className="p-3">Fecha</th>
                <th className="p-3">Ítems Vendidos</th>
                <th className="p-3">Monto Total</th>
                <th className="p-3 text-right">Detalles</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-brand-dark">
              {mockSales.map((s) => (
                <tr key={s.id} className="matrix-table-row font-semibold hover:opacity-90">
                  <td className="p-3 font-mono font-extrabold text-accent-custom">{s.id}</td>
                  <td className="p-3 font-bold">{s.branchName}</td>
                  <td className="p-3 font-bold flex items-center gap-1.5">
                    <Calendar size={14} className="text-accent-custom" />
                    {s.date}
                  </td>
                  <td className="p-3 font-semibold">{s.itemsCount} productos</td>
                  <td className="p-3 font-black text-sm text-accent-custom">S/ {s.totalAmount.toLocaleString()}</td>
                  <td className="p-3 text-right">
                    <button className="text-accent-custom hover:underline font-extrabold">Ver Comprobante</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
