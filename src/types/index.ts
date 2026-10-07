export type LocationKind = "depot" | "pickup" | "drop" | "hub";

export interface Location {
  id: string;
  name: string;
  area: string;
  lat: number;
  lng: number;
  kind: LocationKind;
  x?: number;
  y?: number;
  z?: number;
}

export interface RoadEdge {
  from: string;
  to: string;
  distanceKm: number;
  travelMinutes: number;
  bidirectional: boolean;
}

export type DeliveryPriority = "HIGH" | "MEDIUM" | "LOW";
export type DeliveryRiskLevel = "SAFE" | "MEDIUM RISK" | "HIGH RISK";
export type DeliveryStatus = "pending" | "selected" | "deferred" | "in_transit" | "delivered";

export interface DeliveryRequest {
  id: string;
  pickupLocationId: string;
  dropLocationId: string;
  weightKg: number;
  profit: number;
  deadlineMinutesFromStart: number;
  priority: DeliveryPriority;
  status: DeliveryStatus;
  packageType: string;
  assignedVehicleId?: string;
  deferredReason?: string;
  riskLevel?: DeliveryRiskLevel;
  distanceKm?: number;
  travelMinutes?: number;
}

export type VehicleStatus = "available" | "assigned" | "maintenance";

export interface Vehicle {
  id: string;
  driverName: string;
  plate: string;
  capacityKg: number;
  currentLoadKg: number;
  status: VehicleStatus;
  startLocationId: string;
  assignedRouteId?: string;
  completedStopsCount?: number;
}

export interface DijkstraStep {
  type: "INITIALIZATION" | "POP_MIN_HEAP" | "SKIP_VISITED" | "EDGE_RELAXATION" | "DESTINATION_REACHED";
  currNode: string;
  currDist: number;
  targetNode?: string;
  edgeWeight?: number;
  newDist?: number;
  visited: string[];
  distances: Record<string, number>;
  heap: Array<{ priority: number; item: string }>;
  explanation: string;
}

export interface DijkstraResult {
  start: string;
  destination: string;
  distanceKm: number;
  travelMinutes: number;
  path: string[];
  steps: DijkstraStep[];
  traceSummary: string[];
}

export interface GreedyResult {
  selectedDeliveries: DeliveryRequest[];
  deferredDeliveries: Array<{ request: DeliveryRequest; reason: string }>;
  totalWeightKg: number;
  totalProfit: number;
  unusedCapacityKg: number;
  capacityUtilizationPct: number;
  steps: Array<{
    requestId: string;
    action: "ACCEPTED" | "SKIPPED";
    weightKg: number;
    profit: number;
    ratio: number;
    remainingCapacityKg: number;
    explanation: string;
  }>;
}

export interface DpCellExplanation {
  itemIdx: number;
  capacityCol: number;
  status: "BASE" | "CANNOT_FIT" | "DECIDED";
  decision?: "TAKE" | "SKIP";
  weightKg?: number;
  profit?: number;
  skipVal: number;
  takeVal?: number;
  chosenVal: number;
  formula: string;
}

export interface KnapsackDpResult {
  selectedDeliveries: DeliveryRequest[];
  deferredDeliveries: Array<{ request: DeliveryRequest; reason: string }>;
  totalWeightKg: number;
  totalProfit: number;
  unusedCapacityKg: number;
  capacityUtilizationPct: number;
  dpTable: number[][]; // [items+1][capacity+1]
  itemLabels: string[];
  capacityCols: number[];
  backtrackCells: Array<{ row: number; col: number; chosen: boolean }>;
  traceSteps: string[];
  unitScale: number; // e.g. 1 kg increment
}

export type StopAction = "DEPOT_START" | "PICKUP" | "DROP" | "DEPOT_RETURN";

export interface PlanStop {
  stopNumber: number;
  locationId: string;
  locationName: string;
  action: StopAction;
  requestId?: string;
  arrivalMinute: number;
  departureMinute: number;
  deadlineMinute?: number;
  isLate: boolean;
  slackMinutes?: number;
  legDistanceKm: number;
  legTravelMinutes: number;
  legPathNodes: string[];
  loadAfterStopKg: number;
  capacityKg: number;
  status: "completed" | "current" | "future";
}

export interface FeasibilityRepair {
  removedRequestId: string;
  reason: string;
  recalculatedArrivalMinute: number;
  violatedDeadlineMinute: number;
}

export interface FinalPlan {
  id: string;
  createdAt: string;
  vehicle: Vehicle;
  acceptedRequests: DeliveryRequest[];
  deferredRequests: Array<{ request: DeliveryRequest; reason: string }>;
  stops: PlanStop[];
  totalDistanceKm: number;
  totalTravelMinutes: number;
  totalProfit: number;
  totalWeightKg: number;
  capacityUtilizationPct: number;
  allDeadlinesMet: boolean;
  repairs: FeasibilityRepair[];
  dijkstraLegs: Record<string, DijkstraResult>;
  greedyComparison: GreedyResult;
  dpResult: KnapsackDpResult;
  notes: string[];
}
