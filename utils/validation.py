"""
Validation utilities for GeoFlow

Purpose:
- Enforce mathematical invariants
- Catch silent geometric errors
- Ensure curvature, transport, and flow consistency
"""

import math
from core.metric import shortest_path_metric
from core.curvature import ricci_tensor
from core.measure import random_walk_measure

def validate_graph(G):
    for (u, v), w in G._weights.items():
        if w <= 0:
            raise ValueError(f"Non-positive edge weight on ({u}, {v})")

        if (v, u) not in G._weights:
            raise ValueError(f"Asymmetric edge detected: ({u}, {v})")

    for u in G.vertices():
        for v in G.neighbors(u):
            if u not in G.neighbors(v):
                raise ValueError(f"Adjacency not symmetric: {u} <-> {v}")

def validate_probability_measure(mu, tol=1e-8):
    total = 0.0
    for x, p in mu.items():
        if p < -tol:
            raise ValueError(f"Negative probability at {x}")
        total += p

    if abs(total - 1.0) > tol:
        raise ValueError(f"Measure not normalized: sum = {total}")


def validate_random_walk_measure(G, x):
    mu = random_walk_measure(G, x)
    validate_probability_measure(mu)

    deg = G.degree(x)
    if deg == 0:
        if len(mu.support) != 1 or x not in mu.support:
            raise ValueError("Isolated vertex measure incorrect")
        return

    expected = 1.0 / deg
    for y in G.neighbors(x):
        if abs(mu[y] - expected) > 1e-8:
            raise ValueError("Random walk measure not uniform")

def validate_metric(G):
    dist = shortest_path_metric(G)

    for x in G.vertices():
        if dist[(x, x)] != 0:
            raise ValueError("Metric violates d(x,x)=0")

    for (x, y), dxy in dist.items():
        if (y, x) not in dist:
            raise ValueError("Metric not symmetric")
        if dist[(y, x)] != dxy:
            raise ValueError("Metric symmetry violated")

    verts = G.vertices()
    for i in range(min(10, len(verts))):
        x = verts[i]
        for y in verts:
            for z in verts:
                if dist[(x, z)] > dist[(x, y)] + dist[(y, z)] + 1e-8:
                    raise ValueError("Triangle inequality violated")

def validate_ricci_bounds(G, lower=-2.0, upper=1.0):
    dist = shortest_path_metric(G)
    ricci = ricci_tensor(G, dist)

    for (u, v), kappa in ricci.items():
        if kappa > upper + 1e-8:
            raise ValueError(f"Curvature exceeds upper bound: {kappa}")
        if kappa < lower - 1e-8:
            raise ValueError(f"Curvature below lower bound: {kappa}")


def validate_flat_space(G, tol=1e-6):
    dist = shortest_path_metric(G)
    ricci = ricci_tensor(G, dist)

    values = list(ricci.values())
    mean = sum(values) / len(values)

    if abs(mean) > tol:
        raise ValueError("Expected flat curvature, detected deviation")

def validate_ricci_flow_step(G_before, G_after):
    for (u, v), w in G_after._weights.items():
        if w <= 0:
            raise ValueError("Ricci flow produced non-positive weight")

    if set(G_before.edges()) != set(G_after.edges()):
        raise ValueError("Ricci flow changed graph topology")

def full_validation(G):
    validate_graph(G)
    validate_metric(G)

    for v in G.vertices():
        validate_random_walk_measure(G, v)

    validate_ricci_bounds(G)

    return True
