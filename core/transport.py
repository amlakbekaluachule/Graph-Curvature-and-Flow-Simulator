import numpy as np

def wasserstein_1(mu, nu, dist):
    X = list(mu.keys())
    Y = list(nu.keys())

    supply = np.array([mu[x] for x in X])
    demand = np.array([nu[y] for y in Y])

    cost = np.zeros((len(X), len(Y)))
    for i, x in enumerate(X):
        for j, y in enumerate(Y):
            cost[i, j] = dist[(x, y)]

    i = j = 0
    total = 0.0
    supply = supply.copy()
    demand = demand.copy()

    while i < len(supply) and j < len(demand):
        flow = min(supply[i], demand[j])
        total += flow * cost[i, j]
        supply[i] -= flow
        demand[j] -= flow
        if supply[i] == 0:
            i += 1
        if demand[j] == 0:
            j += 1

    return total
