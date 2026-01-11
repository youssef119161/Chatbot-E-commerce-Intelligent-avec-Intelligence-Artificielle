# Script PowerShell pour résoudre les problèmes Angular
Write-Host "🔧 Résolution des Problèmes Angular (PowerShell)" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Aller dans le dossier frontend
Set-Location -Path "frontend"

Write-Host ""
Write-Host "🧹 Nettoyage du cache npm..." -ForegroundColor Yellow
npm cache clean --force

Write-Host ""
Write-Host "🗑️ Suppression des node_modules..." -ForegroundColor Yellow
if (Test-Path "node_modules") {
    Remove-Item -Recurse -Force "node_modules"
    Write-Host "✅ node_modules supprimé" -ForegroundColor Green
} else {
    Write-Host "ℹ️ node_modules n'existe pas" -ForegroundColor Blue
}

Write-Host ""
Write-Host "🗑️ Suppression du package-lock.json..." -ForegroundColor Yellow
if (Test-Path "package-lock.json") {
    Remove-Item -Force "package-lock.json"
    Write-Host "✅ package-lock.json supprimé" -ForegroundColor Green
} else {
    Write-Host "ℹ️ package-lock.json n'existe pas" -ForegroundColor Blue
}

Write-Host ""
Write-Host "📦 Réinstallation des dépendances..." -ForegroundColor Yellow
npm install

Write-Host ""
Write-Host "🔧 Vérification d'Angular CLI..." -ForegroundColor Yellow
try {
    ng version
    Write-Host "✅ Angular CLI disponible" -ForegroundColor Green
} catch {
    Write-Host "❌ Angular CLI manquant, installation..." -ForegroundColor Red
    npm install -g @angular/cli
}

Write-Host ""
Write-Host "🚀 Démarrage d'Angular..." -ForegroundColor Green
Write-Host "🔗 L'application sera disponible sur : http://localhost:4200" -ForegroundColor Cyan
Write-Host "⏹️  Appuyez sur Ctrl+C pour arrêter" -ForegroundColor Yellow
Write-Host ""

# Essayer ng serve, sinon npx ng serve
try {
    ng serve --port 4200
} catch {
    Write-Host "❌ Erreur avec ng serve, essai avec npx..." -ForegroundColor Red
    npx ng serve --port 4200
}