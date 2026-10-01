import React, { useEffect } from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Calculator, Play, CheckCircle2, Clock } from 'lucide-react';
import { getVectores } from '../api/vectoresApi';
import { getMatrices } from '../api/matricesApi';
import api from '../api/api';

export const OperacionesPage: React.FC = () => {
  const [selectedOp, setSelectedOp] = React.useState<string>('PRODUCTO_ESCALAR');
  const [loading, setLoading] = React.useState(false);
  const [result, setResult] = React.useState<any>(null);
  
  const [vectores, setVectores] = React.useState<any[]>([]);
  const [matrices, setMatrices] = React.useState<any[]>([]);
  
  const [vectorA, setVectorA] = React.useState<string>('');
  const [vectorB, setVectorB] = React.useState<string>('');
  const [matrizA, setMatrizA] = React.useState<string>('');
  const [matrizB, setMatrizB] = React.useState<string>('');

  useEffect(() => {
    async function load() {
      try {
        const [vecs, mats] = await Promise.all([getVectores(), getMatrices()]);
        setVectores(vecs);
        setMatrices(mats);
        if (vecs.length >= 2) { setVectorA(String(vecs[0].id)); setVectorB(String(vecs[1].id)); }
        else if (vecs.length === 1) { setVectorA(String(vecs[0].id)); setVectorB(String(vecs[0].id)); }
        if (mats.length >= 2) { setMatrizA(String(mats[0].id)); setMatrizB(String(mats[1].id)); }
        else if (mats.length === 1) { setMatrizA(String(mats[0].id)); setMatrizB(String(mats[0].id)); }
      } catch (err) { console.error(err); }
    }
    load();
  }, []);

  const handleExecute = async () => {
    setLoading(true);
    setResult(null);
    try {
      let res;
      const t0 = performance.now();
      
      if (selectedOp === 'PRODUCTO_ESCALAR') {
        res = await api.post('/api/operaciones/producto-punto/vector', { vector_a_id: Number(vectorA), vector_b_id: Number(vectorB) });
      } else if (selectedOp === 'RESTA_MATRICES') {
        res = await api.post('/api/operaciones/resta/matriz', { matriz_a_id: Number(matrizA), matriz_b_id: Number(matrizB) });
      } else if (selectedOp === 'TRANSPOSICION_MATRIZ') {
        res = await api.post('/api/operaciones/transposicion/matriz', { matriz_id: Number(matrizA) });
      } else if (selectedOp === 'SUMA_VECTORES') {
        res = await api.post('/api/operaciones/suma/vector', { vector_a_id: Number(vectorA), vector_b_id: Number(vectorB) });
      }
      
      const t1 = performance.now();
      setResult({ ...res?.data, executionTimeMs: Math.round(t1 - t0) });
    } catch (err: any) {
      if (err.response?.status === 403) {
        alert("🔒 Acceso Denegado: No tienes permisos para ejecutar operaciones matemáticas.");
      } else if (err.response?.status === 400 || err.response?.status === 422) {
        alert(`Error matemático o de validación: ${err.response.data?.detail || 'Dimensiones incompatibles'}`);
      } else {
        alert("Ocurrió un error al ejecutar la operación.");
      }
    } finally {
      setLoading(false);
    }
  };

  const renderOperandSelectors = () => {
    if (selectedOp === 'PRODUCTO_ESCALAR' || selectedOp === 'SUMA_VECTORES') {
      return (
        <div className="space-y-2 mt-4 p-3 bg-slate-50 dark:bg-brand-darker rounded-xl border border-slate-200 dark:border-brand-dark">
          <label className="block font-semibold text-slate-700 dark:text-slate-300">Seleccionar Vectores</label>
          <select value={vectorA} onChange={e => setVectorA(e.target.value)} className="w-full p-2 bg-white dark:bg-brand-dark rounded border border-slate-300 dark:border-brand-dark mb-2">
            {vectores.map(v => <option key={v.id} value={v.id}>{v.nombre} (dim: {v.dimension})</option>)}
          </select>
          <select value={vectorB} onChange={e => setVectorB(e.target.value)} className="w-full p-2 bg-white dark:bg-brand-dark rounded border border-slate-300 dark:border-brand-dark">
            {vectores.map(v => <option key={v.id} value={v.id}>{v.nombre} (dim: {v.dimension})</option>)}
          </select>
        </div>
      );
    }
    
    if (selectedOp === 'RESTA_MATRICES') {
      return (
        <div className="space-y-2 mt-4 p-3 bg-slate-50 dark:bg-brand-darker rounded-xl border border-slate-200 dark:border-brand-dark">
          <label className="block font-semibold text-slate-700 dark:text-slate-300">Seleccionar Matrices</label>
          <select value={matrizA} onChange={e => setMatrizA(e.target.value)} className="w-full p-2 bg-white dark:bg-brand-dark rounded border border-slate-300 dark:border-brand-dark mb-2">
            {matrices.map(m => <option key={m.id} value={m.id}>{m.nombre} ({m.filas}x{m.columnas})</option>)}
          </select>
          <select value={matrizB} onChange={e => setMatrizB(e.target.value)} className="w-full p-2 bg-white dark:bg-brand-dark rounded border border-slate-300 dark:border-brand-dark">
            {matrices.map(m => <option key={m.id} value={m.id}>{m.nombre} ({m.filas}x{m.columnas})</option>)}
          </select>
        </div>
      );
    }

    if (selectedOp === 'TRANSPOSICION_MATRIZ') {
      return (
        <div className="space-y-2 mt-4 p-3 bg-slate-50 dark:bg-brand-darker rounded-xl border border-slate-200 dark:border-brand-dark">
          <label className="block font-semibold text-slate-700 dark:text-slate-300">Seleccionar Matriz</label>
          <select value={matrizA} onChange={e => setMatrizA(e.target.value)} className="w-full p-2 bg-white dark:bg-brand-dark rounded border border-slate-300 dark:border-brand-dark">
            {matrices.map(m => <option key={m.id} value={m.id}>{m.nombre} ({m.filas}x{m.columnas})</option>)}
          </select>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Motor de Operaciones de Álgebra Lineal</h1>
        <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mt-1">Ejecución de operaciones vectoriales y matriciales procesadas por FastAPI backend</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1 space-y-4">
          <CardHeader title="Configurar Cálculo" subtitle="Selecciona el tipo de operación" />

          <div className="space-y-3 text-xs">
            <div>
              <label className="block font-bold text-slate-800 dark:text-slate-200 mb-1">Operación Matemática</label>
              <select 
                value={selectedOp}
                onChange={(e) => setSelectedOp(e.target.value)}
                className="w-full p-2.5 bg-slate-100 dark:bg-brand-dark border border-slate-300 dark:border-brand-dark rounded-xl text-slate-900 dark:text-slate-100 font-bold focus:ring-brand-teal focus:border-brand-teal"
              >
                <option value="PRODUCTO_ESCALAR">Producto Punto (Vectores)</option>
                <option value="SUMA_VECTORES">Suma de Vectores</option>
                <option value="RESTA_MATRICES">Resta Matricial</option>
                <option value="TRANSPOSICION_MATRIZ">Transposición Matricial (M^T)</option>
              </select>
            </div>

            {renderOperandSelectors()}

            <Button 
              onClick={handleExecute} 
              disabled={loading || (vectores.length === 0 && matrices.length === 0)} 
              variant="primary" 
              className="w-full py-2.5 mt-2"
            >
              <Play size={16} />
              <span>{loading ? 'Calculando en Servidor...' : 'Ejecutar Operación'}</span>
            </Button>
            {(vectores.length === 0 && matrices.length === 0) && <p className="text-red-500 text-[10px] text-center">Debes crear vectores/matrices primero.</p>}
          </div>
        </Card>

        <Card className="lg:col-span-2 space-y-4">
          <CardHeader title="Resultado del Análisis" subtitle="Salida del motor matemático y explicación analítica" />

          {result ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-emerald-100 dark:bg-emerald-950/60 border border-emerald-300 dark:border-emerald-800 rounded-xl">
                <div className="flex items-center gap-2 text-emerald-900 dark:text-emerald-300 text-xs font-bold">
                  <CheckCircle2 size={18} className="text-emerald-600 dark:text-emerald-400" />
                  <span>Operación Procesada Exitosamente</span>
                </div>
                <span className="text-[11px] text-emerald-800 dark:text-emerald-400 flex items-center gap-1 font-mono font-bold">
                  <Clock size={12} /> {result.executionTimeMs} ms en Servidor
                </span>
              </div>

              <div className="bg-brand-darkest text-slate-100 p-4 rounded-xl font-mono text-xs border border-brand-dark shadow-inner overflow-x-auto">
                <p className="text-[10px] text-brand-mint font-bold mb-2">SALIDA MATEMÁTICA ({result.resultado?.tipo_resultado || 'DESCONOCIDO'}):</p>
                
                {result.resultado?.tipo_resultado === 'ESCALAR' && (
                  <div className="text-3xl font-black text-brand-mint">
                    {result.resultado.datos}
                  </div>
                )}

                {result.resultado?.tipo_resultado === 'VECTOR' && Array.isArray(result.resultado.datos) && (
                  <div className="flex items-center gap-3">
                    <span className="text-2xl text-slate-500">[</span>
                    {result.resultado.datos.map((v: any, i: number) => (
                      <span key={i} className="text-brand-mint font-bold text-base">{Number(v).toFixed(2)}</span>
                    ))}
                    <span className="text-2xl text-slate-500 font-light">]</span>
                  </div>
                )}

                {result.resultado?.tipo_resultado === 'MATRIZ' && Array.isArray(result.resultado.datos) && (
                  <div className="space-y-1">
                    {result.resultado.datos.map((row: any[], r: number) => (
                      <div key={r} className="flex gap-4">
                        {row.map((val: any, c: number) => (
                          <span key={c} className={`w-12 text-center font-bold ${val < 0 ? 'text-red-400' : 'text-brand-mint'}`}>
                            {Number(val).toFixed(2)}
                          </span>
                        ))}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="py-16 text-center text-slate-500 dark:text-slate-400 space-y-2">
              <Calculator size={36} className="mx-auto text-slate-400 dark:text-slate-500" />
              <p className="text-xs font-bold">Selecciona una operación y operandos para ejecutar</p>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};
