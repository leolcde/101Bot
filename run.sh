#!/bin/bash

set -e

# Prefer Docker Compose v2 plugin when available.
if docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD="docker compose"
  COMPOSE_V2=true
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD="docker-compose"
  COMPOSE_V2=false
else
  echo "❌ Docker Compose introuvable (ni 'docker compose' ni 'docker-compose')."
  exit 1
fi

echo "ℹ️ Compose utilisé: $COMPOSE_CMD"

echo "🚀 Shutting down services..."
$COMPOSE_CMD down --remove-orphans
echo "🚀 Starting services..."
$COMPOSE_CMD up -d --build

echo "⏳ Waiting for Postgres init..."
until docker exec n8n-postgres pg_isready -U n8n -d n8n_auth > /dev/null 2>&1; do
  sleep 1
done

echo "⏳ Pulling llama3.2:3b.."
docker exec -it persona-ollama ollama pull llama3.2:3b

echo "✅ Postgres ready !"
echo "✅ n8n -> http://localhost:5678"
echo "✅ pythonscript -> http://pythonscript:8000"
echo "✅ ollama -> http://ollama:11435"

if [ "$COMPOSE_V2" = true ]; then
  $COMPOSE_CMD logs -f
else
  echo "⚠️ Compose v1 détecté: 'logs -f' peut planter avec KeyError: 'id'."
  echo "⚠️ Affichage des derniers logs sans suivi temps réel."
  $COMPOSE_CMD logs --tail=200
fi