
import api from "./api";
import { Matriz, MatrizCreate } from "../types/matrices";

export async function getMatrices(): Promise<Matriz[]> {
  const response = await api.get<Matriz[]>("/api/matrices/");
  return response.data;
}

export async function createMatriz(data: MatrizCreate): Promise<Matriz> {
  const response = await api.post<Matriz>("/api/matrices/", data);
  return response.data;
}

export async function deleteMatriz(id: number): Promise<void> {
  await api.delete(`/api/matrices/${id}`);
}
