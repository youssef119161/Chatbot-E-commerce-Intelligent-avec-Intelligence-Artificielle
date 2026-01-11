@echo off
echo 🚀 Démarrage du Frontend Angular
echo ================================

echo 📍 Changement vers le dossier frontend...
cd /d "%~dp0frontend"

echo 🔍 Vérification de Node.js...
node --version
if %errorlevel% neq 0 (
    echo ❌ Node.js n'est pas installé !
    echo 💡 Installez Node.js depuis https://nodejs.org/
    pause
    exit /b 1
)

echo 🔍 Vérification d'Angular CLI...
ng version
if %errorlevel% neq 0 (
    echo 📦 Installation d'Angular CLI...
    npm install -g @angular/cli
)

echo 🌐 Démarrage du serveur Angular...
echo 🔗 L'application sera disponible sur : http://localhost:4200
echo ⏹️  Appuyez sur Ctrl+C pour arrêter
echo.
ng serve --open

pause