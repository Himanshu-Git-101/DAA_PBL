import React, { useState, useMemo } from 'react';
import { DeliveryRequest, Vehicle } from '../../types';
import { runGreedySelection, GreedyCriterion } from '../../lib/algorithms/greedySelection';
import { SlidersHorizontal, CheckCircle2, XCircle, BookOpen, AlertCircle } from 'lucide-react';

interface Lab3GreedyProps {
  candidates: DeliveryRequest[];
  vehicle: Vehicle;
}

export const Lab3Greedy: React.FC<Lab3GreedyProps> = ({ candidates, vehicle }) => {
  const [criterion, setCriterion] = useState<GreedyCriterion>("profit_density");

  const greedyResult = useMemo(() => {
    return runGreedySelection(candidates, vehicle.capacityKg, criterion);
  }, [candidates, vehicle.capacityKg, criterion]);

  return (
    <div className="lab-step-container space-y-4 text-xs text-slate-700 font-sans">
      {/* Overview Banner with Simple Intuition */}
      <div className="p-4 rounded-xl bg-orange-50 border border-orange-200 flex items-start gap-3 shadow-sm">
        <div className="w-9 h-9 rounded-lg bg-orange-500 text-white flex items-center justify-center shrink-0 shadow-sm">
          <SlidersHorizontal className="w-5 h-5" />
        </div>
        <div className="space-y-1">
          <h4 className="text-sm font-bold text-slate-900">
            Lab 3: Greedy Package Selection Heuristics
          </h4>
          <p className="text-slate-600 leading-relaxed text-xs">
            <strong>Core Intuition:</strong> A Greedy heuristic sorts all candidate deliveries once by a simple rule, then packs items one by one into the vehicle until capacity is full.
            It never backtracks or considers combinations. It runs fast in <code className="bg-orange-100 text-orange-800 px-1 py-0.5 rounded font-mono font-bold">O(n log n)</code>, but often leaves awkward unused space.
          </p>
        </div>
      </div>

      {/* 3 Heuristic Criteria Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <button
          onClick={() => setCriterion("profit_density")}
          className={`p-3.5 rounded-xl border text-left transition-all ${
            criterion === "profit_density"
              ? "bg-orange-50 border-orange-500 shadow-sm ring-1 ring-orange-500"
              : "bg-white border-slate-200 hover:border-orange-300"
          }`}
        >
          <div className="flex items-center justify-between mb-1">
            <span className="font-bold text-slate-900 text-xs">1. Profit Density (₹/kg)</span>
            {criterion === "profit_density" && (
              <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-orange-600 text-white">ACTIVE</span>
            )}
          </div>
          <p className="text-slate-500 text-[11px] leading-normal">
            Prioritizes the highest profit per kilogram (<code className="text-orange-700 font-bold">profit ÷ weight</code>). Standard courier industry baseline heuristic.
          </p>
        </button>

        <button
          onClick={() => setCriterion("highest_profit")}
          className={`p-3.5 rounded-xl border text-left transition-all ${
            criterion === "highest_profit"
              ? "bg-orange-50 border-orange-500 shadow-sm ring-1 ring-orange-500"
              : "bg-white border-slate-200 hover:border-orange-300"
          }`}
        >
          <div className="flex items-center justify-between mb-1">
            <span className="font-bold text-slate-900 text-xs">2. Highest Absolute Profit (₹)</span>
            {criterion === "highest_profit" && (
              <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-orange-600 text-white">ACTIVE</span>
            )}
          </div>
          <p className="text-slate-500 text-[11px] leading-normal">
            Grabs high-value orders first (e.g. ₹1,680 3D Printers). However, heavy items eat up vehicle payload quickly, leaving fewer total orders delivered.
          </p>
        </button>

        <button
          onClick={() => setCriterion("earliest_deadline")}
          className={`p-3.5 rounded-xl border text-left transition-all ${
            criterion === "earliest_deadline"
              ? "bg-orange-50 border-orange-500 shadow-sm ring-1 ring-orange-500"
              : "bg-white border-slate-200 hover:border-orange-300"
          }`}
        >
          <div className="flex items-center justify-between mb-1">
            <span className="font-bold text-slate-900 text-xs">3. Earliest Deadline First (EDF)</span>
            {criterion === "earliest_deadline" && (
              <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-orange-600 text-white">ACTIVE</span>
            )}
          </div>
          <p className="text-slate-500 text-[11px] leading-normal">
            Prioritizes customer urgency regardless of profit. Best for critical SLA compliance (e.g. medical deliveries with 180 min deadlines).
          </p>
        </button>
      </div>

      {/* Outcomes Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-sm">
          <span className="text-slate-500 font-semibold text-[11px]">Total Profit Generated:</span>
          <div className="text-lg font-bold font-mono text-emerald-700 mt-1">
            ₹{greedyResult.totalProfit}
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-sm">
          <span className="text-slate-500 font-semibold text-[11px]">Vehicle Payload Used:</span>
          <div className="text-lg font-bold font-mono text-slate-900 mt-1">
            {greedyResult.totalWeightKg} <span className="text-xs text-slate-500 font-normal">/ {vehicle.capacityKg} kg</span>
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-sm">
          <span className="text-slate-500 font-semibold text-[11px]">Unused Capacity Left:</span>
          <div className="text-lg font-bold font-mono text-orange-600 mt-1">
            {greedyResult.unusedCapacityKg} kg
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-sm">
          <span className="text-slate-500 font-semibold text-[11px]">Packages Accepted:</span>
          <div className="text-lg font-bold font-mono text-slate-900 mt-1">
            {greedyResult.selectedDeliveries.length} <span className="text-xs text-slate-500 font-normal">/ {candidates.length}</span>
          </div>
        </div>
      </div>

      {/* Greedy Step-by-Step Scan Table */}
      <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-sm space-y-2">
        <div className="flex items-center justify-between pb-2 border-b border-slate-100">
          <div>
            <h5 className="font-bold text-slate-900 text-xs">Sequential Greedy Decision Trace</h5>
            <span className="text-[11px] text-slate-500">
              Evaluated in sorted order ({criterion.replace("_", " ").toUpperCase()}). Green = Packed into vehicle. Red = Skipped due to capacity.
            </span>
          </div>
          <span className="text-[11px] font-mono text-orange-600 font-semibold bg-orange-50 px-2 py-0.5 rounded border border-orange-200">
            {greedyResult.selectedDeliveries.length} Accepted • {greedyResult.deferredDeliveries.length} Deferred
          </span>
        </div>

        <div className="overflow-x-auto max-h-72">
          <table className="w-full text-left border-collapse text-[11px]">
            <thead className="bg-slate-50 text-slate-600 sticky top-0 border-b border-slate-200">
              <tr>
                <th className="p-2 font-semibold">Rank</th>
                <th className="p-2 font-semibold">Package ID</th>
                <th className="p-2 text-right font-semibold">Weight</th>
                <th className="p-2 text-right font-semibold">Profit</th>
                <th className="p-2 text-right font-semibold">Density (₹/kg)</th>
                <th className="p-2 text-center font-semibold">Decision</th>
                <th className="p-2 font-semibold">Remaining Vehicle Payload</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono">
              {greedyResult.steps.map((st, i) => {
                const isAccepted = st.action === "ACCEPTED";
                return (
                  <tr key={st.requestId} className={isAccepted ? "bg-emerald-50/50" : "bg-rose-50/30"}>
                    <td className="p-2 text-slate-500">#{i + 1}</td>
                    <td className="p-2 text-slate-900 font-bold">{st.requestId}</td>
                    <td className="p-2 text-right text-slate-700">{st.weightKg} kg</td>
                    <td className="p-2 text-right text-emerald-700 font-bold">₹{st.profit}</td>
                    <td className="p-2 text-right text-orange-700 font-bold">{st.ratio}</td>
                    <td className="p-2 text-center">
                      {isAccepted ? (
                        <span className="inline-flex items-center gap-1 text-emerald-700 font-bold bg-emerald-100 px-2 py-0.5 rounded border border-emerald-300">
                          <CheckCircle2 className="w-3 h-3" /> ACCEPT
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-rose-700 font-bold bg-rose-100 px-2 py-0.5 rounded border border-rose-200">
                          <XCircle className="w-3 h-3" /> SKIP
                        </span>
                      )}
                    </td>
                    <td className="p-2 text-slate-600">
                      {st.remainingCapacityKg} kg remaining
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Viva Insight Box */}
      <div className="p-4 rounded-xl bg-orange-50 border border-orange-200 space-y-2">
        <div className="flex items-center gap-2 text-slate-900 font-bold text-xs">
          <BookOpen className="w-4 h-4 text-orange-600" />
          <span>Faculty Viva Defense: Why does Greedy fail to achieve optimal profit?</span>
        </div>
        <p className="text-slate-700 leading-relaxed text-xs">
          <strong>The Classical Knapsack Counterexample:</strong> If vehicle capacity is 10 kg, and we have one heavy item (6 kg, ₹60) and two smaller items (5 kg each, ₹50 each = ₹100 total):
          Greedy takes the 6 kg item first because of its standalone size or density, leaving 4 kg empty (profit = ₹60).
          The true mathematical optimum is taking both 5 kg items together for 10 kg and ₹100 profit!
          To guarantee 100% optimal package selection, we need <strong>0/1 Knapsack Dynamic Programming (Lab 4)</strong>.
        </p>
      </div>
    </div>
  );
};
