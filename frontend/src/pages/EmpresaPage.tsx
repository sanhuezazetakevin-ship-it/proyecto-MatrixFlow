import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { mockCompany } from '../services/mockData';
import { Building2, MapPin, Phone, FileText } from 'lucide-react';

export const EmpresaPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Información de la Empresa</h1>
        <p className="text-xs text-slate-500 mt-1">Configuración corporativa general de TechMatrix Global S.A.C.</p>
      </div>

      <Card>
        <CardHeader title="Perfil Corporativo" subtitle="Datos legales y de contacto" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-slate-100 rounded-lg text-slate-600">
                <Building2 size={20} />
              </div>
              <div>
                <p className="text-xs text-slate-500">Razón Social</p>
                <p className="font-semibold text-slate-800 text-sm">{mockCompany.name}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="p-2 bg-slate-100 rounded-lg text-slate-600">
                <FileText size={20} />
              </div>
              <div>
                <p className="text-xs text-slate-500">RUC / Tax ID</p>
                <p className="font-semibold text-slate-800 text-sm">{mockCompany.taxId}</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-slate-100 rounded-lg text-slate-600">
                <MapPin size={20} />
              </div>
              <div>
                <p className="text-xs text-slate-500">Dirección Fiscal</p>
                <p className="font-semibold text-slate-800 text-sm">{mockCompany.address}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="p-2 bg-slate-100 rounded-lg text-slate-600">
                <Phone size={20} />
              </div>
              <div>
                <p className="text-xs text-slate-500">Teléfono Corporativo</p>
                <p className="font-semibold text-slate-800 text-sm">{mockCompany.phone}</p>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};
