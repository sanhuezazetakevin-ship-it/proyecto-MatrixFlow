import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { mockBranches } from '../services/mockData';
import { MapPin, Plus } from 'lucide-react';

export const SucursalesPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Gestión de Sucursales</h1>
          <p className="text-xs text-slate-500 mt-1">Administración de sedes operativas y nodos de origen de vectores</p>
        </div>
        <Button variant="primary"><Plus size={16} /> Nueva Sucursal</Button>
      </div>

      <Card>
        <CardHeader title="Sedes Empresariales Registradas" />
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
              <tr>
                <th className="p-3">Código</th>
                <th className="p-3">Nombre Sucursal</th>
                <th className="p-3">Ciudad</th>
                <th className="p-3">Dirección</th>
                <th className="p-3 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {mockBranches.map((b) => (
                <tr key={b.id} className="hover:bg-slate-50/80">
                  <td className="p-3 font-mono font-semibold text-primary">{b.code}</td>
                  <td className="p-3 font-medium text-slate-900 flex items-center gap-2">
                    <MapPin size={14} className="text-slate-400" />
                    {b.name}
                  </td>
                  <td className="p-3 text-slate-600">{b.city}</td>
                  <td className="p-3 text-slate-600">{b.address}</td>
                  <td className="p-3 text-right">
                    <button className="text-primary hover:underline font-medium text-xs">Editar</button>
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
