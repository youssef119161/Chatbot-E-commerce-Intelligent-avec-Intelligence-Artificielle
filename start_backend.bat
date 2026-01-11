@echo off
echo 🚀 Démarrage du Backend FastAPI
echo ===============================

cd backend

echo 📡 Lancement du serveur FastAPI...
echo 🔗 API : http://localhost:8000
echo 📚 Documentation : http://localhost:8000/docs
echo.
echo ⏹️  Appuyez sur Ctrl+C pour arrêter le serveur
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000