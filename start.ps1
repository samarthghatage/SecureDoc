$ErrorActionPreference = 'Stop'
if (-not (Get-Command py -ErrorAction SilentlyContinue)) { Write-Error 'Python launcher (py) was not found.' }
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) { Write-Error 'npm was not found. Install Node.js first.' }
if (-not (Test-Path '.venv\Scripts\python.exe')) { Write-Host 'Create the environment first: py -m venv .venv' -ForegroundColor Yellow; exit 1 }
if (-not (Test-Path 'frontend\node_modules')) { Write-Host 'Install frontend dependencies first: cd frontend; npm install' -ForegroundColor Yellow; exit 1 }
Start-Process powershell -ArgumentList '-NoExit','-Command','& .\.venv\Scripts\Activate.ps1; py -m backend.app'
Start-Process powershell -ArgumentList '-NoExit','-Command','cd frontend; npm run dev'
Write-Host 'SecureDoc started: http://127.0.0.1:5173' -ForegroundColor Cyan
