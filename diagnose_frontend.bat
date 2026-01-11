@echo off
echo 🔍 Diagnostic Frontend Angular
echo ==============================

echo.
echo 📍 Changement vers le dossier frontend...
cd /d "%~dp0frontend"

echo.
echo 📋 Informations système...
echo Node.js version:
node --version
echo.
echo npm version:
npm --version
echo.

echo 📋 Vérification des fichiers Angular...
if exist package.json (
    echo ✅ package.json trouvé
) else (
    echo ❌ package.json manquant !
)

if exist angular.json (
    echo ✅ angular.json trouvé
) else (
    echo ❌ angular.json manquant !
)

if exist node_modules (
    echo ✅ node_modules existe
) else (
    echo ❌ node_modules manquant - Exécutez: npm install
)

echo.
echo 📋 Vérification d'Angular CLI...
ng version
if %errorlevel% neq 0 (
    echo ❌ Angular CLI non disponible
    echo 💡 Installez avec: npm install -g @angular/cli
) else (
    echo ✅ Angular CLI disponible
)

echo.
echo 📋 Test de compilation...
ng build --configuration development --verbose
if %errorlevel% neq 0 (
    echo ❌ Erreurs de compilation détectées !
    echo 💡 Vérifiez les erreurs ci-dessus
) else (
    echo ✅ Compilation réussie !
)

echo.
echo 📋 Résumé du diagnostic terminé
pause