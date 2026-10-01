import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { mockAuditLogs } from '../services/mockData';

export const HistorialPage: React.FC = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Historial & Auditoría de Operaciones</h1>
        <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mt-1">Trazabilidad completa de operaciones matemáticas ejecutadas (Usuario, IP, Módulo, Fecha)</p>
      </div>

      <Card>
        <CardHeader title="Registro Auditado de Eventos" />
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-slate-200 font-bold border-b border-slate-200 dark:border-brand-dark">
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
            <tbody className="divide-y divide-slate-200 dark:divide-brand-dark/60 text-slate-800 dark:text-slate-200">
              {mockAuditLogs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-100/70 dark:hover:bg-brand-dark/40">
                  <td className="p-3 font-mono font-bold text-slate-900 dark:text-slate-200">{log.id}</td>
                  <td className="p-3 text-slate-700 dark:text-slate-300 font-mono text-[11px] font-semibold">{log.timestamp}</td>
                  <td className="p-3 font-bold text-slate-900 dark:text-white">{log.userName}</td>
                  <td className="p-3 text-slate-700 dark:text-slate-300 font-medium">{log.userRole}</td>
                  <td className="p-3 font-bold text-brand-teal dark:text-brand-mint">{log.action}</td>
                  <td className="p-3 text-slate-700 dark:text-slate-300 font-medium">{log.module}</td>
                  <td className="p-3 font-mono text-[11px] text-slate-600 dark:text-slate-400 font-semibold">{log.ipAddress}</td>
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
