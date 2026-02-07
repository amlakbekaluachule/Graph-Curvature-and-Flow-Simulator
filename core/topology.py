from core.curvature import ricci_tensor
from core.metric import shortest_path_metric

def curvature_singularity(G, threshold=-0.5):
    dist = shortest_path_metric(G)
    ricci = ricci_tensor(G, dist)
    critical = []

    for (u, v), kappa in ricci.items():
        if kappa < threshold:
            critical.append((u, v, kappa))

    return critical
