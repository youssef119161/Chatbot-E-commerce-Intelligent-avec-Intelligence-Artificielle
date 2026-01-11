# Script PowerShell pour corriger toutes les erreurs Angular
Write-Host "🔧 Correction Automatique des Erreurs Angular" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Aller dans le dossier frontend
Set-Location -Path "frontend"

Write-Host ""
Write-Host "🔍 Vérification des erreurs TypeScript..." -ForegroundColor Yellow

# Compiler pour voir les erreurs
Write-Host "📋 Compilation TypeScript..." -ForegroundColor Yellow
npx tsc --noEmit

Write-Host ""
Write-Host "🔧 Tentative de build Angular..." -ForegroundColor Yellow
ng build --configuration development

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Build réussi ! Démarrage du serveur..." -ForegroundColor Green
    ng serve --port 4200
} else {
    Write-Host "❌ Erreurs de build détectées" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 Tentatives de correction..." -ForegroundColor Yellow
    
    # Installer les dépendances manquantes
    Write-Host "📦 Installation des dépendances Angular..." -ForegroundColor Yellow
    npm install @angular/common @angular/core @angular/forms @angular/platform-browser @angular/router
    
    # Réessayer le build
    Write-Host "🔄 Nouvelle tentative de build..." -ForegroundColor Yellow
    ng build --configuration development
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Build réussi après correction ! Démarrage..." -ForegroundColor Green
        ng serve --port 4200
    } else {
        Write-Host "❌ Erreurs persistantes. Affichage des détails..." -ForegroundColor Red
        ng serve --verbose
    }
}