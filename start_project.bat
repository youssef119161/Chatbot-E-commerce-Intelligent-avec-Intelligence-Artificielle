@echo off
echo 🚀 Démarrage du projet Chatbot E-commerce
echo ==========================================

echo.
echo 📋 Vérification des prérequis...

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    pause
    exit /b 1
)
echo ✅ Python détecté

REM Vérifier Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js n'est pas installé ou pas dans le PATH
    pause
    exit /b 1
)
echo ✅ Node.js détecté

echo.
echo 🔧 Installation des dépendances...

REM Installer les dépendances Python
echo 📦 Installation des dépendances Python...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Erreur lors de l'installation des dépendances Python
    pause
    exit /b 1
)
echo ✅ Dépendances Python installées

cd ..

REM Installer les dépendances Angular
echo 📦 Installation des dépendances Angular...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ❌ Erreur lors de l'installation des dépendances Angular
    pause
    exit /b 1
)
echo ✅ Dépendances Angular installées

cd ..

echo.
echo 🎉 Installation terminée avec succès !
echo.
echo 📖 Instructions de démarrage :
echo.
echo 1. Backend FastAPI :
echo    cd backend
echo    uvicorn main:app --reload
echo    API disponible sur : http://localhost:8000
echo    Documentation : http://localhost:8000/docs
echo.
echo 2. Frontend Angular :
echo    cd frontend  
echo    ng serve
echo    Application disponible sur : http://localhost:4200
echo.
echo 💡 Conseil : Ouvrez 2 terminaux pour démarrer les deux serveurs
echo.
pause