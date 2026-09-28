import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { mockAuditLogs } from '../services/mockData';
import { History, ShieldAlert } from 'lucide-react';

export const HistorialPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Historial & Auditoría de Operaciones</h1>
        <p className="text-xs text-slate-500 mt-1">Trazabilidad completa de operaciones matemáticas ejecutadas (Usuario, IP, Módulo, Fecha)</p>
      </div>

      <Card>
        <CardHeader title="Registro Auditado de Eventos" />
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
              <tr>
                <th className="p-3">ID Evento</th>
                <th className="p-3">Fecha y Hora</th>
                <th className="p-3">Usuario</th>
                <th className="p-3">Rol</th>
                <th className="p-3">Acción Ejecutada</th>
                <th className="p-3">Módulo</th>
                <th className="p-3">IP Origen</th>
                <th className="p-3">Estado</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {mockAuditLogs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-50/80">
                  <td className="p-3 font-mono font-semibold text-slate-700">{log.id}</td>
                  <td className="p-3 text-slate-600 font-mono text-[11px]">{log.timestamp}</td>
                  <td className="p-3 font-medium text-slate-900">{log.userName}</td>
                  <td className="p-3 text-slate-500">{log.userRole}</td>
                  <td className="p-3 font-semibold text-slate-800">{log.action}</td>
                  <td className="p-3 text-slate-600">{log.module}</td>
                  <td className="p-3 font-mono text-[11px] text-slate-500">{log.ipAddress}</td>
                  <td className="p-3">
                    <Badge variant={log.status === 'EXITOSO' ? 'success' : 'danger'}>
                      {log.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
