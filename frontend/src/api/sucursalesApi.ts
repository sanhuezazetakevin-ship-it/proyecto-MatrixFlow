
import api from "./api";
import { Sucursal, SucursalCreate } from "../types/sucursales";

export async function getSucursales(): Promise<Sucursal[]> {
  const response = await api.get<Sucursal[]>("/api/sucursales/");
  return response.data;
}

export async function createSucursal(data: SucursalCreate): Promise<Sucursal> {
  const response = await api.post<Sucursal>("/api/sucursales/", data);
  return response.data;
}

