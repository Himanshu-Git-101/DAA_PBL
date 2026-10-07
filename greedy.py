"""
greedy.py - Greedy Package Selection Algorithm based on Profit-to-Weight Ratio.
Time Complexity: O(n log n) due to sorting.
"""
from typing import List, Dict, Any


def greedy_package_selection(packages: List[Dict[str, Any]], vehicle_capacity: float) -> Dict[str, Any]:
    """
    Selects deliveries greedily by prioritizing packages with the highest profit per kg.
    
    Args:
        packages: list of dictionaries, each having 'name', 'weight', 'profit', 'deadline', 'destination'
        vehicle_capacity: maximum weight the vehicle can carry (e.g., 30 kg)

    Returns:
        dict containing selected packages, total weight, total profit, unused capacity, and trace steps.
    """
    # Calculate profit density (ratio)
    scored_packages = []
    for p in packages:
        item = dict(p)
        w = float(item["weight"])
        item["ratio"] = round(item["profit"] / w, 2) if w > 0 else 0
        scored_packages.append(item)

    # Sort descending by ratio
    sorted_packages = sorted(scored_packages, key=lambda x: x["ratio"], reverse=True)

    selected: List[Dict[str, Any]] = []
    current_weight = 0.0
    current_profit = 0.0
    trace_steps: List[str] = []

    sorted_summary = ", ".join([f"{p['name']} ({p['ratio']} ₹/kg)" for p in sorted_packages])
    trace_steps.append(f"Sorted packages by Profit/Weight ratio: {sorted_summary}")

    for p in sorted_packages:
        w = p["weight"]
        if current_weight + w <= vehicle_capacity:
            selected.append(p)
            current_weight += w
            current_profit += p["profit"]
            rem = vehicle_capacity - current_weight
            trace_steps.append(
                f"✓ Checked {p['name']} ({w} kg) → FITS! Remaining capacity: {rem:.1f} kg"
            )
        else:
            rem = vehicle_capacity - current_weight
            trace_steps.append(
                f"✗ Checked {p['name']} ({w} kg) → EXCEEDS remaining capacity ({rem:.1f} kg). SKIPPED."
            )

    unused_cap = vehicle_capacity - current_weight
    utilization = round((current_weight / vehicle_capacity) * 100, 1) if vehicle_capacity > 0 else 0

    return {
        "selected_packages": selected,
        "total_weight": current_weight,
        "total_profit": current_profit,
        "unused_capacity": unused_cap,
        "vehicle_capacity": vehicle_capacity,
        "capacity_utilization": utilization,
        "sorted_packages": sorted_packages,
        "trace_steps": trace_steps
    }
