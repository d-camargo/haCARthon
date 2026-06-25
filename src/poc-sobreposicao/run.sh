#!/usr/bin/env bash
# PoC de sobreposição — executa no PostGIS via Docker (caminho canônico).
# Requer Docker + Docker Compose. Para rodar sem Docker, use ./verificar_local.sh
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p saida

echo ">> Subindo PostGIS..."
docker compose up -d

echo ">> Aguardando o banco ficar pronto..."
until docker compose exec -T db pg_isready -U poc -d poc >/dev/null 2>&1; do sleep 2; done

run() { docker compose exec -T db psql -U poc -d poc -v ON_ERROR_STOP=1 -q -f "/sql/$1"; }

echo ">> 01 schema";   run 01_schema.sql
echo ">> 02 carga";    run 02_carga.sql
echo ">> 03 detecção"; run 03_deteccao.sql

echo ">> Pronto. GeoJSON das sobreposições em ./saida/sobreposicoes.geojson"
echo ">> Para derrubar tudo: docker compose down -v"
