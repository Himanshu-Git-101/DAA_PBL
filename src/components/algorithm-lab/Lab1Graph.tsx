import React, { useState } from 'react';
import { LogisticsGraph } from '../../lib/algorithms/graph';
import { Location } from '../../types';
import { Network, ArrowRight, BookOpen, MapPin } from 'lucide-react';

interface Lab1GraphProps {
  graph: LogisticsGraph;
  selectedLocationId: string | null;
  onSelectLocationId: (id: string | null) => void;
}

export const Lab1Graph: React.FC<Lab1GraphProps> = ({
  graph,
  selectedLocationId,
  onSelectLocationId
}) => {
  const [activeTab, setActiveTab] = useState<"list" | "theory">("list");
  const locations = graph.getAllLocations();

  return (
    <div className="lab-step-container space-y-4 text-xs text-slate-700 font-sans">
      {/* Intro banner in Orange & White */}
      <div className="p-4 rounded-xl bg-orange-50 border border-orange-200 flex items-start gap-3 shadow-sm">
        <div className="w-9 h-9 rounded-lg bg-orange-500 text-white flex items-center justify-center shrink-0 shadow-sm">
          <Network className="w-5 h-5" />
        </div>
        <div>
          <h4 className="text-sm font-bold text-slate-900 mb-1">
            Lab 1: Road Network Graph & Adjacency List Structure
          </h4>
          <p className="text-slate-600 leading-relaxed text-xs">
            Urban delivery maps are sparse graphs: each junction connects to only 2–4 immediate neighboring roads.
            SmartRoute models the street network as a memory-efficient <strong className="text-orange-900">Adjacency List</strong> taking <code className="bg-orange-100/70 text-orange-800 px-1 py-0.5 rounded font-mono font-bold">O(|V| + |E|)</code> space,
            avoiding a wasteful <code className="bg-slate-100 text-slate-700 px-1 py-0.5 rounded font-mono">O(|V|²)</code> matrix where &gt;80% of cells would be dead zeroes.
          </p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-2">
        <button
          onClick={() => setActiveTab("list")}
          className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
            activeTab === "list"
              ? "bg-orange-600 text-white shadow-sm"
              : "bg-white text-slate-600 border border-slate-200 hover:text-orange-600 hover:bg-orange-50/50"
          }`}
        >
          Interactive Adjacency List
        </button>
        <button
          onClick={() => setActiveTab("theory")}
          className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
            activeTab === "theory"
              ? "bg-orange-600 text-white shadow-sm"
              : "bg-white text-slate-600 border border-slate-200 hover:text-orange-600 hover:bg-orange-50/50"
          }`}
        >
          Viva Defense & Asymptotics
        </button>
      </div>

      {activeTab === "list" && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Adjacency List Rows */}
          <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-sm overflow-y-auto max-h-[480px] space-y-2">
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <h5 className="font-bold text-slate-900 text-xs">Vertex Adjacency Records</h5>
              <span className="text-[11px] text-orange-600 font-mono font-semibold">Click a row to inspect</span>
            </div>

            {locations.map((loc) => {
              const neighbors = graph.getNeighbors(loc.id);
              const isSelected = loc.id === selectedLocationId;

              return (
                <div
                  key={loc.id}
                  onClick={() => onSelectLocationId(isSelected ? null : loc.id)}
                  className={`p-3 rounded-lg border cursor-pointer transition-all ${
                    isSelected
                      ? "bg-orange-50 border-orange-500 shadow-sm"
                      : "bg-slate-50/70 border-slate-200 hover:border-orange-300 hover:bg-orange-50/30"
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <div className="flex items-center gap-2">
                      <span className={`font-bold text-xs ${isSelected ? "text-orange-950" : "text-slate-900"}`}>
                        {loc.name}
                      </span>
                      <span className={`text-[10px] uppercase font-mono px-1.5 py-0.5 rounded font-semibold ${
                        loc.kind === 'depot' ? 'bg-orange-100 text-orange-800' : 'bg-slate-200 text-slate-700'
                      }`}>
                        {loc.kind}
                      </span>
                    </div>
                    <span className="font-mono text-[11px] text-slate-500 font-semibold">
                      deg(v) = {neighbors.length}
                    </span>
                  </div>

                  {/* Edges List */}
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    {neighbors.map((edge, idx) => (
                      <span
                        key={idx}
                        className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-white border border-slate-200 font-mono text-[11px] text-slate-700 shadow-2xs"
                      >
                        <ArrowRight className="w-2.5 h-2.5 text-orange-500" />
                        <span className="font-semibold text-slate-900">{edge.to}</span>
                        <span className="text-emerald-600 font-bold">({edge.distanceKm} km)</span>
                      </span>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Node Detail & Mathematical Formulation */}
          <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-sm space-y-4">
            <h5 className="font-bold text-slate-900 text-xs pb-2 border-b border-slate-100">
              Vertex Inspection & Weights
            </h5>

            {selectedLocationId ? (
              (() => {
                const loc = graph.getLocation(selectedLocationId);
                const neighbors = graph.getNeighbors(selectedLocationId);
                return (
                  <div className="space-y-3">
                    <div className="p-3.5 rounded-lg bg-orange-50/80 border border-orange-200">
                      <div className="flex items-center gap-2">
                        <MapPin className="w-4 h-4 text-orange-600" />
                        <span className="text-slate-900 font-bold text-sm">{loc?.name}</span>
                      </div>
                      <div className="text-slate-600 text-[11px] mt-0.5">{loc?.area}</div>
                      <div className="mt-2.5 grid grid-cols-2 gap-2 text-[11px] font-mono text-slate-700 bg-white p-2 rounded border border-orange-100">
                        <div>GPS: <span className="font-bold text-slate-900">{loc?.lat.toFixed(4)}, {loc?.lng.toFixed(4)}</span></div>
                        <div>Kind: <span className="font-bold text-orange-700 uppercase">{loc?.kind}</span></div>
                      </div>
                    </div>

                    <div>
                      <h6 className="font-bold text-slate-900 mb-2 text-xs">Outgoing Road Segments:</h6>
                      <ul className="space-y-1.5">
                        {neighbors.map((edge, idx) => (
                          <li
                            key={idx}
                            className="p-2.5 rounded bg-slate-50 border border-slate-200 flex items-center justify-between font-mono"
                          >
                            <span className="font-semibold text-slate-800">→ {edge.to}</span>
                            <span className="text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                              {edge.distanceKm} km (~{edge.travelMinutes} mins)
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                );
              })()
            ) : (
              <div className="py-16 text-center text-slate-400">
                <MapPin className="w-8 h-8 text-slate-300 mx-auto mb-2" />
                Select any location from the list on the left to inspect degree, coordinates, and edge weights.
              </div>
            )}
          </div>
        </div>
      )}

      {activeTab === "theory" && (
        <div className="p-5 rounded-xl bg-white border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center gap-2 text-slate-900 font-bold text-sm pb-2 border-b border-slate-100">
            <BookOpen className="w-4 h-4 text-orange-600" />
            <span>Viva Defense: Graph Theory & Data Structure Selection</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-slate-700">
            <div className="p-4 rounded-xl bg-orange-50/50 border border-orange-200 space-y-2">
              <h6 className="font-bold text-orange-950 text-xs">Why Adjacency List over Adjacency Matrix?</h6>
              <p className="text-slate-600 leading-relaxed text-xs">
                In real urban logistics, a metropolitan area with 10,000 junctions averages only 3–4 outgoing roads per junction (~35,000 edges total).
                An Adjacency Matrix requires <code className="bg-white px-1 py-0.5 rounded border border-orange-200 text-orange-800 font-bold">10,000 × 10,000 = 100,000,000</code> cells (&gt;99% empty zeros).
                An Adjacency List stores only existing road connections, saving over 99% RAM and allowing linear iteration through actual outgoing branches.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
              <h6 className="font-bold text-slate-900 text-xs">Time & Space Complexity Bounds</h6>
              <ul className="space-y-1.5 text-slate-600 font-mono text-[11px]">
                <li className="flex justify-between border-b border-slate-200 pb-1">
                  <span>Graph Memory Footprint:</span>
                  <strong className="text-orange-600">O(|V| + |E|)</strong>
                </li>
                <li className="flex justify-between border-b border-slate-200 pb-1">
                  <span>Iterating Neighbors of u:</span>
                  <strong className="text-orange-600">O(deg(u))</strong>
                </li>
                <li className="flex justify-between border-b border-slate-200 pb-1">
                  <span>Edge Lookup (u, v):</span>
                  <strong className="text-orange-600">O(deg(u))</strong>
                </li>
                <li className="flex justify-between">
                  <span>Road Insertion:</span>
                  <strong className="text-orange-600">O(1)</strong>
                </li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
