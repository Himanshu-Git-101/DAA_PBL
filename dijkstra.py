"""
dijkstra.py - Shortest path algorithm using a manual Min-Heap Priority Queue.
Implemented from scratch without external libraries.
"""
from typing import Dict, List, Tuple, Optional, Any
import math
from graph import Graph


class MinHeapPriorityQueue:
    """
    A simple Binary Min-Heap Priority Queue storing (priority, item).
    Demonstrates manual heap operations for DSA examination.
    """
    def __init__(self):
        self.heap: List[Tuple[float, Any]] = []

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def push(self, priority: float, item: Any) -> None:
        """Push an element and sift up to preserve the min-heap property."""
        self.heap.append((priority, item))
        self._sift_up(len(self.heap) - 1)

    def pop(self) -> Tuple[float, Any]:
        """Pop and return the minimum element (lowest priority number)."""
        if self.is_empty():
            raise IndexError("pop from empty priority queue")
        min_elem = self.heap[0]
        last_elem = self.heap.pop()
        if not self.is_empty():
            self.heap[0] = last_elem
            self._sift_down(0)
        return min_elem

    def _sift_up(self, idx: int) -> None:
        parent = (idx - 1) // 2
        while idx > 0 and self.heap[idx][0] < self.heap[parent][0]:
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx: int) -> None:
        size = len(self.heap)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx

            if left < size and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < size and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest != idx:
                self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
                idx = smallest
            else:
                break

    def get_elements(self) -> List[Tuple[float, Any]]:
        return list(self.heap)


def dijkstra(graph: Graph, start: str, destination: str) -> Tuple[float, List[str], List[str]]:
    """
    Finds the shortest path and minimum travel distance from start to destination.
    Returns:
        distance: float
        path: list of location names
        trace_steps: list of major steps executed (for viva explanation)
    """
    distances: Dict[str, float] = {node: float("inf") for node in graph.get_locations()}
    previous: Dict[str, Optional[str]] = {node: None for node in graph.get_locations()}
    visited = set()
    trace_steps: List[str] = []

    distances[start] = 0.0
    pq = MinHeapPriorityQueue()
    pq.push(0.0, start)

    trace_steps.append(f"Initialize distance to {start} = 0, others = ∞")

    while not pq.is_empty():
        curr_dist, curr_node = pq.pop()

        if curr_node in visited:
            continue
        visited.add(curr_node)

        trace_steps.append(f"Checking location '{curr_node}' (current distance: {curr_dist:.1f} km)")

        if curr_node == destination:
            trace_steps.append(f"Reached destination '{curr_node}' with distance {curr_dist:.1f} km")
            break

        for neighbor, weight in graph.get_neighbors(curr_node):
            if neighbor in visited:
                continue
            new_dist = curr_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = curr_node
                pq.push(new_dist, neighbor)
                trace_steps.append(
                    f"  → Found shorter path to '{neighbor}': {new_dist:.1f} km (via {curr_node})"
                )

    # Reconstruct path
    path: List[str] = []
    curr = destination
    if distances[destination] != float("inf"):
        while curr:
            path.append(curr)
            curr = previous.get(curr)
        path.reverse()
        trace_steps.append(f"Shortest path confirmed: {' → '.join(path)} ({distances[destination]:.1f} km)")
    else:
        path = []

    return distances[destination], path, trace_steps


def dijkstra_detailed(graph: Graph, start: str, destination: str) -> Dict[str, Any]:
    """
    Step-by-step Dijkstra execution tracer designed for interactive educational playback.
    Records heap state, visited nodes, tentative distances, and plain-English pedagogical notes.
    """
    distances: Dict[str, float] = {node: float("inf") for node in graph.get_locations()}
    previous: Dict[str, Optional[str]] = {node: None for node in graph.get_locations()}
    visited = set()
    steps: List[Dict[str, Any]] = []

    distances[start] = 0.0
    pq = MinHeapPriorityQueue()
    pq.push(0.0, start)

    steps.append({
        "type": "INITIALIZATION",
        "curr_node": start,
        "curr_dist": 0.0,
        "visited": list(visited),
        "distances": dict(distances),
        "heap": pq.get_elements(),
        "explanation": f"🎯 Start at '{start}'. Set Tentative Distance = 0 km. All other {len(distances)-1} locations set to ∞. Pushed ({start}, 0 km) into Min-Heap."
    })

    while not pq.is_empty():
        curr_dist, curr_node = pq.pop()

        if curr_node in visited:
            steps.append({
                "type": "SKIP_VISITED",
                "curr_node": curr_node,
                "curr_dist": curr_dist,
                "visited": list(visited),
                "distances": dict(distances),
                "heap": pq.get_elements(),
                "explanation": f"⏭️ Min-Heap popped '{curr_node}' ({curr_dist:.1f} km), but it was ALREADY permanently finalized. Skipping duplicate entry."
            })
            continue

        visited.add(curr_node)

        steps.append({
            "type": "POP_MIN_HEAP",
            "curr_node": curr_node,
            "curr_dist": curr_dist,
            "visited": list(visited),
            "distances": dict(distances),
            "heap": pq.get_elements(),
            "explanation": f"⭐ Min-Heap extracted '{curr_node}' as the unvisited node with minimum tentative distance ({curr_dist:.1f} km). Marked as PERMANENTLY VISITED."
        })

        if curr_node == destination:
            steps.append({
                "type": "DESTINATION_REACHED",
                "curr_node": curr_node,
                "curr_dist": curr_dist,
                "visited": list(visited),
                "distances": dict(distances),
                "heap": pq.get_elements(),
                "explanation": f"🏁 Destination '{destination}' reached! Optimal shortest path locked at {curr_dist:.1f} km. Early exit triggered."
            })
            break

        for neighbor, weight in graph.get_neighbors(curr_node):
            if neighbor in visited:
                continue
            old_dist = distances[neighbor]
            new_dist = curr_dist + weight
            if new_dist < old_dist:
                distances[neighbor] = new_dist
                previous[neighbor] = curr_node
                pq.push(new_dist, neighbor)
                old_str = "∞" if old_dist == float("inf") else f"{old_dist:.1f} km"
                steps.append({
                    "type": "EDGE_RELAXATION",
                    "curr_node": curr_node,
                    "target_node": neighbor,
                    "edge_weight": weight,
                    "curr_dist": curr_dist,
                    "new_dist": new_dist,
                    "visited": list(visited),
                    "distances": dict(distances),
                    "heap": pq.get_elements(),
                    "explanation": f"🔄 RELAXATION: Road '{curr_node}' → '{neighbor}' ({weight:.1f} km). Path through '{curr_node}' ({curr_dist:.1f} + {weight:.1f} = {new_dist:.1f} km) is SHORTER than previous tentative ({old_str}). Updated distance and pushed into Min-Heap!"
                })

    path: List[str] = []
    curr = destination
    if distances[destination] != float("inf"):
        while curr:
            path.append(curr)
            curr = previous.get(curr)
        path.reverse()

    return {
        "start": start,
        "destination": destination,
        "distance": distances[destination],
        "path": path,
        "steps": steps
    }
