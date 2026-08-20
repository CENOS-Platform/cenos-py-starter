# CENOS Python Starter

One workspace and one local virtual environment for all CENOS Python tutorials.

## Quick start

1. Install the supported 64-bit Python version shown in starter-config.json.
2. Open this folder in File Explorer.
3. Double-click setup.cmd, or run: .\setup.cmd
4. Run: .\run-example.cmd 01_environment_check

The scripts call .venv\Scripts\python.exe directly, so activation is not required.

## Before publishing

Pin `cenos_py` to the tested release in requirements.txt and implement the real connection call once in src/cenos_adapter.py. Tutorial users do not configure the package or import name.

## Structure

- cases/: small input cases
- examples/: numbered tutorials
- outputs/: generated results
- src/: shared CENOS helpers
- setup.cmd: one-command setup
- run-example.cmd: reliable example runner
- check_installation.py: actionable diagnostics

## Commands

    .\setup.cmd
    .\run-example.cmd
    .\run-example.cmd 02_cenos_import
    .\.venv\Scripts\python.exe .\check_installation.py

## VS Code

Open this folder after setup. The included setting selects .venv\Scripts\python.exe.

## Reset

Close programs using .venv, delete only the .venv folder, then run setup.cmd again. Cases and outputs remain untouched.
