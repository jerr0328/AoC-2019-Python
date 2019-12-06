from collections import defaultdict
from typing import Set


class Orbits:
    def __init__(self, orbits: dict):
        self.orbits = orbits
        self.memo = defaultdict(int)

    def calculate_depth(self, node: str) -> int:
        if node not in self.orbits:
            return 0
        if node in self.memo:
            return self.memo[node]

        depth = 1 + self.calculate_depth(self.orbits[node])
        self.memo[node] = depth
        return depth

    def total_orbits(self) -> int:
        return sum(self.calculate_depth(node) for node in self.orbits)

    def ancestors(self, node: str) -> Set[str]:
        if node not in self.orbits:
            return set()
        ancestor = self.orbits[node]
        ancestors = self.ancestors(ancestor)
        ancestors.add(ancestor)
        return ancestors

    def transfers_needed(self, src: str, dst: str) -> int:
        src_orbit = self.orbits[src]
        dst_orbit = self.orbits[dst]
        if src_orbit == dst_orbit:
            return 0
        src_depth = self.calculate_depth(src_orbit)
        dst_depth = self.calculate_depth(dst_orbit)

        src_ancestors = self.ancestors(src_orbit)
        dst_ancestors = self.ancestors(dst_orbit)

        common_ancestors = src_ancestors.intersection(dst_ancestors)
        heighest_common_ancestor_height = 0
        for ancestor in common_ancestors:
            ancestor_height = self.calculate_depth(ancestor)
            if ancestor_height > heighest_common_ancestor_height:
                heighest_common_ancestor_height = ancestor_height

        return src_depth + dst_depth - (2 * heighest_common_ancestor_height)

    @classmethod
    def from_file(cls):
        orbits = {}
        with open("data/6.txt", "r") as f:
            for line in f:
                node, satellite = line.strip().split(")")
                orbits[satellite] = node
        return cls(orbits)
