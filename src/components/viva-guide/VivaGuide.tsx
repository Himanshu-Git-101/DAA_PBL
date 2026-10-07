import React from 'react';
import { BookOpen, GraduationCap, Clock, Award, Users, CheckCircle2, ShieldCheck } from 'lucide-react';

export const VivaGuide: React.FC = () => {
  const glossary = [
    { term: "Vertex (Node)", def: "A discrete delivery location, customer address, or logistics hub in the road network." },
    { term: "Edge", def: "A navigable road arterial connecting two vertices, assigned physical distance (km) and travel time (min)." },
    { term: "Weight", def: "The non-negative cost associated with traversing an edge. In SmartRoute, distance in kilometers." },
    { term: "Adjacency List", def: "An array/map of lists where each vertex stores only its immediate outgoing edges. Consumes O(V + E) space." },
    { term: "Min-Heap", def: "A complete binary tree where the key at the root is the minimum among all keys. Enables O(log V) priority queue extract-min." },
    { term: "Relaxation", def: "Testing whether the path to neighbor v through u is shorter than previously known tentative distance: dist[u] + weight(u,v) < dist[v]." },
    { term: "0/1 Knapsack DP", def: "Bellman recurrence dividing global optimization into subproblems where each item is either picked (1) or skipped (0)." },
    { term: "Greedy Heuristic", def: "An algorithm that makes the locally optimal choice at each stage with the hope of finding a global optimum. Fast but suboptimal." },
    { term: "Time Complexity", def: "Theoretical upper bound on CPU steps as input size grows (e.g. O((V+E) log V) for Dijkstra)." },
    { term: "Feasibility", def: "State where all operational constraints (vehicle max weight, customer deadlines, pickup-before-drop) are strictly respected." },
    { term: "Heuristic", def: "A practical approximation method that finds good, feasible solutions within polynomial time for NP-hard problems without guarantee of global optimality." }
  ];

  return (
    <div className="viva-guide-container p-4 md:p-8 max-w-5xl mx-auto space-y-6 text-xs text-slate-800">
      {/* Course & Team Academic Attribution Header in Orange & White */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-orange-500 via-orange-600 to-amber-500 text-white shadow-lg border border-orange-400/40">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/20 text-white font-bold text-[11px] mb-2 backdrop-blur-sm">
              <GraduationCap className="w-4 h-4" />
              <span>Data Structures and Algorithms • Project Based Learning</span>
            </div>
            <h1 className="text-2xl font-bold font-display tracking-tight text-white mb-1">
              SmartRoute: Last-Mile Delivery Operations Engine
            </h1>
            <p className="text-orange-100 text-xs max-w-2xl">
              An educational and commercial last-mile operations prototype built to defend core algorithmic trade-offs during faculty viva evaluation.
            </p>
          </div>
        </div>

        {/* Instructor & Team Cards Grid */}
        <div className="mt-5 grid grid-cols-1 md:grid-cols-2 gap-3 pt-4 border-t border-white/20">
          <div className="p-3.5 rounded-xl bg-white/10 backdrop-blur-md border border-white/20 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white text-orange-600 flex items-center justify-center font-bold text-lg shrink-0 shadow-sm">
              👨‍🏫
            </div>
            <div>
              <div className="text-[10px] font-bold uppercase tracking-wider text-orange-200">
                Course Instructor & Faculty Guide
              </div>
              <div className="text-sm font-bold text-white">Dr. Syed Javed Pasha</div>
              <div className="text-[11px] text-orange-100">Department of Computer Science & Engineering</div>
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-white/10 backdrop-blur-md border border-white/20">
            <div className="text-[10px] font-bold uppercase tracking-wider text-orange-200 mb-1 flex items-center gap-1.5">
              <Users className="w-3.5 h-3.5" />
              <span>Project Development Team</span>
            </div>
            <div className="grid grid-cols-2 gap-1 text-xs text-white font-semibold">
              <div>• Himanshu Pandit</div>
              <div>• Devyani Pawar</div>
              <div>• Heman</div>
              <div>• Rimika Jain</div>
            </div>
          </div>
        </div>
      </div>

      {/* 5-7 Minute Faculty Viva Presentation Script */}
      <div className="p-6 rounded-2xl bg-white border border-orange-200 shadow-sm space-y-4">
        <div className="flex items-center gap-2 text-slate-900 font-bold text-sm border-b border-orange-100 pb-3">
          <Clock className="w-5 h-5 text-orange-500" />
          <span>Recommended 5–7 Minute Faculty Viva Walkthrough Script</span>
        </div>

        <ol className="space-y-3.5 pl-1">
          <li className="p-3.5 rounded-xl bg-orange-50/50 border border-orange-100 space-y-1">
            <div className="font-bold text-slate-900 flex items-center gap-2">
              <span className="w-5 h-5 rounded-full bg-orange-500 text-white flex items-center justify-center text-[10px] font-mono">1</span>
              <span>Step 1: Problem Statement & Graph Representation (1 min)</span>
            </div>
            <p className="text-slate-600 pl-7 leading-relaxed">
              "We model last-mile logistics in Hyderabad as an undirected weighted road network with 13 hubs centered on Main Parcel Warehouse. Hubs are vertices and arterial roads are edges stored as an Adjacency List to guarantee <code>O(V + E)</code> spatial efficiency over dense matrices."
            </p>
          </li>

          <li className="p-3.5 rounded-xl bg-orange-50/50 border border-orange-100 space-y-1">
            <div className="font-bold text-slate-900 flex items-center gap-2">
              <span className="w-5 h-5 rounded-full bg-orange-500 text-white flex items-center justify-center text-[10px] font-mono">2</span>
              <span>Step 2: Shortest Paths via Dijkstra & Min-Heap (1.5 mins)</span>
            </div>
            <p className="text-slate-600 pl-7 leading-relaxed">
              "Open Algorithm Lab → Lab 2. Demonstrate how the manual Binary Min-Heap Priority Queue extracts the minimum tentative distance in <code>O(log V)</code> time, relaxing adjacent roads with arithmetic: <code>currDist + edge &lt; oldDist</code>."
            </p>
          </li>

          <li className="p-3.5 rounded-xl bg-orange-50/50 border border-orange-100 space-y-1">
            <div className="font-bold text-slate-900 flex items-center gap-2">
              <span className="w-5 h-5 rounded-full bg-orange-500 text-white flex items-center justify-center text-[10px] font-mono">3</span>
              <span>Step 3: Greedy vs. 0/1 Knapsack Dynamic Programming (1.5 mins)</span>
            </div>
            <p className="text-slate-600 pl-7 leading-relaxed">
              "Show Lab 3 vs Lab 4. Explain why greedy sorting by profit density (₹/kg) can miss optimal combinations. Click a cell in the 2D DP table to show Bellman's recurrence: <code>dp[i][c] = max(skip, take)</code>, and trace the golden backtracking path."
            </p>
          </li>

          <li className="p-3.5 rounded-xl bg-orange-50/50 border border-orange-100 space-y-1">
            <div className="font-bold text-slate-900 flex items-center gap-2">
              <span className="w-5 h-5 rounded-full bg-orange-500 text-white flex items-center justify-center text-[10px] font-mono">4</span>
              <span>Step 4: Route Construction, Load Invariants & Feasibility Repair (1.5 mins)</span>
            </div>
            <p className="text-slate-600 pl-7 leading-relaxed">
              "Demonstrate Lab 5 and Operations Overview. Show that Knapsack chooses items, but stop sequencing requires Pickup-Before-Drop and deadline verification. Show how violating packages are transparently repaired to ensure 100% on-time delivery."
            </p>
          </li>

          <li className="p-3.5 rounded-xl bg-orange-50/50 border border-orange-100 space-y-1">
            <div className="font-bold text-slate-900 flex items-center gap-2">
              <span className="w-5 h-5 rounded-full bg-orange-500 text-white flex items-center justify-center text-[10px] font-mono">5</span>
              <span>Step 5: Academic Honesty & Boundary Statement (30 seconds)</span>
            </div>
            <p className="text-slate-600 pl-7 leading-relaxed">
              "Conclude with the honest viva statement: SmartRoute is an educational polynomial heuristic pipeline. It does not claim global optimality for the NP-hard multi-vehicle routing problem with time windows (VRP-TW)."
            </p>
          </li>
        </ol>
      </div>

      {/* Viva Glossary Grid */}
      <div className="p-6 rounded-2xl bg-white border border-orange-200 shadow-sm space-y-3">
        <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-orange-500" />
          <span>Examiner Viva Glossary</span>
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {glossary.map((item, idx) => (
            <div key={idx} className="p-3 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <div className="font-bold text-orange-600 text-xs">{item.term}</div>
              <div className="text-slate-600 leading-relaxed text-[11px]">{item.def}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
