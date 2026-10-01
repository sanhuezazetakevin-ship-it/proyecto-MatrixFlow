
export interface MatrizValor {
  fila: number;
  columna: number;
  valor: number;
}

export interface Matriz {
  id: number;
  nombre: string;
  descripcion: string | null;
  filas: number;
  columnas: number;
  usuario_id: number;
  created_at: string;
  valores: MatrizValor[];
}

export interface MatrizCreate {
  nombre: string;
  descripcion?: string;
  valores: number[][];
}
