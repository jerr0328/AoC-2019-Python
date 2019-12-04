from typing import List, Sequence

from shapely.geometry import LineString, Point


def closest_intersection(paths: Sequence[List[str]]) -> int:
    first = build_linestring(paths[0])
    second = build_linestring(paths[1])
    intersections = first.intersection(second)
    center = Point(0, 0)
    shortest_dist = 0
    for intersect in intersections:
        if intersect != center:
            dist = abs(int(intersect.x)) + abs(int(intersect.y))
            if not shortest_dist or dist < shortest_dist:
                shortest_dist = dist
            print(f"Intersection at {intersect.coords[0]}, distance: {dist}")
    return shortest_dist


def shortest_dist(paths: Sequence[List[str]]) -> int:
    first = build_linestring(paths[0])
    second = build_linestring(paths[1])
    intersections = first.intersection(second)
    center = Point(0, 0)
    shortest_len = 0
    for intersect in intersections:
        if intersect != center:
            first_len = partial_length(first, intersect)
            second_len = partial_length(second, intersect)
            len = first_len + second_len
            print(f"Intersection at {intersect.coords[0]}, length: {len}")
            if not shortest_len or len < shortest_len:
                shortest_len = len

    return shortest_len


def partial_length(ls: LineString, until: Point) -> int:
    previous = Point(0, 0)
    line = [previous]
    for point in ls.coords[1:]:
        if LineString([previous, point]).intersects(until):
            line.append(until)
            return int(LineString(line).length)
        line.append(point)
        previous = point


def read_file() -> List[List[str]]:
    with open("data/3.txt", "r") as f:
        return [line.split(",") for line in f]


def build_linestring(path: List[str]):
    last = (0, 0)
    coords = [(0, 0)]
    for item in path:
        direction = item[0]
        dist = int(item[1:])
        if direction == "U":  # Up
            last = (last[0], last[1] + dist)
        elif direction == "D":  # Down
            last = (last[0], last[1] - dist)
        elif direction == "L":  # Left
            last = (last[0] - dist, last[1])
        elif direction == "R":  # Right
            last = (last[0] + dist, last[1])

        coords.append(last)
    return LineString(coords)
