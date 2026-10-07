import { DeliveryRequest, GreedyResult } from '../../types';

export type GreedyCriterion = "profit_density" | "highest_profit" | "earliest_deadline";

export function runGreedySelection(
  candidates: DeliveryRequest[],
  capacityKg: number,
  criterion: GreedyCriterion = "profit_density"
): GreedyResult {
  const sorted = [...candidates].sort((a, b) => {
    if (criterion === "profit_density") {
      const ratioA = a.weightKg > 0 ? a.profit / a.weightKg : 0;
      const ratioB = b.weightKg > 0 ? b.profit / b.weightKg : 0;
      return ratioB - ratioA; // Descending
    } else if (criterion === "highest_profit") {
      return b.profit - a.profit; // Descending
    } else {
      return a.deadlineMinutesFromStart - b.deadlineMinutesFromStart; // Ascending
    }
  });

  const selectedDeliveries: DeliveryRequest[] = [];
  const deferredDeliveries: Array<{ request: DeliveryRequest; reason: string }> = [];
  const steps: GreedyResult["steps"] = [];

  let currentWeight = 0;
  let currentProfit = 0;

  for (const req of sorted) {
    const ratio = req.weightKg > 0 ? Math.round((req.profit / req.weightKg) * 100) / 100 : 0;

    if (currentWeight + req.weightKg <= capacityKg) {
      selectedDeliveries.push(req);
      currentWeight += req.weightKg;
      currentProfit += req.profit;
      const rem = Math.round((capacityKg - currentWeight) * 10) / 10;

      steps.push({
        requestId: req.id,
        action: "ACCEPTED",
        weightKg: req.weightKg,
        profit: req.profit,
        ratio,
        remainingCapacityKg: rem,
        explanation: `ACCEPT: ${req.id} (${req.weightKg} kg, ₹${req.profit}, ${ratio} ₹/kg). Fits within remaining capacity. New remaining: ${rem} kg.`
      });
    } else {
      const rem = Math.round((capacityKg - currentWeight) * 10) / 10;
      const reason = `Exceeds vehicle remaining capacity (${req.weightKg} kg > ${rem} kg)`;
      deferredDeliveries.push({ request: req, reason });

      steps.push({
        requestId: req.id,
        action: "SKIPPED",
        weightKg: req.weightKg,
        profit: req.profit,
        ratio,
        remainingCapacityKg: rem,
        explanation: `SKIP: ${req.id} (${req.weightKg} kg) exceeds remaining capacity of ${rem} kg. Deferred.`
      });
    }
  }

  const unusedCapacityKg = Math.round((capacityKg - currentWeight) * 10) / 10;
  const capacityUtilizationPct = capacityKg > 0 ? Math.round((currentWeight / capacityKg) * 1000) / 10 : 0;

  return {
    selectedDeliveries,
    deferredDeliveries,
    totalWeightKg: Math.round(currentWeight * 10) / 10,
    totalProfit: currentProfit,
    unusedCapacityKg,
    capacityUtilizationPct,
    steps
  };
}
