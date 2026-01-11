@echo off
echo 🚀 Démarrage Final du Projet Chatbot E-commerce
echo ===============================================

echo.
echo 📋 Vérification des prérequis...

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé !
    pause
    exit /b 1
)
echo ✅ Python OK

REM Vérifier Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js n'est pas installé !
    pause
    exit /b 1
)
echo ✅ Node.js OK

echo.
echo 🔧 Démarrage du Backend...
cd backend
start "Backend FastAPI" cmd /k "uvicorn main:app --reload"
echo ✅ Backend démarré sur http://localhost:8000

echo.
echo 🔧 Démarrage du Frontend...
cd ..\frontend

REM Vérifier les dépendances
if not exist node_modules (
    echo 📦 Installation des dépendances...
    npm install
)

REM Démarrer Angular
echo 🌐 Démarrage d'Angular...
start "Frontend Angular" cmd /k "ng serve --port 4200"
echo ✅ Frontend démarré sur http://localhost:4200

echo.
echo 🎉 Projet démarré avec succès !
echo.
echo 📖 Accès aux applications :
echo 🔗 Backend API : http://localhost:8000
echo 📚 Documentation : http://localhost:8000/docs
echo 🌐 Application : http://localhost:4200
echo.
echo 💡 Attendez quelques secondes que les serveurs se lancent
echo 💡 Puis ouvrez http://localhost:4200 dans votre navigateur
echo.
pause