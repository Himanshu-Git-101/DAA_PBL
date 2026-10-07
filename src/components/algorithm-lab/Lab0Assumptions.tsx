import React, { useState } from 'react';
import { FinalPlan, DeliveryRequest, Vehicle } from '../../types';
import { LogisticsGraph } from '../../lib/algorithms/graph';
import { Info, Edit3, Check, ShieldCheck, Gauge } from 'lucide-react';

interface Lab0AssumptionsProps {
  plan: FinalPlan | null;
  graph: LogisticsGraph;
  vehicle: Vehicle;
  deliveries: DeliveryRequest[];
  onUpdateVehicleCapacity: (newCap: number) => void;
  onUpdateDeliveryProfit: (id: string, newProfit: number) => void;
}

export const Lab0Assumptions: React.FC<Lab0AssumptionsProps> = ({
  plan,
  graph,
  vehicle,
  deliveries,
  onUpdateVehicleCapacity
}) => {
  const [editingCapacity, setEditingCapacity] = useState(false);
  const [capVal, setCapVal] = useState(vehicle.capacityKg.toString());

  const handleSaveCapacity = () => {
    const parsed = parseFloat(capVal);
    if (!isNaN(parsed) && parsed > 0) {
      onUpdateVehicleCapacity(parsed);
    }
    setEditingCapacity(false);
  };

  return (
    <div className="lab-step-container space-y-5 text-xs text-slate-800">
      {/* Overview Banner in Orange & White */}
      <div className="p-4 rounded-2xl bg-orange-50 border border-orange-200 flex items-start gap-3 shadow-xs">
        <div className="p-2 rounded-xl bg-orange-500 text-white shrink-0 mt-0.5">
          <Info className="w-5 h-5" />
        </div>
        <div>
          <h4 className="text-sm font-bold text-slate-900 mb-1">
            Lab 0: Mathematical Model, Inputs & Assumptions
          </h4>
          <p className="text-slate-600 leading-relaxed">
            Every optimization in SmartRoute is computed deterministically from this exact shared state.
            We model last-mile distribution on a weighted road network with physical vehicle load constraints
            and strict customer deadlines.
          </p>
        </div>
      </div>

      {/* Grid of Assumptions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Core Constraints */}
        <div className="p-4 rounded-2xl bg-white border border-slate-200 space-y-3 shadow-xs">
          <div className="flex items-center gap-2 text-slate-900 font-bold">
            <Gauge className="w-4 h-4 text-orange-500" />
            <span>Operational Assumptions</span>
          </div>
          <ul className="space-y-2 text-slate-600">
            <li className="flex items-start gap-2">
              <span className="text-orange-500 font-bold">•</span>
              <span><strong>Average Fleet Speed:</strong> 28 km/h in urban Hyderabad traffic.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-orange-500 font-bold">•</span>
              <span><strong>Stop Service Time:</strong> 3.0 minutes for physical handover.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-orange-500 font-bold">•</span>
              <span><strong>Depot Origin:</strong> Amazon FC (Begumpet) at time <code>t = 0</code> mins.</span>
            </li>
          </ul>
        </div>

        {/* Active Vehicle & Interactive Edit */}
        <div className="p-4 rounded-2xl bg-white border border-slate-200 space-y-3 shadow-xs">
          <div className="flex items-center justify-between text-slate-900 font-bold">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>Active Vehicle Constraint</span>
            </div>
          </div>
          <div className="space-y-2 text-slate-700">
            <div>
              <span className="text-slate-500 font-semibold">Unit ID:</span> <strong className="text-slate-900">{vehicle.id}</strong>
            </div>
            <div>
              <span className="text-slate-500 font-semibold">Driver:</span> <span className="text-slate-800 font-medium">{vehicle.driverName}</span>
            </div>

            {/* Editable Demo Value: Vehicle Capacity */}
            <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
              <div>
                <span className="text-slate-500 block text-[11px] font-bold">VEHICLE CAPACITY</span>
                {editingCapacity ? (
                  <div className="flex items-center gap-1.5 mt-1">
                    <input
                      type="number"
                      value={capVal}
                      onChange={(e) => setCapVal(e.target.value)}
                      className="w-16 bg-slate-50 border-2 border-orange-500 text-slate-900 p-1 rounded font-mono text-xs focus:outline-none"
                    />
                    <button
                      onClick={handleSaveCapacity}
                      className="p-1 bg-orange-500 text-white rounded hover:bg-orange-600"
                    >
                      <Check className="w-3.5 h-3.5" />
                    </button>
                  </div>
                ) : (
                  <div className="text-base font-bold text-orange-600 font-mono flex items-center gap-2 mt-0.5">
                    <span>{vehicle.capacityKg} kg</span>
                    <button
                      onClick={() => setEditingCapacity(true)}
                      className="p-1 text-slate-400 hover:text-orange-600 rounded hover:bg-orange-50"
                      title="Edit vehicle capacity for live rerun"
                    >
                      <Edit3 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Graph Network Summary */}
        <div className="p-4 rounded-2xl bg-white border border-slate-200 space-y-3 shadow-xs">
          <div className="flex items-center gap-2 text-slate-900 font-bold">
            <Info className="w-4 h-4 text-orange-500" />
            <span>Network Dimensions</span>
          </div>
          <div className="space-y-2 text-slate-700">
            <div className="flex justify-between py-1 border-b border-slate-100">
              <span className="text-slate-500 font-semibold">Vertices (|V|):</span>
              <strong className="text-slate-900 font-mono">{graph.getAllLocations().length} hubs</strong>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-100">
              <span className="text-slate-500 font-semibold">Edges (|E|):</span>
              <strong className="text-slate-900 font-mono">{graph.getAllEdges().length} arterial roads</strong>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-slate-500 font-semibold">Candidate Requests:</span>
              <strong className="text-slate-900 font-mono">{deliveries.length} orders</strong>
            </div>
          </div>
        </div>
      </div>

      {/* Candidate Requests Table */}
      <div className="p-4 rounded-2xl bg-white border border-slate-200 shadow-xs">
        <h5 className="font-bold text-slate-900 mb-2">Input Candidate Deliveries ({deliveries.length} Records)</h5>
        <div className="overflow-x-auto max-h-56">
          <table className="w-full text-left border-collapse text-[11px]">
            <thead className="bg-orange-50/70 text-slate-700 font-bold sticky top-0">
              <tr>
                <th className="p-2">ID</th>
                <th className="p-2">Pickup → Drop</th>
                <th className="p-2 text-right">Weight (kg)</th>
                <th className="p-2 text-right">Profit (₹)</th>
                <th className="p-2 text-right">Profit/kg</th>
                <th className="p-2 text-right">Deadline</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {deliveries.map((d) => (
                <tr key={d.id} className="hover:bg-orange-50/30">
                  <td className="p-2 font-mono font-bold text-slate-800">{d.id}</td>
                  <td className="p-2 text-slate-700">{d.pickupLocationId} → {d.dropLocationId}</td>
                  <td className="p-2 text-right font-mono font-semibold">{d.weightKg}</td>
                  <td className="p-2 text-right font-mono text-emerald-600 font-bold">₹{d.profit}</td>
                  <td className="p-2 text-right font-mono text-orange-600 font-bold">
                    {d.weightKg > 0 ? (d.profit / d.weightKg).toFixed(1) : 0}
                  </td>
                  <td className="p-2 text-right font-mono text-slate-800 font-semibold">{d.deadlineMinutesFromStart}m</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
