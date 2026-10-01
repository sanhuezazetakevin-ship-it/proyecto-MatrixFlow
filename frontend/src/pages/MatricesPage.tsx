import React, { useEffect, useState } from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Grid3X3, Plus, Edit2, Loader2, Trash2 } from 'lucide-react';
import { getMatrices, createMatriz } from '../api/matricesApi';
import type { Matriz } from '../types/matrices';
import { Modal } from '../components/ui/Modal';
import api from '../api/api';

export const MatricesPage: React.FC = () => {
  const [matrices, setMatrices] = useState<Matriz[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  
  const [currentMatriz, setCurrentMatriz] = useState<Matriz | null>(null);
  
  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    valoresInput: ''
  });

  async function loadMatrices() {
    try {
      const data = await getMatrices();
      setMatrices(data);
    } catch (err: any) {
      console.error(err);
      setError('Error al cargar las matrices.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadMatrices();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      // Parsear matriz CSV-like
      const rows = formData.valoresInput.trim().split('\n');
      const valores = rows.map(r => r.split(',').map(v => parseFloat(v.trim())).filter(v => !isNaN(v)));
      
      // Validar dimensiones
      if (valores.length === 0 || valores[0].length === 0) {
        alert("Matriz inválida.");
        setSubmitting(false); return;
      }
      const cols = valores[0].length;
      for (const row of valores) {
        if (row.length !== cols) {
          alert("Todas las filas deben tener la misma cantidad de columnas.");
          setSubmitting(false); return;
        }
      }

      await createMatriz({
        nombre: formData.nombre,
        descripcion: formData.descripcion,
        valores: valores
      });
      await loadMatrices();
      setIsCreateOpen(false);
      setFormData({ nombre: '', descripcion: '', valoresInput: '' });
    } catch (err: any) {
      if (err.response?.status === 403) {
        alert("🔒 Acceso Denegado: No tienes permisos para crear matrices.");
      } else {
        alert("Ocurrió un error al crear la matriz.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentMatriz) return;
    setSubmitting(true);
    try {
      await api.patch(`/api/matrices/${currentMatriz.id}`, {
        nombre: formData.nombre,
        descripcion: formData.descripcion
      });
      await loadMatrices();
      setIsEditOpen(false);
    } catch (err: any) {
      if (err.response?.status === 403) {
        alert("🔒 Acceso Denegado: No tienes permisos para actualizar matrices.");
      } else {
        alert("Ocurrió un error al actualizar.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    if(!confirm("¿Estás seguro de eliminar esta matriz?")) return;
    try {
      await api.delete(`/api/matrices/${id}`);
      await loadMatrices();
    } catch (err: any) {
      if (err.response?.status === 403) {
        alert("🔒 Acceso Denegado: Solo el Administrador puede eliminar.");
      } else {
        alert("Ocurrió un error al eliminar.");
      }
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Editor & Gestión de Matrices</h1>
          <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mt-1">Representación matricial multidimensional M (m × n)</p>
        </div>
        <Button variant="primary" onClick={() => setIsCreateOpen(true)}><Plus size={16} /> Nueva Matriz</Button>
      </div>

      {loading ? (
        <div className="flex justify-center items-center py-20">
          <Loader2 className="animate-spin text-brand-teal" size={32} />
        </div>
      ) : error ? (
        <div className="bg-red-500/10 border border-red-500/20 text-red-500 p-4 rounded-xl text-sm font-semibold">
          {error}
        </div>
      ) : matrices.length === 0 ? (
        <div className="text-center py-20 text-slate-500 text-sm">
          No hay matrices creadas aún.
        </div>
      ) : (
        <div className="space-y-6">
          {matrices.map((m) => {
            const grid: number[][] = Array.from({ length: m.filas }, () => Array(m.columnas).fill(0));
            m.valores.forEach(v => {
              if (v.fila - 1 < m.filas && v.columna - 1 < m.columnas) {
                grid[v.fila - 1][v.columna - 1] = Number(v.valor);
              }
            });

            return (
              <Card key={m.id}>
                <CardHeader 
                  title={m.nombre} 
                  subtitle={`Orden ${m.filas} × ${m.columnas}`}
                  action={
                    <div className="flex items-center gap-2">
                      <Badge variant="success">{`Matriz ${m.filas}x${m.columnas}`}</Badge>
                      <button onClick={() => handleDelete(m.id)} className="p-1 hover:bg-red-100 dark:hover:bg-red-500/20 text-red-500 rounded transition-colors" title="Eliminar">
                        <Trash2 size={14} />
                      </button>
                    </div>
                  }
                />

                <div className="overflow-x-auto my-3 p-4 bg-brand-darkest rounded-xl text-slate-100 font-mono text-xs border border-brand-dark shadow-inner">
                  <div className="flex items-center gap-2 mb-3 text-brand-mint font-bold text-[11px]">
                    <Grid3X3 size={16} className="text-brand-mint" />
                    <span>CUADRÍCULA MATRICIAL (M_[m × n]):</span>
                  </div>
                  <table className="w-full text-center border-collapse">
                    <thead>
                      <tr className="border-b border-brand-dark">
                        <th className="p-2 text-left text-slate-400 font-semibold">Fila / Columna</th>
                        {Array.from({ length: m.columnas }).map((_, cIdx) => (
                          <th key={cIdx} className="p-2 text-brand-mint font-bold">Col {cIdx + 1}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-brand-dark/60">
                      {grid.map((row, rIdx) => (
                        <tr key={rIdx} className="hover:bg-brand-dark/40">
                          <td className="p-2 text-left font-bold text-slate-200">Fila {rIdx + 1}</td>
                          {row.map((val, cIdx) => (
                            <td key={cIdx} className="p-2">
                              <span className="w-16 bg-brand-darker inline-block text-center font-black text-brand-mint py-1 rounded-lg border border-brand-dark text-xs">{val}</span>
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <div className="flex items-center justify-between text-xs text-slate-600 dark:text-slate-400 font-medium pt-2">
                  <span>Registrada el: {new Date(m.created_at).toLocaleDateString()}</span>
                  <Button variant="secondary" size="sm" onClick={() => { setCurrentMatriz(m); setFormData({...formData, nombre: m.nombre, descripcion: m.descripcion||''}); setIsEditOpen(true); }}>
                    <Edit2 size={14} /> Editar Detalles
                  </Button>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      {/* Modals */}
      <Modal isOpen={isCreateOpen} onClose={() => setIsCreateOpen(false)} title="Crear Nueva Matriz">
        <form onSubmit={handleCreate} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Nombre</label>
            <input required value={formData.nombre} onChange={e => setFormData({...formData, nombre: e.target.value})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white" />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Descripción</label>
            <input value={formData.descripcion} onChange={e => setFormData({...formData, descripcion: e.target.value})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white" />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Valores (Filas separadas por línea, columnas por coma)</label>
            <textarea required value={formData.valoresInput} onChange={e => setFormData({...formData, valoresInput: e.target.value})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs font-mono focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white" rows={4} placeholder="1, 2, 3&#10;4, 5, 6" />
            <p className="text-[10px] text-slate-500 mt-1">Ejemplo para 2x3: Dos líneas, tres números separados por coma en cada línea.</p>
          </div>
          <div className="pt-2 flex justify-end gap-2">
            <Button variant="secondary" type="button" onClick={() => setIsCreateOpen(false)}>Cancelar</Button>
            <Button variant="primary" type="submit" disabled={submitting}>{submitting ? 'Guardando...' : 'Crear Matriz'}</Button>
          </div>
        </form>
      </Modal>

      <Modal isOpen={isEditOpen} onClose={() => setIsEditOpen(false)} title="Editar Matriz">
        <form onSubmit={handleUpdate} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Nombre</label>
            <input required value={formData.nombre} onChange={e => setFormData({...formData, nombre: e.target.value})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white" />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Descripción</label>
            <input value={formData.descripcion} onChange={e => setFormData({...formData, descripcion: e.target.value})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white" />
          </div>
          <div className="pt-2 flex justify-end gap-2">
            <Button variant="secondary" type="button" onClick={() => setIsEditOpen(false)}>Cancelar</Button>
            <Button variant="primary" type="submit" disabled={submitting}>{submitting ? 'Guardando...' : 'Actualizar'}</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
