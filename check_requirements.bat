@echo off
echo 🔍 Vérification des Prérequis du Projet
echo =======================================

echo.
echo 📋 Vérification de Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé !
    echo 💡 Installez Python depuis https://python.org/
    set PYTHON_OK=0
) else (
    echo ✅ Python détecté
    set PYTHON_OK=1
)

echo.
echo 📋 Vérification de Node.js...
node --version
if %errorlevel% neq 0 (
    echo ❌ Node.js n'est pas installé !
    echo 💡 Installez Node.js depuis https://nodejs.org/
    set NODE_OK=0
) else (
    echo ✅ Node.js détecté
    set NODE_OK=1
)

echo.
echo 📋 Vérification d'Angular CLI...
ng version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Angular CLI n'est pas installé !
    echo 💡 Installez avec : npm install -g @angular/cli
    set ANGULAR_OK=0
) else (
    echo ✅ Angular CLI détecté
    set ANGULAR_OK=1
)

echo.
echo 📋 Vérification des dépendances Python...
cd backend
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ FastAPI n'est pas installé !
    echo 💡 Installez avec : pip install -r requirements.txt
    set FASTAPI_OK=0
) else (
    echo ✅ FastAPI détecté
    set FASTAPI_OK=1
)

cd ..

echo.
echo 📋 Vérification des dépendances Angular...
cd frontend
if exist node_modules (
    echo ✅ Dépendances Angular installées
    set ANGULAR_DEPS_OK=1
) else (
    echo ❌ Dépendances Angular manquantes !
    echo 💡 Installez avec : npm install
    set ANGULAR_DEPS_OK=0
)

cd ..

echo.
echo ==========================================
echo 📊 RÉSUMÉ DES VÉRIFICATIONS
echo ==========================================
if %PYTHON_OK%==1 echo ✅ Python
if %PYTHON_OK%==0 echo ❌ Python
if %NODE_OK%==1 echo ✅ Node.js
if %NODE_OK%==0 echo ❌ Node.js
if %ANGULAR_OK%==1 echo ✅ Angular CLI
if %ANGULAR_OK%==0 echo ❌ Angular CLI
if %FASTAPI_OK%==1 echo ✅ FastAPI
if %FASTAPI_OK%==0 echo ❌ FastAPI
if %ANGULAR_DEPS_OK%==1 echo ✅ Dépendances Angular
if %ANGULAR_DEPS_OK%==0 echo ❌ Dépendances Angular

echo.
if %PYTHON_OK%==1 if %NODE_OK%==1 if %ANGULAR_OK%==1 if %FASTAPI_OK%==1 if %ANGULAR_DEPS_OK%==1 (
    echo 🎉 Tous les prérequis sont installés !
    echo 🚀 Vous pouvez démarrer le projet !
) else (
    echo ⚠️  Certains prérequis manquent. Installez-les avant de continuer.
)

echo.
pause