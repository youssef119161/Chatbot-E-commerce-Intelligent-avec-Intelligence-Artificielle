# Script PowerShell Corrigé pour le Frontend
Write-Host "🌐 Démarrage Frontend Angular (Corrigé)" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Aller dans le dossier frontend
Set-Location -Path "frontend"

Write-Host ""
Write-Host "📋 Vérification de Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js non trouvé !" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📦 Vérification des dépendances..." -ForegroundColor Yellow
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installation des dépendances..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Erreur d'installation npm" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✅ Dépendances OK" -ForegroundColor Green

Write-Host ""
Write-Host "🔧 Test de compilation..." -ForegroundColor Yellow
ng build --configuration development
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreurs de compilation détectées" -ForegroundColor Red
    Write-Host "💡 Tentative de correction..." -ForegroundColor Yellow
    npm install --force
    ng build --configuration development
}

Write-Host ""
Write-Host "🚀 Démarrage du serveur Angular..." -ForegroundColor Green
Write-Host "🔗 Application sera disponible sur : http://localhost:4200" -ForegroundColor Cyan
Write-Host "⏹️  Appuyez sur Ctrl+C pour arrêter" -ForegroundColor Yellow
Write-Host ""

# Démarrer Angular
try {
    ng serve --port 4200 --host localhost --open
} catch {
    try {
        Write-Host "Essai avec npx..." -ForegroundColor Blue
        npx ng serve --port 4200 --host localhost --open
    } catch {
        Write-Host "❌ Erreur de démarrage Angular" -ForegroundColor Red
        Write-Host "💡 Vérifiez les erreurs ci-dessus" -ForegroundColor Yellow
    }
}