import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { mockProducts } from '../services/mockData';
import { Plus, Tag } from 'lucide-react';

export const ProductosPage: React.FC = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="matrix-card-title text-2xl font-extrabold">Catálogo de Productos</h1>
          <p className="matrix-card-subtitle text-xs font-semibold mt-1">Variables y artículos que conforman la dimensión de las matrices de ventas</p>
        </div>
        <Button variant="primary"><Plus size={16} /> Nuevo Producto</Button>
      </div>

      <Card>
        <CardHeader title="Catálogo de Productos Tech" />
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="matrix-table-head font-extrabold">
              <tr>
                <th className="p-3">SKU / Código</th>
                <th className="p-3">Producto</th>
                <th className="p-3">Precio Unitario</th>
                <th className="p-3">Unidad</th>
                <th className="p-3">Stock Global</th>
                <th className="p-3 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-brand-dark">
              {mockProducts.map((p) => (
                <tr key={p.id} className="matrix-table-row font-semibold hover:opacity-90">
                  <td className="p-3 font-mono font-bold">{p.code}</td>
                  <td className="p-3 font-bold flex items-center gap-2">
                    <Tag size={14} className="text-brand-teal dark:text-brand-mint" />
                    {p.name}
                  </td>
                  <td className="p-3 font-black text-brand-teal dark:text-brand-mint">S/ {p.price.toLocaleString()}</td>
                  <td className="p-3 opacity-80">{p.unit}</td>
                  <td className="p-3 font-bold">{p.stock} unids</td>
                  <td className="p-3 text-right">
                    <button className="text-brand-teal dark:text-brand-mint hover:underline font-bold">Editar</button>
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
