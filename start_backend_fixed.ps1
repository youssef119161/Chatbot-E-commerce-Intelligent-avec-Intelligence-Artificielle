# Script PowerShell Corrigé pour le Backend
Write-Host "🔧 Démarrage Backend FastAPI (Corrigé)" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Aller dans le dossier backend
Set-Location -Path "backend"

Write-Host ""
Write-Host "📋 Vérification de Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python non trouvé !" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📦 Vérification des dépendances..." -ForegroundColor Yellow
pip show fastapi | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "📦 Installation des dépendances..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Erreur d'installation des dépendances" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✅ Dépendances OK" -ForegroundColor Green

Write-Host ""
Write-Host "🚀 Démarrage du serveur FastAPI..." -ForegroundColor Green
Write-Host "🔗 API sera disponible sur : http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 Documentation sur : http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "⏹️  Appuyez sur Ctrl+C pour arrêter" -ForegroundColor Yellow
Write-Host ""

# Essayer différentes méthodes de démarrage
try {
    Write-Host "Méthode 1: python main.py..." -ForegroundColor Blue
    python main.py
} catch {
    try {
        Write-Host "Méthode 2: uvicorn direct..." -ForegroundColor Blue
        uvicorn main:app --reload --host 0.0.0.0 --port 8000
    } catch {
        try {
            Write-Host "Méthode 3: python -m uvicorn..." -ForegroundColor Blue
            python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
        } catch {
            Write-Host "❌ Toutes les méthodes ont échoué" -ForegroundColor Red
            Write-Host "💡 Vérifiez les erreurs ci-dessus" -ForegroundColor Yellow
        }
    }
}