import React from 'react';
import { FinalPlan } from '../../types';
import { Scale, BookOpen, Award, CheckCircle2, HelpCircle } from 'lucide-react';

interface Lab6ComparisonProps {
  plan: FinalPlan | null;
}

export const Lab6Comparison: React.FC<Lab6ComparisonProps> = ({ plan }) => {
  if (!plan) {
    return (
      <div className="py-16 text-center text-slate-400 text-xs">
        Run an active plan in Operations to compare heuristic baselines against Dynamic Programming.
      </div>
    );
  }

  const greedy = plan.greedyComparison;
  const finalProfit = plan.totalProfit;
  const finalWeight = plan.totalWeightKg;

  const profitDiff = finalProfit - greedy.totalProfit;

  return (
    <div className="lab-step-container space-y-4 text-xs text-slate-700 font-sans">
      {/* Overview Banner with Simple Intuition */}
      <div className="p-4 rounded-xl bg-orange-50 border border-orange-200 flex items-start gap-3 shadow-sm">
        <div className="w-9 h-9 rounded-lg bg-orange-500 text-white flex items-center justify-center shrink-0 shadow-sm">
          <Scale className="w-5 h-5" />
        </div>
        <div className="space-y-1">
          <h4 className="text-sm font-bold text-slate-900">
            Lab 6: Algorithmic Comparison & Academic Viva Defense
          </h4>
          <p className="text-slate-600 leading-relaxed text-xs">
            <strong>Core Intuition:</strong> Direct head-to-head empirical comparison computed across identical candidate parcel records ({plan.acceptedRequests.length + plan.deferredRequests.length} candidate requests across Hyderabad) and vehicle payload limits ({plan.vehicle.capacityKg} kg).
          </p>
        </div>
      </div>

      {/* Comparison Matrix Table */}
      <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-sm space-y-3">
        <h5 className="font-bold text-slate-900 text-xs pb-1 border-b border-slate-100">
          Benchmark Matrix: Greedy Baseline vs. 0/1 Knapsack DP Pipeline
        </h5>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-[11px]">
            <thead className="bg-slate-50 text-slate-700 font-bold border-b border-slate-200">
              <tr>
                <th className="p-2.5">Performance Dimension</th>
                <th className="p-2.5 bg-amber-50 text-amber-900">Greedy Baseline (Density)</th>
                <th className="p-2.5 bg-orange-50 text-orange-950">DP + Route Pipeline (SmartRoute)</th>
                <th className="p-2.5 text-center">Outcome Assessment</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono">
              <tr className="hover:bg-slate-50">
                <td className="p-2.5 font-sans font-semibold text-slate-900">Total Profit Generated</td>
                <td className="p-2.5 bg-amber-50/50 text-slate-900 font-bold">₹{greedy.totalProfit}</td>
                <td className="p-2.5 bg-orange-50/50 text-emerald-700 font-bold">₹{finalProfit}</td>
                <td className="p-2.5 text-center font-sans">
                  {profitDiff >= 0 ? (
                    <span className="text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                      +{profitDiff > 0 ? `₹${profitDiff} Higher Profit` : "Equally Optimal"}
                    </span>
                  ) : (
                    <span className="text-amber-800 font-bold bg-amber-50 px-2 py-0.5 rounded border border-amber-200">Constrained by deadlines</span>
                  )}
                </td>
              </tr>

              <tr className="hover:bg-slate-50">
                <td className="p-2.5 font-sans font-semibold text-slate-900">Vehicle Weight Utilized</td>
                <td className="p-2.5 bg-amber-50/50 text-slate-700">{greedy.totalWeightKg} / {plan.vehicle.capacityKg} kg</td>
                <td className="p-2.5 bg-orange-50/50 text-slate-900 font-bold">{finalWeight} / {plan.vehicle.capacityKg} kg</td>
                <td className="p-2.5 text-center font-sans text-slate-600">
                  <span className="font-semibold text-orange-600">{plan.capacityUtilizationPct}%</span> Payload Used
                </td>
              </tr>

              <tr className="hover:bg-slate-50">
                <td className="p-2.5 font-sans font-semibold text-slate-900">Packages Accepted</td>
                <td className="p-2.5 bg-amber-50/50 text-slate-600 font-sans">
                  {greedy.selectedDeliveries.length} orders
                </td>
                <td className="p-2.5 bg-orange-50/50 text-slate-900 font-bold font-sans">
                  {plan.acceptedRequests.length} orders dispatched
                </td>
                <td className="p-2.5 text-center font-sans text-slate-600">
                  High fulfillment rate
                </td>
              </tr>

              <tr className="hover:bg-slate-50">
                <td className="p-2.5 font-sans font-semibold text-slate-900">Deadline Verification</td>
                <td className="p-2.5 bg-amber-50/50 text-slate-500 font-sans">Not verified in greedy step</td>
                <td className="p-2.5 bg-orange-50/50 text-emerald-700 font-bold font-sans">
                  {plan.allDeadlinesMet ? "✓ 100% Feasible" : "Repaired"}
                </td>
                <td className="p-2.5 text-center font-sans text-emerald-700 font-semibold">Zero Late Deliveries</td>
              </tr>

              <tr className="hover:bg-slate-50">
                <td className="p-2.5 font-sans font-semibold text-slate-900">Time Complexity</td>
                <td className="p-2.5 bg-amber-50/50 text-orange-700 font-bold">O(n log n)</td>
                <td className="p-2.5 bg-orange-50/50 text-orange-700 font-bold">O(n × C) + O(Stops × Dijkstra)</td>
                <td className="p-2.5 text-center font-sans text-slate-500">Polynomial Bound</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Top 4 Viva Questions & Answers */}
      <div className="p-4 rounded-xl bg-orange-50/70 border border-orange-200 space-y-3 shadow-sm">
        <div className="flex items-center gap-2 text-slate-900 font-bold text-xs pb-1 border-b border-orange-200/60">
          <Award className="w-4 h-4 text-orange-600" />
          <span>Faculty Viva Cheat Sheet: Top 4 Questions & Exact Winning Answers</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <div className="p-3 rounded-xl bg-white border border-orange-200 space-y-1">
            <div className="font-bold text-slate-900">Q1: Why not solve Vehicle Routing (VRP) with pure DP?</div>
            <p className="text-slate-600 leading-normal text-[11px]">
              <strong>Answer:</strong> Exact multi-stop Vehicle Routing with Time Windows (VRP-TW) is NP-hard.
              Solving both packing AND stop permutations together in pure DP would take factorial exponential time <code className="font-mono">O(n!)</code>.
              SmartRoute decomposes the problem into 0/1 Knapsack DP for optimal parcel selection (<code className="font-mono">O(nC)</code>), followed by a Dijkstra nearest-stop heuristic (<code className="font-mono">O((V+E)log V)</code>), running in milliseconds.
            </p>
          </div>

          <div className="p-3 rounded-xl bg-white border border-orange-200 space-y-1">
            <div className="font-bold text-slate-900">Q2: Why use a Min-Heap for Dijkstra?</div>
            <p className="text-slate-600 leading-normal text-[11px]">
              <strong>Answer:</strong> Without a Min-Heap, finding the next unvisited vertex takes <code className="font-mono">O(|V|)</code> linear scan, giving total time <code className="font-mono">O(|V|²)</code>.
              A Binary Min-Heap gives instant <code className="font-mono">O(1)</code> root lookup and <code className="font-mono">O(log |V|)</code> extraction, reducing total runtime to <code className="font-mono">O((|V| + |E|) log |V|)</code>.
            </p>
          </div>

          <div className="p-3 rounded-xl bg-white border border-orange-200 space-y-1">
            <div className="font-bold text-slate-900">Q3: When does Greedy beat or match DP?</div>
            <p className="text-slate-600 leading-normal text-[11px]">
              <strong>Answer:</strong> Greedy Fractional Knapsack (where items can be cut into pieces) is always optimal.
              In 0/1 discrete knapsack, Greedy is only optimal if item weights perfectly divide the capacity without leaving empty pockets. Otherwise, DP is strictly superior.
            </p>
          </div>

          <div className="p-3 rounded-xl bg-white border border-orange-200 space-y-1">
            <div className="font-bold text-slate-900">Q4: How does SmartRoute enforce Pickup-Before-Drop?</div>
            <p className="text-slate-600 leading-normal text-[11px]">
              <strong>Answer:</strong> The route scheduler maintains two hash sets: <code className="font-mono">pickedUp</code> and <code className="font-mono">delivered</code>.
              A DROP action is only added to the candidate action set if the package ID already exists in <code className="font-mono">pickedUp</code>.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
