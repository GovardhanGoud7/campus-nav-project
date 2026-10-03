""" Campus Navigation — Pathfinding Engine ======================================== Models the campus (outdoor paths + 2 multi-floor buildings) as a weighted graph and finds the shortest walking route between any two points using Dijkstra's algorithm. This is the same core technique real indoor-navigation apps (Google Maps Indoor, university wayfinding apps) use under the hood. """
import heapq

# --- Campus graph: node -> {neighbor: distance_in_meters} ---
CAMPUS_GRAPH = {
    # Outdoor network
    "Main Gate":            {"Parking Area": 40, "Canteen": 60},
    "Parking Area":         {"Main Gate": 40, "Central Plaza": 50},
    "Central Plaza":        {"Parking Area": 50, "Library Entrance": 35,
                              "Admin Entrance": 45, "Canteen": 30},
    "Canteen":              {"Main Gate": 60, "Central Plaza": 30},

    # Library building — Floor 1
    "Library Entrance":     {"Central Plaza": 35, "Library Hallway A": 15},
    "Library Hallway A":    {"Library Entrance": 15, "Room L101": 10,
                              "Room L102": 12, "Staircase L": 8},
    "Room L101":            {"Library Hallway A": 10},
    "Room L102":            {"Library Hallway A": 12},

    # Library building — Floor 2 (via staircase)
    "Staircase L":          {"Library Hallway A": 8, "Library Hallway B": 10},
    "Library Hallway B":    {"Staircase L": 10, "Room L201": 9, "Room L202": 11},
    "Room L201":            {"Library Hallway B": 9},
    "Room L202":            {"Library Hallway B": 11},

    # Admin building — Floor 1
    "Admin Entrance":       {"Central Plaza": 45, "Admin Hallway A": 14},
    "Admin Hallway A":      {"Admin Entrance": 14, "Room A101": 9, "Staircase A": 10},
    "Room A101":            {"Admin Hallway A": 9},

    # Admin building — Floor 2
    "Staircase A":          {"Admin Hallway A": 10, "Admin Hallway B": 9},
    "Admin Hallway B":      {"Staircase A": 9, "Room A201": 8, "Room A202": 10},
    "Room A201":            {"Admin Hallway B": 8},
    "Room A202":            {"Admin Hallway B": 10},
}

FRIENDLY_NAMES = {
    "Room L101": "Room L101 (Reading Hall)",
    "Room L102": "Room L102 (Reference Section)",
    "Room L201": "Room L201 (Digital Library)",
    "Room L202": "Room L202 (Study Pods)",
    "Room A101": "Room A101 (Exam Cell)",
    "Room A201": "Room A201 (Principal's Office)",
    "Room A202": "Room A202 (Accounts Office)",
}


def dijkstra(graph, start, end):
    """Returns (total_distance, path_as_list_of_nodes) for the shortest route."""
    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    visited = set()
    queue = [(0, start)]

    while queue:
        current_dist, current_node = heapq.heappop(queue)
        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == end:
            break

        for neighbor, weight in graph.get(current_node, {}).items():
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    # Reconstruct path
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()

    if distances[end] == float("inf"):
        return None, []  # no route found
    return distances[end], path


def generate_directions(path):
    """Convert a raw node path into human-readable turn-by-turn directions."""
    if not path or len(path) < 2:
        return ["You are already at your destination."]

    directions = [f"Start at {path[0]}."]
    for i in range(1, len(path)):
        prev, curr = path[i - 1], path[i]
        label = FRIENDLY_NAMES.get(curr, curr)

        if "Staircase" in curr:
            directions.append(f"Head to {label} and go up to the next floor.")
        elif "Entrance" in curr:
            directions.append(f"Walk to {label} and enter the building.")
        elif curr.startswith("Room"):
            directions.append(f"Arrive at {label}.")
        else:
            directions.append(f"Continue to {label}.")
    return directions


if __name__ == "__main__":
    print("Campus graph loaded:", len(CAMPUS_GRAPH), "nodes")