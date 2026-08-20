from __future__ import annotations
import subprocess
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
raise SystemExit(subprocess.call([sys.executable, str(root / "check_installation.py")]))
