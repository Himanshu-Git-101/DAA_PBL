import React, { useState, useMemo } from 'react';
import { LogisticsGraph } from '../../lib/algorithms/graph';
import { runDijkstra } from '../../lib/algorithms/dijkstra';
import { ChevronLeft, ChevronRight, RotateCcw, Cpu, Crown, ArrowRight, BookOpen, Lightbulb } from 'lucide-react';

interface Lab2DijkstraProps {
  graph: LogisticsGraph;
}

export const Lab2Dijkstra: React.FC<Lab2DijkstraProps> = ({ graph }) => {
  const locations = graph.getAllLocations();
  const [startId, setStartId] = useState<string>("Main Parcel Warehouse");
  const [destId, setDestId] = useState<string>("Woxsen University");
  const [stepIdx, setStepIdx] = useState<number>(0);

  const dijkstraResult = useMemo(() => {
    return runDijkstra(graph, startId, destId, 32);
  }, [graph, startId, destId]);

  const currentStep = dijkstraResult.steps[stepIdx] || dijkstraResult.steps[0];
  const totalSteps = dijkstraResult.steps.length;

  const handleNext = () => {
    if (stepIdx < totalSteps - 1) setStepIdx(stepIdx + 1);
  };
  const handlePrev = () => {
    if (stepIdx > 0) setStepIdx(stepIdx - 1);
  };
  const handleReset = () => {
    setStepIdx(0);
  };

  return (
    <div className="lab-step-container space-y-4 text-xs text-slate-700 font-sans">
      {/* Overview Banner with Simple Intuition */}
      <div className="p-4 rounded-xl bg-orange-50 border border-orange-200 flex items-start gap-3 shadow-sm">
        <div className="w-9 h-9 rounded-lg bg-orange-500 text-white flex items-center justify-center shrink-0 shadow-sm">
          <Cpu className="w-5 h-5" />
        </div>
        <div className="space-y-1">
          <h4 className="text-sm font-bold text-slate-900">
            Lab 2: Dijkstra's Shortest Path Algorithm (Powered by Binary Min-Heap)
          </h4>
          <p className="text-slate-600 leading-relaxed text-xs">
            <strong>Core Intuition:</strong> Finds the guaranteed fastest driving route between any two junctions in Hyderabad.
            By organizing unexplored junctions in a <strong>Binary Min-Heap Priority Queue</strong>, we instantly retrieve the closest junction in <code className="bg-orange-100 text-orange-800 px-1 py-0.5 rounded font-mono font-bold">O(log |V|)</code> rather than scanning all junctions in <code className="bg-slate-100 text-slate-700 px-1 py-0.5 rounded font-mono">O(|V|)</code>.
          </p>
        </div>
      </div>

      {/* 3-Step Simple Explanation Card */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="p-3 rounded-xl bg-white border border-slate-200 shadow-2xs space-y-1">
          <div className="flex items-center gap-1.5 font-bold text-slate-900 text-xs">
            <span className="w-5 h-5 rounded-full bg-orange-100 text-orange-700 flex items-center justify-center text-[10px] font-bold">1</span>
            <span>Initialize Distances</span>
          </div>
          <p className="text-slate-500 text-[11px] leading-relaxed">
            Set distance to start location = <strong>0 km</strong>. Set all other junctions to <strong>∞ (infinity)</strong>. Insert start node into the Min-Heap.
          </p>
        </div>

        <div className="p-3 rounded-xl bg-white border border-slate-200 shadow-2xs space-y-1">
          <div className="flex items-center gap-1.5 font-bold text-slate-900 text-xs">
            <span className="w-5 h-5 rounded-full bg-orange-100 text-orange-700 flex items-center justify-center text-[10px] font-bold">2</span>
            <span>Extract-Min & Relax</span>
          </div>
          <p className="text-slate-500 text-[11px] leading-relaxed">
            Extract the closest node from the Min-Heap. Inspect all connected roads. If <code>dist[u] + road &lt; dist[v]</code>, update <code>dist[v]</code> (Edge Relaxation).
          </p>
        </div>

        <div className="p-3 rounded-xl bg-white border border-slate-200 shadow-2xs space-y-1">
          <div className="flex items-center gap-1.5 font-bold text-slate-900 text-xs">
            <span className="w-5 h-5 rounded-full bg-orange-100 text-orange-700 flex items-center justify-center text-[10px] font-bold">3</span>
            <span>Finalize Shortest Path</span>
          </div>
          <p className="text-slate-500 text-[11px] leading-relaxed">
            Repeat until destination is reached. Reconstruct exact road turn-by-turn trajectory by backtracking through recorded parent pointers.
          </p>
        </div>
      </div>

      {/* Selector & Controls Bar */}
      <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3 flex-wrap">
          <div className="flex items-center gap-2 text-xs">
            <div className="flex items-center gap-1.5 bg-slate-50 border border-slate-200 px-2.5 py-1.5 rounded-lg">
              <span className="text-slate-500 font-semibold">From:</span>
              <select
                value={startId}
                onChange={(e) => {
                  setStartId(e.target.value);
                  setStepIdx(0);
                }}
                className="bg-transparent font-bold text-slate-900 text-xs focus:outline-none cursor-pointer"
              >
                {locations.map((loc) => (
                  <option key={loc.id} value={loc.id}>{loc.name}</option>
                ))}
              </select>
            </div>

            <ArrowRight className="w-4 h-4 text-orange-500" />

            <div className="flex items-center gap-1.5 bg-slate-50 border border-slate-200 px-2.5 py-1.5 rounded-lg">
              <span className="text-slate-500 font-semibold">To:</span>
              <select
                value={destId}
                onChange={(e) => {
                  setDestId(e.target.value);
                  setStepIdx(0);
                }}
                className="bg-transparent font-bold text-slate-900 text-xs focus:outline-none cursor-pointer"
              >
                {locations.map((loc) => (
                  <option key={loc.id} value={loc.id}>{loc.name}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Stepper buttons */}
        <div className="flex items-center gap-2">
          <span className="font-mono text-slate-600 text-[11px] font-semibold bg-slate-100 px-2.5 py-1 rounded-lg">
            Step {stepIdx + 1} of {totalSteps}
          </span>
          <button
            onClick={handlePrev}
            disabled={stepIdx === 0}
            className="p-1.5 bg-white border border-slate-200 hover:bg-slate-50 disabled:opacity-30 rounded-lg text-slate-700 transition-colors shadow-2xs"
            title="Previous step"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <button
            onClick={handleNext}
            disabled={stepIdx >= totalSteps - 1}
            className="px-3 py-1.5 bg-orange-600 hover:bg-orange-500 disabled:opacity-30 rounded-lg text-white font-bold transition-all shadow-sm flex items-center gap-1"
          >
            <span>Next Step</span>
            <ChevronRight className="w-4 h-4" />
          </button>
          <button
            onClick={handleReset}
            className="p-1.5 bg-white border border-slate-200 hover:bg-slate-50 rounded-lg text-slate-500 hover:text-slate-900 transition-colors shadow-2xs"
            title="Reset to step 1"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Step Explanation Banner */}
      {currentStep && (
        <div className="p-3.5 rounded-xl bg-orange-50/90 border border-orange-200 flex items-start gap-3 shadow-2xs">
          <div className="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-orange-600 text-white shrink-0 mt-0.5">
            {currentStep.type}
          </div>
          <div className="text-slate-800 text-xs font-medium leading-relaxed">
            {currentStep.explanation}
          </div>
        </div>
      )}

      {/* Detailed execution state grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Min-Heap Contents */}
        <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <h5 className="font-bold text-slate-900 text-xs">Min-Heap Priority Queue</h5>
            <span className="text-[10px] text-orange-600 font-mono font-bold bg-orange-50 px-1.5 py-0.5 rounded border border-orange-200">
              Entries: {currentStep ? currentStep.heap.length : 0}
            </span>
          </div>
          <div className="text-[11px] text-slate-500 leading-normal">
            Binary Min-Heap keeps lowest tentative distance at index 0. <code className="text-orange-700 font-bold font-mono">poll()</code> runs in <code className="text-orange-700 font-mono font-bold">O(log |V|)</code>.
          </div>

          <div className="overflow-y-auto max-h-56 space-y-1.5 font-mono text-[11px]">
            {currentStep && currentStep.heap.length > 0 ? (
              currentStep.heap.map((entry, idx) => (
                <div
                  key={idx}
                  className={`p-2 rounded-lg border flex items-center justify-between transition-all ${
                    idx === 0
                      ? "bg-orange-50 border-orange-400 text-orange-950 font-bold shadow-2xs"
                      : "bg-slate-50 border-slate-200 text-slate-700"
                  }`}
                >
                  <span className="flex items-center gap-1.5">
                    {idx === 0 && <Crown className="w-3.5 h-3.5 text-orange-600" />}
                    <span>{idx === 0 ? "Root: " : `[${idx}] `}{entry.item}</span>
                  </span>
                  <span className="text-emerald-700 font-bold">{entry.priority.toFixed(1)} km</span>
                </div>
              ))
            ) : (
              <div className="py-6 text-center text-slate-400">Min-Heap is currently empty.</div>
            )}
          </div>
        </div>

        {/* Tentative Distance Table */}
        <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <h5 className="font-bold text-slate-900 text-xs">Tentative Distances [d]</h5>
            <span className="text-[10px] text-slate-500 font-mono">Total Nodes: {locations.length}</span>
          </div>
          <div className="overflow-y-auto max-h-56">
            <table className="w-full text-left border-collapse text-[11px]">
              <thead className="bg-slate-50 text-slate-600 sticky top-0 border-b border-slate-200">
                <tr>
                  <th className="p-1.5 font-semibold">Vertex</th>
                  <th className="p-1.5 text-right font-semibold">Distance</th>
                  <th className="p-1.5 text-right font-semibold">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-mono">
                {locations.map((loc) => {
                  const dist = currentStep?.distances[loc.id];
                  const isVisited = currentStep?.visited.includes(loc.id);
                  const isCurrent = currentStep?.currNode === loc.id;

                  return (
                    <tr key={loc.id} className={isCurrent ? "bg-orange-50 font-bold" : ""}>
                      <td className="p-1.5 text-slate-800">{loc.name}</td>
                      <td className="p-1.5 text-right text-emerald-700 font-bold">
                        {dist === Infinity ? "∞" : `${dist?.toFixed(1)} km`}
                      </td>
                      <td className="p-1.5 text-right text-[10px]">
                        {isVisited ? (
                          <span className="text-emerald-700 font-bold bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">FINALIZED</span>
                        ) : dist !== undefined && dist < Infinity ? (
                          <span className="text-orange-700 font-bold bg-orange-50 px-1.5 py-0.5 rounded border border-orange-200">FRONTIER</span>
                        ) : (
                          <span className="text-slate-400">UNVISITED</span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Finalized Path & Viva Defense */}
        <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-sm space-y-3">
          <div className="pb-2 border-b border-slate-100">
            <h5 className="font-bold text-slate-900 text-xs">Calculated Shortest Path</h5>
          </div>

          <div className="p-3 rounded-lg bg-orange-50/60 border border-orange-200 space-y-1.5">
            <div className="text-orange-900 font-bold text-[11px]">Reconstructed Route Sequence:</div>
            <div className="flex items-center flex-wrap gap-1 font-mono text-[11px] text-slate-900 font-bold">
              {dijkstraResult.path.map((node, i) => (
                <React.Fragment key={node}>
                  <span className="text-orange-600">{node}</span>
                  {i < dijkstraResult.path.length - 1 && <span className="text-slate-400">→</span>}
                </React.Fragment>
              ))}
            </div>
            <div className="mt-2 text-[11px] text-emerald-700 font-mono font-bold bg-white p-2 rounded border border-orange-100 flex items-center justify-between">
              <span>Total Distance:</span>
              <span>{dijkstraResult.distanceKm} km (~{dijkstraResult.travelMinutes} mins)</span>
            </div>
          </div>

          <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-1.5 text-[11px]">
            <div className="flex items-center gap-1.5 text-slate-900 font-bold">
              <BookOpen className="w-3.5 h-3.5 text-orange-600" />
              <span>Viva Defense Q&A:</span>
            </div>
            <p className="text-slate-600 leading-normal">
              <strong>Q: Why not simple BFS?</strong><br />
              BFS only works for unweighted graphs (all road distances = 1). Because roads in Hyderabad have varying distances (3 km to 24 km), Dijkstra is required.
            </p>
            <p className="text-slate-600 leading-normal">
              <strong>Time Complexity:</strong> <code className="text-orange-700 font-bold font-mono">O((|V| + |E|) log |V|)</code>.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
