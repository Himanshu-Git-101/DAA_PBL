import { LogisticsGraph } from './graph';
import { MinHeapPriorityQueue } from './minHeap';
import { DijkstraResult, DijkstraStep } from '../../types';

export function runDijkstra(
  graph: LogisticsGraph,
  startId: string,
  targetId: string,
  speedKmH: number = 28
): DijkstraResult {
  const allLocations = graph.getAllLocations();
  const distances: Record<string, number> = {};
  const previous: Record<string, string | null> = {};
  const visited = new Set<string>();
  const steps: DijkstraStep[] = [];
  const traceSummary: string[] = [];

  for (const loc of allLocations) {
    distances[loc.id] = Infinity;
    previous[loc.id] = null;
  }

  distances[startId] = 0;
  const pq = new MinHeapPriorityQueue<string>();
  pq.push(0, startId);

  steps.push({
    type: "INITIALIZATION",
    currNode: startId,
    currDist: 0,
    visited: Array.from(visited),
    distances: { ...distances },
    heap: pq.getElements(),
    explanation: `Initialize source '${startId}' distance = 0 km. Set all other ${allLocations.length - 1} node distances to ∞. Pushed (${startId}, 0 km) into Min-Heap.`
  });
  traceSummary.push(`Initialized tentative distances: ${startId} = 0 km, all other nodes = ∞.`);

  while (!pq.isEmpty()) {
    const { priority: currDist, item: currNode } = pq.pop();

    if (visited.has(currNode)) {
      steps.push({
        type: "SKIP_VISITED",
        currNode,
        currDist,
        visited: Array.from(visited),
        distances: { ...distances },
        heap: pq.getElements(),
        explanation: `Min-Heap extracted '${currNode}' with tentative ${currDist.toFixed(1)} km, but this node was already finalized. Skipping stale entry.`
      });
      continue;
    }

    visited.add(currNode);

    steps.push({
      type: "POP_MIN_HEAP",
      currNode,
      currDist,
      visited: Array.from(visited),
      distances: { ...distances },
      heap: pq.getElements(),
      explanation: `Extracted '${currNode}' (minimum tentative distance: ${currDist.toFixed(1)} km). Permanently finalized.`
    });

    if (currNode === targetId) {
      steps.push({
        type: "DESTINATION_REACHED",
        currNode,
        currDist,
        visited: Array.from(visited),
        distances: { ...distances },
        heap: pq.getElements(),
        explanation: `Destination '${targetId}' reached with finalized distance ${currDist.toFixed(1)} km! Triggering early termination.`
      });
      traceSummary.push(`Destination '${targetId}' finalized at ${currDist.toFixed(1)} km.`);
      break;
    }

    const neighbors = graph.getNeighbors(currNode);
    for (const edge of neighbors) {
      if (visited.has(edge.to)) continue;

      const alt = currDist + edge.distanceKm;
      const oldDist = distances[edge.to];

      if (alt < oldDist) {
        distances[edge.to] = alt;
        previous[edge.to] = currNode;
        pq.push(alt, edge.to);

        const oldLabel = oldDist === Infinity ? "∞" : `${oldDist.toFixed(1)} km`;
        steps.push({
          type: "EDGE_RELAXATION",
          currNode,
          currDist,
          targetNode: edge.to,
          edgeWeight: edge.distanceKm,
          newDist: alt,
          visited: Array.from(visited),
          distances: { ...distances },
          heap: pq.getElements(),
          explanation: `RELAXATION: Road '${currNode}' → '${edge.to}' (${edge.distanceKm.toFixed(1)} km). New path distance (${currDist.toFixed(1)} + ${edge.distanceKm.toFixed(1)} = ${alt.toFixed(1)} km) < old tentative (${oldLabel}). Updated and pushed to Min-Heap!`
        });
        traceSummary.push(`Relaxed edge ${currNode} → ${edge.to}: updated distance to ${alt.toFixed(1)} km.`);
      }
    }
  }

  // Path reconstruction
  const path: string[] = [];
  let curr: string | null = targetId;
  if (distances[targetId] !== Infinity) {
    while (curr) {
      path.push(curr);
      curr = previous[curr];
    }
    path.reverse();
  }

  const finalDistance = distances[targetId] === Infinity ? 0 : Math.round(distances[targetId] * 10) / 10;
  const travelMinutes = Math.round((finalDistance / speedKmH) * 60 * 10) / 10;

  return {
    start: startId,
    destination: targetId,
    distanceKm: finalDistance,
    travelMinutes,
    path,
    steps,
    traceSummary
  };
}
