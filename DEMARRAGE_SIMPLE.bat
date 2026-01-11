@echo off
title Chatbot E-commerce - Demarrage
color 0A

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                    CHATBOT E-COMMERCE                        ║
echo  ║                   Demarrage Automatique                      ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 Demarrage du projet...
echo.

REM Demarrer le backend
echo 📡 Lancement du Backend FastAPI...
cd backend
start "Backend - FastAPI" cmd /k "echo Backend FastAPI && echo ================== && uvicorn main:app --reload"

REM Attendre 3 secondes
timeout /t 3 /nobreak >nul

REM Demarrer le frontend
echo 🌐 Lancement du Frontend Angular...
cd ..\frontend
start "Frontend - Angular" cmd /k "echo Frontend Angular && echo =================== && ng serve --open"

echo.
echo ✅ Projet demarre !
echo.
echo 📖 Acces aux applications :
echo    🔗 Backend API : http://localhost:8000
echo    📚 Documentation : http://localhost:8000/docs  
echo    🌐 Application : http://localhost:4200
echo.
echo 💡 Attendez quelques secondes que tout se charge...
echo 💡 L'application s'ouvrira automatiquement dans votre navigateur
echo.
echo ⏹️  Fermez cette fenetre quand vous avez fini
pause