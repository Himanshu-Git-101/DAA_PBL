# SmartRoute — Last-Mile Delivery Operations & DSA Learning Lab

> **A polished, interactive last-mile delivery operations prototype and educational backend laboratory for university Data Structures & Algorithms examinations.**

### 🎓 Academic Project Information
- **Course**: Data Structures & Algorithms (PBL Final Project)
- **Course Instructor**: **Dr. Syed Javed Pasha**
- **Project Team**:
  - **Himanshu Pandit**
  - **Devyani Pawar**
  - **Heman**
  - **Rimika Jain**
- **Coverage**: Greater Hyderabad Metropolitan Logistics & **Woxsen University Campus**

---

## 🌟 Executive Summary & Academic Promise

**SmartRoute** bridges the gap between commercial logistics fleet management and core computer science fundamentals. Dispatchers can inspect delivery requests, select vehicles, and compute legal stop routes across Hyderabad's road network, while students and faculty can step through the exact algorithms that generated those decisions.

> *"Plan today’s deliveries, see every route clearly, and understand exactly how the route and package choices were calculated."*

### The Two Core Product Areas

1. **Operations Overview (Dispatch Console):**
   - Live KPI summary strip computed directly from active data: total orders, accepted/selected, backlog/deferred, available fleet, planned profit, and cumulative distance.
   - Dual-synchronized **Leaflet / Google Maps 3D** canvas displaying the road graph, stop sequences, and animated simulation replay.
   - Dual route layer toggle: **Dijkstra Teaching Route** (straight geometric edges along graph vertices) vs. **Road Route** (smooth road geometry).
   - Filterable & sortable delivery request table with real-time selection synchronization with map markers.
   - Interactive **Add Delivery** modal with inline validation.
   - Fleet telematics cards with vehicle capacity and live load utilization bars.
   - Route Plan Panel with ordered stops, arrival times, deadlines, slack, and load tracking.

2. **Algorithm Lab (Educational Backend View):**
   - **Lab 0 — Model Inputs & Assumptions:** View and live-edit vehicle capacity and delivery values.
   - **Lab 1 — Graph Representation:** Interactive Adjacency List with $O(|V| + |E|)$ spatial complexity defense.
   - **Lab 2 — Dijkstra with Min-Heap:** Step-by-step priority queue trace, edge relaxation arithmetic, early termination, and $O((|V| + |E|) \log |V|)$ complexity.
   - **Lab 3 — Greedy Baseline:** Heuristic ranking (Profit Density, Highest Profit, Earliest Deadline) and localized sub-optimality analysis.
   - **Lab 4 — 0/1 Knapsack Dynamic Programming:** Full 2D memoization table with cell-by-cell arithmetic inspector, Bellman recurrence callout, and golden backtracking trail.
   - **Lab 5 — Route Construction:** Nearest-stop sequencing, Pickup-Before-Drop invariant, continuous vehicle load tracking, and automatic feasibility repair for overdue stops.
   - **Lab 6 — Benchmark & Viva Defense:** Side-by-side empirical comparison matrix and honest limitations disclosure.

---

## 🚀 Quickstart Guide

### Prerequisites
- **Node.js** (v18+) & **npm**
- **Python** (3.10+ with `pytest` for running Python backend unit tests)

### 1. Launch the Interactive Web Application

```bash
# Install dependencies
npm install

# Start the Vite development server
npm run dev
```

Visit **`http://localhost:5173/`** in your browser.

### 2. Run Python Unit Tests

The core algorithms are also implemented and tested in pure Python:

```bash
# Run pytest verification suite
pytest tests/test_algorithms.py
```
*All 4 tests verify Min-Heap Priority Queue, Dijkstra shortest path, Greedy selection, and 0/1 Knapsack DP optimality.*

---

## 🗺️ Map Integration & Graceful Fallback

SmartRoute is built with zero-credential resilience:
1. **Default Zero-Config Fallback (Active):** Uses **Leaflet** with **Carto Dark** tiles. High contrast, fast, completely free, and works without an API key or internet setup.
2. **Optional Google Maps 3D Platform:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Add your Google Maps Platform API key:
     ```env
     VITE_GOOGLE_MAPS_API_KEY=your_api_key_here
     ```
   - Ensure the **Maps JavaScript API** is enabled in your Google Cloud Console.

---

## 🎓 5–7 Minute Faculty Viva Walkthrough Script

| Time | Stage | Action & Explanation |
| :--- | :--- | :--- |
| **0:00 - 1:00** | **Operations Overview** | Point to the KPI strip and delivery list. Explain parcel weights, profits, and deadlines. Select vehicle `V-101` (25 kg capacity). |
| **1:00 - 2:00** | **Plan Generation** | Click **Plan Deliveries**. Show how 0/1 Knapsack DP selects the optimal subset while the stop sequence is constructed respecting **Pickup-Before-Drop** and deadlines. |
| **2:00 - 3:30** | **Algorithm Lab: Graph & Dijkstra** | Switch to **Algorithm Lab**. Show Lab 1 (Adjacency List vs Matrix). Open Lab 2 and step through the Binary Min-Heap relaxation arithmetic: $\text{currDist} + \text{edge} < \text{oldDist}$. |
| **3:30 - 5:00** | **Lab 4: 0/1 Knapsack DP** | Inspect the 2D DP table. Click a cell to display Bellman's recurrence: $\max(\text{skip}, \text{take})$. Trace the golden backtracking path. |
| **5:00 - 6:00** | **Lab 5: Route Feasibility Repair** | Show load tracking after each stop (starts at 0 kg, never exceeds vehicle capacity). Demonstrate how late deliveries are transparently repaired. |
| **6:00 - 7:00** | **Viva Defense & Academic Honesty** | Deliver the core boundary statement: Dijkstra solves shortest paths, Knapsack solves item value, and the stop sequencer is a polynomial heuristic—not a global VRP solver. |

---

## 📖 Examiner Viva Glossary

- **Vertex (Node):** A physical location, hub, or customer address in the service network.
- **Edge:** A direct road connection with non-negative distance in km and travel time in minutes.
- **Weight:** The cost of traversing an edge (road distance in km).
- **Adjacency List:** A graph representation taking $O(|V| + |E|)$ memory, optimal for sparse street networks.
- **Min-Heap (Priority Queue):** Complete binary tree maintaining minimum element at the root for $O(\log |V|)$ extraction.
- **Relaxation:** Updating a neighbor's tentative distance if a shorter path is discovered via the current node.
- **Greedy Choice:** Making the locally optimal decision at each step without backtracking ($O(n \log n)$).
- **0/1 Knapsack DP:** Sub-problem memoization maximizing parcel profit within vehicle weight ($O(n \times C)$).
- **Feasibility:** Guaranteeing that vehicle capacity is never exceeded and all delivered packages arrive before their deadline.
- **Heuristic:** A practical polynomial-time approximation for NP-hard logistics problems.

---

## ⚖️ Academic Limitations & Boundary Statement

> *"We model the service area as a weighted graph. Locations are vertices and roads are edges, stored as adjacency lists. Dijkstra’s algorithm uses a min-heap to find short paths between locations. We compare a simple greedy package-picking rule with 0/1 knapsack dynamic programming to choose valuable packages that fit the vehicle. We then build a pickup-before-drop route and check its load and delivery deadlines. The route planner is an educational heuristic; it is not a globally optimal industrial vehicle-routing solver."*

---

## 🛠️ Project Structure

```text
├── src/
│   ├── types/
│   │   └── index.ts                 # TypeScript interfaces (Location, Delivery, Plan, etc.)
│   ├── lib/
│   │   ├── algorithms/
│   │   │   ├── graph.ts             # Adjacency list representation & Hyderabad network
│   │   │   ├── minHeap.ts           # Scratch binary min-heap priority queue
│   │   │   ├── dijkstra.ts          # Dijkstra shortest path with full step trace
│   │   │   ├── greedySelection.ts   # Greedy baselines (density, profit, deadline)
│   │   │   ├── knapsack.ts          # 0/1 Knapsack DP with full 2D table & backtracking
│   │   │   └── scheduleRoute.ts     # Pickup-before-drop, load tracking & repair
│   │   ├── data/
│   │   │   └── sampleDay.ts         # Initial vehicles and Hyderabad deliveries
│   │   └── planning/
│   │       └── buildPlan.ts         # Master planning engine
│   ├── components/
│   │   ├── app-shell/
│   │   │   └── Navbar.tsx           # Brand, operating day selector, area switch
│   │   ├── operations/
│   │   │   ├── MapView.tsx          # Dual-layer Leaflet / Google map with replay
│   │   │   ├── DeliveryTable.tsx    # Filterable, sortable delivery list
│   │   │   ├── DeliveryModal.tsx    # Add delivery dialog with validation
│   │   │   ├── FleetPanel.tsx       # Fleet cards with capacity meters
│   │   │   └── RoutePlanPanel.tsx   # Ordered stops, timings, load & feasibility
│   │   ├── algorithm-lab/
│   │   │   ├── AlgorithmLab.tsx     # Stepper timeline controller
│   │   │   ├── Lab0Assumptions.tsx  # Model parameters & editable demo value
│   │   │   ├── Lab1Graph.tsx        # Interactive Adjacency List inspection
│   │   │   ├── Lab2Dijkstra.tsx     # Min-Heap trace & relaxation arithmetic
│   │   │   ├── Lab3Greedy.tsx       # Greedy baseline analysis
│   │   │   ├── Lab4Knapsack.tsx     # Interactive 2D DP table & backtracking
│   │   │   ├── Lab5RouteConstruction.tsx # Route invariants & repair trace
│   │   │   └── Lab6Comparison.tsx   # Benchmark matrix & viva defense
│   │   └── viva-guide/
│   │       └── VivaGuide.tsx        # Presentation script & glossary
│   ├── styles/
│   │   └── index.css                # Obsidian design tokens & Leaflet styles
│   ├── App.tsx                      # Root state & view switcher
│   └── main.tsx                     # React DOM entry point
├── tests/
│   └── test_algorithms.py           # Python test suite verifying DSA logic
├── graph.py                         # Python Adjacency List graph
├── dijkstra.py                      # Python Min-Heap & Dijkstra
├── greedy.py                        # Python Greedy package selection
├── dynamic_programming.py           # Python 0/1 Knapsack DP
├── data/
│   └── deliveries.csv               # Raw dataset
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

---

Built with pride for academic and algorithmic craftsmanship.
