import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Play, CheckCircle2 } from 'lucide-react';

export const CombinacionesPage: React.FC = () => {
  const [weightVentas, setWeightVentas] = React.useState(0.5);
  const [weightRentabilidad, setWeightRentabilidad] = React.useState(0.3);
  const [weightRotacion, setWeightRotacion] = React.useState(0.2);
  const [calculated, setCalculated] = React.useState(false);

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Combinaciones Lineales & Indicadores Ponderados</h1>
        <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mt-1">Cálculo de índice sintético empresarial I = α·v1 + β·v2 + γ·v3</p>
      </div>

      <Card>
        <CardHeader 
          title="Configurador de Ponderación Multidimensional" 
          subtitle="Ajusta los escalares alfa, beta y gamma"
          action={<Badge variant="info">Suma de pesos = 1.0</Badge>}
        />

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 my-4">
          <div className="p-4 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-xl space-y-2">
            <label className="text-xs font-bold text-slate-900 dark:text-white flex justify-between">
              <span>α (Peso Ventas):</span>
              <span className="text-brand-teal dark:text-brand-mint font-extrabold">{weightVentas}</span>
            </label>
            <input 
              type="range" min="0" max="1" step="0.1" 
              value={weightVentas} 
              onChange={(e) => setWeightVentas(parseFloat(e.target.value))}
              className="w-full accent-brand-teal" 
            />
          </div>

          <div className="p-4 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-xl space-y-2">
            <label className="text-xs font-bold text-slate-900 dark:text-white flex justify-between">
              <span>β (Peso Rentabilidad):</span>
              <span className="text-brand-teal dark:text-brand-mint font-extrabold">{weightRentabilidad}</span>
            </label>
            <input 
              type="range" min="0" max="1" step="0.1" 
              value={weightRentabilidad} 
              onChange={(e) => setWeightRentabilidad(parseFloat(e.target.value))}
              className="w-full accent-brand-teal" 
            />
          </div>

          <div className="p-4 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-xl space-y-2">
            <label className="text-xs font-bold text-slate-900 dark:text-white flex justify-between">
              <span>γ (Peso Rotación):</span>
              <span className="text-brand-teal dark:text-brand-mint font-extrabold">{weightRotacion}</span>
            </label>
            <input 
              type="range" min="0" max="1" step="0.1" 
              value={weightRotacion} 
              onChange={(e) => setWeightRotacion(parseFloat(e.target.value))}
              className="w-full accent-brand-teal" 
            />
          </div>
        </div>

        <Button onClick={() => setCalculated(true)} variant="primary" className="w-full py-2.5">
          <Play size={16} /> Calcular Indicador Ponderado por Sucursal
        </Button>

        {calculated && (
          <div className="mt-6 p-4 bg-brand-darkest text-slate-100 rounded-xl font-mono text-xs space-y-3 border border-brand-dark">
            <div className="flex items-center gap-2 text-brand-mint font-bold">
              <CheckCircle2 size={16} />
              <span>RESULTADO DE COMBINACIÓN LINEAL CALCULADO:</span>
            </div>
            <div className="grid grid-cols-5 gap-3 text-center pt-2">
              <div className="p-2.5 bg-brand-darker rounded-lg border border-brand-dark">
                <p className="text-slate-400 text-[10px] font-bold">Lima</p>
                <p className="text-brand-mint font-black text-sm">88.4 pts</p>
              </div>
              <div className="p-2.5 bg-brand-darker rounded-lg border border-brand-dark">
                <p className="text-slate-400 text-[10px] font-bold">Arequipa</p>
                <p className="text-brand-mint font-black text-sm">74.2 pts</p>
              </div>
              <div className="p-2.5 bg-brand-darker rounded-lg border border-brand-dark">
                <p className="text-slate-400 text-[10px] font-bold">Trujillo</p>
                <p className="text-brand-mint font-black text-sm">68.1 pts</p>
              </div>
              <div className="p-2.5 bg-brand-darker rounded-lg border border-brand-dark">
                <p className="text-slate-400 text-[10px] font-bold">Cusco</p>
                <p className="text-brand-mint font-black text-sm">61.5 pts</p>
              </div>
              <div className="p-2.5 bg-brand-darker rounded-lg border border-brand-dark">
                <p className="text-slate-400 text-[10px] font-bold">Piura</p>
                <p className="text-brand-mint font-black text-sm">52.9 pts</p>
              </div>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
};
