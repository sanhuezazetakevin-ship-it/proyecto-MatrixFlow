import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { mockSales } from '../services/mockData';
import { ShoppingCart, Plus, Calendar } from 'lucide-react';

export const VentasPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Registro de Ventas</h1>
          <p className="text-xs text-slate-500 mt-1">Histórico transaccional utilizado como fuente para la matriz Q_Real</p>
        </div>
        <Button variant="primary"><Plus size={16} /> Registrar Venta</Button>
      </div>

      <Card>
        <CardHeader title="Ventas por Comprobante" />
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
              <tr>
                <th className="p-3">ID Venta</th>
                <th className="p-3">Sucursal</th>
                <th className="p-3">Fecha</th>
                <th className="p-3">Ítems Vendidos</th>
                <th className="p-3">Monto Total</th>
                <th className="p-3 text-right">Detalles</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {mockSales.map((s) => (
                <tr key={s.id} className="hover:bg-slate-50/80">
                  <td className="p-3 font-mono font-semibold text-primary">{s.id}</td>
                  <td className="p-3 font-medium text-slate-800">{s.branchName}</td>
                  <td className="p-3 text-slate-500 flex items-center gap-1.5">
                    <Calendar size={14} />
                    {s.date}
                  </td>
                  <td className="p-3 text-slate-700">{s.itemsCount} productos</td>
                  <td className="p-3 font-bold text-slate-900">S/ {s.totalAmount.toLocaleString()}</td>
                  <td className="p-3 text-right">
                    <button className="text-primary hover:underline font-medium">Ver Comprobante</button>
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
