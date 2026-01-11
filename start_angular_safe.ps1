# Script PowerShell sécurisé pour démarrer Angular
Write-Host "🚀 Démarrage Sécurisé d'Angular" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green

# Aller dans le dossier frontend
Set-Location -Path "frontend"

Write-Host ""
Write-Host "📋 Vérifications préliminaires..." -ForegroundColor Yellow

# Vérifier Node.js
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js non trouvé !" -ForegroundColor Red
    exit 1
}

# Vérifier npm
try {
    $npmVersion = npm --version
    Write-Host "✅ npm: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm non trouvé !" -ForegroundColor Red
    exit 1
}

# Vérifier les dépendances
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installation des dépendances..." -ForegroundColor Yellow
    npm install
}

Write-Host ""
Write-Host "🔧 Démarrage d'Angular..." -ForegroundColor Cyan

# Essayer différentes méthodes de démarrage
try {
    Write-Host "Méthode 1: ng serve..." -ForegroundColor Blue
    ng serve --port 4200 --host localhost
} catch {
    try {
        Write-Host "Méthode 2: npx ng serve..." -ForegroundColor Blue
        npx ng serve --port 4200 --host localhost
    } catch {
        try {
            Write-Host "Méthode 3: npm start..." -ForegroundColor Blue
            npm start
        } catch {
            Write-Host "❌ Toutes les méthodes ont échoué" -ForegroundColor Red
            Write-Host "💡 Essayez manuellement: ng build puis servez le dossier dist/" -ForegroundColor Yellow
        }
    }
}