"""
    📋 Problem Statement
    We are given:
        - A set of libraries.
        - Some libraries depend on others.

    Goal:
        Install libraries in an order such that no library is installed before its dependencies are installed.

    Constraints:
        No cycles (i.e., library A depends on B, and B on A — NOT allowed).
        - Dependencies form a Directed Acyclic Graph (no cycles).

    📄 Example
        Suppose:
            Library	Depends On
                A	-
                B	A
                C	A
                D	B, C

            Valid Installation Order:
                A → B → C → D
                or
                A → C → B → D

            Because:
                B needs A.
                C needs A.
                D needs B and C.
"""
import json
from collections import defaultdict, deque
from typing import Dict


class TopologicalSort:
    """
        We will use Kahn’s Algorithm (BFS-based Topological Sort):
            - Track indegrees (number of dependencies).
            - Pick nodes with 0 indegree first (means no pending dependency).
            - After processing, reduce indegrees of connected nodes.


        Steps:
            1. **Build Graph**:

               - Adjacency List → who depends on whom.

               - `indegree`: number of dependencies pending for each library.

            2. **Initialize Queue**:

               - Add all libraries with **0 indegree** (i.e., no dependencies).

            3. **Process Queue**:

               - Remove a library.

               - Add it to output.

               - Decrease indegree of its neighbors.

               - If a neighbor’s indegree becomes 0 → add to queue.

            4. **Detect Cycles**:

               - If not all libraries are processed → **Cycle detected** (impossible to install).
    """

    def __init__(self):
        # Adjacency list: key = library, value = list of libraries depending on it
        self.graph = defaultdict(list)
        # Indegree: key = library, value = number of libraries it depends on
        #   i.e., how many prerequisites still remaining
        self.indegree = defaultdict(int)
        # Track all libraries even if they have no outgoing or incoming edges
        self.libraries = set()  # all libraries

    def build_graph(self, dependencies: Dict):
        """
           Build the graph and indegree map from the given dependency dictionary.
           Each edge 'A → B' implies B depends on A.
        """
        # Build graph and indegree map
        for lib, deps in dependencies.items():
            self.libraries.add(lib)
            for dep in deps:
                # Add edge: dep → lib (dep must come before lib)
                self.graph[dep].append(lib)
                # Increment indegree for 'lib' because it depends on 'dep'
                self.indegree[lib] += 1
                # Ensure the dependency library is tracked too
                self.libraries.add(dep)

    def get_zero_indegree_nodes(self) -> deque:
        """
            Initializes the queue with nodes that have 0 indegree, meaning they have no dependencies and can be installed first.
        """
        queue = deque()
        for lib in self.libraries:
            if self.indegree[lib] == 0:
                queue.append(lib)
        return queue

    def topological_sort_dag(self, dependencies):
        """
            Perform Kahn's algorithm (BFS-based Topological Sort).
            Returns a valid installation order or raises Exception on cycle detection.
        """
        # Build the graph
        self.build_graph(dependencies=dependencies)
        # Get the zero degree nodes
        queue = self.get_zero_indegree_nodes()
        print(f"queue: {queue}, libs: {self.libraries}, indegrees: {self.indegree}, graph: {self.graph}")

        installation_order = []
        while queue:
            # [FIFO] Pick library with no pending dependencies
            lib = queue.popleft()
            installation_order.append(lib)

            # Go through libraries that depend on this "lib"
            for dependent in self.graph[lib]:
                self.indegree[dependent] -= 1  # Remove this dependency
                if self.indegree[dependent] == 0:
                    queue.append(dependent)

        # If not all libraries are in the order -> cycle exists (Not a DAG)
        if len(installation_order) != len(self.libraries):
            raise Exception(f"Cycle Detected! Not a DAG: {dependencies}")

        return installation_order


t_dependencies = {
    "B": ["A"],
    "C": ["A"],
    "D": ["B", "C"],
    "E": ["D"]
}
topo_sort_obj = TopologicalSort()
res_installation_order = topo_sort_obj.topological_sort_dag(dependencies=t_dependencies)
print(f"The installation order for deps: {json.dumps(t_dependencies)} is: {res_installation_order}")
