// User & Auth Types
export type UserRole = 'ADMINISTRADOR' | 'ANALISTA' | 'CONSULTA';

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  avatarUrl?: string;
}

// Business Domain Types
export interface Company {
  id: string;
  name: string;
  taxId: string;
  address: string;
  phone: string;
}

export interface Branch {
  id: string;
  companyId: string;
  name: string;
  city: string;
  address: string;
  code: string;
}

export interface ProductCategory {
  id: string;
  name: string;
  code: string;
}

export interface Product {
  id: string;
  categoryId: string;
  code: string;
  name: string;
  price: number;
  unit: string;
  stock: number;
}

export interface Sale {
  id: string;
  branchId: string;
  branchName: string;
  date: string;
  totalAmount: number;
  itemsCount: number;
}

export interface InventoryItem {
  id: string;
  branchId: string;
  branchName: string;
  productId: string;
  productName: string;
  quantity: number;
  minStock: number;
  status: 'OPTIMO' | 'CRITICO' | 'EXCESO';
}

// Mathematical Domain Types (Vector & Matrix)
export interface BusinessVector {
  id: string;
  name: string;
  dimension: number;
  values: number[];
  labels: string[]; // e.g. ["Laptop", "PC", "Monitor"]
  branchId?: string;
  createdAt: string;
}

export interface BusinessMatrix {
  id: string;
  name: string;
  rows: number;
  cols: number;
  rowLabels: string[]; // e.g. ["Lima", "Arequipa", "Trujillo"]
  colLabels: string[]; // e.g. ["Laptop", "PC", "Monitor"]
  values: number[][]; // 2D array [row][col]
  createdAt: string;
}

export type MathOperationType = 
  | 'SUMA_VECTORES'
  | 'RESTA_VECTORES'
  | 'PRODUCTO_ESCALAR'
  | 'ESCALAR_VECTOR'
  | 'SUMA_MATRICES'
  | 'RESTA_MATRICES'
  | 'MULTIPLICACION_MATRICIAL'
  | 'TRANSPOSICION_MATRIZ'
  | 'ESCALAR_MATRIZ'
  | 'COMBINACION_LINEAL';

export interface MathOperationRequest {
  type: MathOperationType;
  operandAId?: string;
  operandBId?: string;
  scalar?: number;
  linearCombinationWeights?: number[];
  vectors?: string[];
}

export interface MathOperationResult {
  id: string;
  operationType: MathOperationType;
  executionDate: string;
  executedBy: string;
  status: 'SUCCESS' | 'ERROR';
  resultType: 'VECTOR' | 'MATRIZ' | 'ESCALAR';
  resultVector?: number[];
  resultMatrix?: number[][];
  resultScalar?: number;
  executionTimeMs: number;
  explanation: string;
}

export interface AuditLog {
  id: string;
  timestamp: string;
  userName: string;
  userRole: UserRole;
  action: string;
  module: string;
  ipAddress: string;
  status: 'EXITOSO' | 'DENEGADO' | 'ERROR';
}
