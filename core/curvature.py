from core.measure import random_walk_measure
from core.transport import wasserstein_1

def ollivier_ricci(G, x, y, dist):
    mu_x = random_walk_measure(G, x)
    mu_y = random_walk_measure(G, y)

    W = wasserstein_1(mu_x, mu_y, dist)
    dxy = dist[(x, y)]

    if dxy == 0:
        return 0.0
    return 1.0 - W / dxy


def ricci_tensor(G, dist):
    ricci = {}
    for x in G.vertices():
        for y in G.neighbors(x):
            ricci[(x, y)] = ollivier_ricci(G, x, y, dist)
    return ricci
