import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { mockMatrices } from '../services/mockData';
import { Grid3X3, Plus, Edit2 } from 'lucide-react';

export const MatricesPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Editor & Gestión de Matrices</h1>
          <p className="text-xs text-slate-500 mt-1">Representación matricial multidimensional M (m × n) (Sucursales vs Productos)</p>
        </div>
        <Button variant="primary"><Plus size={16} /> Nueva Matriz</Button>
      </div>

      <div className="space-y-6">
        {mockMatrices.map((m) => (
          <Card key={m.id}>
            <CardHeader 
              title={m.name} 
              subtitle={`Orden ${m.rows} × ${m.cols} (Filas: Sucursales, Columnas: Productos)`}
              action={<Badge variant="success">{`Matriz ${m.rows}x${m.cols}`}</Badge>}
            />

            {/* Matrix 2D Visual Editable Grid */}
            <div className="overflow-x-auto my-3 p-4 bg-slate-900 rounded-xl text-slate-100 font-mono text-xs border border-slate-800">
              <div className="flex items-center gap-2 mb-3 text-slate-400 text-[11px]">
                <Grid3X3 size={16} className="text-accent" />
                <span>CUADRÍCULA MATRICIAL (M_[m × n]):</span>
              </div>

              <table className="w-full text-center border-collapse">
                <thead>
                  <tr className="border-b border-slate-800">
                    <th className="p-2 text-left text-slate-500 font-semibold">Sucursal / Producto</th>
                    {m.colLabels.map((col, idx) => (
                      <th key={idx} className="p-2 text-accent font-semibold">{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {m.values.map((row, rIdx) => (
                    <tr key={rIdx} className="hover:bg-slate-800/40">
                      <td className="p-2 text-left font-medium text-slate-300">{m.rowLabels[rIdx]}</td>
                      {row.map((val, cIdx) => (
                        <td key={cIdx} className="p-2">
                          <input 
                            type="number" 
                            defaultValue={val} 
                            className="w-16 bg-slate-800 text-center font-bold text-white py-1 rounded border border-slate-700 focus:outline-none focus:border-accent text-xs"
                          />
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="flex items-center justify-between text-xs text-slate-500 pt-2">
              <span>Registrada el: {m.createdAt}</span>
              <Button variant="secondary" size="sm">
                <Edit2 size={14} /> Guardar Cambios en Matriz
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
