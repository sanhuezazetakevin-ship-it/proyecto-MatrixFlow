import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { UserPlus, Shield } from 'lucide-react';

export const UsuariosPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Usuarios & Control de Accesos (RBAC)</h1>
          <p className="text-xs text-slate-500 mt-1">Administración de credenciales y asignación de roles del sistema</p>
        </div>
        <Button variant="primary"><UserPlus size={16} /> Crear Usuario</Button>
      </div>

      <Card>
        <CardHeader title="Usuarios Registrados" />
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
              <tr>
                <th className="p-3">Nombre</th>
                <th className="p-3">Correo Electrónico</th>
                <th className="p-3">Rol Asignado</th>
                <th className="p-3">Permisos</th>
                <th className="p-3 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              <tr className="hover:bg-slate-50/80">
                <td className="p-3 font-semibold text-slate-900">Gabriel Administrator</td>
                <td className="p-3 text-slate-600">admin@matrixflow.com</td>
                <td className="p-3"><Badge variant="info">ADMINISTRADOR</Badge></td>
                <td className="p-3 text-slate-500">Acceso total (CRUD + Operaciones + Audit)</td>
                <td className="p-3 text-right"><button className="text-primary font-medium">Editar</button></td>
              </tr>
              <tr className="hover:bg-slate-50/80">
                <td className="p-3 font-semibold text-slate-900">Analista de Ventas</td>
                <td className="p-3 text-slate-600">analista@matrixflow.com</td>
                <td className="p-3"><Badge variant="success">ANALISTA</Badge></td>
                <td className="p-3 text-slate-500">Crear matrices, ejecutar cálculos</td>
                <td className="p-3 text-right"><button className="text-primary font-medium">Editar</button></td>
              </tr>
              <tr className="hover:bg-slate-50/80">
                <td className="p-3 font-semibold text-slate-900">Gerente Consultor</td>
                <td className="p-3 text-slate-600">gerente@matrixflow.com</td>
                <td className="p-3"><Badge variant="default">CONSULTA</Badge></td>
                <td className="p-3 text-slate-500">Solo lectura de dashboard y reportes</td>
                <td className="p-3 text-right"><button className="text-primary font-medium">Editar</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
