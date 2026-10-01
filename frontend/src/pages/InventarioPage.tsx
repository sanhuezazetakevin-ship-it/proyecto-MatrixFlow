import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { mockInventory } from '../services/mockData';

export const InventarioPage: React.FC = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Control de Inventarios</h1>
        <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mt-1">Existencias y rotación de stock por cada sede comercial</p>
      </div>

      <Card>
        <CardHeader title="Estado de Existencias por Sucursal" />
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-slate-200 font-bold border-b border-slate-200 dark:border-brand-dark">
              <tr>
                <th className="p-3">Sucursal</th>
                <th className="p-3">Producto</th>
                <th className="p-3">Stock Actual</th>
                <th className="p-3">Stock Mínimo</th>
                <th className="p-3">Estado</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-brand-dark/60 text-slate-800 dark:text-slate-200">
              {mockInventory.map((item) => (
                <tr key={item.id} className="hover:bg-slate-100/70 dark:hover:bg-brand-dark/40">
                  <td className="p-3 font-semibold text-slate-900 dark:text-white">{item.branchName}</td>
                  <td className="p-3 font-bold text-slate-900 dark:text-slate-200">{item.productName}</td>
                  <td className="p-3 font-black text-slate-900 dark:text-brand-mint text-sm">{item.quantity} unids</td>
                  <td className="p-3 text-slate-600 dark:text-slate-400 font-medium">{item.minStock} unids</td>
                  <td className="p-3">
                    <Badge variant={item.status === 'OPTIMO' ? 'success' : item.status === 'CRITICO' ? 'danger' : 'warning'}>
                      {item.status}
                    </Badge>
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
