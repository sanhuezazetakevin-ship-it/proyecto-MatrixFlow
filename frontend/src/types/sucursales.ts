
export interface Sucursal {
  id: number;
  empresa_id: number;
  nombre: string;
  codigo: string;
  direccion: string | null;
  ciudad: string | null;
  telefono: string | null;
  activo: boolean;
  created_at: string;
}

export interface SucursalCreate {
  empresa_id: number;
  nombre: string;
  codigo: string;
  direccion?: string;
  ciudad?: string;
  telefono?: string;
}

