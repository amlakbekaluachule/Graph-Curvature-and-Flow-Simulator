from collections import defaultdict
from typing import Dict, Set, Tuple

class Graph:
    def __init__(self):
        self._adj: Dict[int, Set[int]] = defaultdict(set)
        self._weights: Dict[Tuple[int, int], float] = {}

    def add_vertex(self, v: int):
        self._adj[v]

    def add_edge(self, u: int, v: int, w: float = 1.0):
        self.add_vertex(u)
        self.add_vertex(v)
        self._adj[u].add(v)
        self._adj[v].add(u)
        self._weights[(u, v)] = w
        self._weights[(v, u)] = w

    def vertices(self):
        return list(self._adj.keys())

    def edges(self):
        return list(self._weights.keys())

    def neighbors(self, v: int):
        return self._adj[v]

    def weight(self, u: int, v: int):
        return self._weights[(u, v)]

    def set_weight(self, u: int, v: int, w: float):
        self._weights[(u, v)] = w
        self._weights[(v, u)] = w

    def degree(self, v: int):
        return len(self._adj[v])
