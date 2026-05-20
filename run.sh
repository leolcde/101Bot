#!/bin/bash

set -e

echo "🚀 Démarrage des services..."
docker compose down --remove-orphans
docker compose up -d

echo "⏳ Attente que Postgres soit prêt..."
until docker exec n8n-postgres pg_isready -U n8n -d n8n_auth > /dev/null 2>&1; do
  sleep 1
done

echo "✅ Postgres prêt !"
echo "✅ n8n dispo sur http://localhost:5678"
echo "✅ API dispo sur http://localhost:8000"

docker compose logs -f