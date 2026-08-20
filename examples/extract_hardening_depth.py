import math

import cenos_py


def extract_hardening_depth(line_data, surface_point, threshold):
    points = line_data["point_data"]
    temperatures = line_data["field_data"]
    # CENOS returns 0 for points outside the mesh.
    samples = [
        (point, temperature)
        for point, temperature in zip(points, temperatures)
        if temperature != 0
    ]

    if not samples:
        return None

    if samples[0][1] >= threshold:
        for (point_1, temperature_1), (point_2, temperature_2) in zip(samples, samples[1:]):
            if temperature_1 >= threshold > temperature_2:
                fraction = (threshold - temperature_1) / (temperature_2 - temperature_1)
                crossing = tuple(
                    point_1[i] + fraction * (point_2[i] - point_1[i])
                    for i in range(3)
                )
                return math.dist(surface_point, crossing)

        # The whole sampled line is above the threshold.
        return math.dist(surface_point, samples[-1][0])

    for (point_1, temperature_1), (point_2, temperature_2) in zip(samples, samples[1:]):
        if temperature_1 < threshold <= temperature_2:
            fraction = (threshold - temperature_1) / (temperature_2 - temperature_1)
            crossing = tuple(
                point_1[i] + fraction * (point_2[i] - point_1[i]) for i in range(3)
            )
            return math.dist(surface_point, crossing)

    return None


if __name__ == "__main__":
    case = cenos_py.CenosCaseIH("D:/source/cenos")
    case.open("D:/cases/IH/pythonAPI/shaft_scanning")

    lines = [
        ((-0.00824, -0.115, -0.0045), (-0.0075, -0.115, 0.00305)),
        ((-0.00824, -0.105, -0.00483), (-0.0075, -0.105, 0.0031)),
        ((-0.00824, -0.093, -0.00483), (-0.0075, -0.093, 0.0031)),
    ]

    for surface_point, inside_point in lines:
        line_data = case.results.get_max_temperature_over_line(
            5.0, surface_point, inside_point
        )
        depth = extract_hardening_depth(line_data, surface_point, 850.0)