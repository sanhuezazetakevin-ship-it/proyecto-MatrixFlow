import axios from 'axios';
import { 
  mockCompany, mockBranches, mockProducts, mockSales, mockInventory, 
  mockVectors, mockMatrices, mockAuditLogs, mockUser 
} from './mockData';
import { 
  BusinessVector, BusinessMatrix, MathOperationRequest, MathOperationResult, AuditLog 
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor for JWT auth token injection
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('matrixflow_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Front-end API service with fallbacks for Phase 1 development
export const businessService = {
  getCompany: async () => mockCompany,
  getBranches: async () => mockBranches,
  getProducts: async () => mockProducts,
  getSales: async () => mockSales,
  getInventory: async () => mockInventory,
};

export const mathService = {
  getVectors: async (): Promise<BusinessVector[]> => mockVectors,
  getMatrices: async (): Promise<BusinessMatrix[]> => mockMatrices,
  
  executeOperation: async (req: MathOperationRequest): Promise<MathOperationResult> => {
    // Local simulation of NumPy mathematical engine for Phase 1
    const start = performance.now();
    let result: MathOperationResult;

    if (req.type === 'PRODUCTO_ESCALAR') {
      const v1 = mockVectors.find(v => v.id === req.operandAId) || mockVectors[0];
      const v2 = mockVectors.find(v => v.id === req.operandBId) || mockVectors[1];
      const scalarResult = v1.values.reduce((acc, val, i) => acc + val * (v2.values[i] || 0), 0);

      result = {
        id: `res-${Date.now()}`,
        operationType: 'PRODUCTO_ESCALAR',
        executionDate: new Date().toISOString().replace('T', ' ').substring(0, 19),
        executedBy: mockUser.name,
        status: 'SUCCESS',
        resultType: 'ESCALAR',
        resultScalar: scalarResult,
        executionTimeMs: Math.round(performance.now() - start),
        explanation: `Producto escalar entre "${v1.name}" y "${v2.name}". Ingresos Totales Calculados = S/ ${scalarResult.toLocaleString()}`,
      };
    } else if (req.type === 'RESTA_MATRICES') {
      const m1 = mockMatrices[0];
      const m2 = mockMatrices[1];
      const diffMatrix = m1.values.map((row, r) => 
        row.map((val, c) => val - m2.values[r][c])
      );

      result = {
        id: `res-${Date.now()}`,
        operationType: 'RESTA_MATRICES',
        executionDate: new Date().toISOString().replace('T', ' ').substring(0, 19),
        executedBy: mockUser.name,
        status: 'SUCCESS',
        resultType: 'MATRIZ',
        resultMatrix: diffMatrix,
        executionTimeMs: Math.round(performance.now() - start),
        explanation: `Resta Matricial (Ventas Reales - Metas Planificadas). Matriz de Brechas de Rendimiento Calculada.`,
      };
    } else if (req.type === 'TRANSPOSICION_MATRIZ') {
      const m = mockMatrices.find(m => m.id === req.operandAId) || mockMatrices[0];
      const transposed = m.colLabels.map((_, colIndex) => 
        m.values.map(row => row[colIndex])
      );

      result = {
        id: `res-${Date.now()}`,
        operationType: 'TRANSPOSICION_MATRIZ',
        executionDate: new Date().toISOString().replace('T', ' ').substring(0, 19),
        executedBy: mockUser.name,
        status: 'SUCCESS',
        resultType: 'MATRIZ',
        resultMatrix: transposed,
        executionTimeMs: Math.round(performance.now() - start),
        explanation: `Transposición de matriz "${m.name}". Perspectiva permutada de Sucursal/Producto a Producto/Sucursal.`,
      };
    } else {
      // Default Vector Sum fallback
      const v1 = mockVectors[0];
      const v2 = mockVectors[2];
      const sumVector = v1.values.map((val, i) => val + (v2.values[i] || 0));

      result = {
        id: `res-${Date.now()}`,
        operationType: 'SUMA_VECTORES',
        executionDate: new Date().toISOString().replace('T', ' ').substring(0, 19),
        executedBy: mockUser.name,
        status: 'SUCCESS',
        resultType: 'VECTOR',
        resultVector: sumVector,
        executionTimeMs: Math.round(performance.now() - start),
        explanation: `Suma vectorial de cantidades vendidas en Lima y Arequipa.`,
      };
    }

    return result;
  },

  getAuditLogs: async (): Promise<AuditLog[]> => mockAuditLogs,
};
