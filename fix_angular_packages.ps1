# Script de Correction des Packages Angular
Write-Host "🔧 Correction des Packages Angular Manquants" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Aller dans le dossier frontend
Set-Location -Path "frontend"

Write-Host ""
Write-Host "🧹 Nettoyage complet..." -ForegroundColor Yellow

# Supprimer node_modules et package-lock.json
if (Test-Path "node_modules") {
    Write-Host "🗑️ Suppression de node_modules..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "node_modules"
}

if (Test-Path "package-lock.json") {
    Write-Host "🗑️ Suppression de package-lock.json..." -ForegroundColor Yellow
    Remove-Item -Force "package-lock.json"
}

Write-Host ""
Write-Host "📦 Installation complète des dépendances..." -ForegroundColor Green
npm install

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur avec npm install, essai avec --force..." -ForegroundColor Red
    npm install --force
}

Write-Host ""
Write-Host "🔧 Installation d'Angular DevKit..." -ForegroundColor Green
npm install @angular-devkit/build-angular --save-dev

Write-Host ""
Write-Host "🔧 Installation d'Angular CLI..." -ForegroundColor Green
npm install -g @angular/cli@latest

Write-Host ""
Write-Host "🧪 Test de compilation..." -ForegroundColor Yellow
ng build --configuration development

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Tout est corrigé ! Démarrage d'Angular..." -ForegroundColor Green
    Write-Host "🔗 Application sera disponible sur : http://localhost:4200" -ForegroundColor Cyan
    Write-Host ""
    ng serve --port 4200 --open
} else {
    Write-Host ""
    Write-Host "❌ Il reste des erreurs. Essayons une approche alternative..." -ForegroundColor Red
    Write-Host ""
    Write-Host "🔄 Installation avec legacy-peer-deps..." -ForegroundColor Yellow
    npm install --legacy-peer-deps
    
    Write-Host ""
    Write-Host "🔄 Nouvelle tentative..." -ForegroundColor Yellow
    ng serve --port 4200
}