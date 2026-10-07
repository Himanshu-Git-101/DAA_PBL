import React from 'react';
import { FinalPlan } from '../../types';
import { PlanningStrategy } from '../../lib/planning/buildPlan';
import { Play, RotateCcw, Cpu, Clock, AlertTriangle, Package, TrendingUp } from 'lucide-react';

interface RoutePlanPanelProps {
  plan: FinalPlan | null;
  onRunPlan: (strategy: PlanningStrategy) => void;
  onResetPlan: () => void;
  onOpenAlgorithmLab: () => void;
  currentStrategy: PlanningStrategy;
  onChangeStrategy: (s: PlanningStrategy) => void;
}

export const RoutePlanPanel: React.FC<RoutePlanPanelProps> = ({
  plan,
  onRunPlan,
  onResetPlan,
  onOpenAlgorithmLab,
  currentStrategy,
  onChangeStrategy
}) => {
  return (
    <div className="route-plan-panel flex flex-col h-full bg-white border border-orange-200 rounded-2xl overflow-hidden shadow-xs text-xs">
      {/* Header & Primary Actions */}
      <div className="p-3.5 border-b border-orange-100 bg-white flex flex-wrap items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="font-bold text-slate-900 text-sm">Route Schedule & Sequence</h3>
            {plan && (
              <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                plan.allDeadlinesMet
                  ? "bg-emerald-100 text-emerald-800 border border-emerald-200"
                  : "bg-amber-100 text-amber-800 border border-amber-200"
              }`}>
                {plan.allDeadlinesMet ? "✓ 100% On-Time" : "Constrained"}
              </span>
            )}
          </div>
          <div className="text-[11px] text-slate-500 mt-0.5 font-medium">
            Continuous vehicle load & arrival deadline verification
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2 flex-wrap">
          <select
            value={currentStrategy}
            onChange={(e) => onChangeStrategy(e.target.value as PlanningStrategy)}
            className="bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs text-slate-800 font-medium focus:outline-none focus:border-orange-500 cursor-pointer"
          >
            <option value="dp_knapsack">0/1 Knapsack DP (Optimal Profit)</option>
            <option value="greedy_density">Greedy: Profit Density (₹/kg)</option>
            <option value="greedy_profit">Greedy: Highest Profit (₹)</option>
            <option value="greedy_deadline">Greedy: Earliest Deadline</option>
          </select>

          <button
            onClick={() => onRunPlan(currentStrategy)}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-orange-500 hover:bg-orange-600 text-white font-bold rounded-lg shadow-sm transition-all active:scale-95"
          >
            <Play className="w-3.5 h-3.5" />
            <span>Plan Deliveries</span>
          </button>

          <button
            onClick={onResetPlan}
            className="p-1.5 bg-slate-50 hover:bg-slate-100 text-slate-600 hover:text-slate-900 rounded-lg transition-colors border border-slate-200"
            title="Reset Plan"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>

          <button
            onClick={onOpenAlgorithmLab}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-orange-50 hover:bg-orange-100 text-orange-700 font-bold rounded-lg border border-orange-200 transition-colors"
          >
            <Cpu className="w-3.5 h-3.5 text-orange-600" />
            <span>Algorithm Lab</span>
          </button>
        </div>
      </div>

      {/* Summary KPI Strip */}
      {plan && (
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 p-3 bg-orange-50/40 border-b border-orange-100 text-[11px]">
          <div className="p-2 rounded-lg bg-white border border-orange-100 shadow-xs">
            <div className="text-slate-500 flex items-center gap-1 font-semibold">
              <TrendingUp className="w-3 h-3 text-orange-600" />
              <span>Profit</span>
            </div>
            <div className="font-mono text-orange-600 font-bold text-sm mt-0.5">
              ₹{plan.totalProfit}
            </div>
          </div>

          <div className="p-2 rounded-lg bg-white border border-orange-100 shadow-xs">
            <div className="text-slate-500 flex items-center gap-1 font-semibold">
              <Package className="w-3 h-3 text-orange-600" />
              <span>Dispatched</span>
            </div>
            <div className="font-mono text-slate-800 font-bold text-sm mt-0.5">
              {plan.acceptedRequests.length} / {plan.acceptedRequests.length + plan.deferredRequests.length}
            </div>
          </div>

          <div className="p-2 rounded-lg bg-white border border-orange-100 shadow-xs">
            <div className="text-slate-500 font-semibold">Distance</div>
            <div className="font-mono text-slate-800 font-bold text-sm mt-0.5">
              {plan.totalDistanceKm} km
            </div>
          </div>

          <div className="p-2 rounded-lg bg-white border border-orange-100 shadow-xs">
            <div className="text-slate-500 flex items-center gap-1 font-semibold">
              <Clock className="w-3 h-3 text-orange-600" />
              <span>Duration</span>
            </div>
            <div className="font-mono text-slate-800 font-bold text-sm mt-0.5">
              {plan.totalTravelMinutes}m
            </div>
          </div>

          <div className="p-2 rounded-lg bg-white border border-orange-100 shadow-xs">
            <div className="text-slate-500 font-semibold">Capacity</div>
            <div className="font-mono text-slate-800 font-bold text-sm mt-0.5">
              {plan.capacityUtilizationPct}%
            </div>
          </div>
        </div>
      )}

      {/* Ordered Stops List */}
      <div className="flex-1 overflow-auto p-3 space-y-2">
        {!plan || plan.stops.length === 0 ? (
          <div className="py-12 text-center text-slate-400">
            <p>No active route. Click <strong>Plan Deliveries</strong> to calculate optimal route.</p>
          </div>
        ) : (
          plan.stops.map((stop) => {
            const isPickup = stop.action === "PICKUP";
            const isDrop = stop.action === "DROP";

            let actionColor = "bg-orange-100 text-orange-800 border-orange-300";
            if (isPickup) actionColor = "bg-sky-100 text-sky-800 border-sky-300";
            if (isDrop) actionColor = "bg-emerald-100 text-emerald-800 border-emerald-300";

            return (
              <div
                key={stop.stopNumber}
                className="p-3 rounded-xl bg-white border border-slate-200 hover:border-orange-300 hover:bg-orange-50/20 transition-all flex items-center justify-between gap-3 text-xs shadow-xs"
              >
                <div className="flex items-center gap-3">
                  {/* Stop Number Circle in Orange */}
                  <div className="w-6 h-6 rounded-full bg-orange-500 text-white font-bold flex items-center justify-center text-[11px] shrink-0 shadow-xs">
                    {stop.stopNumber}
                  </div>

                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-slate-900">{stop.locationName}</span>
                      <span className={`px-2 py-0.2 rounded text-[10px] font-bold border ${actionColor}`}>
                        {stop.action.replace("_", " ")}
                      </span>
                      {stop.requestId && (
                        <span className="font-mono font-bold text-orange-600 text-[11px]">
                          ({stop.requestId})
                        </span>
                      )}
                    </div>

                    <div className="text-[11px] text-slate-500 mt-1 flex items-center gap-3">
                      <span>Leg: <strong className="text-slate-700">{stop.legDistanceKm} km</strong></span>
                      <span>•</span>
                      <span>Arrival: <strong className="text-slate-700">{stop.arrivalMinute}m</strong></span>
                      {stop.deadlineMinute && (
                        <>
                          <span>•</span>
                          <span>Deadline: <strong className="text-orange-600">{stop.deadlineMinute}m</strong></span>
                          <span>•</span>
                          <span>Slack: <strong className={stop.slackMinutes && stop.slackMinutes >= 0 ? "text-emerald-600" : "text-rose-600"}>{stop.slackMinutes}m</strong></span>
                        </>
                      )}
                    </div>
                  </div>
                </div>

                {/* Load Counter after stop */}
                <div className="text-right shrink-0">
                  <div className="text-slate-400 text-[10px] font-semibold">VEHICLE LOAD</div>
                  <div className="text-slate-900 font-bold font-mono text-xs">
                    {stop.loadAfterStopKg} / {stop.capacityKg} kg
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Feasibility Repair Callout if any removals happened */}
      {plan && plan.repairs.length > 0 && (
        <div className="p-3 bg-amber-50 border-t border-amber-200 text-amber-900 text-[11px]">
          <div className="flex items-center gap-1.5 font-bold mb-1 text-amber-800">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
            <span>Feasibility Repair Applied (Late Orders Deferred):</span>
          </div>
          {plan.repairs.map((r, i) => (
            <div key={i} className="pl-5 text-amber-800">
              • Deferred <strong>{r.removedRequestId}</strong>: {r.reason}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
