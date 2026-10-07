import React, { useState } from 'react';
import { KnapsackDpResult, DeliveryRequest, Vehicle } from '../../types';
import { explainDpCell } from '../../lib/algorithms/knapsack';
import { Layers, CheckCircle, Sparkles, CornerDownRight, BookOpen, Lightbulb } from 'lucide-react';

interface Lab4KnapsackProps {
  dpResult: KnapsackDpResult;
  candidates: DeliveryRequest[];
  vehicle: Vehicle;
}

export const Lab4Knapsack: React.FC<Lab4KnapsackProps> = ({
  dpResult,
  candidates,
  vehicle
}) => {
  const [selectedCell, setSelectedCell] = useState<{ row: number; col: number } | null>(null);

  const cellExplanation = selectedCell
    ? explainDpCell(candidates, dpResult.dpTable, selectedCell.row, selectedCell.col, dpResult.unitScale)
    : null;

  const isBacktrackCell = (r: number, c: number) => {
    return dpResult.backtrackCells.some(cell => cell.row === r && cell.col === c);
  };

  const isChosenBacktrackCell = (r: number, c: number) => {
    return dpResult.backtrackCells.some(cell => cell.row === r && cell.col === c && cell.chosen);
  };

  return (
    <div className="lab-step-container space-y-4 text-xs text-slate-700 font-sans">
      {/* Overview Banner with Simple Intuition */}
      <div className="p-4 rounded-xl bg-orange-50 border border-orange-200 flex items-start gap-3 shadow-sm">
        <div className="w-9 h-9 rounded-lg bg-orange-500 text-white flex items-center justify-center shrink-0 shadow-sm">
          <Layers className="w-5 h-5" />
        </div>
        <div className="space-y-1">
          <h4 className="text-sm font-bold text-slate-900">
            Lab 4: 0/1 Knapsack Dynamic Programming (Guaranteed Global Maximum Profit)
          </h4>
          <p className="text-slate-600 leading-relaxed text-xs">
            <strong>Core Intuition:</strong> You cannot deliver half an AI server or 0.4 of a medicine box. Every delivery is <strong>0 (LEAVE IT)</strong> or <strong>1 (TAKE IT)</strong>.
            By constructing a 2D memoization table across all weight increments from 0 to {vehicle.capacityKg} kg, Dynamic Programming systematically considers every combination in <code className="bg-orange-100 text-orange-800 px-1 py-0.5 rounded font-mono font-bold">O(n × C)</code> time and guarantees the 100% mathematical global maximum profit!
          </p>
        </div>
      </div>

      {/* 2-Choice Decision Logic Card */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-2xs space-y-1.5">
          <div className="flex items-center gap-1.5 font-bold text-slate-900 text-xs">
            <span className="w-2.5 h-2.5 rounded-full bg-slate-400" />
            <span>Choice 1: SKIP Item (i)</span>
          </div>
          <p className="text-slate-500 text-[11px] leading-normal">
            If we skip this parcel, the max profit is whatever we previously achieved with the first <code>i - 1</code> packages at capacity <code>c</code>:
            <br />
            <code className="text-slate-700 font-mono font-semibold bg-slate-100 px-1.5 py-0.5 rounded mt-1 inline-block">SKIP = dp[i - 1][c]</code>
          </p>
        </div>

        <div className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-2xs space-y-1.5">
          <div className="flex items-center gap-1.5 font-bold text-slate-900 text-xs">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
            <span>Choice 2: TAKE Item (i)</span>
          </div>
          <p className="text-slate-500 text-[11px] leading-normal">
            If item weight fits (<code>w_i ≤ c</code>), take its profit and add the optimal profit of the remaining space <code>c - w_i</code>:
            <br />
            <code className="text-emerald-800 font-mono font-semibold bg-emerald-50 px-1.5 py-0.5 rounded mt-1 inline-block">TAKE = profit[i] + dp[i - 1][c - weight[i]]</code>
          </p>
        </div>
      </div>

      {/* Interactive 2D DP Table */}
      <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-sm space-y-3">
        <div className="flex items-center justify-between flex-wrap gap-2 pb-2 border-b border-slate-100">
          <div>
            <h5 className="font-bold text-slate-900 text-xs">Full 2D Dynamic Programming Memoization Table</h5>
            <span className="text-[11px] text-slate-500">
              Click any cell to inspect its exact mathematical comparison. The optimal backtrack trail is highlighted in green.
            </span>
          </div>

          <div className="flex items-center gap-3 text-[11px] font-mono">
            <span className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded bg-amber-100 border border-amber-400 inline-block"></span>
              <span className="text-amber-800 font-semibold">Backtrack Trail</span>
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded bg-emerald-100 border border-emerald-500 inline-block"></span>
              <span className="text-emerald-800 font-semibold">Item Chosen</span>
            </span>
          </div>
        </div>

        {/* Scrollable Table Matrix */}
        <div className="overflow-x-auto border border-slate-200 rounded-lg max-h-72">
          <table className="border-collapse text-[11px] font-mono min-w-full">
            <thead className="bg-slate-50 text-slate-700 sticky top-0 z-10 select-none border-b border-slate-200">
              <tr>
                <th className="p-2 border-r border-slate-200 text-left min-w-[140px] font-bold">
                  Package (i) \ Cap (c)
                </th>
                {dpResult.capacityCols.map((col) => (
                  <th key={col} className="p-2 border-r border-slate-200 text-center min-w-[42px] font-semibold text-slate-600">
                    {col}kg
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {dpResult.dpTable.map((row, rIdx) => {
                const label = dpResult.itemLabels[rIdx] || `i=${rIdx}`;

                return (
                  <tr key={rIdx} className="hover:bg-slate-50">
                    <td className="p-2 border-r border-slate-200 font-sans font-semibold text-slate-800 bg-slate-50/80 sticky left-0 z-5">
                      {label}
                    </td>

                    {row.map((val, cIdx) => {
                      const isBacktrack = isBacktrackCell(rIdx, cIdx);
                      const isChosen = isChosenBacktrackCell(rIdx, cIdx);
                      const isSelected = selectedCell?.row === rIdx && selectedCell?.col === cIdx;

                      let cellBg = "bg-white text-slate-700";
                      if (isChosen) {
                        cellBg = "bg-emerald-100 text-emerald-900 font-bold border-2 border-emerald-500 shadow-2xs";
                      } else if (isBacktrack) {
                        cellBg = "bg-amber-50 text-amber-900 font-bold border border-amber-400";
                      } else if (isSelected) {
                        cellBg = "bg-orange-100 text-orange-950 font-bold border-2 border-orange-500";
                      }

                      return (
                        <td
                          key={cIdx}
                          onClick={() => setSelectedCell({ row: rIdx, col: cIdx })}
                          className={`p-1.5 border-r border-slate-100 text-center cursor-pointer transition-colors hover:bg-orange-50 ${cellBg}`}
                        >
                          {val}
                        </td>
                      );
                    })}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Selected Cell Recurrence Arithmetic Inspector */}
      {cellExplanation && (
        <div className="p-4 rounded-xl bg-orange-50/80 border border-orange-300 space-y-2 shadow-sm animate-fadeIn">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-slate-900 font-bold text-xs">
              <CornerDownRight className="w-4 h-4 text-orange-600" />
              <span>
                Inspecting Cell: dp[{cellExplanation.itemIdx}][{cellExplanation.capacityCol}]
                {cellExplanation.itemIdx > 0 && ` (${candidates[cellExplanation.itemIdx - 1]?.id})`}
              </span>
            </div>
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-orange-600 text-white">
              {cellExplanation.status}
            </span>
          </div>

          <div className="p-3 rounded-lg bg-white border border-orange-200 font-mono text-xs text-slate-900 font-semibold shadow-2xs">
            {cellExplanation.formula}
          </div>

          {cellExplanation.decision && (
            <div className="text-[11px] text-slate-700">
              Decision for this parcel: <strong className={cellExplanation.decision === "TAKE" ? "text-emerald-700" : "text-amber-700"}>
                {cellExplanation.decision}
              </strong>. (Take Profit = ₹{cellExplanation.takeVal} vs Skip Profit = ₹{cellExplanation.skipVal}).
            </div>
          )}
        </div>
      )}

      {/* Backtracked Selection Summary */}
      <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-sm space-y-2">
        <div className="flex items-center justify-between pb-1 border-b border-slate-100">
          <h5 className="font-bold text-slate-900 text-xs">Optimal Backtracking Result</h5>
          <span className="font-mono text-emerald-700 font-bold text-xs">
            Total Profit: ₹{dpResult.totalProfit} • Weight: {dpResult.totalWeightKg} kg
          </span>
        </div>
        <div className="text-slate-600 text-xs">
          Backtracking from <code className="bg-slate-100 px-1 py-0.5 rounded font-mono text-slate-800">dp[{candidates.length}][{vehicle.capacityKg}]</code> backward along the table identifies
          which items contributed to the maximum total profit:
        </div>
        <div className="flex flex-wrap gap-2 pt-1">
          {dpResult.selectedDeliveries.map((item) => (
            <div
              key={item.id}
              className="p-2.5 rounded-lg bg-emerald-50 border border-emerald-300 flex items-center gap-2 font-mono shadow-2xs"
            >
              <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
              <span className="text-slate-900 font-bold">{item.id}</span>
              <span className="text-slate-600">({item.weightKg} kg, ₹{item.profit})</span>
            </div>
          ))}
        </div>
      </div>

      {/* Viva Defense Tip */}
      <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1.5 text-xs text-slate-700">
        <div className="flex items-center gap-2 font-bold text-slate-900">
          <BookOpen className="w-4 h-4 text-orange-600" />
          <span>Faculty Viva Defense: Why is 0/1 Knapsack pseudo-polynomial?</span>
        </div>
        <p className="leading-relaxed text-slate-600">
          The time complexity is <code className="text-orange-700 font-bold font-mono">O(n × C)</code> where <code>n</code> is candidate count and <code>C</code> is vehicle capacity.
          It is called "pseudo-polynomial" because its runtime depends on the numeric value of <code>C</code>, not just the number of bits in the input. In last-mile delivery, <code>C</code> is a fixed physical vehicle payload (e.g. 75 kg), making it run in fractions of a millisecond!
        </p>
      </div>
    </div>
  );
};
