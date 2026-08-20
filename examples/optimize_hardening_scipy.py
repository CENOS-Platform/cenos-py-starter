from scipy.optimize import brentq

from extract_hardening_depth import extract_hardening_depth
from shaft_scanning_case import get_shaft_scanning_case


TARGET_DEPTH = 0.003  # 3 mm
TEMPERATURE = 850.0
CURRENT = 4000
SCAN_DISTANCE = 0.036  # 36 mm

LINES = [
    ((-0.00824, -0.115, -0.0045), (-0.0075, -0.115, 0.00305)),
    ((-0.00824, -0.105, -0.00483), (-0.0075, -0.105, 0.0031)),
    ((-0.00824, -0.093, -0.00483), (-0.0075, -0.093, 0.0031)),
]


def minimum_depth(process_time):
    velocity = SCAN_DISTANCE / process_time
    case = get_shaft_scanning_case(CURRENT, velocity, process_time)
    case.calculate()

    depths = []
    for surface_point, inside_point in LINES:
        line_data = case.results.get_max_temperature_over_line(
            process_time, surface_point, inside_point
        )
        depth = extract_hardening_depth(line_data, surface_point, TEMPERATURE)
        depths.append(0.0 if depth is None else depth)

    case.close()
    print(f"{process_time:.2f} s -> " + ", ".join(f"{d * 1000:.2f} mm" for d in depths))
    return min(depths)


# The fastest valid process is where the minimum depth reaches exactly 3 mm.
fastest_time = brentq(
    lambda process_time: minimum_depth(process_time) - TARGET_DEPTH,
    2.0,
    5.0,
    xtol=0.05,
)

print(f"\nFastest process: {fastest_time:.2f} s at {CURRENT} A")
