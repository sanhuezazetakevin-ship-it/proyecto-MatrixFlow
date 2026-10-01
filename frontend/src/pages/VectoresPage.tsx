import React, { useEffect, useState } from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Binary, Plus, Loader2, Edit2, Trash2 } from 'lucide-react';
import { getVectores, createVector } from '../api/vectoresApi';
import type { Vector, VectorCreate } from '../types/vectores';
import { Modal } from '../components/ui/Modal';
import api from '../api/api'; // Necesario para actualizar y eliminar directo si no están en api

export const VectoresPage: React.FC = () => {
  const [vectores, setVectores] = useState<Vector[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  
  const [currentVector, setCurrentVector] = useState<Vector | null>(null);
  
  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    valoresInput: ''
  });

  async function loadVectores() {
    try {
      const data = await getVectores();
      setVectores(data);
    } catch (err: any) {
      console.error(err);
      setError('Error al cargar los vectores.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadVectores();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      // Parsear valores separados por coma
      const valoresNumericos = formData.valoresInput.split(',').map(v => parseFloat(v.trim())).filter(v => !isNaN(v));
      if (valoresNumericos.length === 0) {
        alert("Debe ingresar al menos un valor numérico válido.");
        setSubmitting(false);
        return;
      }

      await createVector({
        nombre: formData.nombre,
        descripcion: formData.descripcion,
        valores: valoresNumericos
      });
      await loadVectores();
      setIsCreateOpen(false);
      setFormData({ nombre: '', descripcion: '', valoresInput: '' });
    } catch (err: any) {
      if (err.response?.status === 403) {
        alert("🔒 Acceso Denegado: No tienes permisos de Operador o Administrador para crear vectores.");
      } else {
        alert("Ocurrió un error al crear el vector.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentVector) return;
    setSubmitting(true);
    try {
      await api.patch(`/api/vectores/${currentVector.id}`, {
        nombre: formData.nombre,
        descripcion: formData.descripcion
      });
      await loadVectores();
      setIsEditOpen(false);
    } catch (err: any) {
      if (err.response?.status === 403) {
        alert("🔒 Acceso Denegado: No tienes permisos para actualizar vectores.");
      } else {
        alert("Ocurrió un error al actualizar el vector.");
      }
    } finally {
      setSubmitting(false);
    }
  };
  
  const handleDelete = async (id: number) => {
    if(!confirm("¿Estás seguro de eliminar este vector?")) return;
    try {
      await api.delete(`/api/vectores/${id}`);
      await loadVectores();
    } catch (err: any) {
      if (err.response?.status === 403) {
        alert("🔒 Acceso Denegado: Solo el Administrador puede eliminar vectores.");
      } else {
        alert("Ocurrió un error al eliminar el vector.");
      }
    }
  };

  const openEdit = (v: Vector) => {
    setCurrentVector(v);
    setFormData({ nombre: v.nombre, descripcion: v.descripcion || '', valoresInput: '' });
    setIsEditOpen(true);
  };

  const openCreate = () => {
    setFormData({ nombre: '', descripcion: '', valoresInput: '' });
    setIsCreateOpen(true);
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Gestión de Vectores</h1>
          <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mt-1">Representación de datos unidimensionales de ventas y precios V (1D)</p>
        </div>
        <Button variant="primary" onClick={openCreate}><Plus size={16} /> Crear Vector</Button>
      </div>

      {loading ? (
        <div className="flex justify-center items-center py-20">
          <Loader2 className="animate-spin text-brand-teal" size={32} />
        </div>
      ) : error ? (
        <div className="bg-red-500/10 border border-red-500/20 text-red-500 p-4 rounded-xl text-sm font-semibold">
          {error}
        </div>
      ) : vectores.length === 0 ? (
        <div className="text-center py-20 text-slate-500 text-sm">
          No hay vectores creados aún.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {vectores.map((v) => (
            <Card key={v.id} className="space-y-4">
              <CardHeader 
                title={v.nombre} 
                subtitle={`Dimensión n = ${v.dimension}`}
                action={
                  <div className="flex items-center gap-2">
                    <Badge variant="info">Vector 1D</Badge>
                    <button onClick={() => handleDelete(v.id)} className="p-1 hover:bg-red-100 dark:hover:bg-red-500/20 text-red-500 rounded transition-colors" title="Eliminar">
                      <Trash2 size={14} />
                    </button>
                  </div>
                }
              />
              
              {/* Visual Vector Representation */}
              <div className="bg-brand-darkest text-slate-100 p-4 rounded-xl font-mono text-xs overflow-x-auto border border-brand-dark shadow-inner">
                <div className="text-[11px] text-brand-mint font-bold mb-2 flex items-center gap-2">
                  <Binary size={14} className="text-brand-mint" />
                  <span>VALORES DEL VECTOR (v):</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-2xl text-slate-500 font-light">[</span>
                  {v.valores.map((val) => (
                    <div key={val.posicion} className="flex flex-col items-center">
                      <span className="text-brand-mint font-black text-base">{Number(val.valor).toFixed(2)}</span>
                      <span className="text-[10px] text-slate-400 font-semibold mt-1">pos {val.posicion}</span>
                    </div>
                  ))}
                  <span className="text-2xl text-slate-500 font-light">]</span>
                </div>
              </div>

              <div className="flex items-center justify-between text-xs text-slate-600 dark:text-slate-400 font-medium pt-1">
                <span>Creado: {new Date(v.created_at).toLocaleDateString()}</span>
                <button onClick={() => openEdit(v)} className="flex items-center gap-1 text-brand-teal dark:text-brand-mint hover:underline font-bold">
                  <Edit2 size={12}/> Editar Vector
                </button>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Modals de CRUD */}
      <Modal isOpen={isCreateOpen} onClose={() => setIsCreateOpen(false)} title="Crear Nuevo Vector">
        <form onSubmit={handleCreate} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Nombre del Vector</label>
            <input required value={formData.nombre} onChange={e => setFormData({...formData, nombre: e.target.value})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white" placeholder="Ej: Ventas Enero" />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Descripción</label>
            <input value={formData.descripcion} onChange={e => setFormData({...formData, descripcion: e.target.value})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white" placeholder="Opcional" />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Valores Numéricos (separados por comas)</label>
            <textarea required value={formData.valoresInput} onChange={e => setFormData({...formData, valoresInput: e.target.value})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white" rows={3} placeholder="150.50, 200, 45, 90.99" />
          </div>
          <div className="pt-2 flex justify-end gap-2">
            <Button variant="secondary" type="button" onClick={() => setIsCreateOpen(false)}>Cancelar</Button>
            <Button variant="primary" type="submit" disabled={submitting}>{submitting ? 'Guardando...' : 'Crear'}</Button>
          </div>
        </form>
      </Modal>

      <Modal isOpen={isEditOpen} onClose={() => setIsEditOpen(false)} title="Actualizar Vector">
        <form onSubmit={handleUpdate} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Nombre del Vector</label>
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
