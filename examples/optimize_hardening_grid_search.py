# Manual grid-search version of the hardening optimization tutorial.
from extract_hardening_depth import extract_hardening_depth
from shaft_scanning_case import get_shaft_scanning_case


TARGET_DEPTH = 0.003  # 3 mm
TEMPERATURE = 850.0
SCAN_DISTANCE = 0.036  # 36 mm

LINES = [
    ((-0.00824, -0.115, -0.0045), (-0.0075, -0.115, 0.00305)),
    ((-0.00824, -0.105, -0.00483), (-0.0075, -0.105, 0.0031)),
    ((-0.00824, -0.093, -0.00483), (-0.0075, -0.093, 0.0031)),
]

# Try the fastest times first. Current has no optimization penalty in this tutorial.
for process_time in [2.0, 3.0, 4.0, 5.0]:
    velocity = SCAN_DISTANCE / process_time

    for current in [2000, 2500, 3000, 3500, 4000]:
        print(f"Trying {process_time:.1f} s, {current} A...")

        case = get_shaft_scanning_case(current, velocity, process_time)
        case.calculate()

        depths = []
        for surface_point, inside_point in LINES:
            line_data = case.results.get_max_temperature_over_line(
                process_time, surface_point, inside_point
            )
            depth = extract_hardening_depth(line_data, surface_point, TEMPERATURE)
            depths.append(0.0 if depth is None else depth)

        print("Depths:", ", ".join(f"{depth * 1000:.2f} mm" for depth in depths))

        passed = min(depths) >= TARGET_DEPTH
        case.close()

        if passed:
            print(f"\nBest result: {process_time:.1f} s, {current} A")
            break
    else:
        continue
    break
else:
    print("No tested combination reached 3 mm on all lines.")
