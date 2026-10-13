import React, { useState, useEffect } from 'react';
import { FinalPlan, DeliveryRequest, Vehicle } from '../../types';
import { LogisticsGraph } from '../../lib/algorithms/graph';
import { Lab0Assumptions } from './Lab0Assumptions';
import { Lab1Graph } from './Lab1Graph';
import { Lab2Dijkstra } from './Lab2Dijkstra';
import { Lab3Greedy } from './Lab3Greedy';
import { Lab4Knapsack } from './Lab4Knapsack';
import { Lab5RouteConstruction } from './Lab5RouteConstruction';
import { Lab6Comparison } from './Lab6Comparison';
import {
  ChevronLeft,
  ChevronRight,
  Play,
  Pause,
  RotateCcw,
  ArrowLeft,
  GraduationCap
} from 'lucide-react';

interface AlgorithmLabProps {
  plan: FinalPlan | null;
  graph: LogisticsGraph;
  vehicle: Vehicle;
  deliveries: DeliveryRequest[];
  onBackToOperations: () => void;
  onUpdateVehicleCapacity: (newCap: number) => void;
  onUpdateDeliveryProfit: (id: string, newProfit: number) => void;
}

const LAB_STEPS = [
  { id: 0, title: "Lab 0: Assumptions & Inputs", desc: "Model parameters, fleet constraints, requests" },
  { id: 1, title: "Lab 1: Graph Representation", desc: "Adjacency list, vertices, road edges, degree" },
  { id: 2, title: "Lab 2: Dijkstra & Min-Heap", desc: "Step trace, relaxations, O((V+E) log V)" },
  { id: 3, title: "Lab 3: Greedy Baseline", desc: "Density ranking heuristic & local trade-offs" },
  { id: 4, title: "Lab 4: 0/1 Knapsack DP", desc: "Bellman recurrence, memo table & backtracking" },
  { id: 5, title: "Lab 5: Route Construction", desc: "Pickup-before-drop, load tracking & repair" },
  { id: 6, title: "Lab 6: Benchmark & Viva", desc: "Empirical comparison & academic boundaries" }
];

export const AlgorithmLab: React.FC<AlgorithmLabProps> = ({
  plan,
  graph,
  vehicle,
  deliveries,
  onBackToOperations,
  onUpdateVehicleCapacity,
  onUpdateDeliveryProfit
}) => {
  const getInitialStep = (): number => {
    if (typeof window !== 'undefined') {
      const hash = window.location.hash.toLowerCase();
      const match = hash.match(/lab[_-]?(\d)/i);
      if (match) {
        const s = parseInt(match[1], 10);
        if (s >= 0 && s < LAB_STEPS.length) return s;
      }
    }
    return 0;
  };
  const [activeStep, setActiveStep] = useState<number>(getInitialStep);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [playbackSpeed, setPlaybackSpeed] = useState<number>(1.0);
  const [selectedLocationId, setSelectedLocationId] = useState<string | null>(null);

  useEffect(() => {
    const handleHash = () => {
      const hash = window.location.hash.toLowerCase();
      const match = hash.match(/lab[_-]?(\d)/i);
      if (match) {
        const s = parseInt(match[1], 10);
        if (s >= 0 && s < LAB_STEPS.length) setActiveStep(s);
      }
    };
    window.addEventListener('hashchange', handleHash);
    return () => window.removeEventListener('hashchange', handleHash);
  }, []);

  useEffect(() => {
    let timer: any;
    if (isPlaying) {
      const intervalMs = Math.round(4000 / playbackSpeed);
      timer = setInterval(() => {
        setActiveStep((prev) => {
          if (prev >= LAB_STEPS.length - 1) {
            setIsPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }, intervalMs);
    }
    return () => clearInterval(timer);
  }, [isPlaying, playbackSpeed]);

  const handleNext = () => {
    if (activeStep < LAB_STEPS.length - 1) setActiveStep(activeStep + 1);
  };

  const handlePrev = () => {
    if (activeStep > 0) setActiveStep(activeStep - 1);
  };

  return (
    <div className="algorithm-lab-wrapper flex flex-col h-full bg-slate-50 text-slate-800">
      {/* Top Shell Bar */}
      <div className="p-3.5 border-b border-orange-200 bg-white flex flex-wrap items-center justify-between gap-3 text-xs shadow-xs">
        <div className="flex items-center gap-3">
          <button
            onClick={onBackToOperations}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-orange-50 hover:bg-orange-100 text-orange-700 font-bold rounded-lg border border-orange-200 transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Operations</span>
          </button>

          <div className="h-4 w-px bg-slate-200 hidden sm:block" />

          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-slate-900 text-sm">Algorithm Lab</span>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-orange-100 text-orange-700">
                DSA Defense
              </span>
            </div>
            <div className="text-[11px] text-slate-500">
              Instructor: <strong>Dr. Syed Javed Pasha</strong> • Project: <strong>Himanshu, Devyani, Heman, Rimika</strong>
            </div>
          </div>
        </div>

        {/* Stepper Timeline Controls */}
        <div className="flex items-center gap-2">
          <div className="flex items-center bg-slate-100 border border-slate-200 rounded-lg p-0.5">
            <button
              onClick={handlePrev}
              disabled={activeStep === 0}
              className="p-1.5 text-slate-600 hover:text-slate-900 disabled:opacity-30 rounded transition-colors"
              title="Previous Step"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>

            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="px-2.5 py-1 text-slate-800 hover:text-orange-600 font-bold flex items-center gap-1 transition-colors"
              title={isPlaying ? "Pause Tour" : "Play Guided Tour"}
            >
              {isPlaying ? <Pause className="w-3.5 h-3.5 text-orange-600" /> : <Play className="w-3.5 h-3.5 text-emerald-600" />}
              <span className="font-mono text-[11px]">
                {activeStep + 1} / {LAB_STEPS.length}
              </span>
            </button>

            <button
              onClick={handleNext}
              disabled={activeStep >= LAB_STEPS.length - 1}
              className="p-1.5 text-slate-600 hover:text-slate-900 disabled:opacity-30 rounded transition-colors"
              title="Next Step"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          {/* Speed Selector */}
          <select
            value={playbackSpeed}
            onChange={(e) => setPlaybackSpeed(parseFloat(e.target.value))}
            className="bg-white border border-slate-200 rounded-lg px-2 py-1 text-[11px] text-slate-700 font-medium focus:outline-none focus:border-orange-500"
          >
            <option value={0.5}>0.5x Speed</option>
            <option value={1.0}>1.0x Speed</option>
            <option value={2.0}>2.0x Speed</option>
          </select>

          <button
            onClick={() => {
              setActiveStep(0);
              setIsPlaying(false);
            }}
            className="p-1.5 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-lg border border-slate-200"
            title="Reset to Lab 0"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Lab Steps Nav Strip */}
      <div className="bg-white border-b border-orange-100 px-4 py-2 flex items-center gap-1.5 overflow-x-auto text-xs scrollbar-none shadow-xs">
        {LAB_STEPS.map((s) => {
          const isActive = s.id === activeStep;
          return (
            <button
              key={s.id}
              onClick={() => {
                setActiveStep(s.id);
                setIsPlaying(false);
              }}
              className={`px-3.5 py-1.5 rounded-xl whitespace-nowrap transition-all flex items-center gap-1.5 font-bold ${
                isActive
                  ? "bg-orange-500 text-white shadow-sm"
                  : "text-slate-600 hover:text-orange-600 hover:bg-orange-50/60"
              }`}
            >
              <span>{s.title.split(":")[0]}</span>
              {isActive && <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse" />}
            </button>
          );
        })}
      </div>

      {/* Main Lab Content Area */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6 max-w-7xl mx-auto w-full">
        {activeStep === 0 && (
          <Lab0Assumptions
            plan={plan}
            graph={graph}
            vehicle={vehicle}
            deliveries={deliveries}
            onUpdateVehicleCapacity={onUpdateVehicleCapacity}
            onUpdateDeliveryProfit={onUpdateDeliveryProfit}
          />
        )}

        {activeStep === 1 && (
          <Lab1Graph
            graph={graph}
            selectedLocationId={selectedLocationId}
            onSelectLocationId={setSelectedLocationId}
          />
        )}

        {activeStep === 2 && (
          <Lab2Dijkstra graph={graph} />
        )}

        {activeStep === 3 && (
          <Lab3Greedy candidates={deliveries} vehicle={vehicle} />
        )}

        {activeStep === 4 && (
          <Lab4Knapsack
            dpResult={plan ? plan.dpResult : {
              selectedDeliveries: [],
              deferredDeliveries: [],
              totalWeightKg: 0,
              totalProfit: 0,
              unusedCapacityKg: vehicle.capacityKg,
              capacityUtilizationPct: 0,
              dpTable: [[0]],
              itemLabels: ["Base"],
              capacityCols: [0],
              backtrackCells: [],
              traceSteps: [],
              unitScale: 1
            }}
            candidates={deliveries}
            vehicle={vehicle}
          />
        )}

        {activeStep === 5 && (
          <Lab5RouteConstruction plan={plan} />
        )}

        {activeStep === 6 && (
          <Lab6Comparison plan={plan} />
        )}
      </div>
    </div>
  );
};
