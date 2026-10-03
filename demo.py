from pathfinding_engine import (
    CAMPUS_GRAPH,
    dijkstra,
    generate_directions
)


routes = [

    ("Main Gate", "Room L201"),

    ("Parking Area", "Room A101"),

    ("Room L102", "Room A202"),

    ("Canteen", "Room L101")

]


for start, end in routes:

    print("=" * 60)

    print(
        f"ROUTE: {start} -> {end}"
    )

    print("=" * 60)


    distance, path = dijkstra(
        CAMPUS_GRAPH,
        start,
        end
    )


    if distance is None:

        print("No route found.")

        continue


    print(
        f"Distance: {distance} meters"
    )


    print(
        "Path:",
        " -> ".join(path)
    )


    print("\nDirections:")


    directions = generate_directions(path)


    for number, direction in enumerate(
        directions,
        1
    ):

        print(
            f"{number}. {direction}"
        )


    print()