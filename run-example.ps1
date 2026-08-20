[CmdletBinding()]
param([Parameter(Position = 0)][string]$Example)
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$python = Join-Path $root '.venv\Scripts\python.exe'
$examples = Join-Path $root 'examples'
if (-not (Test-Path -LiteralPath $python)) { Write-Host '[ERROR] .venv was not found. Run setup.cmd first.' -ForegroundColor Red; exit 1 }
$available = @(Get-ChildItem -LiteralPath $examples -Filter '*.py' | Sort-Object Name)
if ([string]::IsNullOrWhiteSpace($Example)) {
    Write-Host 'Available examples:' -ForegroundColor Cyan
    foreach ($item in $available) { Write-Host "  $($item.BaseName)" }
    Write-Host 'Usage: .\run-example.cmd 01_environment_check'
    exit 0
}
if (-not $Example.EndsWith('.py')) { $Example += '.py' }
$script = Join-Path $examples $Example
if (-not (Test-Path -LiteralPath $script)) { Write-Host "[ERROR] Example '$Example' was not found." -ForegroundColor Red; exit 1 }
$env:PYTHONPATH = $root
Push-Location $root
try { & $python $script; exit $LASTEXITCODE } finally { Pop-Location }
