@echo off
echo 🔧 Résolution des Problèmes Angular
echo ===================================

echo.
echo 📍 Changement vers le dossier frontend...
cd /d "%~dp0frontend"

echo.
echo 🔍 Diagnostic des problèmes...

echo.
echo 📋 Vérification de Node.js...
node --version
if %errorlevel% neq 0 (
    echo ❌ Node.js n'est pas installé !
    echo 💡 Installez Node.js depuis https://nodejs.org/
    pause
    exit /b 1
)

echo.
echo 📋 Vérification de npm...
npm --version
if %errorlevel% neq 0 (
    echo ❌ npm n'est pas disponible !
    pause
    exit /b 1
)

echo.
echo 🧹 Nettoyage du cache npm...
npm cache clean --force

echo.
echo 🗑️ Suppression des node_modules...
if exist node_modules (
    rmdir /s /q node_modules
    echo ✅ node_modules supprimé
) else (
    echo ℹ️ node_modules n'existe pas
)

echo.
echo 🗑️ Suppression du package-lock.json...
if exist package-lock.json (
    del package-lock.json
    echo ✅ package-lock.json supprimé
) else (
    echo ℹ️ package-lock.json n'existe pas
)

echo.
echo 📦 Réinstallation des dépendances...
npm install
if %errorlevel% neq 0 (
    echo ❌ Erreur lors de l'installation !
    echo 💡 Essayez manuellement : npm install --legacy-peer-deps
    pause
    exit /b 1
)

echo.
echo 🔧 Installation d'Angular CLI globalement...
npm install -g @angular/cli@latest
if %errorlevel% neq 0 (
    echo ⚠️ Impossible d'installer Angular CLI globalement
    echo 💡 Continuons avec la version locale...
)

echo.
echo ✅ Nettoyage terminé !
echo.
echo 🚀 Tentative de démarrage d'Angular...
echo 🔗 L'application sera disponible sur : http://localhost:4200
echo ⏹️  Appuyez sur Ctrl+C pour arrêter
echo.

ng serve --port 4200 --host 0.0.0.0
if %errorlevel% neq 0 (
    echo.
    echo ❌ Erreur avec ng serve !
    echo 💡 Essayons avec npx...
    npx ng serve --port 4200 --host 0.0.0.0
)

pause