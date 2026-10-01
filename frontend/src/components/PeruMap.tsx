import React from "react";
import type { Sucursal } from "../types/sucursales";

const CITY_COORDS: Record<string, { top: string; left: string }> = {
  TUMBES: { top: "8%", left: "12%" },
  PIURA: { top: "18%", left: "10%" },
  SULLANA: { top: "15%", left: "14%" },
  CHICLAYO: { top: "28%", left: "17%" },
  TRUJILLO: { top: "35%", left: "22%" },
  CAJAMARCA: { top: "25%", left: "26%" },
  JAEN: { top: "20%", left: "24%" },
  LIMA: { top: "58%", left: "34%" },
  HUANCAYO: { top: "56%", left: "46%" },
  PUCALLPA: { top: "42%", left: "62%" },
  ICA: { top: "70%", left: "43%" },
  AYACUCHO: { top: "68%", left: "54%" },
  CUSCO: { top: "65%", left: "67%" },
  AREQUIPA: { top: "82%", left: "60%" },
  JULIACA: { top: "75%", left: "78%" },
};

// Eliminamos el SVG manual porque era feo
const PeruSilhouette = () => (
  <img 
    src="/peru-silhouette.png" 
    alt="Mapa del Perú" 
    className="absolute inset-0 w-full h-full object-contain opacity-50 contrast-150 grayscale"
  />
);

interface PeruMapProps {
  sucursales: Sucursal[];
}

export const PeruMap: React.FC<PeruMapProps> = ({ sucursales }) => {
  // Normalizamos nombres de ciudades para hacer match con nuestro diccionario
  const mappedPoints = sucursales.filter(s => s.activo).map((suc) => {
    const cityName = suc.ciudad ? suc.ciudad.toUpperCase().trim() : "";
    const coords = CITY_COORDS[cityName];
    return {
      name: cityName || suc.nombre,
      top: coords?.top || "50%",
      left: coords?.left || "50%",
      hasCoords: !!coords,
    };
  }).filter(p => p.hasCoords);

  return (
    <div className="relative w-full aspect-[3/4] bg-brand-darkest rounded-2xl border border-brand-dark overflow-hidden flex items-center justify-center p-4 shadow-inner">
      <div className="absolute top-4 left-4 z-20">
        <h3 className="text-white font-bold text-sm tracking-tight">Mapa de Sucursales</h3>
        <p className="text-[10px] text-brand-mint font-semibold uppercase">Cobertura Nacional Activa</p>
      </div>
      
      {/* Contenedor del mapa */}
      <div className="relative w-full h-full max-w-[300px] max-h-[400px] flex items-center justify-center">
        
        {/* Fondo punteado general para dar la textura */}
        <div 
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: `radial-gradient(circle, #94a3b8 1px, transparent 1px)`,
            backgroundSize: "8px 8px"
          }}
        ></div>

        {/* Silueta de Perú real (desde la imagen proporcionada) */}
        <PeruSilhouette />

        {/* Puntos rojos de sucursales dinámicos */}
        {mappedPoints.map((suc, idx) => (
          <div 
            key={`${suc.name}-${idx}`}
            className="absolute group flex items-center gap-1.5 z-30"
            style={{ top: suc.top, left: suc.left }}
          >
            <div className="w-2.5 h-2.5 bg-red-500 rounded-full shadow-[0_0_8px_rgba(239,68,68,0.8)] border border-red-300 animate-pulse"></div>
            <span className="text-[9px] font-bold text-slate-200 drop-shadow-md whitespace-nowrap bg-brand-darkest/70 px-1 py-0.5 rounded backdrop-blur-sm">{suc.name}</span>
          </div>
        ))}

        {mappedPoints.length === 0 && (
          <div className="absolute inset-0 flex items-center justify-center z-40">
             <span className="text-xs text-brand-teal/50 font-semibold bg-brand-darkest/80 px-3 py-1 rounded-full">Sin datos de sedes</span>
          </div>
        )}
      </div>
    </div>
  );
};
