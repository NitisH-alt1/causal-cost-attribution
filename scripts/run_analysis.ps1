Write-Host "`n=== CLOUD ECONOMICS INTELLIGENCE PLATFORM ===" -ForegroundColor Cyan
Write-Host "Starting end-to-end causal cost analysis..." -ForegroundColor White

Write-Host "`n[1/6] Starting Docker services..." -ForegroundColor Yellow
docker compose up -d

Write-Host "`n[2/6] Generating checkout telemetry..." -ForegroundColor Yellow
Invoke-WebRequest `
    -Uri http://localhost:8001/checkout `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"product_id":"product-001","quantity":1,"amount":100.0}' `
    | Out-Null

Write-Host "Telemetry generated." -ForegroundColor Green

Write-Host "`n[3/6] Waiting for distributed trace..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "`n[4/6] Running causal + cost analysis pipeline..." -ForegroundColor Yellow
python -m analyzer.pipeline.run_pipeline

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nPIPELINE FAILED." -ForegroundColor Red
    exit 1
}

Write-Host "`n[5/6] Verifying dashboard..." -ForegroundColor Yellow
Invoke-RestMethod http://localhost:8081/health

Write-Host "`n[6/6] Final analysis result..." -ForegroundColor Yellow
Invoke-RestMethod http://localhost:8081/api/causal-chain | ConvertTo-Json -Depth 10

Write-Host "`n=== ANALYSIS COMPLETE ===" -ForegroundColor Green
Write-Host "Dashboard: http://localhost:8081" -ForegroundColor Cyan
