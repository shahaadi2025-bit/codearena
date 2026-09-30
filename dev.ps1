# Starts the backend (port 4000) and frontend (port 3000) in two PowerShell windows.
# Run from the repo root:  powershell -ExecutionPolicy Bypass -File .\dev.ps1
Start-Process powershell -ArgumentList '-NoExit', '-Command', "Set-Location '$PSScriptRoot\backend'; npm run dev"
Start-Process powershell -ArgumentList '-NoExit', '-Command', "Set-Location '$PSScriptRoot\frontend'; npm run dev"
Write-Host "Backend:  http://localhost:4000/health"
Write-Host "Frontend: http://localhost:3000"
