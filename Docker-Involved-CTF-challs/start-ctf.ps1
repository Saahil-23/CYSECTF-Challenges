# CTF Challenge Manager for Windows PowerShell
param(
    [string]$Command = "start"
)

$ChallengeNetwork = "ctf-network"

switch ($Command.ToLower()) {
    "start" {
        Write-Host "🚀 Starting all CTF challenges..." -ForegroundColor Green
        
        # Create network if it doesn't exist
        docker network create $ChallengeNetwork 2>$null
        
        # Build and start services
        docker compose up -d --build
        
        Write-Host "✅ CTF challenges started!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📋 Running challenges:" -ForegroundColor Yellow
        Write-Host "   🗝️   Key of Three (Chmod): nc localhost 1337" -ForegroundColor White
        Write-Host "   🍪   The Secret Bake (HTTP): http://localhost:5000" -ForegroundColor White
        Write-Host ""
        Write-Host "🛑   Stop with: .\start-ctf.ps1 stop" -ForegroundColor Cyan
        Write-Host "📊   View logs: .\start-ctf.ps1 logs" -ForegroundColor Cyan
    }
    
    "stop" {
        Write-Host "🛑 Stopping all CTF challenges..." -ForegroundColor Yellow
        docker compose down
        docker network rm $ChallengeNetwork 2>$null
        Write-Host "✅ CTF challenges stopped!" -ForegroundColor Green
    }
    
    "status" {
        Write-Host "📊 CTF Challenges Status:" -ForegroundColor Cyan
        docker compose ps
    }
    
    "logs" {
        docker compose logs -f
    }
    
    "restart" {
        .\start-ctf.ps1 stop
        Start-Sleep -Seconds 2
        .\start-ctf.ps1 start
    }
    
    default {
        Write-Host "Usage: .\start-ctf.ps1 [start|stop|status|logs|restart]" -ForegroundColor White
        Write-Host ""
        Write-Host "Commands:" -ForegroundColor Yellow
        Write-Host "  start   - Build and start all challenges" -ForegroundColor White
        Write-Host "  stop    - Stop all challenges" -ForegroundColor White
        Write-Host "  status  - Show status of all containers" -ForegroundColor White
        Write-Host "  logs    - Follow logs from all services" -ForegroundColor White
        Write-Host "  restart - Restart all challenges" -ForegroundColor White
    }
}