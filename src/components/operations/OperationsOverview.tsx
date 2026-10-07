import React, { useState } from 'react';
import { DeliveryRequest, Vehicle, FinalPlan } from '../../types';
import { LogisticsGraph } from '../../lib/algorithms/graph';
import { MapView } from './MapView';
import { DeliveryTable } from './DeliveryTable';
import { DeliveryModal } from './DeliveryModal';
import { FleetPanel } from './FleetPanel';
import { RoutePlanPanel } from './RoutePlanPanel';
import { PlanningStrategy } from '../../lib/planning/buildPlan';
import {
  Package,
  TrendingUp,
  Truck,
  CheckCircle2,
  AlertCircle,
  Route,
  Award,
  Users
} from 'lucide-react';

interface OperationsOverviewProps {
  graph: LogisticsGraph;
  deliveries: DeliveryRequest[];
  vehicles: Vehicle[];
  selectedVehicleId: string;
  onSelectVehicleId: (id: string) => void;
  plan: FinalPlan | null;
  onRunPlan: (strategy: PlanningStrategy) => void;
  onResetPlan: () => void;
  onOpenAlgorithmLab: () => void;
  onAddDelivery: (newDelivery: DeliveryRequest) => void;
  currentStrategy: PlanningStrategy;
  onChangeStrategy: (s: PlanningStrategy) => void;
  replayProgress: number;
  isReplaying: boolean;
  onToggleReplay: () => void;
  onResetReplay: () => void;
}

export const OperationsOverview: React.FC<OperationsOverviewProps> = ({
  graph,
  deliveries,
  vehicles,
  selectedVehicleId,
  onSelectVehicleId,
  plan,
  onRunPlan,
  onResetPlan,
  onOpenAlgorithmLab,
  onAddDelivery,
  currentStrategy,
  onChangeStrategy,
  replayProgress,
  isReplaying,
  onToggleReplay,
  onResetReplay
}) => {
  const [selectedDeliveryId, setSelectedDeliveryId] = useState<string | null>(null);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [activeBottomTab, setActiveBottomTab] = useState<"deliveries" | "fleet">("deliveries");

  // Computed metrics
  const totalOrders = deliveries.length;
  const selectedCount = plan ? plan.acceptedRequests.length : 0;
  const deferredCount = plan ? plan.deferredRequests.length : 0;
  const availableFleetCount = vehicles.filter(v => v.status === "available").length;
  const expectedProfit = plan ? plan.totalProfit : 0;
  const totalDistance = plan ? plan.totalDistanceKm : 0;

  return (
    <div className="operations-overview flex flex-col h-full bg-slate-50 text-slate-800 overflow-y-auto">
      {/* Project Honor & Team Attribution Strip */}
      <div className="bg-gradient-to-r from-orange-500 via-orange-600 to-amber-600 px-4 py-2 text-white flex flex-wrap items-center justify-between text-xs shadow-xs">
        <div className="flex items-center gap-2">
          <Award className="w-4 h-4 text-orange-100" />
          <span className="font-bold tracking-wide">
            Course Instructor: <span className="underline decoration-orange-200">Dr. Syed Javed Pasha</span>
          </span>
        </div>
        <div className="flex items-center gap-2">
          <Users className="w-4 h-4 text-orange-100" />
          <span className="font-medium text-orange-100">
            Project By: <strong className="text-white">Himanshu Pandit</strong>, <strong className="text-white">Devyani Pawar</strong>, <strong className="text-white">Heman</strong>, <strong className="text-white">Rimika Jain</strong>
          </span>
        </div>
      </div>

      {/* Top KPI Summary Strip in Orange & White */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 p-4 bg-white border-b border-orange-100 text-xs shadow-xs">
        <div className="p-3.5 rounded-xl bg-orange-50/60 border border-orange-200 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div className="text-slate-600 font-semibold flex items-center justify-between">
            <span>Total Requests</span>
            <Package className="w-4 h-4 text-orange-500" />
          </div>
          <div className="text-xl font-bold text-slate-900 mt-1">
            {totalOrders}
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-emerald-50/70 border border-emerald-200 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div className="text-emerald-800 font-semibold flex items-center justify-between">
            <span>Planned Deliveries</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-xl font-bold text-emerald-700 mt-1">
            {selectedCount}
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-rose-50/70 border border-rose-200 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div className="text-rose-800 font-semibold flex items-center justify-between">
            <span>Deferred Backlog</span>
            <AlertCircle className="w-4 h-4 text-rose-500" />
          </div>
          <div className="text-xl font-bold text-rose-700 mt-1">
            {deferredCount}
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-sky-50/70 border border-sky-200 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div className="text-sky-800 font-semibold flex items-center justify-between">
            <span>Available Fleet</span>
            <Truck className="w-4 h-4 text-sky-600" />
          </div>
          <div className="text-xl font-bold text-sky-700 mt-1">
            {availableFleetCount} Units
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-orange-50/80 border border-orange-200 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div className="text-orange-900 font-semibold flex items-center justify-between">
            <span>Planned Profit</span>
            <TrendingUp className="w-4 h-4 text-orange-600" />
          </div>
          <div className="text-xl font-bold text-orange-600 mt-1 font-mono">
            ₹{expectedProfit}
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div className="text-slate-600 font-semibold flex items-center justify-between">
            <span>Route Distance</span>
            <Route className="w-4 h-4 text-orange-500" />
          </div>
          <div className="text-xl font-bold text-slate-900 mt-1 font-mono">
            {totalDistance} km
          </div>
        </div>
      </div>

      {/* Main Operations Grid */}
      <div className="flex-1 p-4 grid grid-cols-1 lg:grid-cols-12 gap-4 min-h-[700px]">
        {/* Left Column: Map & Tables (7 cols) */}
        <div className="lg:col-span-7 flex flex-col gap-4">
          {/* Google Maps Container */}
          <div className="h-[430px] rounded-2xl overflow-hidden shadow-sm border border-orange-200 bg-white relative isolate z-0">
            <MapView
              graph={graph}
              stops={plan ? plan.stops : []}
              selectedDeliveryId={selectedDeliveryId}
              onSelectDeliveryId={setSelectedDeliveryId}
              replayProgress={replayProgress}
              isReplaying={isReplaying}
              onToggleReplay={onToggleReplay}
              onResetReplay={onResetReplay}
              deliveries={deliveries}
            />
          </div>

          {/* Bottom Tabs: Delivery Table OR Fleet */}
          <div className="flex-1 flex flex-col bg-white border border-orange-200 rounded-2xl overflow-hidden shadow-xs min-h-[350px]">
            <div className="flex items-center gap-2 px-4 pt-3 border-b border-orange-100 bg-orange-50/30">
              <button
                onClick={() => setActiveBottomTab("deliveries")}
                className={`pb-2.5 px-3 text-xs font-bold border-b-2 transition-all ${
                  activeBottomTab === "deliveries"
                    ? "border-orange-500 text-orange-600"
                    : "border-transparent text-slate-500 hover:text-slate-900"
                }`}
              >
                Delivery Orders ({deliveries.length})
              </button>
              <button
                onClick={() => setActiveBottomTab("fleet")}
                className={`pb-2.5 px-3 text-xs font-bold border-b-2 transition-all ${
                  activeBottomTab === "fleet"
                    ? "border-orange-500 text-orange-600"
                    : "border-transparent text-slate-500 hover:text-slate-900"
                }`}
              >
                Fleet Telematics ({vehicles.length})
              </button>
            </div>

            <div className="flex-1 overflow-hidden p-2">
              {activeBottomTab === "deliveries" ? (
                <DeliveryTable
                  deliveries={deliveries}
                  selectedDeliveryId={selectedDeliveryId}
                  onSelectDeliveryId={setSelectedDeliveryId}
                  onOpenAddModal={() => setIsAddModalOpen(true)}
                />
              ) : (
                <FleetPanel
                  vehicles={vehicles}
                  selectedVehicleId={selectedVehicleId}
                  onSelectVehicleId={onSelectVehicleId}
                  plan={plan}
                />
              )}
            </div>
          </div>
        </div>

        {/* Right Column: Route Plan & Schedule (5 cols) */}
        <div className="lg:col-span-5 flex flex-col">
          <RoutePlanPanel
            plan={plan}
            onRunPlan={onRunPlan}
            onResetPlan={onResetPlan}
            onOpenAlgorithmLab={onOpenAlgorithmLab}
            currentStrategy={currentStrategy}
            onChangeStrategy={onChangeStrategy}
          />
        </div>
      </div>

      {/* Add Delivery Modal */}
      <DeliveryModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        onAddDelivery={onAddDelivery}
        locations={graph.getAllLocations()}
      />
    </div>
  );
};
