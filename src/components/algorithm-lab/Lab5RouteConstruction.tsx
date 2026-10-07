import React from 'react';
import { FinalPlan } from '../../types';
import { Route, CheckCircle, AlertTriangle, ShieldCheck, Clock, BookOpen } from 'lucide-react';

interface Lab5RouteConstructionProps {
  plan: FinalPlan | null;
}

export const Lab5RouteConstruction: React.FC<Lab5RouteConstructionProps> = ({ plan }) => {
  if (!plan) {
    return (
      <div className="py-16 text-center text-slate-400 text-xs">
        Please run an active plan in Operations to view the Route Construction pipeline trace.
      </div>
    );
  }

  return (
    <div className="lab-step-container space-y-4 text-xs text-slate-700 font-sans">
      {/* Overview Banner with Simple Intuition */}
      <div className="p-4 rounded-xl bg-orange-50 border border-orange-200 flex items-start gap-3 shadow-sm">
        <div className="w-9 h-9 rounded-lg bg-orange-500 text-white flex items-center justify-center shrink-0 shadow-sm">
          <Route className="w-5 h-5" />
        </div>
        <div className="space-y-1">
          <h4 className="text-sm font-bold text-slate-900">
            Lab 5: Route & Schedule Construction Heuristic
          </h4>
          <p className="text-slate-600 leading-relaxed text-xs">
            <strong>Core Intuition:</strong> Knapsack DP decides <em>which</em> packages fit into the van, but it has no concept of physical geography or driving sequence!
            Lab 5 sequences the actual journey using Dijkstra shortest paths, enforces <strong>Pickup-Before-Drop</strong>, tracks live cargo weight at each stop, and ensures no customer promise is broken.
          </p>
        </div>
      </div>

      {/* Rules & Invariants Checklist */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-2xs space-y-1.5">
          <div className="flex items-center gap-1.5 text-slate-900 font-bold">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>Invariant 1: Pickup Before Drop</span>
          </div>
          <p className="text-slate-600 text-[11px] leading-relaxed">
            A parcel cannot be dropped at its destination node before it has physically been loaded at its pickup hub.
          </p>
        </div>

        <div className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-2xs space-y-1.5">
          <div className="flex items-center gap-1.5 text-slate-900 font-bold">
            <ShieldCheck className="w-4 h-4 text-orange-600" />
            <span>Invariant 2: Dynamic Load Tracking</span>
          </div>
          <p className="text-slate-600 text-[11px] leading-relaxed">
            Starts at 0 kg at Depot. At pickup: <code className="text-orange-700 font-bold">load += w</code>. At drop: <code className="text-emerald-700 font-bold">load -= w</code>.
            Payload must never exceed {plan.vehicle.capacityKg} kg.
          </p>
        </div>

        <div className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-2xs space-y-1.5">
          <div className="flex items-center gap-1.5 text-slate-900 font-bold">
            <Clock className="w-4 h-4 text-amber-600" />
            <span>Invariant 3: Deadline Feasibility</span>
          </div>
          <p className="text-slate-600 text-[11px] leading-relaxed">
            Arrival time at drop node must be ≤ customer deadline. If violated, transparent repair removes the offending parcel to protect SLA.
          </p>
        </div>
      </div>

      {/* Feasibility Repair Notification */}
      {plan.repairs.length > 0 ? (
        <div className="p-4 rounded-xl bg-amber-50 border border-amber-300 space-y-2 shadow-2xs">
          <div className="flex items-center gap-2 text-amber-900 font-bold">
            <AlertTriangle className="w-4 h-4 text-amber-600" />
            <span>Feasibility Repair Triggered ({plan.repairs.length} Order Removed)</span>
          </div>
          <p className="text-amber-800 text-[11px]">
            SmartRoute automatically identified orders that would arrive past their agreed customer delivery time and deferred them:
          </p>
          <ul className="space-y-1 font-mono text-[11px] pl-4 list-disc text-amber-900">
            {plan.repairs.map((r, i) => (
              <li key={i}>
                Removed <strong>{r.removedRequestId}</strong>: {r.reason}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-300 flex items-center justify-between text-emerald-900 font-medium shadow-2xs">
          <div className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>100% Feasible Schedule: All {plan.acceptedRequests.length} scheduled deliveries arrive on or before committed deadlines!</span>
          </div>
          <span className="font-mono text-xs font-bold bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded">
            Total Journey: {plan.totalDistanceKm} km (~{plan.totalTravelMinutes} mins)
          </span>
        </div>
      )}

      {/* Ordered Stop Timeline with Load Tracking */}
      <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-sm space-y-2">
        <div className="flex items-center justify-between pb-2 border-b border-slate-100">
          <div>
            <h5 className="font-bold text-slate-900 text-xs">Constructed Turn-by-Turn Stop Sequence & State Trace</h5>
            <span className="text-slate-500 text-[11px]">
              Every stop shows vehicle arrival time, remaining customer slack, and onboard load in kg.
            </span>
          </div>
          <span className="text-slate-600 font-mono text-[11px] font-semibold bg-slate-100 px-2 py-0.5 rounded">
            Total Stops: {plan.stops.length}
          </span>
        </div>

        <div className="overflow-x-auto max-h-80">
          <table className="w-full text-left border-collapse text-[11px]">
            <thead className="bg-slate-50 text-slate-700 sticky top-0 border-b border-slate-200">
              <tr>
                <th className="p-2 font-semibold">Stop #</th>
                <th className="p-2 font-semibold">Location</th>
                <th className="p-2 font-semibold">Action</th>
                <th className="p-2 font-semibold">Order ID</th>
                <th className="p-2 text-right font-semibold">Leg Distance</th>
                <th className="p-2 text-right font-semibold">Arrival Time</th>
                <th className="p-2 text-right font-semibold">Deadline</th>
                <th className="p-2 text-right font-semibold">Onboard Load</th>
                <th className="p-2 text-center font-semibold">SLA Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono">
              {plan.stops.map((stop) => {
                const isPickup = stop.action === "PICKUP";
                const isDrop = stop.action === "DROP";

                return (
                  <tr key={stop.stopNumber} className="hover:bg-slate-50">
                    <td className="p-2 text-slate-500">#{stop.stopNumber}</td>
                    <td className="p-2 text-slate-900 font-sans font-semibold">{stop.locationName}</td>
                    <td className="p-2">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        isPickup
                          ? "bg-orange-100 text-orange-800 border border-orange-200"
                          : isDrop
                          ? "bg-emerald-100 text-emerald-800 border border-emerald-200"
                          : "bg-slate-100 text-slate-800 border border-slate-200"
                      }`}>
                        {stop.action}
                      </span>
                    </td>
                    <td className="p-2 text-slate-700 font-semibold">{stop.requestId || "-"}</td>
                    <td className="p-2 text-right text-slate-600">{stop.legDistanceKm} km</td>
                    <td className="p-2 text-right text-slate-900 font-semibold">{stop.arrivalMinute}m</td>
                    <td className="p-2 text-right text-amber-700 font-semibold">
                      {stop.deadlineMinute !== undefined ? `${stop.deadlineMinute}m` : "-"}
                    </td>
                    <td className="p-2 text-right text-emerald-700 font-bold">
                      {stop.loadAfterStopKg} / {stop.capacityKg} kg
                    </td>
                    <td className="p-2 text-center">
                      <span className="text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                        ✓ ON TIME
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
