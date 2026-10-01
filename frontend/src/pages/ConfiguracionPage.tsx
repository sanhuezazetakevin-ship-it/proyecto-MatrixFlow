import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Save } from 'lucide-react';

export const ConfiguracionPage: React.FC = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Configuración del Sistema</h1>
        <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mt-1">Parámetros del motor matemático y conexión con la API de FastAPI</p>
      </div>

      <Card className="space-y-4">
        <CardHeader title="Parámetros Globales" subtitle="Configuración de FastAPI + NumPy" />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div>
            <label className="block font-bold text-slate-800 dark:text-slate-200 mb-1">URL de API Backend (FastAPI)</label>
            <input 
              type="text" 
              defaultValue="http://localhost:8000/api/v1"
              className="w-full p-2.5 bg-slate-100 dark:bg-brand-dark border border-slate-300 dark:border-brand-dark rounded-xl text-slate-900 dark:text-slate-100 font-mono font-bold"
            />
          </div>

          <div>
            <label className="block font-bold text-slate-800 dark:text-slate-200 mb-1">Tolerancia Decimal NumPy</label>
            <input 
              type="number" 
              defaultValue={4}
              className="w-full p-2.5 bg-slate-100 dark:bg-brand-dark border border-slate-300 dark:border-brand-dark rounded-xl text-slate-900 dark:text-slate-100 font-bold"
            />
          </div>
        </div>

        <Button variant="primary"><Save size={16} /> Guardar Parámetros</Button>
      </Card>
    </div>
  );
};
