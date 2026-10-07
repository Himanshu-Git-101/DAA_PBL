import React, { useState } from 'react';
import {
  Compass,
  Cpu,
  GraduationCap,
  Calendar,
  ChevronLeft,
  ChevronRight,
  Users,
  Award,
  BookOpen
} from 'lucide-react';

export type AppView = "operations" | "algorithm_lab" | "viva_guide";

interface NavbarProps {
  currentView: AppView;
  onChangeView: (v: AppView) => void;
  operatingDate: string;
  onPrevDay: () => void;
  onNextDay: () => void;
  onResetDemoDay: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentView,
  onChangeView,
  operatingDate,
  onPrevDay,
  onNextDay,
  onResetDemoDay
}) => {
  const [teamModalOpen, setTeamModalOpen] = useState(false);

  return (
    <header className="navbar-header h-16 bg-white border-b-2 border-orange-500/20 px-4 md:px-6 flex items-center justify-between text-xs select-none shadow-sm z-30">
      {/* Brand & Project Info */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-orange-600 via-orange-500 to-amber-500 flex items-center justify-center shadow-md shadow-orange-500/30 text-white font-bold text-base">
            SR
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-slate-900 text-base tracking-tight">SmartRoute</span>
              <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full bg-orange-100 text-orange-700 border border-orange-200">
                DSA Project
              </span>
            </div>
            <div className="text-[11px] text-slate-500 font-medium hidden sm:block">
              Guided by <strong className="text-orange-700 font-bold">Dr. Syed Javed Pasha</strong>
            </div>
          </div>
        </div>
      </div>

      {/* Center: Team Members & Academic Recognition Pill */}
      <div className="hidden xl:flex items-center gap-2">
        <button
          onClick={() => setTeamModalOpen(true)}
          className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-orange-50 hover:bg-orange-100 border border-orange-200 text-slate-700 transition-all shadow-xs"
        >
          <Award className="w-3.5 h-3.5 text-orange-600 shrink-0" />
          <span className="text-[11px]">
            <strong>Instructor:</strong> Dr. Syed Javed Pasha
          </span>
          <span className="text-slate-300">|</span>
          <Users className="w-3.5 h-3.5 text-orange-600 shrink-0" />
          <span className="text-[11px] text-slate-600 font-medium">
            Team: <strong>Himanshu</strong>, <strong>Devyani</strong>, <strong>Heman</strong>, <strong>Rimika</strong>
          </span>
        </button>
      </div>

      {/* Right Controls: Date Selector + Navigation View Tabs */}
      <div className="flex items-center gap-2.5">
        {/* Date Selector */}
        <div className="hidden md:flex items-center gap-1 bg-slate-50 border border-slate-200 rounded-lg px-2 py-1 text-slate-600">
          <Calendar className="w-3.5 h-3.5 text-orange-500" />
          <button onClick={onPrevDay} className="p-0.5 hover:text-orange-600 rounded">
            <ChevronLeft className="w-3.5 h-3.5" />
          </button>
          <span className="font-semibold text-slate-800 text-[11px] px-1">
            {operatingDate}
          </span>
          <button onClick={onNextDay} className="p-0.5 hover:text-orange-600 rounded">
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={onResetDemoDay}
            className="ml-1 text-[10px] font-bold px-1.5 py-0.5 rounded bg-orange-500 text-white hover:bg-orange-600 transition-colors"
          >
            Reset
          </button>
        </div>

        {/* Primary View Switcher */}
        <nav className="flex items-center gap-1 bg-slate-100 border border-slate-200 rounded-xl p-1">
          <button
            onClick={() => onChangeView("operations")}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              currentView === "operations"
                ? "bg-orange-500 text-white shadow-sm"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <Compass className="w-3.5 h-3.5" />
            <span>Operations</span>
          </button>

          <button
            onClick={() => onChangeView("algorithm_lab")}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              currentView === "algorithm_lab"
                ? "bg-orange-500 text-white shadow-sm"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <Cpu className="w-3.5 h-3.5" />
            <span>Algorithm Lab</span>
          </button>

          <button
            onClick={() => onChangeView("viva_guide")}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              currentView === "viva_guide"
                ? "bg-slate-900 text-white shadow-sm"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <GraduationCap className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Viva Guide</span>
          </button>
        </nav>
      </div>

      {/* Academic Team Information Modal */}
      {teamModalOpen && (
        <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
          <div className="bg-white border-2 border-orange-300 rounded-2xl shadow-2xl max-w-lg w-full p-6 text-slate-800">
            <div className="flex items-center justify-between pb-3 border-b border-orange-100 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-orange-500 flex items-center justify-center text-white">
                  <GraduationCap className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-base text-slate-900">Academic Project Credits</h3>
                  <div className="text-[11px] text-slate-500">Data Structures and Algorithms PBL</div>
                </div>
              </div>
              <button
                onClick={() => setTeamModalOpen(false)}
                className="text-slate-400 hover:text-slate-700 font-bold text-lg"
              >
                ✕
              </button>
            </div>

            {/* Course Instructor Card */}
            <div className="p-4 rounded-xl bg-orange-50/70 border border-orange-200 mb-4">
              <div className="text-[10px] font-bold uppercase tracking-wider text-orange-600 mb-1">
                Course Instructor & Guide
              </div>
              <div className="text-base font-bold text-slate-900">Dr. Syed Javed Pasha</div>
              <div className="text-xs text-slate-600 mt-0.5">
                Department of Computer Science & Engineering
              </div>
            </div>

            {/* Team Members */}
            <div>
              <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-2">
                Project Development Team
              </div>
              <div className="grid grid-cols-2 gap-2.5">
                {[
                  { name: "Himanshu Pandit", role: "Full-Stack & Planning Pipeline" },
                  { name: "Devyani Pawar", role: "Graph & Dijkstra Implementation" },
                  { name: "Heman", role: "Knapsack DP & Analysis" },
                  { name: "Rimika Jain", role: "Greedy Heuristics & Map Testing" }
                ].map((member, i) => (
                  <div
                    key={i}
                    className="p-3 rounded-xl bg-slate-50 border border-slate-200 hover:border-orange-300 transition-colors"
                  >
                    <div className="font-bold text-slate-900 text-xs">{member.name}</div>
                    <div className="text-[11px] text-orange-700 mt-0.5 font-medium">{member.role}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-5 pt-3 border-t border-slate-100 flex justify-end">
              <button
                onClick={() => setTeamModalOpen(false)}
                className="px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white rounded-xl text-xs font-bold shadow-md shadow-orange-500/20"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};
