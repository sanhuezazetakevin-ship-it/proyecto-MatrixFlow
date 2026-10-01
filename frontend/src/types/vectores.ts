
export interface VectorValor {
  posicion: number;
  valor: number;
}

export interface Vector {
  id: number;
  nombre: string;
  descripcion: string | null;
  dimension: number;
  usuario_id: number;
  created_at: string;
  valores: VectorValor[];
}

export interface VectorCreate {
  nombre: string;
  descripcion?: string;
  valores: number[];
}
