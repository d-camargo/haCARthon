#!/usr/bin/env bash
# Pipeline — passo 2: CARREGAR o GeoJSON no PostGIS e rodar a detecção (caminho canônico).
# Requer um PostGIS acessível. O jeito mais simples é reusar o compose da PoC:
#     (cd ../poc-sobreposicao && docker compose up -d)
# Uso: ./carregar.sh <caminho_geojson>
#   ex.: ./carregar.sh ../../data/sicar/imoveis_pr_itaguaje.geojson
set -euo pipefail
cd "$(dirname "$0")"

GJ="${1:?uso: ./carregar.sh <caminho_geojson>}"
PGCONN="${PGCONN:-PG:host=localhost port=5432 dbname=poc user=poc password=poc}"
PSQL=(docker compose -f ../poc-sobreposicao/docker-compose.yml exec -T db psql -U poc -d poc -v ON_ERROR_STOP=1)

echo ">> Carregando $GJ no PostGIS (reprojetando para 4674, geometria MULTI)..."
ogr2ogr -f PostgreSQL "$PGCONN" "$GJ" \
  -nln imovel_car -t_srs EPSG:4674 -nlt MULTIPOLYGON \
  -lco GEOMETRY_NAME=geom -lco FID=ogc_fid -overwrite

echo ">> Saneando geometrias e criando índice..."
"${PSQL[@]}" -q -f /sql/10_schema_real.sql 2>/dev/null \
  || "${PSQL[@]}" -q < sql/10_schema_real.sql

echo ">> Rodando detecção..."
mkdir -p saida
"${PSQL[@]}" -q < sql/11_deteccao_car.sql

echo ">> GeoJSON das sobreposições reais em ./saida/sobreposicoes_reais.geojson"
