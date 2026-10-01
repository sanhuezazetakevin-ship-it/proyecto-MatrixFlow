import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { UserPlus } from 'lucide-react';

export const UsuariosPage: React.FC = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Usuarios & Control de Accesos (RBAC)</h1>
          <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mt-1">Administración de credenciales y asignación de roles del sistema</p>
        </div>
        <Button variant="primary"><UserPlus size={16} /> Crear Usuario</Button>
      </div>

      <Card>
        <CardHeader title="Usuarios Registrados" />
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-slate-200 font-bold border-b border-slate-200 dark:border-brand-dark">
              <tr>
                <th className="p-3">Nombre</th>
                <th className="p-3">Correo Electrónico</th>
                <th className="p-3">Rol Asignado</th>
                <th className="p-3">Permisos</th>
                <th className="p-3 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-brand-dark/60 text-slate-800 dark:text-slate-200">
              <tr className="hover:bg-slate-100/70 dark:hover:bg-brand-dark/40">
                <td className="p-3 font-bold text-slate-900 dark:text-white">Gabriel Administrator</td>
                <td className="p-3 text-slate-700 dark:text-slate-300 font-semibold">admin@matrixflow.com</td>
                <td className="p-3"><Badge variant="info">ADMINISTRADOR</Badge></td>
                <td className="p-3 text-slate-600 dark:text-slate-400 font-medium">Acceso total (CRUD + Operaciones + Audit)</td>
                <td className="p-3 text-right"><button className="text-brand-teal dark:text-brand-mint font-bold hover:underline">Editar</button></td>
              </tr>
              <tr className="hover:bg-slate-100/70 dark:hover:bg-brand-dark/40">
                <td className="p-3 font-bold text-slate-900 dark:text-white">Analista de Ventas</td>
                <td className="p-3 text-slate-700 dark:text-slate-300 font-semibold">analista@matrixflow.com</td>
                <td className="p-3"><Badge variant="success">ANALISTA</Badge></td>
                <td className="p-3 text-slate-600 dark:text-slate-400 font-medium">Crear matrices, ejecutar cálculos</td>
                <td className="p-3 text-right"><button className="text-brand-teal dark:text-brand-mint font-bold hover:underline">Editar</button></td>
              </tr>
              <tr className="hover:bg-slate-100/70 dark:hover:bg-brand-dark/40">
                <td className="p-3 font-bold text-slate-900 dark:text-white">Gerente Consultor</td>
                <td className="p-3 text-slate-700 dark:text-slate-300 font-semibold">gerente@matrixflow.com</td>
                <td className="p-3"><Badge variant="default">CONSULTA</Badge></td>
                <td className="p-3 text-slate-600 dark:text-slate-400 font-medium">Solo lectura de dashboard y reportes</td>
                <td className="p-3 text-right"><button className="text-brand-teal dark:text-brand-mint font-bold hover:underline">Editar</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
