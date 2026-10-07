import React from 'react';
import { Vehicle, FinalPlan } from '../../types';
import { Truck, CheckCircle2, ShieldAlert, Package, Gauge } from 'lucide-react';

interface FleetPanelProps {
  vehicles: Vehicle[];
  selectedVehicleId: string;
  onSelectVehicleId: (id: string) => void;
  plan?: FinalPlan | null;
}

export const FleetPanel: React.FC<FleetPanelProps> = ({
  vehicles,
  selectedVehicleId,
  onSelectVehicleId,
  plan
}) => {
  return (
    <div className="fleet-panel bg-white p-3 flex flex-col gap-3 text-xs font-sans">
      <div className="flex items-center justify-between pb-2 border-b border-orange-100">
        <div className="flex items-center gap-2">
          <Truck className="w-4 h-4 text-orange-500" />
          <h3 className="font-bold text-slate-900 text-xs uppercase tracking-wider">Fleet Telematics & Dynamic Capacity</h3>
        </div>
        <div className="flex items-center gap-2 text-[11px] font-bold">
          <span className="text-orange-700 bg-orange-50 px-2.5 py-0.5 rounded-full border border-orange-200">
            1 Active Shift
          </span>
          <span className="text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
            {vehicles.length - 1} Standby Units
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {vehicles.map((v) => {
          const isSelected = v.id === selectedVehicleId;
          const isMaintenance = v.status === "maintenance";

          // If vehicle is active in current plan, show live plan load and utilization
          const currentLoad = isSelected && plan ? plan.totalWeightKg : v.currentLoadKg;
          const utilizationPct = v.capacityKg > 0
            ? Math.min(100, Math.round((currentLoad / v.capacityKg) * 100))
            : 0;

          return (
            <div
              key={v.id}
              onClick={() => {
                if (!isMaintenance) {
                  onSelectVehicleId(v.id);
                }
              }}
              className={`p-3.5 rounded-xl border transition-all text-xs flex flex-col justify-between ${
                isMaintenance
                  ? "bg-slate-50 border-slate-200 opacity-60 cursor-not-allowed"
                  : isSelected
                  ? "bg-orange-50/70 border-2 border-orange-500 shadow-md shadow-orange-500/10 cursor-pointer"
                  : "bg-white border-slate-200 hover:border-orange-300 hover:bg-orange-50/20 cursor-pointer shadow-xs"
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center gap-1.5">
                    <span className="font-bold text-slate-900 text-sm">{v.id}</span>
                    <span className="text-[10px] text-slate-500 font-mono">({v.plate})</span>
                  </div>

                  {/* Status Badge */}
                  {isMaintenance ? (
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-200 flex items-center gap-1">
                      <ShieldAlert className="w-2.5 h-2.5" /> Maintenance
                    </span>
                  ) : isSelected ? (
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-orange-600 text-white flex items-center gap-1 shadow-xs">
                      <CheckCircle2 className="w-2.5 h-2.5" /> Active Unit
                    </span>
                  ) : (
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                      Available (Click to switch)
                    </span>
                  )}
                </div>

                <div className="text-slate-800 font-bold text-xs mb-1">
                  {v.driverName}
                </div>

                <div className="text-[11px] text-slate-500 mb-2 flex items-center justify-between">
                  <span>Hub: <strong className="text-slate-700">{v.startLocationId}</strong></span>
                  {isSelected && plan && (
                    <span className="inline-flex items-center gap-1 text-orange-700 font-bold bg-orange-100 px-1.5 py-0.5 rounded text-[10px]">
                      <Package className="w-2.5 h-2.5" /> {plan.acceptedRequests.length} orders
                    </span>
                  )}
                </div>
              </div>

              {/* Dynamic Capacity Load Bar */}
              <div className="pt-2 border-t border-slate-100">
                <div className="flex items-center justify-between text-[11px] font-semibold text-slate-700 mb-1">
                  <span>
                    Payload: <strong className="text-slate-900">{currentLoad.toFixed(1)}</strong> / {v.capacityKg} kg
                  </span>
                  <span className={utilizationPct > 0 ? "text-orange-600 font-bold" : "text-slate-400"}>
                    {utilizationPct}%
                  </span>
                </div>
                <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden p-0.5 border border-slate-200">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      isMaintenance
                        ? "bg-rose-400"
                        : utilizationPct > 85
                        ? "bg-amber-500"
                        : "bg-gradient-to-r from-orange-500 to-amber-500"
                    }`}
                    style={{ width: `${Math.max(utilizationPct > 0 ? 6 : 0, utilizationPct)}%` }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
