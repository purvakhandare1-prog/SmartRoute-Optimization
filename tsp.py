import math


def calculate_distance(lat1, lon1, lat2, lon2):

    return math.sqrt(
        (lat1 - lat2) ** 2 +
        (lon1 - lon2) ** 2
    )


def tsp_dp(locations):

    n = len(locations)

    dist = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):

            if i != j:

                dist[i][j] = calculate_distance(
                    float(locations[i][2]),
                    float(locations[i][3]),
                    float(locations[j][2]),
                    float(locations[j][3])
                )

    memo = {}

    def visit(mask, pos):

        if mask == (1 << n) - 1:
            return dist[pos][0], [0]

        if (mask, pos) in memo:
            return memo[(mask, pos)]

        best_cost = float("inf")
        best_path = []

        for city in range(n):

            if not (mask & (1 << city)):

                cost, path = visit(mask | (1 << city), city)

                cost += dist[pos][city]

                if cost < best_cost:

                    best_cost = cost
                    best_path = [city] + path

        memo[(mask, pos)] = (best_cost, best_path)

        return memo[(mask, pos)]

    minimum_distance, path = visit(1, 0)

    route = []
    ordered_locations = []

    route.append(locations[0][1])
    ordered_locations.append(locations[0])

    for index in path:
        route.append(locations[index][1])
        ordered_locations.append(locations[index])

    return minimum_distance, route, ordered_locations