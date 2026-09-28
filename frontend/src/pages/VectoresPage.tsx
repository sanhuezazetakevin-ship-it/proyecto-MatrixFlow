import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { mockVectors } from '../services/mockData';
import { Binary, Plus } from 'lucide-react';

export const VectoresPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Gestión de Vectores</h1>
          <p className="text-xs text-slate-500 mt-1">Representación de datos unidimensionales de ventas y precios V (1D)</p>
        </div>
        <Button variant="primary"><Plus size={16} /> Crear Vector</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {mockVectors.map((v) => (
          <Card key={v.id} className="space-y-4">
            <CardHeader 
              title={v.name} 
              subtitle={`Dimensión n = ${v.dimension}`}
              action={<Badge variant="info">Vector 1D</Badge>}
            />
            
            {/* Visual Vector Representation */}
            <div className="bg-slate-900 text-slate-100 p-4 rounded-xl font-mono text-xs overflow-x-auto border border-slate-800">
              <div className="text-[10px] text-slate-400 mb-2 flex items-center gap-2">
                <Binary size={14} className="text-accent" />
                <span>VALORES DEL VECTOR (v):</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-2xl text-slate-500 font-light">[</span>
                {v.values.map((val, idx) => (
                  <div key={idx} className="flex flex-col items-center">
                    <span className="text-accent font-bold text-sm">{val}</span>
                    <span className="text-[10px] text-slate-400 mt-1">{v.labels[idx]}</span>
                  </div>
                ))}
                <span className="text-2xl text-slate-500 font-light">]</span>
              </div>
            </div>

            <div className="flex items-center justify-between text-xs text-slate-500 pt-1">
              <span>Creado: {v.createdAt}</span>
              <button className="text-primary hover:underline font-medium">Editar Vector</button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
