"""
    Finding the shortest path from a given node to all other nodes [is a classic heap (priority queue) problem.]

    📚 Problem Recognized:
        You are describing Dijkstra’s Algorithm.

    🔥 Why Dijkstra uses a Heap?
        Problem:
            - You have a graph with weighted edges.
            - You want to find the shortest distance from a source node to all other nodes.

    Challenge:
        As you move, you discover new paths with different costs.

        You must always expand the path with the minimum current cost first.
            👉 Heap helps by giving you the next minimum cost node quickly.

    🧠 Key Ideas:
        Concept	Description
        Graph	Nodes + weighted edges
        Priority Queue (Min-Heap)	To always pick the node with the smallest distance discovered so far
        Dijkstra's Core Idea	Greedily extend the shortest known path first

    ✅ Step-by-Step with Intuition
    Step	            Action
     1	    Initialize distances: all ∞, source = 0
     2	    Use a Min-Heap to always pick the node with the smallest known distance
     3	    For each neighbor, check: is new path shorter? If yes, update it
     4	    Repeat until all nodes are visited
"""

import heapq
from typing import Dict, List, Tuple


class DijkstraShortestPath:
    def __init__(self, graph: Dict[str, List[Tuple[str, int]]]):
        self.graph = graph

    def find_shortest_paths_for_source(self, source: str) -> Dict[str, int]:
        distances = {}
        for node in self.graph:
            distances[node] = float('inf')
        distances[source] = 0

        # Step2: Use the min-heap to always expand the closes node
        min_heap = [(0, source)]

        while min_heap:
            current_dist, current_node = heapq.heappop(min_heap)

            # If we already have a shorter distance recorded, skip
            if current_dist > distances[current_node]:
                continue

            # Step3: Explore neighbors
            for neighbor, weight in self.graph[current_node]:
                distance_through_current = current_dist + weight

                # Step4: If new path is shorter, update and push to heap
                if distance_through_current < distances[neighbor]:
                    distances[neighbor] = distance_through_current
                    heapq.heappush(min_heap, (distance_through_current, neighbor))

        return distances


# Example usage
if __name__ == "__main__":
    t_graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 5)],
        'C': [('D', 1)],
        'D': []
    }

    dijkstra = DijkstraShortestPath(t_graph)
    result = dijkstra.find_shortest_paths_for_source('A')
    print("Shortest distances from A:", result)
