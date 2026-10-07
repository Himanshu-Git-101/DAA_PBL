"""
tests/test_algorithms.py - Verification suite for Core DSA components:
1. Binary Min-Heap Priority Queue (push, pop, min order, empty checks)
2. Graph & Dijkstra Shortest Path (correct distances and node paths)
3. Greedy Package Selection by Profit-to-Weight density
4. 0/1 Knapsack Dynamic Programming Optimality vs Greedy
"""
import pytest
from graph import Graph, create_sample_city
from dijkstra import MinHeapPriorityQueue, dijkstra
from greedy import greedy_package_selection
from dynamic_programming import knapsack_dp


def test_min_heap_priority_queue():
    pq = MinHeapPriorityQueue()
    assert pq.is_empty()

    pq.push(10, 'C')
    pq.push(3, 'A')
    pq.push(7, 'B')
    pq.push(1, 'Root')

    assert pq.pop() == (1, 'Root')
    assert pq.pop() == (3, 'A')
    assert pq.pop() == (7, 'B')
    assert pq.pop() == (10, 'C')
    assert pq.is_empty()


def test_graph_and_dijkstra():
    g = create_sample_city()
    dist, path, _ = dijkstra(g, 'Warehouse', 'Customer')

    assert dist == 20
    assert path[0] == 'Warehouse'
    assert path[-1] == 'Customer'

    dist_a, path_a, _ = dijkstra(g, 'Warehouse', 'A')
    assert dist_a == 5
    assert path_a == ['Warehouse', 'A']


def test_greedy_selection():
    packages = [
        {'name': 'P1', 'weight': 5, 'profit': 500, 'deadline': 40, 'destination': 'C'},
        {'name': 'P2', 'weight': 10, 'profit': 900, 'deadline': 60, 'destination': 'E'},
        {'name': 'P3', 'weight': 15, 'profit': 1200, 'deadline': 70, 'destination': 'G'},
        {'name': 'P4', 'weight': 8, 'profit': 700, 'deadline': 50, 'destination': 'D'},
    ]
    res = greedy_package_selection(packages, 20)
    selected_names = [p['name'] for p in res['selected_packages']]

    assert selected_names == ['P1', 'P2']
    assert res['total_weight'] == 15
    assert res['total_profit'] == 1400


def test_dp_knapsack_optimality():
    packages = [
        {'name': 'P1', 'weight': 5, 'profit': 500, 'deadline': 40, 'destination': 'C'},
        {'name': 'P2', 'weight': 10, 'profit': 900, 'deadline': 60, 'destination': 'E'},
        {'name': 'P3', 'weight': 15, 'profit': 1200, 'deadline': 70, 'destination': 'G'},
        {'name': 'P4', 'weight': 8, 'profit': 700, 'deadline': 50, 'destination': 'D'},
    ]
    dp_res = knapsack_dp(packages, 20)

    # DP achieves higher profit (1700) using items P1 + P3 than Greedy (1400)
    assert dp_res['total_profit'] == 1700
    assert dp_res['total_weight'] == 20
    selected_names = {p['name'] for p in dp_res['selected_packages']}
    assert selected_names == {'P1', 'P3'}
