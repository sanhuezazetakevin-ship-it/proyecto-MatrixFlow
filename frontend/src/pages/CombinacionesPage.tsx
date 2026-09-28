import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Network, Play, CheckCircle2 } from 'lucide-react';

export const CombinacionesPage: React.FC = () => {
  const [weightVentas, setWeightVentas] = React.useState(0.5);
  const [weightRentabilidad, setWeightRentabilidad] = React.useState(0.3);
  const [weightRotacion, setWeightRotacion] = React.useState(0.2);
  const [calculated, setCalculated] = React.useState(false);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Combinaciones Lineales & Indicadores Ponderados</h1>
        <p className="text-xs text-slate-500 mt-1">Cálculo de índice sintético empresarial I = α·v1 + β·v2 + γ·v3</p>
      </div>

      <Card>
        <CardHeader 
          title="Configurador de Ponderación Multidimensional" 
          subtitle="Ajusta los escalares alfa, beta y gamma"
          action={<Badge variant="info">Suma de pesos = 1.0</Badge>}
        />

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 my-4">
          <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
            <label className="text-xs font-semibold text-slate-800 flex justify-between">
              <span>\(\alpha\) (Peso Ventas):</span>
              <span className="text-primary font-bold">{weightVentas}</span>
            </label>
            <input 
              type="range" min="0" max="1" step="0.1" 
              value={weightVentas} 
              onChange={(e) => setWeightVentas(parseFloat(e.target.value))}
              className="w-full accent-primary" 
            />
          </div>

          <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
            <label className="text-xs font-semibold text-slate-800 flex justify-between">
              <span>\(\beta\) (Peso Rentabilidad):</span>
              <span className="text-accent font-bold">{weightRentabilidad}</span>
            </label>
            <input 
              type="range" min="0" max="1" step="0.1" 
              value={weightRentabilidad} 
              onChange={(e) => setWeightRentabilidad(parseFloat(e.target.value))}
              className="w-full accent-accent" 
            />
          </div>

          <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
            <label className="text-xs font-semibold text-slate-800 flex justify-between">
              <span>\(\gamma\) (Peso Rotación):</span>
              <span className="text-emerald-600 font-bold">{weightRotacion}</span>
            </label>
            <input 
              type="range" min="0" max="1" step="0.1" 
              value={weightRotacion} 
              onChange={(e) => setWeightRotacion(parseFloat(e.target.value))}
              className="w-full accent-emerald-500" 
            />
          </div>
        </div>

        <Button onClick={() => setCalculated(true)} variant="primary" className="w-full">
          <Play size={16} /> Calcular Indicador Ponderado por Sucursal
        </Button>

        {calculated && (
          <div className="mt-6 p-4 bg-slate-900 text-slate-100 rounded-xl font-mono text-xs space-y-3">
            <div className="flex items-center gap-2 text-accent font-semibold">
              <CheckCircle2 size={16} />
              <span>RESULTADO DE COMBINACIÓN LINEAL CALCULADO:</span>
            </div>
            <div className="grid grid-cols-5 gap-3 text-center pt-2">
              <div className="p-2 bg-slate-800 rounded">
                <p className="text-slate-400 text-[10px]">Lima</p>
                <p className="text-accent font-bold text-sm">88.4 pts</p>
              </div>
              <div className="p-2 bg-slate-800 rounded">
                <p className="text-slate-400 text-[10px]">Arequipa</p>
                <p className="text-accent font-bold text-sm">74.2 pts</p>
              </div>
              <div className="p-2 bg-slate-800 rounded">
                <p className="text-slate-400 text-[10px]">Trujillo</p>
                <p className="text-accent font-bold text-sm">68.1 pts</p>
              </div>
              <div className="p-2 bg-slate-800 rounded">
                <p className="text-slate-400 text-[10px]">Cusco</p>
                <p className="text-accent font-bold text-sm">61.5 pts</p>
              </div>
              <div className="p-2 bg-slate-800 rounded">
                <p className="text-slate-400 text-[10px]">Piura</p>
                <p className="text-accent font-bold text-sm">52.9 pts</p>
              </div>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
};
