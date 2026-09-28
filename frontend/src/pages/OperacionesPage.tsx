import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { mathService } from '../services/api';
import { MathOperationType, MathOperationResult } from '../types';
import { Calculator, Play, CheckCircle2, Clock } from 'lucide-react';

export const OperacionesPage: React.FC = () => {
  const [selectedOp, setSelectedOp] = React.useState<MathOperationType>('PRODUCTO_ESCALAR');
  const [loading, setLoading] = React.useState(false);
  const [result, setResult] = React.useState<MathOperationResult | null>(null);

  const handleExecute = async () => {
    setLoading(true);
    try {
      const res = await mathService.executeOperation({ type: selectedOp });
      setResult(res);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Motor de Operaciones de Álgebra Lineal</h1>
        <p className="text-xs text-slate-500 mt-1">Ejecución de operaciones vectoriales y matriciales procesadas por NumPy</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Controls Column */}
        <Card className="lg:col-span-1 space-y-4">
          <CardHeader title="Configurar Cálculo" subtitle="Selecciona el tipo de operación" />

          <div className="space-y-3 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Operación Matemática</label>
              <select 
                value={selectedOp}
                onChange={(e) => setSelectedOp(e.target.value as MathOperationType)}
                className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 font-medium focus:ring-primary focus:border-primary"
              >
                <option value="PRODUCTO_ESCALAR">Producto Escalar (Ingresos: Cantidades · Precios)</option>
                <option value="RESTA_MATRICES">Resta Matricial (Reales - Metas)</option>
                <option value="TRANSPOSICION_MATRIZ">Transposición Matricial (M^T)</option>
                <option value="SUMA_VECTORES">Suma de Vectores (Acumulado de Ventas)</option>
              </select>
            </div>

            {selectedOp === 'PRODUCTO_ESCALAR' && (
              <div className="p-3 bg-cyan-50 border border-cyan-200 rounded-lg text-cyan-900 text-[11px]">
                <strong>Fórmula:</strong> q · p = ∑ (qi × pi)  
                <br />Multiplica cantidad de productos de una sede por su vector de precios unitarios.
              </div>
            )}

            {selectedOp === 'RESTA_MATRICES' && (
              <div className="p-3 bg-cyan-50 border border-cyan-200 rounded-lg text-cyan-900 text-[11px]">
                <strong>Fórmula:</strong> Q_Real - Q_Meta  
                <br />Calcula la brecha o desviación entre la venta real y la meta en cada sede.
              </div>
            )}

            {selectedOp === 'TRANSPOSICION_MATRIZ' && (
              <div className="p-3 bg-cyan-50 border border-cyan-200 rounded-lg text-cyan-900 text-[11px]">
                <strong>Fórmula:</strong> \(M^T\)  
                <br />Permuta las filas por columnas para cambiar el enfoque analítico.
              </div>
            )}

            <Button 
              onClick={handleExecute} 
              disabled={loading} 
              variant="primary" 
              className="w-full mt-2"
            >
              <Play size={16} />
              <span>{loading ? 'Calculando con NumPy...' : 'Ejecutar Operación'}</span>
            </Button>
          </div>
        </Card>

        {/* Results Column */}
        <Card className="lg:col-span-2 space-y-4">
          <CardHeader title="Resultado del Análisis" subtitle="Salida del motor matemático y explicación analítica" />

          {result ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-emerald-50 border border-emerald-200 rounded-xl">
                <div className="flex items-center gap-2 text-emerald-800 text-xs font-semibold">
                  <CheckCircle2 size={18} className="text-emerald-600" />
                  <span>Operación Procesada Exitosamente</span>
                </div>
                <span className="text-[11px] text-emerald-700 flex items-center gap-1 font-mono">
                  <Clock size={12} /> {result.executionTimeMs} ms
                </span>
              </div>

              {/* Display Result Based on Type */}
              <div className="bg-slate-900 text-slate-100 p-4 rounded-xl font-mono text-xs border border-slate-800">
                <p className="text-[10px] text-slate-400 mb-2">SALIDA MATEMÁTICA:</p>
                {result.resultType === 'ESCALAR' && (
                  <div className="text-3xl font-bold text-accent">
                    S/ {result.resultScalar?.toLocaleString()}
                  </div>
                )}

                {result.resultType === 'VECTOR' && (
                  <div className="flex items-center gap-3">
                    <span className="text-2xl text-slate-500">[</span>
                    {result.resultVector?.map((v, i) => (
                      <span key={i} className="text-accent font-bold text-base">{v}</span>
                    ))}
                    <span className="text-2xl text-slate-500 font-light">]</span>
                  </div>
                )}

                {result.resultType === 'MATRIZ' && (
                  <div className="space-y-1">
                    {result.resultMatrix?.map((row, r) => (
                      <div key={r} className="flex gap-4">
                        {row.map((val, c) => (
                          <span key={c} className={`w-12 text-center font-bold ${val < 0 ? 'text-red-400' : 'text-accent'}`}>
                            {val}
                          </span>
                        ))}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-700">
                <h4 className="font-semibold text-slate-900 mb-1">Explicación Empresarial:</h4>
                <p>{result.explanation}</p>
              </div>
            </div>
          ) : (
            <div className="py-16 text-center text-slate-400 space-y-2">
              <Calculator size={36} className="mx-auto text-slate-300" />
              <p className="text-xs font-medium">Selecciona una operación y presiona "Ejecutar Operación"</p>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};
