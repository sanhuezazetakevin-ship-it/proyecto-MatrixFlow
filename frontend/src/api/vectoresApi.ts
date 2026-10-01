
import api from "./api";
import { Vector, VectorCreate } from "../types/vectores";

export async function getVectores(): Promise<Vector[]> {
  const response = await api.get<Vector[]>("/api/vectores/");
  return response.data;
}

export async function createVector(data: VectorCreate): Promise<Vector> {
  const response = await api.post<Vector>("/api/vectores/", data);
  return response.data;
}

export async function deleteVector(id: number): Promise<void> {
  await api.delete(`/api/vectores/${id}`);
}
