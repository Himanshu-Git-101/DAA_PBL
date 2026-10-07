import { DeliveryRequest, KnapsackDpResult, DpCellExplanation } from '../../types';

export function runKnapsackDp(
  candidates: DeliveryRequest[],
  capacityKg: number,
  unitScale: number = 1 // 1 kg integer increments
): KnapsackDpResult {
  const n = candidates.length;
  // Convert vehicle capacity to integer capacity units
  const maxCapUnits = Math.floor(capacityKg / unitScale);

  // Initialize dp table: (n + 1) rows x (maxCapUnits + 1) cols
  const dpTable: number[][] = Array.from({ length: n + 1 }, () =>
    new Array(maxCapUnits + 1).fill(0)
  );

  for (let i = 1; i <= n; i++) {
    const item = candidates[i - 1];
    const wUnits = Math.round(item.weightKg / unitScale);
    const p = item.profit;

    for (let c = 0; c <= maxCapUnits; c++) {
      if (wUnits <= c) {
        const take = p + dpTable[i - 1][c - wUnits];
        const skip = dpTable[i - 1][c];
        dpTable[i][c] = Math.max(skip, take);
      } else {
        dpTable[i][c] = dpTable[i - 1][c];
      }
    }
  }

  // Backtracking
  const selectedDeliveries: DeliveryRequest[] = [];
  const backtrackCells: Array<{ row: number; col: number; chosen: boolean }> = [];
  let currC = maxCapUnits;

  for (let i = n; i > 0; i--) {
    const wasChosen = dpTable[i][currC] !== dpTable[i - 1][currC];
    backtrackCells.push({ row: i, col: currC, chosen: wasChosen });

    if (wasChosen) {
      const item = candidates[i - 1];
      selectedDeliveries.push(item);
      const wUnits = Math.round(item.weightKg / unitScale);
      currC -= wUnits;
    }
  }
  backtrackCells.push({ row: 0, col: currC, chosen: false });
  selectedDeliveries.reverse();

  const selectedIds = new Set(selectedDeliveries.map(d => d.id));
  const deferredDeliveries: Array<{ request: DeliveryRequest; reason: string }> = [];

  for (const c of candidates) {
    if (!selectedIds.has(c.id)) {
      deferredDeliveries.push({
        request: c,
        reason: "Excluded by 0/1 Knapsack optimal DP combination for total vehicle profit maximization"
      });
    }
  }

  const totalWeightKg = selectedDeliveries.reduce((sum, d) => sum + d.weightKg, 0);
  const totalProfit = dpTable[n][maxCapUnits];
  const unusedCapacityKg = Math.max(0, Math.round((capacityKg - totalWeightKg) * 10) / 10);
  const capacityUtilizationPct = capacityKg > 0 ? Math.round((totalWeightKg / capacityKg) * 1000) / 10 : 0;

  const itemLabels = ["Base (0)"]
    .concat(candidates.map(d => `${d.id} (${d.weightKg}kg, ₹${d.profit})`));
  const capacityCols = Array.from({ length: maxCapUnits + 1 }, (_, i) => i * unitScale);

  const traceSteps = [
    `Constructed 2D DP Table: ${n + 1} item rows × ${maxCapUnits + 1} capacity columns.`,
    `Base row (i = 0): dp[0][c] = 0 for all capacities c.`,
    `Recurrence applied: dp[i][c] = max(dp[i-1][c], dp[i-1][c - w_i] + p_i).`,
    `Optimal Knapsack profit achieved: ₹${totalProfit} (total weight: ${totalWeightKg.toFixed(1)} kg).`,
    `Backtracked ${selectedDeliveries.length} items: [${selectedDeliveries.map(d => d.id).join(", ")}].`
  ];

  return {
    selectedDeliveries,
    deferredDeliveries,
    totalWeightKg: Math.round(totalWeightKg * 10) / 10,
    totalProfit,
    unusedCapacityKg,
    capacityUtilizationPct,
    dpTable,
    itemLabels,
    capacityCols,
    backtrackCells,
    traceSteps,
    unitScale
  };
}

export function explainDpCell(
  candidates: DeliveryRequest[],
  dpTable: number[][],
  itemRow: number,
  capCol: number,
  unitScale: number = 1
): DpCellExplanation {
  if (itemRow <= 0 || itemRow > candidates.length) {
    return {
      itemIdx: itemRow,
      capacityCol: capCol,
      status: "BASE",
      skipVal: 0,
      chosenVal: 0,
      formula: "Base Row (i = 0): 0 items considered. Profit is inherently 0 for all capacities."
    };
  }

  const item = candidates[itemRow - 1];
  const wUnits = Math.round(item.weightKg / unitScale);
  const profit = item.profit;
  const skipVal = dpTable[itemRow - 1][capCol];

  if (wUnits > capCol) {
    return {
      itemIdx: itemRow,
      capacityCol: capCol,
      status: "CANNOT_FIT",
      weightKg: item.weightKg,
      skipVal,
      chosenVal: skipVal,
      formula: `Item ${item.id} (${item.weightKg} kg / ${wUnits} units) > Current Capacity (${capCol * unitScale} kg). Cannot fit, so carry upper cell: dp[${itemRow-1}][${capCol}] = ₹${skipVal}.`
    };
  }

  const takeVal = profit + dpTable[itemRow - 1][capCol - wUnits];
  const chosenVal = Math.max(skipVal, takeVal);
  const decision = takeVal >= skipVal ? "TAKE" : "SKIP";

  return {
    itemIdx: itemRow,
    capacityCol: capCol,
    status: "DECIDED",
    decision,
    weightKg: item.weightKg,
    profit,
    skipVal,
    takeVal,
    chosenVal,
    formula: `max(SKIP: dp[${itemRow-1}][${capCol}] = ₹${skipVal}, TAKE: ₹${profit} + dp[${itemRow-1}][${capCol - wUnits}] = ₹${takeVal}) = ₹${chosenVal} (${decision}).`
  };
}
