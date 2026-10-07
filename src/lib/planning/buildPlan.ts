import { LogisticsGraph } from '../algorithms/graph';
import { runGreedySelection, GreedyCriterion } from '../algorithms/greedySelection';
import { runKnapsackDp } from '../algorithms/knapsack';
import { buildFeasibleRouteSchedule } from '../algorithms/scheduleRoute';
import { DeliveryRequest, Vehicle, FinalPlan } from '../../types';

export type PlanningStrategy = "dp_knapsack" | "greedy_density" | "greedy_profit" | "greedy_deadline";

export function buildCompletePlan(
  graph: LogisticsGraph,
  vehicle: Vehicle,
  candidates: DeliveryRequest[],
  strategy: PlanningStrategy = "dp_knapsack",
  depotId: string = "Main Parcel Warehouse"
): FinalPlan {
  // Step 1: Pre-filtering impossible candidates
  // E.g. individual items whose direct travel time alone exceeds deadline
  const feasibleCandidates: DeliveryRequest[] = [];
  const deferredOnInit: Array<{ request: DeliveryRequest; reason: string }> = [];

  for (const req of candidates) {
    if (req.weightKg > vehicle.capacityKg) {
      deferredOnInit.push({
        request: req,
        reason: `Package weight (${req.weightKg} kg) strictly exceeds total vehicle capacity (${vehicle.capacityKg} kg)`
      });
      continue;
    }
    feasibleCandidates.push(req);
  }

  // Step 2: Compute Greedy baseline for comparison
  const greedyBaseline = runGreedySelection(feasibleCandidates, vehicle.capacityKg, "profit_density");

  // Step 3: Compute Knapsack DP for optimal item subset selection
  const dpResult = runKnapsackDp(feasibleCandidates, vehicle.capacityKg, 1);

  // Step 4: Pick which set of items to schedule based on active planning strategy
  let itemsToSchedule: DeliveryRequest[];
  if (strategy === "dp_knapsack") {
    itemsToSchedule = dpResult.selectedDeliveries;
  } else if (strategy === "greedy_profit") {
    const greedyProfit = runGreedySelection(feasibleCandidates, vehicle.capacityKg, "highest_profit");
    itemsToSchedule = greedyProfit.selectedDeliveries;
  } else if (strategy === "greedy_deadline") {
    const greedyDeadline = runGreedySelection(feasibleCandidates, vehicle.capacityKg, "earliest_deadline");
    itemsToSchedule = greedyDeadline.selectedDeliveries;
  } else {
    itemsToSchedule = greedyBaseline.selectedDeliveries;
  }

  // Step 5: Construct route schedule with pickup-before-drop, load tracking and feasibility repair
  const scheduleOutcome = buildFeasibleRouteSchedule(
    graph,
    vehicle,
    itemsToSchedule,
    depotId,
    2.5,
    32
  );

  // Combine deferred lists
  const allDeferred = [...deferredOnInit, ...scheduleOutcome.deferredDeliveries];
  // Add items that were not selected by DP/Greedy
  const acceptedIds = new Set(scheduleOutcome.acceptedDeliveries.map(d => d.id));
  for (const c of feasibleCandidates) {
    if (!acceptedIds.has(c.id) && !allDeferred.some(d => d.request.id === c.id)) {
      allDeferred.push({
        request: c,
        reason: "Deferred: Not included in chosen subset or removed during feasibility verification."
      });
    }
  }

  const totalProfit = scheduleOutcome.acceptedDeliveries.reduce((sum, d) => sum + d.profit, 0);
  const totalWeightKg = scheduleOutcome.acceptedDeliveries.reduce((sum, d) => sum + d.weightKg, 0);
  const capacityUtilizationPct = vehicle.capacityKg > 0
    ? Math.round((totalWeightKg / vehicle.capacityKg) * 1000) / 10
    : 0;

  const notes: string[] = [
    `Generated on ${new Date().toLocaleTimeString()} using ${strategy.toUpperCase()} heuristic pipeline.`,
    `Depot: ${depotId}. Active vehicle: ${vehicle.id} (${vehicle.driverName}, ${vehicle.capacityKg} kg capacity).`,
    `Total stops: ${scheduleOutcome.stops.length}. Cumulative road distance: ${scheduleOutcome.totalDistanceKm} km.`,
    `Deadlines verification status: ${scheduleOutcome.allDeadlinesMet ? "100% FEASIBLE (All arrivals on-time)" : "CONSTRAINTS ADJUSTED"}.`
  ];

  return {
    id: `PLAN-${Date.now().toString(36).toUpperCase()}`,
    createdAt: new Date().toISOString(),
    vehicle: {
      ...vehicle,
      currentLoadKg: totalWeightKg,
      status: "assigned"
    },
    acceptedRequests: scheduleOutcome.acceptedDeliveries,
    deferredRequests: allDeferred,
    stops: scheduleOutcome.stops,
    totalDistanceKm: scheduleOutcome.totalDistanceKm,
    totalTravelMinutes: scheduleOutcome.totalTravelMinutes,
    totalProfit,
    totalWeightKg,
    capacityUtilizationPct,
    allDeadlinesMet: scheduleOutcome.allDeadlinesMet,
    repairs: scheduleOutcome.repairs,
    dijkstraLegs: scheduleOutcome.dijkstraLegs,
    greedyComparison: greedyBaseline,
    dpResult,
    notes
  };
}
