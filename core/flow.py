from core.curvature import ricci_tensor
from core.metric import shortest_path_metric

def ricci_flow(G, step=0.01):
    dist = shortest_path_metric(G)
    ricci = ricci_tensor(G, dist)

    for (u, v), kappa in ricci.items():
        w = G.weight(u, v)
        new_w = max(1e-4, w * (1 - step * kappa))
        G.set_weight(u, v, new_w)
