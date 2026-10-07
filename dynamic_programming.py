"""
dynamic_programming.py - 0/1 Knapsack Dynamic Programming for optimal package selection.
Time Complexity: O(n * C) where n = packages count, C = vehicle capacity.
Space Complexity: O(n * C) for the full 2D table.
"""
from typing import List, Dict, Any, Tuple


def knapsack_dp(packages: List[Dict[str, Any]], vehicle_capacity: int) -> Dict[str, Any]:
    """
    Computes optimal subset of packages to maximize profit within vehicle capacity.
    Constructs full 2D table and backtracks optimal combination.
    """
    n = len(packages)
    C = int(vehicle_capacity)

    # dp[i][c] = max profit considering first i packages with capacity c
    dp: List[List[float]] = [[0.0] * (C + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        pkg = packages[i - 1]
        w = int(pkg["weight"])
        p = float(pkg["profit"])
        for c in range(C + 1):
            if w <= c:
                dp[i][c] = max(dp[i - 1][c], dp[i - 1][c - w] + p)
            else:
                dp[i][c] = dp[i - 1][c]

    # Backtracking to find selected items
    selected: List[Dict[str, Any]] = []
    backtrack_cells: List[Tuple[int, int]] = []
    curr_c = C

    for i in range(n, 0, -1):
        backtrack_cells.append((i, curr_c))
        if dp[i][curr_c] != dp[i - 1][curr_c]:
            pkg = packages[i - 1]
            selected.append(pkg)
            curr_c -= int(pkg["weight"])

    backtrack_cells.append((0, curr_c))
    selected.reverse()

    total_weight = sum(p["weight"] for p in selected)
    total_profit = dp[n][C]
    unused_capacity = vehicle_capacity - total_weight

    package_labels = ["Base (0)"] + [f"{p['name']} ({p['weight']}kg, ₹{p['profit']})" for p in packages]
    capacity_cols = list(range(C + 1))

    trace_steps = [
        f"Built 2D DP Table of size ({n + 1} packages) × ({C + 1} kg capacity).",
        "Base Case: dp[0][c] = 0 for all capacities c.",
        "Recurrence applied: dp[i][c] = max(dp[i-1][c], dp[i-1][c - w_i] + p_i).",
        f"Maximum Profit achievable: ₹{total_profit}.",
        f"Backtracked selected items: {', '.join([p['name'] for p in selected])}."
    ]

    utilization = round((total_weight / vehicle_capacity) * 100, 1) if vehicle_capacity > 0 else 0

    return {
        "selected_packages": selected,
        "total_weight": total_weight,
        "total_profit": total_profit,
        "unused_capacity": unused_capacity,
        "vehicle_capacity": vehicle_capacity,
        "capacity_utilization": utilization,
        "dp_table": dp,
        "package_labels": package_labels,
        "capacity_cols": capacity_cols,
        "backtrack_cells": backtrack_cells,
        "trace_steps": trace_steps
    }


def explain_dp_cell(packages: List[Dict[str, Any]], dp_table: List[List[float]], item_idx: int, cap: int) -> Dict[str, Any]:
    """
    Returns step-by-step arithmetic breakdown for any cell (i, c) in the DP table.
    """
    if item_idx <= 0 or item_idx > len(packages):
        return {"explanation": "Base row (i=0): 0 packages considered, profit is always 0."}

    pkg = packages[item_idx - 1]
    w = int(pkg["weight"])
    p = float(pkg["profit"])
    name = pkg["name"]

    skip_val = dp_table[item_idx - 1][cap]

    if w > cap:
        return {
            "status": "CANNOT_FIT",
            "weight": w,
            "capacity": cap,
            "skip_val": skip_val,
            "result": skip_val,
            "formula": f"w ({w} kg) > c ({cap} kg) → Cannot fit. Carry upper cell: dp[{item_idx-1}][{cap}] = {skip_val}"
        }
    else:
        take_val = p + dp_table[item_idx - 1][cap - w]
        chosen = max(skip_val, take_val)
        decision = "TAKE" if take_val >= skip_val else "SKIP"
        return {
            "status": "DECIDED",
            "decision": decision,
            "weight": w,
            "profit": p,
            "capacity": cap,
            "skip_val": skip_val,
            "take_val": take_val,
            "result": chosen,
            "formula": f"max(SKIP: dp[{item_idx-1}][{cap}] = {skip_val}, TAKE: {p} + dp[{item_idx-1}][{cap-w}] = {take_val}) = {chosen}"
        }
