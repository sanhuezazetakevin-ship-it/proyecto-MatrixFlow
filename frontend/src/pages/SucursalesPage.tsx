import React, { useEffect, useState } from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { MapPin, Plus, Loader2 } from 'lucide-react';
import { PeruMap } from '../components/PeruMap';
import { getSucursales, createSucursal } from '../api/sucursalesApi';
import type { Sucursal } from '../types/sucursales';
import { Modal } from '../components/ui/Modal';
import { mockBranches } from '../services/mockData';

import api from '../api/api';

export const SucursalesPage: React.FC = () => {
  const [sucursales, setSucursales] = useState<Sucursal[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  
  const [currentSucursal, setCurrentSucursal] = useState<Sucursal | null>(null);
  
  const [formData, setFormData] = useState({
    codigo: '',
    nombre: '',
    ciudad: '',
    direccion: ''
  });
  const [submitting, setSubmitting] = useState(false);

  async function load() {
    try {
      const data = await getSucursales();
      const apiCities = new Set((data || []).map(d => d.ciudad?.toUpperCase()));
      
      const demoBranches = mockBranches
        .filter(b => !apiCities.has(b.city.toUpperCase()))
        .map(b => ({
          id: b.id as any,
          empresa_id: 1,
          nombre: b.name,
          codigo: b.code,
          ciudad: b.city,
          direccion: b.address,
          telefono: null,
          activo: true,
          created_at: new Date().toISOString()
        }));
        
      setSucursales([...(data || []), ...demoBranches]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await createSucursal({
        empresa_id: 1,
        codigo: formData.codigo,
        nombre: formData.nombre,
        ciudad: formData.ciudad,
        direccion: formData.direccion
      });
      await load();
      setIsModalOpen(false);
      setFormData({ codigo: '', nombre: '', ciudad: '', direccion: '' });
    } catch (err: any) {
      if (err.response?.status === 403) {
        alert("🔒 Acceso Denegado: Necesitas rol de Operador o Admin para crear.");
      } else {
        alert("Error al crear sucursal.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if(!currentSucursal) return;
    
    // Prevent updating mock data
    if (currentSucursal.id > 1000) {
      alert("No puedes editar los datos de demostración, crea una sucursal real primero.");
      return;
    }
    
    setSubmitting(true);
    try {
      await api.patch(`/api/sucursales/${currentSucursal.id}`, {
        nombre: formData.nombre,
        codigo: formData.codigo,
        ciudad: formData.ciudad,
        direccion: formData.direccion
      });
      await load();
      setIsEditOpen(false);
    } catch (err: any) {
      if (err.response?.status === 403) {
        alert("🔒 Acceso Denegado: Necesitas rol de Operador o Admin para editar.");
      } else {
        alert("Error al actualizar sucursal.");
      }
    } finally {
      setSubmitting(false);
    }
  };


  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Gestión de Sucursales</h1>
          <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mt-1">Administración de sedes operativas y nodos de origen de vectores</p>
        </div>
        <Button variant="primary" onClick={() => setIsModalOpen(true)}>
          <Plus size={16} /> Nueva Sucursal
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        <div className="lg:col-span-2">
          <Card>
            <CardHeader title="Sedes Empresariales (Nivel Perú)" />
            <div className="overflow-x-auto min-h-[300px]">
              {loading ? (
                <div className="flex justify-center items-center py-20">
                  <Loader2 className="animate-spin text-brand-teal" size={32} />
                </div>
              ) : sucursales.length === 0 ? (
                <div className="text-center py-10 text-slate-500 text-sm">
                  No hay sucursales creadas.
                </div>
              ) : (
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-slate-200 font-bold border-b border-slate-200 dark:border-brand-dark">
                    <tr>
                      <th className="p-3">Código</th>
                      <th className="p-3">Nombre Sucursal</th>
                      <th className="p-3">Ciudad / Distrito</th>
                      <th className="p-3">Dirección</th>
                      <th className="p-3 text-right">Acciones</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200 dark:divide-brand-dark/60 text-slate-800 dark:text-slate-200">
                    {sucursales.map((b) => (
                      <tr key={b.id} className="hover:bg-slate-100/70 dark:hover:bg-brand-dark/40">
                        <td className="p-3 font-mono font-bold text-brand-teal dark:text-brand-mint">{b.codigo}</td>
                        <td className="p-3 font-semibold text-slate-900 dark:text-white flex items-center gap-2">
                          <MapPin size={14} className="text-brand-teal dark:text-brand-mint" />
                          {b.nombre}
                          {!b.activo && <span className="ml-1 px-1.5 py-0.5 bg-red-500/10 text-red-500 text-[9px] rounded-full">Inactiva</span>}
                        </td>
                        <td className="p-3 font-medium text-slate-700 dark:text-slate-300">{b.ciudad || '-'}</td>
                        <td className="p-3 font-medium text-slate-700 dark:text-slate-300">{b.direccion || '-'}</td>
                        <td className="p-3 text-right">
                          <button 
                            onClick={() => {
                              setCurrentSucursal(b);
                              setFormData({ codigo: b.codigo, nombre: b.nombre, ciudad: b.ciudad||'', direccion: b.direccion||'' });
                              setIsEditOpen(true);
                            }}
                            className="text-brand-teal dark:text-brand-mint hover:underline font-bold"
                          >
                            Editar
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </Card>
        </div>
        
        {/* Mapa de Sucursales */}
        <div className="lg:col-span-1 h-full">
          <PeruMap sucursales={sucursales} />
        </div>
      </div>

      {/* Modal Nueva Sucursal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Crear Nueva Sucursal">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Código de Sede</label>
            <input required maxLength={10} value={formData.codigo} onChange={e => setFormData({...formData, codigo: e.target.value})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white" placeholder="Ej: LIMA-01" />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Nombre</label>
            <input required value={formData.nombre} onChange={e => setFormData({...formData, nombre: e.target.value})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white" placeholder="Sucursal Principal" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Ciudad (Mapa)</label>
              <input required value={formData.ciudad} onChange={e => setFormData({...formData, ciudad: e.target.value.toUpperCase()})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white uppercase" placeholder="LIMA" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Dirección / Distrito</label>
              <input value={formData.direccion} onChange={e => setFormData({...formData, direccion: e.target.value})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white" placeholder="Av. Central 123" />
            </div>
          </div>
          <div className="pt-2 flex justify-end gap-2">
            <Button variant="secondary" type="button" onClick={() => setIsModalOpen(false)}>Cancelar</Button>
            <Button variant="primary" type="submit" disabled={submitting}>{submitting ? 'Guardando...' : 'Guardar Sucursal'}</Button>
          </div>
        </form>
      </Modal>

      {/* Modal Editar Sucursal */}
      <Modal isOpen={isEditOpen} onClose={() => setIsEditOpen(false)} title="Editar Sucursal">
        <form onSubmit={handleUpdate} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Código de Sede</label>
            <input required maxLength={10} value={formData.codigo} onChange={e => setFormData({...formData, codigo: e.target.value})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white" />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Nombre</label>
            <input required value={formData.nombre} onChange={e => setFormData({...formData, nombre: e.target.value})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Ciudad (Mapa)</label>
              <input required value={formData.ciudad} onChange={e => setFormData({...formData, ciudad: e.target.value.toUpperCase()})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white uppercase" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Dirección / Distrito</label>
              <input value={formData.direccion} onChange={e => setFormData({...formData, direccion: e.target.value})} className="w-full px-3 py-2 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-dark rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-brand-teal text-slate-800 dark:text-white" />
            </div>
          </div>
          <div className="pt-2 flex justify-end gap-2">
            <Button variant="secondary" type="button" onClick={() => setIsEditOpen(false)}>Cancelar</Button>
            <Button variant="primary" type="submit" disabled={submitting}>{submitting ? 'Guardando...' : 'Actualizar Sucursal'}</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
