#!/bin/bash

set -e

echo "🚀 Shutting down services..."
docker-compose down --remove-orphans
echo "🚀 Starting services..."
docker-compose up -d --build

echo "⏳ Waiting for Postgres init..."
until docker exec n8n-postgres pg_isready -U n8n -d n8n_auth > /dev/null 2>&1; do
  sleep 1
done

echo "⏳ Pulling llama3.2..."
docker exec -it persona-ollama ollama pull llama3.2

echo "✅ Postgres ready !"
echo "✅ n8n -> http://localhost:5678"
echo "✅ pythonscript -> http://pythonscript:8000"
echo "✅ ollama -> http://ollama:11435"

docker-compose logs -f