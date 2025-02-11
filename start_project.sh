#!/bin/bash

echo "🚀 Démarrage de l'API FastAPI..."
uvicorn api:app --host 127.0.0.1 --port 8000 --reload &

sleep 3  # Attendre que l'API démarre correctement

echo "🌐 Démarrage du frontend React..."
npm start
