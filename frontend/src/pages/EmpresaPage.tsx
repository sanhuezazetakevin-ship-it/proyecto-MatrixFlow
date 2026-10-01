import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { mockCompany } from '../services/mockData';
import { Building2, MapPin, Phone, FileText } from 'lucide-react';

export const EmpresaPage: React.FC = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Información de la Empresa</h1>
        <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mt-1">Configuración corporativa general de TechMatrix Global S.A.C.</p>
      </div>

      <Card>
        <CardHeader title="Perfil Corporativo" subtitle="Datos legales y de contacto" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-brand-mint/20 dark:bg-brand-dark rounded-xl text-brand-teal dark:text-brand-mint border border-brand-teal/30">
                <Building2 size={20} />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-600 dark:text-slate-400">Razón Social</p>
                <p className="font-bold text-slate-900 dark:text-white text-sm">{mockCompany.name}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="p-3 bg-brand-mint/20 dark:bg-brand-dark rounded-xl text-brand-teal dark:text-brand-mint border border-brand-teal/30">
                <FileText size={20} />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-600 dark:text-slate-400">RUC / Tax ID</p>
                <p className="font-bold text-slate-900 dark:text-white text-sm">{mockCompany.taxId}</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-brand-mint/20 dark:bg-brand-dark rounded-xl text-brand-teal dark:text-brand-mint border border-brand-teal/30">
                <MapPin size={20} />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-600 dark:text-slate-400">Dirección Fiscal</p>
                <p className="font-bold text-slate-900 dark:text-white text-sm">{mockCompany.address}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="p-3 bg-brand-mint/20 dark:bg-brand-dark rounded-xl text-brand-teal dark:text-brand-mint border border-brand-teal/30">
                <Phone size={20} />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-600 dark:text-slate-400">Teléfono Corporativo</p>
                <p className="font-bold text-slate-900 dark:text-white text-sm">{mockCompany.phone}</p>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};
