#!/usr/bin/env bash
# Pipeline — verificação SEM Docker (GDAL/Spatialite). Mesmas funções ST_* do PostGIS.
# Reprojeta para EPSG:31982 (UTM 22S) para medir área em metros.
# Uso: ./verificar_local.sh <caminho_geojson> [tolerancia_m2]
#   ex.: ./verificar_local.sh ../../data/sicar/imoveis_pr_itaguaje.geojson 100
set -euo pipefail
cd "$(dirname "$0")"

GJ="${1:?uso: ./verificar_local.sh <caminho_geojson> [tolerancia_m2]}"
TOL="${2:-100}"
DB="$(mktemp -u).sqlite"

ogr2ogr -f SQLite -dsco SPATIALITE=YES "$DB" "$GJ" \
  -nln imovel -t_srs EPSG:31982 -lco GEOMETRY_NAME=geom -nlt MULTIPOLYGON >/dev/null

echo "== Imóveis carregados =="
ogrinfo -ro -q "$DB" -dialect SQLite -sql "SELECT COUNT(*) AS n FROM imovel"

echo "== Top 15 sobreposições CAR x CAR (> ${TOL} m²) =="
ogrinfo -ro -q "$DB" -dialect SQLite -sql "
  SELECT a.cod_imovel AS imovel_a, b.cod_imovel AS imovel_b,
         ROUND(ST_Area(ST_Intersection(ST_MakeValid(a.geom),ST_MakeValid(b.geom)))/10000.0,3) AS sobrep_ha
  FROM imovel a, imovel b
  WHERE a.cod_imovel < b.cod_imovel AND ST_Intersects(a.geom,b.geom)
    AND ST_Area(ST_Intersection(ST_MakeValid(a.geom),ST_MakeValid(b.geom))) > ${TOL}
  ORDER BY sobrep_ha DESC LIMIT 15"

echo "== Total de pares conflitantes (dimensiona o problema) =="
ogrinfo -ro -q "$DB" -dialect SQLite -sql "
  SELECT COUNT(*) AS pares_conflito FROM imovel a, imovel b
  WHERE a.cod_imovel < b.cod_imovel AND ST_Intersects(a.geom,b.geom)
    AND ST_Area(ST_Intersection(ST_MakeValid(a.geom),ST_MakeValid(b.geom))) > ${TOL}"

rm -f "$DB"
