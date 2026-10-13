import React, { useState, useEffect, useMemo } from 'react';
import confetti from 'canvas-confetti';
import { Navbar, AppView } from './components/app-shell/Navbar';
import { OperationsOverview } from './components/operations/OperationsOverview';
import { AlgorithmLab } from './components/algorithm-lab/AlgorithmLab';
import { VivaGuide } from './components/viva-guide/VivaGuide';
import { createHyderabadNetwork } from './lib/algorithms/graph';
import { INITIAL_VEHICLES, INITIAL_DELIVERIES } from './lib/data/sampleDay';
import { buildCompletePlan, PlanningStrategy } from './lib/planning/buildPlan';
import { DeliveryRequest, Vehicle, FinalPlan } from './types';

export const App: React.FC = () => {
  const getInitialView = (): AppView => {
    if (typeof window !== 'undefined') {
      const hash = window.location.hash.toLowerCase();
      if (hash.includes('viva')) return 'viva_guide';
      if (hash.includes('algorithm')) return 'algorithm_lab';
    }
    return 'operations';
  };
  const [currentView, setCurrentView] = useState<AppView>(getInitialView);

  useEffect(() => {
    const handleHash = () => {
      const hash = window.location.hash.toLowerCase();
      if (hash.includes('viva')) setCurrentView('viva_guide');
      else if (hash.includes('algorithm')) setCurrentView('algorithm_lab');
      else if (hash.includes('operations')) setCurrentView('operations');
    };
    window.addEventListener('hashchange', handleHash);
    return () => window.removeEventListener('hashchange', handleHash);
  }, []);

  const handleSetView = (view: AppView) => {
    setCurrentView(view);
    if (typeof window !== 'undefined') {
      window.location.hash = view;
    }
  };
  const [operatingDate, setOperatingDate] = useState<string>("Wed, Oct 07, 2026");

  // Single shared source of truth
  const graph = useMemo(() => createHyderabadNetwork(), []);
  const [vehicles, setVehicles] = useState<Vehicle[]>(INITIAL_VEHICLES);
  const [deliveries, setDeliveries] = useState<DeliveryRequest[]>(INITIAL_DELIVERIES);
  const [selectedVehicleId, setSelectedVehicleId] = useState<string>("V-101");
  const [currentStrategy, setCurrentStrategy] = useState<PlanningStrategy>("dp_knapsack");

  const activeVehicle = useMemo(() => {
    return vehicles.find(v => v.id === selectedVehicleId) || vehicles[0];
  }, [vehicles, selectedVehicleId]);

  // Initial plan generated on load
  const [plan, setPlan] = useState<FinalPlan | null>(() => {
    return buildCompletePlan(graph, INITIAL_VEHICLES[0], INITIAL_DELIVERIES, "dp_knapsack");
  });

  // Dynamically compute live telematics for the fleet based on active plan
  const displayVehicles = useMemo(() => {
    return vehicles.map((v) => {
      if (v.id === selectedVehicleId && plan) {
        return {
          ...v,
          currentLoadKg: plan.totalWeightKg,
          status: "assigned" as const
        };
      }
      return v;
    });
  }, [vehicles, selectedVehicleId, plan]);

  // Handle switching active vehicle with automatic plan recalculation
  const handleSelectVehicle = (vehicleId: string) => {
    setSelectedVehicleId(vehicleId);
    const targetVehicle = vehicles.find(v => v.id === vehicleId) || vehicles[0];
    const newPlan = buildCompletePlan(graph, targetVehicle, deliveries, currentStrategy);
    setPlan(newPlan);
    setReplayProgress(0);
    setIsReplaying(false);

    // Update deliveries status matching new plan
    const acceptedIds = new Set(newPlan.acceptedRequests.map(d => d.id));
    const deferredMap = new Map(newPlan.deferredRequests.map(d => [d.request.id, d.reason]));

    setDeliveries((prev) =>
      prev.map((d) => {
        if (acceptedIds.has(d.id)) {
          return { ...d, status: "selected", assignedVehicleId: targetVehicle.id };
        } else if (deferredMap.has(d.id)) {
          return { ...d, status: "deferred", deferredReason: deferredMap.get(d.id) };
        } else {
          return { ...d, status: "pending", assignedVehicleId: undefined };
        }
      })
    );
  };

  // Replay animation state
  const [isReplaying, setIsReplaying] = useState(false);
  const [replayProgress, setReplayProgress] = useState(0);

  useEffect(() => {
    let animTimer: any;
    if (isReplaying) {
      animTimer = setInterval(() => {
        setReplayProgress((prev) => {
          if (prev >= 100) {
            setIsReplaying(false);
            return 100;
          }
          return prev + 1.5;
        });
      }, 80);
    }
    return () => clearInterval(animTimer);
  }, [isReplaying]);

  const handleToggleReplay = () => {
    if (replayProgress >= 100) {
      setReplayProgress(0);
    }
    setIsReplaying(!isReplaying);
  };

  const handleResetReplay = () => {
    setIsReplaying(false);
    setReplayProgress(0);
  };

  // Run or Rerun plan
  const handleRunPlan = (strategy: PlanningStrategy) => {
    const newPlan = buildCompletePlan(graph, activeVehicle, deliveries, strategy);
    setPlan(newPlan);
    setCurrentStrategy(strategy);
    setReplayProgress(0);
    setIsReplaying(false);

    // Update deliveries status matching plan
    const acceptedIds = new Set(newPlan.acceptedRequests.map(d => d.id));
    const deferredMap = new Map(newPlan.deferredRequests.map(d => [d.request.id, d.reason]));

    setDeliveries((prev) =>
      prev.map((d) => {
        if (acceptedIds.has(d.id)) {
          return { ...d, status: "selected", assignedVehicleId: activeVehicle.id };
        } else if (deferredMap.has(d.id)) {
          return { ...d, status: "deferred", deferredReason: deferredMap.get(d.id) };
        } else {
          return { ...d, status: "pending", assignedVehicleId: undefined };
        }
      })
    );

    // Delightful micro-feedback
    confetti({
      particleCount: 45,
      spread: 60,
      origin: { y: 0.8 },
      colors: ['#ff6b4a', '#38bdf8', '#10b981']
    });
  };

  // Reset plan to unassigned state without losing user-added requests
  const handleResetPlan = () => {
    setPlan(null);
    setReplayProgress(0);
    setIsReplaying(false);
    setDeliveries((prev) =>
      prev.map((d) => ({
        ...d,
        status: "pending",
        assignedVehicleId: undefined,
        deferredReason: undefined
      }))
    );
  };

  // Add custom delivery
  const handleAddDelivery = (newReq: DeliveryRequest) => {
    setDeliveries((prev) => [newReq, ...prev]);
  };

  // Update vehicle capacity (used in Lab 0 interactive edit)
  const handleUpdateVehicleCapacity = (newCap: number) => {
    setVehicles((prev) =>
      prev.map((v) => (v.id === activeVehicle.id ? { ...v, capacityKg: newCap } : v))
    );
    // Recalculate plan with updated vehicle capacity
    const updatedVehicle = { ...activeVehicle, capacityKg: newCap };
    const newPlan = buildCompletePlan(graph, updatedVehicle, deliveries, currentStrategy);
    setPlan(newPlan);
  };

  // Update delivery profit
  const handleUpdateDeliveryProfit = (id: string, newProfit: number) => {
    setDeliveries((prev) =>
      prev.map((d) => (d.id === id ? { ...d, profit: newProfit } : d))
    );
  };

  // Date controls
  const handlePrevDay = () => {
    setOperatingDate("Tue, Oct 06, 2026");
  };
  const handleNextDay = () => {
    setOperatingDate("Thu, Oct 08, 2026");
  };
  const handleResetDemoDay = () => {
    setOperatingDate("Wed, Oct 07, 2026");
    setVehicles(INITIAL_VEHICLES);
    setDeliveries(INITIAL_DELIVERIES);
    setSelectedVehicleId("V-101");
    setPlan(buildCompletePlan(graph, INITIAL_VEHICLES[0], INITIAL_DELIVERIES, "dp_knapsack"));
    setReplayProgress(0);
    setIsReplaying(false);
  };

  return (
    <div className="app-shell flex flex-col h-screen w-screen overflow-hidden bg-slate-50 font-sans">
      <Navbar
        currentView={currentView}
        onChangeView={handleSetView}
        operatingDate={operatingDate}
        onPrevDay={handlePrevDay}
        onNextDay={handleNextDay}
        onResetDemoDay={handleResetDemoDay}
      />

      <main className="flex-1 overflow-hidden relative">
        {currentView === "operations" && (
          <OperationsOverview
            graph={graph}
            deliveries={deliveries}
            vehicles={displayVehicles}
            selectedVehicleId={selectedVehicleId}
            onSelectVehicleId={handleSelectVehicle}
            plan={plan}
            onRunPlan={handleRunPlan}
            onResetPlan={handleResetPlan}
            onOpenAlgorithmLab={() => handleSetView("algorithm_lab")}
            onAddDelivery={handleAddDelivery}
            currentStrategy={currentStrategy}
            onChangeStrategy={setCurrentStrategy}
            replayProgress={replayProgress}
            isReplaying={isReplaying}
            onToggleReplay={handleToggleReplay}
            onResetReplay={handleResetReplay}
          />
        )}

        {currentView === "algorithm_lab" && (
          <AlgorithmLab
            plan={plan}
            graph={graph}
            vehicle={activeVehicle}
            deliveries={deliveries}
            onBackToOperations={() => setCurrentView("operations")}
            onUpdateVehicleCapacity={handleUpdateVehicleCapacity}
            onUpdateDeliveryProfit={handleUpdateDeliveryProfit}
          />
        )}

        {currentView === "viva_guide" && (
          <div className="h-full overflow-y-auto">
            <VivaGuide />
          </div>
        )}
      </main>
    </div>
  );
};
