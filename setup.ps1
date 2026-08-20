[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$config = Get-Content -LiteralPath (Join-Path $root 'starter-config.json') -Raw | ConvertFrom-Json
$version = [string]$config.python_version
$python = Join-Path $root '.venv\Scripts\python.exe'
try {
    Write-Host 'CENOS Python Starter setup' -ForegroundColor Cyan
    $launcher = Get-Command py.exe -ErrorAction SilentlyContinue
    if (-not $launcher) { throw "Install 64-bit Python $version with the Python Launcher." }
    if (-not (Test-Path -LiteralPath $python)) {
        Write-Host 'Creating .venv...' -ForegroundColor Yellow
        & $launcher.Source "-$version" -m venv (Join-Path $root '.venv')
        if ($LASTEXITCODE -ne 0) { throw 'Could not create .venv. Run: py --list' }
    } else { Write-Host 'Reusing existing .venv.' -ForegroundColor Green }
    & $python -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) { throw 'pip upgrade failed.' }
    & $python -m pip install -r (Join-Path $root 'requirements.txt')
    if ($LASTEXITCODE -ne 0) { throw 'Package installation failed.' }
    & $python (Join-Path $root 'check_installation.py')
    if ($LASTEXITCODE -ne 0) { throw 'Installation check reported an error.' }
    Write-Host 'Setup complete.' -ForegroundColor Green
    Write-Host 'Next: .\run-example.cmd 01_environment_check' -ForegroundColor Cyan
    exit 0
} catch {
    Write-Host "[ERROR] $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
