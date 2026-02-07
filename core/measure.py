class ProbabilityMeasure:
    def __init__(self, support):
        self.support = dict(support)
        self._normalize()

    def _normalize(self):
        total = sum(self.support.values())
        if total <= 0:
            raise ValueError("Invalid probability mass")
        for k in self.support:
            self.support[k] /= total

    def __getitem__(self, key):
        return self.support.get(key, 0.0)

    def keys(self):
        return self.support.keys()

    def items(self):
        return self.support.items()


def random_walk_measure(G, x):
    nbrs = G.neighbors(x)
    if not nbrs:
        return ProbabilityMeasure({x: 1.0})
    p = 1.0 / len(nbrs)
    return ProbabilityMeasure({y: p for y in nbrs})
