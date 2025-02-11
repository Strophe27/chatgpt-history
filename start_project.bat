@echo off
echo 🚀 Démarrage de l'API FastAPI...
start cmd /k "uvicorn api:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 4 >nul

echo 🌐 Démarrage du frontend React...
start cmd /k "npm start"
