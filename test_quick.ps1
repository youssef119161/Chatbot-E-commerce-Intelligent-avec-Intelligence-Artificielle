# Test Rapide du Projet
Write-Host "🧪 Test Rapide du Projet" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

Set-Location -Path "frontend"

Write-Host ""
Write-Host "🔍 Vérification de la compilation TypeScript..." -ForegroundColor Yellow
npx tsc --noEmit --skipLibCheck

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Pas d'erreurs TypeScript !" -ForegroundColor Green
} else {
    Write-Host "❌ Erreurs TypeScript détectées" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔍 Test de build Angular..." -ForegroundColor Yellow
ng build --configuration development

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Build Angular réussi !" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Tout est prêt ! Vous pouvez démarrer avec :" -ForegroundColor Green
    Write-Host "   .\start_project_final.ps1" -ForegroundColor White
} else {
    Write-Host "❌ Erreurs de build Angular" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 Tentative de correction..." -ForegroundColor Yellow
    
    # Réinstaller les dépendances
    npm install --force
    
    # Réessayer
    ng build --configuration development
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Build réussi après correction !" -ForegroundColor Green
    } else {
        Write-Host "❌ Erreurs persistantes - Vérifiez les logs ci-dessus" -ForegroundColor Red
    }
}