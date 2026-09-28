import { 
  Company, Branch, Product, Sale, InventoryItem, 
  BusinessVector, BusinessMatrix, MathOperationResult, AuditLog, User 
} from '../types';

export const mockUser: User = {
  id: 'u-1',
  name: 'Gabriel Administrator',
  email: 'admin@matrixflow.com',
  role: 'ADMINISTRADOR',
};

export const mockCompany: Company = {
  id: 'comp-1',
  name: 'TechMatrix Global S.A.C.',
  taxId: '20601234567',
  address: 'Av. Empresarial 456, San Isidro, Lima',
  phone: '+51 1 456-7890',
};

export const mockBranches: Branch[] = [
  { id: 'b-1', companyId: 'comp-1', name: 'Lima Central', city: 'Lima', address: 'Av. Javier Prado 1230', code: 'LIM-01' },
  { id: 'b-2', companyId: 'comp-1', name: 'Arequipa Norte', city: 'Arequipa', address: 'Av. Ejército 450', code: 'AQP-01' },
  { id: 'b-3', companyId: 'comp-1', name: 'Trujillo Real', city: 'Trujillo', address: 'Calle España 890', code: 'TRU-01' },
  { id: 'b-4', companyId: 'comp-1', name: 'Cusco Imperial', city: 'Cusco', address: 'Av. Sol 340', code: 'CUS-01' },
  { id: 'b-5', companyId: 'comp-1', name: 'Piura Empresarial', city: 'Piura', address: 'Av. Grau 120', code: 'PIU-01' },
];

export const mockProducts: Product[] = [
  { id: 'p-1', categoryId: 'c-1', code: 'PROD-LAP', name: 'Laptop Workstation Pro', price: 4500, unit: 'UNID', stock: 120 },
  { id: 'p-2', categoryId: 'c-1', code: 'PROD-PC', name: 'Desktop PC Enterprise', price: 3200, unit: 'UNID', stock: 85 },
  { id: 'p-3', categoryId: 'c-2', code: 'PROD-MON', name: 'Monitor UltraWide 34"', price: 1800, unit: 'UNID', stock: 210 },
  { id: 'p-4', categoryId: 'c-3', code: 'PROD-TEC', name: 'Teclado Mecánico RGB', price: 350, unit: 'UNID', stock: 450 },
  { id: 'p-5', categoryId: 'c-3', code: 'PROD-MOU', name: 'Mouse Ergonómico Wireless', price: 220, unit: 'UNID', stock: 600 },
];

export const mockSales: Sale[] = [
  { id: 's-101', branchId: 'b-1', branchName: 'Lima Central', date: '2026-09-26', totalAmount: 48500, itemsCount: 18 },
  { id: 's-102', branchId: 'b-2', branchName: 'Arequipa Norte', date: '2026-09-26', totalAmount: 32100, itemsCount: 12 },
  { id: 's-103', branchId: 'b-3', branchName: 'Trujillo Real', date: '2026-09-25', totalAmount: 24900, itemsCount: 9 },
  { id: 's-104', branchId: 'b-4', branchName: 'Cusco Imperial', date: '2026-09-25', totalAmount: 19800, itemsCount: 7 },
  { id: 's-105', branchId: 'b-5', branchName: 'Piura Empresarial', date: '2026-09-24', totalAmount: 15400, itemsCount: 6 },
];

export const mockInventory: InventoryItem[] = [
  { id: 'inv-1', branchId: 'b-1', branchName: 'Lima Central', productId: 'p-1', productName: 'Laptop Workstation Pro', quantity: 45, minStock: 20, status: 'OPTIMO' },
  { id: 'inv-2', branchId: 'b-1', branchName: 'Lima Central', productId: 'p-3', productName: 'Monitor UltraWide 34"', quantity: 12, minStock: 15, status: 'CRITICO' },
  { id: 'inv-3', branchId: 'b-2', branchName: 'Arequipa Norte', productId: 'p-2', productName: 'Desktop PC Enterprise', quantity: 28, minStock: 10, status: 'OPTIMO' },
  { id: 'inv-4', branchId: 'b-3', branchName: 'Trujillo Real', productId: 'p-4', productName: 'Teclado Mecánico RGB', quantity: 180, minStock: 50, status: 'EXCESO' },
];

export const mockVectors: BusinessVector[] = [
  {
    id: 'v-lima-q',
    name: 'Cantidades Vendidas Lima (q_Lima)',
    dimension: 5,
    labels: ['Laptop', 'PC', 'Monitor', 'Teclado', 'Mouse'],
    values: [10, 5, 12, 25, 30],
    branchId: 'b-1',
    createdAt: '2026-09-26 14:30',
  },
  {
    id: 'v-precios-p',
    name: 'Vector de Precios Unitarios (p)',
    dimension: 5,
    labels: ['Laptop', 'PC', 'Monitor', 'Teclado', 'Mouse'],
    values: [4500, 3200, 1800, 350, 220],
    createdAt: '2026-09-26 10:00',
  },
  {
    id: 'v-arequipa-q',
    name: 'Cantidades Vendidas Arequipa (q_Arequipa)',
    dimension: 5,
    labels: ['Laptop', 'PC', 'Monitor', 'Teclado', 'Mouse'],
    values: [6, 4, 8, 15, 20],
    branchId: 'b-2',
    createdAt: '2026-09-26 15:10',
  },
];

export const mockMatrices: BusinessMatrix[] = [
  {
    id: 'm-sales-real',
    name: 'Matriz de Ventas Reales por Sucursal (Q_Real)',
    rows: 5,
    cols: 5,
    rowLabels: ['Lima', 'Arequipa', 'Trujillo', 'Cusco', 'Piura'],
    colLabels: ['Laptop', 'PC', 'Monitor', 'Teclado', 'Mouse'],
    values: [
      [10, 5, 12, 25, 30],
      [6, 4, 8, 15, 20],
      [5, 3, 6, 12, 18],
      [4, 2, 5, 10, 15],
      [3, 2, 4, 8, 12],
    ],
    createdAt: '2026-09-26 16:00',
  },
  {
    id: 'm-sales-target',
    name: 'Matriz de Metas Mensuales (Q_Meta)',
    rows: 5,
    cols: 5,
    rowLabels: ['Lima', 'Arequipa', 'Trujillo', 'Cusco', 'Piura'],
    colLabels: ['Laptop', 'PC', 'Monitor', 'Teclado', 'Mouse'],
    values: [
      [12, 6, 15, 30, 35],
      [8, 5, 10, 20, 25],
      [6, 4, 8, 15, 20],
      [5, 3, 6, 12, 15],
      [4, 3, 5, 10, 15],
    ],
    createdAt: '2026-09-26 09:00',
  },
];

export const mockAuditLogs: AuditLog[] = [
  { id: 'log-1', timestamp: '2026-09-26 18:22:10', userName: 'Gabriel Admin', userRole: 'ADMINISTRADOR', action: 'Ejecutar Producto Escalar', module: 'Operaciones', ipAddress: '192.168.1.45', status: 'EXITOSO' },
  { id: 'log-2', timestamp: '2026-09-26 17:45:00', userName: 'Gabriel Admin', userRole: 'ADMINISTRADOR', action: 'Crear Matriz Q_Real', module: 'Matrices', ipAddress: '192.168.1.45', status: 'EXITOSO' },
  { id: 'log-3', timestamp: '2026-09-26 16:10:30', userName: 'Analista Ventas', userRole: 'ANALISTA', action: 'Resta Matricial Q_Real - Q_Meta', module: 'Operaciones', ipAddress: '192.168.1.88', status: 'EXITOSO' },
];
