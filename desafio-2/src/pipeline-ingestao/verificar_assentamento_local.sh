#!/usr/bin/env bash
# Detecção CAR x Assentamento sobre dados reais, SEM Docker (GDAL/Spatialite).
# Uso: ./verificar_assentamento_local.sh <imoveis.geojson> <assentamentos.geojson> [tol_m2]
set -euo pipefail
cd "$(dirname "$0")"

IMOV="${1:?uso: ./verificar_assentamento_local.sh <imoveis.geojson> <assentamentos.geojson> [tol_m2]}"
ASS="${2:?informe o geojson de assentamentos}"
TOL="${3:-100}"
DB="$(mktemp -u).sqlite"

ogr2ogr -f SQLite -dsco SPATIALITE=YES "$DB" "$IMOV" \
  -nln imovel -t_srs EPSG:31982 -lco GEOMETRY_NAME=geom -nlt MULTIPOLYGON >/dev/null
ogr2ogr -f SQLite -update "$DB" "$ASS" \
  -nln assentamento -t_srs EPSG:31982 -lco GEOMETRY_NAME=geom -nlt MULTIPOLYGON >/dev/null

echo "== Imóveis x Assentamentos =="
ogrinfo -ro -q "$DB" -dialect SQLite -sql "
  SELECT i.cod_imovel AS imovel, a.nome AS assentamento,
         ROUND(ST_Area(ST_Intersection(ST_MakeValid(i.geom),ST_MakeValid(a.geom)))/10000.0,3) AS sobrep_ha,
         ROUND(100.0*ST_Area(ST_Intersection(ST_MakeValid(i.geom),ST_MakeValid(a.geom)))/ST_Area(i.geom),1) AS pct_imovel
  FROM imovel i, assentamento a
  WHERE ST_Intersects(i.geom,a.geom)
    AND ST_Area(ST_Intersection(ST_MakeValid(i.geom),ST_MakeValid(a.geom))) > ${TOL}
  ORDER BY sobrep_ha DESC LIMIT 20"

echo "== Total de imóveis que sobrepõem assentamento =="
ogrinfo -ro -q "$DB" -dialect SQLite -sql "
  SELECT COUNT(DISTINCT i.cod_imovel) AS imoveis_em_conflito
  FROM imovel i, assentamento a
  WHERE ST_Intersects(i.geom,a.geom)
    AND ST_Area(ST_Intersection(ST_MakeValid(i.geom),ST_MakeValid(a.geom))) > ${TOL}"

rm -f "$DB"
