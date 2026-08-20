from __future__ import annotations
import importlib
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]

def load_cenos_api() -> ModuleType:
    return importlib.import_module("cenos_py")

def connect() -> object:
    api = load_cenos_api()
    raise NotImplementedError(f"CENOS module '{api.__name__}' imported. Implement the connection call in src/cenos_adapter.py.")
