from collections import deque

def shortest_path_metric(G):
    dist = {}
    for v in G.vertices():
        dist[(v, v)] = 0
        visited = {v}
        Q = deque([(v, 0)])

        while Q:
            u, d = Q.popleft()
            for w in G.neighbors(u):
                if w not in visited:
                    visited.add(w)
                    dist[(v, w)] = d + 1
                    Q.append((w, d + 1))
    return dist
