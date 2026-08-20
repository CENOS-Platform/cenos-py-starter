from __future__ import annotations
import importlib
import importlib.metadata
import json
import platform
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "starter-config.json").read_text(encoding="utf-8"))
CENOS_DISTRIBUTION = "cenos_py"
CENOS_IMPORT = "cenos_py"

def report(label: str, message: str) -> None:
    print(f"[{label}] {message}")

def main() -> int:
    failures = 0
    required = tuple(map(int, CONFIG["python_version"].split(".")))
    print("CENOS Python setup check\n")
    if sys.version_info[:2] == required:
        report("OK", f"Python {platform.python_version()}")
    else:
        report("ERROR", f"Python {platform.python_version()} found; {CONFIG['python_version']}.x required")
        failures += 1
    bits = struct.calcsize("P") * 8
    if bits == 64:
        report("OK", "64-bit Python")
    else:
        report("ERROR", f"{bits}-bit Python found; install 64-bit Python")
        failures += 1
    outputs = ROOT / "outputs"
    outputs.mkdir(exist_ok=True)
    probe = outputs / ".write-test"
    try:
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        report("OK", "Output folder is writable")
    except OSError as exc:
        report("ERROR", f"Output folder is not writable: {exc}")
        failures += 1
    try:
        version = importlib.metadata.version(CENOS_DISTRIBUTION)
        report("OK", f"{CENOS_DISTRIBUTION} {version} is installed")
    except importlib.metadata.PackageNotFoundError:
        report("ERROR", f"{CENOS_DISTRIBUTION} is not installed; rerun setup.cmd")
        failures += 1
    try:
        importlib.import_module(CENOS_IMPORT)
        report("OK", f"Python import '{CENOS_IMPORT}' succeeded")
    except Exception as exc:
        report("ERROR", f"Python import '{CENOS_IMPORT}' failed: {exc}")
        failures += 1
    print("\nEnvironment is ready." if not failures else f"\nFound {failures} blocking problem(s).")
    return int(bool(failures))

if __name__ == "__main__":
    raise SystemExit(main())
