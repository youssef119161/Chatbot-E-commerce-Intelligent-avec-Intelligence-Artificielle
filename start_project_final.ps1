# Script PowerShell Final pour Démarrer le Projet
Write-Host "🚀 Démarrage Final du Projet Chatbot E-commerce" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green

Write-Host ""
Write-Host "📋 Vérification des prérequis..." -ForegroundColor Yellow

# Vérifier Python
try {
    $pythonVersion = python --version
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python n'est pas installé !" -ForegroundColor Red
    exit 1
}

# Vérifier Node.js
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js n'est pas installé !" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔧 Démarrage du Backend..." -ForegroundColor Cyan

# Démarrer le backend en arrière-plan
Set-Location -Path "backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "uvicorn main:app --reload" -WindowStyle Normal
Write-Host "✅ Backend démarré sur http://localhost:8000" -ForegroundColor Green

Write-Host ""
Write-Host "🔧 Démarrage du Frontend..." -ForegroundColor Cyan

# Aller dans le dossier frontend
Set-Location -Path "../frontend"

# Vérifier les dépendances
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installation des dépendances..." -ForegroundColor Yellow
    npm install
}

Write-Host "🌐 Démarrage d'Angular..." -ForegroundColor Blue

# Démarrer Angular
try {
    ng serve --port 4200 --open
} catch {
    Write-Host "❌ Erreur avec ng serve, essai avec npx..." -ForegroundColor Red
    npx ng serve --port 4200 --open
}

Write-Host ""
Write-Host "🎉 Projet démarré avec succès !" -ForegroundColor Green
Write-Host ""
Write-Host "📖 Accès aux applications :" -ForegroundColor Cyan
Write-Host "🔗 Backend API : http://localhost:8000" -ForegroundColor White
Write-Host "📚 Documentation : http://localhost:8000/docs" -ForegroundColor White
Write-Host "🌐 Application : http://localhost:4200" -ForegroundColor White
Write-Host ""
Write-Host "💡 Si l'application ne s'ouvre pas automatiquement," -ForegroundColor Yellow
Write-Host "💡 ouvrez http://localhost:4200 dans votre navigateur" -ForegroundColor Yellow