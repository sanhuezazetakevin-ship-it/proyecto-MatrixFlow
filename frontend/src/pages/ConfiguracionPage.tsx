import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Save, Server, Sliders } from 'lucide-react';

export const ConfiguracionPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Configuración del Sistema</h1>
        <p className="text-xs text-slate-500 mt-1">Parámetros del motor matemático y conexión con la API de FastAPI</p>
      </div>

      <Card className="space-y-4">
        <CardHeader title="Parámetros Globales" subtitle="Configuración de FastAPI + NumPy" />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div>
            <label className="block font-semibold text-slate-700 mb-1">URL de API Backend (FastAPI)</label>
            <input 
              type="text" 
              defaultValue="http://localhost:8000/api/v1"
              className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 font-mono"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Tolerancia Decimal NumPy</label>
            <input 
              type="number" 
              defaultValue={4}
              className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800"
            />
          </div>
        </div>

        <Button variant="primary"><Save size={16} /> Guardar Parámetros</Button>
      </Card>
    </div>
  );
};
