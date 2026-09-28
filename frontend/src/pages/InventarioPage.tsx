import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { mockInventory } from '../services/mockData';

export const InventarioPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Control de Inventarios</h1>
        <p className="text-xs text-slate-500 mt-1">Existencias y rotación de stock por cada sede comercial</p>
      </div>

      <Card>
        <CardHeader title="Estado de Existencias por Sucursal" />
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
              <tr>
                <th className="p-3">Sucursal</th>
                <th className="p-3">Producto</th>
                <th className="p-3">Stock Actual</th>
                <th className="p-3">Stock Mínimo</th>
                <th className="p-3">Estado</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {mockInventory.map((item) => (
                <tr key={item.id} className="hover:bg-slate-50/80">
                  <td className="p-3 font-medium text-slate-800">{item.branchName}</td>
                  <td className="p-3 text-slate-900">{item.productName}</td>
                  <td className="p-3 font-bold text-slate-900">{item.quantity} unids</td>
                  <td className="p-3 text-slate-500">{item.minStock} unids</td>
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
