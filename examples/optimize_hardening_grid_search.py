# Manual grid-search version of the hardening optimization tutorial.
import csv
from pathlib import Path

from extract_hardening_depth import extract_hardening_depth
from shaft_scanning_case import get_shaft_scanning_case


TARGET_DEPTH = 0.003  # 3 mm
TEMPERATURE = 850.0
SCAN_DISTANCE = 0.036  # 36 mm
RESULTS_FILE = Path(__file__).resolve().parents[1] / "outputs" / "grid_search_results.csv"

LINES = [
    ((-0.00824, -0.115, -0.0045), (-0.0075, -0.115, 0.00305)),
    ((-0.00824, -0.105, -0.00483), (-0.0075, -0.105, 0.0031)),
    ((-0.00824, -0.093, -0.00483), (-0.0075, -0.093, 0.0031)),
]

RESULTS_FILE.parent.mkdir(exist_ok=True)
with RESULTS_FILE.open("w", newline="") as file:
    csv.writer(file).writerow([
        "process_time_s", "current_a", "average_power_w", "peak_power_w",
        "depth_1_mm", "depth_2_mm", "depth_3_mm", "minimum_depth_mm", "passed",
    ])

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

        powers = case.results.get_active_power()
        print("Depths:", ", ".join(f"{depth * 1000:.2f} mm" for depth in depths))

        passed = min(depths) >= TARGET_DEPTH
        with RESULTS_FILE.open("a", newline="") as file:
            csv.writer(file).writerow([
                process_time, current, sum(powers) / len(powers), max(powers),
                *(depth * 1000 for depth in depths), min(depths) * 1000, passed,
            ])
        case.close()

        if passed:
            print(f"\nBest result: {process_time:.1f} s, {current} A")
            break
    else:
        continue
    break
else:
    print("No tested combination reached 3 mm on all lines.")
