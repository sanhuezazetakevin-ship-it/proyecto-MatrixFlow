import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { mockProducts } from '../services/mockData';
import { Plus, Tag } from 'lucide-react';

export const ProductosPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Catálogo de Productos</h1>
          <p className="text-xs text-slate-500 mt-1">Variables y artículos que conforman la dimensión de las matrices de ventas</p>
        </div>
        <Button variant="primary"><Plus size={16} /> Nuevo Producto</Button>
      </div>

      <Card>
        <CardHeader title="Catálogo de Productos Tec" />
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
              <tr>
                <th className="p-3">SKU / Código</th>
                <th className="p-3">Producto</th>
                <th className="p-3">Precio Unitario</th>
                <th className="p-3">Unidad</th>
                <th className="p-3">Stock Global</th>
                <th className="p-3 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {mockProducts.map((p) => (
                <tr key={p.id} className="hover:bg-slate-50/80">
                  <td className="p-3 font-mono font-semibold text-slate-700">{p.code}</td>
                  <td className="p-3 font-medium text-slate-900 flex items-center gap-2">
                    <Tag size={14} className="text-accent" />
                    {p.name}
                  </td>
                  <td className="p-3 font-semibold text-slate-900">S/ {p.price.toLocaleString()}</td>
                  <td className="p-3 text-slate-500">{p.unit}</td>
                  <td className="p-3 font-medium text-slate-700">{p.stock} unids</td>
                  <td className="p-3 text-right">
                    <button className="text-primary hover:underline font-medium">Editar</button>
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
