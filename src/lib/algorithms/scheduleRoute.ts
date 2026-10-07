import { LogisticsGraph } from './graph';
import { runDijkstra } from './dijkstra';
import {
  DeliveryRequest,
  Vehicle,
  PlanStop,
  FeasibilityRepair,
  DijkstraResult
} from '../../types';

export interface RouteScheduleOutcome {
  stops: PlanStop[];
  acceptedDeliveries: DeliveryRequest[];
  deferredDeliveries: Array<{ request: DeliveryRequest; reason: string }>;
  repairs: FeasibilityRepair[];
  totalDistanceKm: number;
  totalTravelMinutes: number;
  dijkstraLegs: Record<string, DijkstraResult>;
  allDeadlinesMet: boolean;
}

/**
 * Builds a feasible pickup-before-drop stop sequence from candidate requests.
 * Uses greedy nearest-feasible-stop heuristic with Dijkstra legs,
 * load tracking, and iterative feasibility repair if any deadline is missed.
 */
export function buildFeasibleRouteSchedule(
  graph: LogisticsGraph,
  vehicle: Vehicle,
  candidates: DeliveryRequest[],
  depotId: string = "Main Parcel Warehouse",
  serviceTimeMinutes: number = 3.0,
  speedKmH: number = 28
): RouteScheduleOutcome {
  let activeCandidates = [...candidates];
  const deferredDeliveries: Array<{ request: DeliveryRequest; reason: string }> = [];
  const repairs: FeasibilityRepair[] = [];
  const dijkstraLegs: Record<string, DijkstraResult> = {};

  // Maximum repair iterations to prevent infinite loops
  const maxIterations = candidates.length + 2;
  let iteration = 0;

  while (iteration < maxIterations) {
    iteration++;

    const outcome = tryConstructSequence(
      graph,
      vehicle,
      activeCandidates,
      depotId,
      serviceTimeMinutes,
      speedKmH,
      dijkstraLegs
    );

    if (outcome.success) {
      return {
        stops: outcome.stops,
        acceptedDeliveries: activeCandidates,
        deferredDeliveries,
        repairs,
        totalDistanceKm: outcome.totalDistanceKm,
        totalTravelMinutes: outcome.totalTravelMinutes,
        dijkstraLegs,
        allDeadlinesMet: true
      };
    } else {
      // Find the violating delivery
      const violator = outcome.violatingDelivery;
      if (!violator) {
        // Fallback break
        break;
      }

      // Repair rule: remove the lowest profit-density request among the offending candidate
      // or the violator itself
      const removeIndex = activeCandidates.findIndex(d => d.id === violator.id);
      if (removeIndex >= 0) {
        const removed = activeCandidates.splice(removeIndex, 1)[0];
        const repairRecord: FeasibilityRepair = {
          removedRequestId: removed.id,
          reason: `Violated delivery deadline: Estimated arrival ${outcome.violatingArrival.toFixed(1)} mins exceeded deadline ${removed.deadlineMinutesFromStart} mins`,
          recalculatedArrivalMinute: outcome.violatingArrival,
          violatedDeadlineMinute: removed.deadlineMinutesFromStart
        };
        repairs.push(repairRecord);
        deferredDeliveries.push({
          request: removed,
          reason: repairRecord.reason
        });
      } else {
        break;
      }
    }
  }

  // Final fallback run with remaining active candidates
  const finalOutcome = tryConstructSequence(
    graph,
    vehicle,
    activeCandidates,
    depotId,
    serviceTimeMinutes,
    speedKmH,
    dijkstraLegs
  );

  return {
    stops: finalOutcome.stops,
    acceptedDeliveries: activeCandidates,
    deferredDeliveries,
    repairs,
    totalDistanceKm: finalOutcome.totalDistanceKm,
    totalTravelMinutes: finalOutcome.totalTravelMinutes,
    dijkstraLegs,
    allDeadlinesMet: finalOutcome.success
  };
}

interface AttemptResult {
  success: boolean;
  stops: PlanStop[];
  totalDistanceKm: number;
  totalTravelMinutes: number;
  violatingDelivery?: DeliveryRequest;
  violatingArrival: number;
}

function tryConstructSequence(
  graph: LogisticsGraph,
  vehicle: Vehicle,
  candidates: DeliveryRequest[],
  depotId: string,
  serviceTimeMinutes: number,
  speedKmH: number,
  dijkstraLegsCache: Record<string, DijkstraResult>
): AttemptResult {
  if (candidates.length === 0) {
    // Empty plan: just depot start and return
    const stops: PlanStop[] = [
      {
        stopNumber: 1,
        locationId: depotId,
        locationName: graph.getLocation(depotId)?.name || depotId,
        action: "DEPOT_START",
        arrivalMinute: 0,
        departureMinute: 0,
        isLate: false,
        legDistanceKm: 0,
        legTravelMinutes: 0,
        legPathNodes: [depotId],
        loadAfterStopKg: 0,
        capacityKg: vehicle.capacityKg,
        status: "current"
      }
    ];
    return { success: true, stops, totalDistanceKm: 0, totalTravelMinutes: 0, violatingArrival: 0 };
  }

  // To build an optimal sequence respecting pickup-before-drop:
  // Track packages: unpicked, picked, delivered.
  const pickedUp = new Set<string>();
  const delivered = new Set<string>();

  const stops: PlanStop[] = [];
  let currentLocation = depotId;
  let currentMinute = 0;
  let currentLoad = 0;
  let totalDist = 0;

  // Add initial depot stop
  stops.push({
    stopNumber: 1,
    locationId: depotId,
    locationName: graph.getLocation(depotId)?.name || depotId,
    action: "DEPOT_START",
    arrivalMinute: 0,
    departureMinute: 0,
    isLate: false,
    legDistanceKm: 0,
    legTravelMinutes: 0,
    legPathNodes: [depotId],
    loadAfterStopKg: 0,
    capacityKg: vehicle.capacityKg,
    status: "current"
  });

  const totalActionsNeeded = candidates.length * 2; // 1 pickup + 1 drop for each
  let actionsCompleted = 0;

  while (actionsCompleted < totalActionsNeeded) {
    // Generate valid next candidate actions:
    // Option A: Pick up any unpicked package whose weight fits currentLoad <= capacity
    // Option B: Drop any picked package that hasn't been delivered
    interface ActionCandidate {
      type: "PICKUP" | "DROP";
      req: DeliveryRequest;
      targetLocationId: string;
      weightDelta: number;
    }

    const availableActions: ActionCandidate[] = [];

    for (const req of candidates) {
      if (!pickedUp.has(req.id)) {
        if (currentLoad + req.weightKg <= vehicle.capacityKg) {
          availableActions.push({
            type: "PICKUP",
            req,
            targetLocationId: req.pickupLocationId,
            weightDelta: req.weightKg
          });
        }
      } else if (!delivered.has(req.id)) {
        availableActions.push({
          type: "DROP",
          req,
          targetLocationId: req.dropLocationId,
          weightDelta: -req.weightKg
        });
      }
    }

    if (availableActions.length === 0) {
      // Deadlock in capacity/ordering
      return {
        success: false,
        stops,
        totalDistanceKm: totalDist,
        totalTravelMinutes: currentMinute,
        violatingArrival: currentMinute
      };
    }

    // Heuristic selection: choose nearest next location using Dijkstra
    let bestAction: ActionCandidate | null = null;
    let bestLegDist = Infinity;
    let bestDijkstraResult: DijkstraResult | null = null;

    for (const act of availableActions) {
      const legKey = `${currentLocation}->${act.targetLocationId}`;
      let dResult = dijkstraLegsCache[legKey];
      if (!dResult) {
        dResult = runDijkstra(graph, currentLocation, act.targetLocationId, speedKmH);
        dijkstraLegsCache[legKey] = dResult;
      }

      // Prioritize urgent drop-offs and freeing vehicle capacity
      let cost = dResult.distanceKm;
      if (act.type === "DROP") {
        cost *= 0.65; // strongly prioritize delivering onboard packages
        const timeRemaining = act.req.deadlineMinutesFromStart - currentMinute;
        if (timeRemaining < 120) {
          cost *= 0.6; // expedite packages with impending deadlines
        }
      }

      if (cost < bestLegDist) {
        bestLegDist = cost;
        bestAction = act;
        bestDijkstraResult = dResult;
      }
    }

    if (!bestAction || !bestDijkstraResult) {
      break;
    }

    // Apply chosen action
    const leg = bestDijkstraResult;
    const arrival = currentMinute + leg.travelMinutes;
    const departure = arrival + serviceTimeMinutes;

    let isLate = false;
    let slack: number | undefined = undefined;

    if (bestAction.type === "DROP") {
      slack = Math.round((bestAction.req.deadlineMinutesFromStart - arrival) * 10) / 10;
      if (arrival > bestAction.req.deadlineMinutesFromStart) {
        isLate = true;
        // Feasibility failure!
        return {
          success: false,
          stops,
          totalDistanceKm: totalDist + leg.distanceKm,
          totalTravelMinutes: arrival,
          violatingDelivery: bestAction.req,
          violatingArrival: arrival
        };
      }
    }

    currentLoad += bestAction.weightDelta;
    currentMinute = departure;
    totalDist += leg.distanceKm;
    currentLocation = bestAction.targetLocationId;

    if (bestAction.type === "PICKUP") {
      pickedUp.add(bestAction.req.id);
    } else {
      delivered.add(bestAction.req.id);
    }
    actionsCompleted++;

    stops.push({
      stopNumber: stops.length + 1,
      locationId: bestAction.targetLocationId,
      locationName: graph.getLocation(bestAction.targetLocationId)?.name || bestAction.targetLocationId,
      action: bestAction.type,
      requestId: bestAction.req.id,
      arrivalMinute: Math.round(arrival * 10) / 10,
      departureMinute: Math.round(departure * 10) / 10,
      deadlineMinute: bestAction.type === "DROP" ? bestAction.req.deadlineMinutesFromStart : undefined,
      isLate,
      slackMinutes: slack,
      legDistanceKm: leg.distanceKm,
      legTravelMinutes: leg.travelMinutes,
      legPathNodes: leg.path,
      loadAfterStopKg: Math.round(currentLoad * 10) / 10,
      capacityKg: vehicle.capacityKg,
      status: "future"
    });
  }

  // Return to depot at end of route
  if (currentLocation !== depotId) {
    const returnLegKey = `${currentLocation}->${depotId}`;
    let returnLeg = dijkstraLegsCache[returnLegKey];
    if (!returnLeg) {
      returnLeg = runDijkstra(graph, currentLocation, depotId, speedKmH);
      dijkstraLegsCache[returnLegKey] = returnLeg;
    }
    const returnArrival = currentMinute + returnLeg.travelMinutes;
    totalDist += returnLeg.distanceKm;

    stops.push({
      stopNumber: stops.length + 1,
      locationId: depotId,
      locationName: graph.getLocation(depotId)?.name || depotId,
      action: "DEPOT_RETURN",
      arrivalMinute: Math.round(returnArrival * 10) / 10,
      departureMinute: Math.round(returnArrival * 10) / 10,
      isLate: false,
      legDistanceKm: returnLeg.distanceKm,
      legTravelMinutes: returnLeg.travelMinutes,
      legPathNodes: returnLeg.path,
      loadAfterStopKg: 0,
      capacityKg: vehicle.capacityKg,
      status: "future"
    });
    currentMinute = returnArrival;
  }

  return {
    success: true,
    stops,
    totalDistanceKm: Math.round(totalDist * 10) / 10,
    totalTravelMinutes: Math.round(currentMinute * 10) / 10,
    violatingArrival: 0
  };
}
