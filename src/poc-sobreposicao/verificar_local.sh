#!/usr/bin/env bash
# Verificação SEM Docker, usando GDAL/Spatialite (mesmas funções ST_* do PostGIS).
# Reprojeta para EPSG:31982 (UTM 22S, metros) para medir área diretamente em m².
# Útil para validar a lógica espacial rapidamente; o caminho canônico é ./run.sh (PostGIS).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p saida
DB=saida/poc.sqlite
rm -f "$DB"

echo ">> Carregando dados (reprojetando 4674 -> 31982 / metros)..."
ogr2ogr -f SQLite -dsco SPATIALITE=YES "$DB" dados/imoveis_car.geojson \
  -nln imovel_car -t_srs EPSG:31982 -lco GEOMETRY_NAME=geom >/dev/null
ogr2ogr -f SQLite -update "$DB" dados/assentamentos.geojson \
  -nln assentamento -t_srs EPSG:31982 -lco GEOMETRY_NAME=geom >/dev/null

echo
echo "== (1) Imóvel CAR x Assentamento (INCRA) =="
ogrinfo -ro -q "$DB" -dialect SQLite -sql "
  SELECT i.cod_imovel, i.nome AS imovel, a.nome AS assentamento,
         ROUND(ST_Area(ST_Intersection(i.geom,a.geom))/10000.0, 2) AS sobrep_ha,
         ROUND(100.0*ST_Area(ST_Intersection(i.geom,a.geom))/ST_Area(i.geom), 1) AS sobrep_pct
  FROM imovel_car i, assentamento a
  WHERE ST_Intersects(i.geom,a.geom)
  ORDER BY sobrep_ha DESC"

echo "== (2) Imóvel CAR x Imóvel CAR =="
ogrinfo -ro -q "$DB" -dialect SQLite -sql "
  SELECT a.cod_imovel AS imovel_a, b.cod_imovel AS imovel_b,
         ROUND(ST_Area(ST_Intersection(a.geom,b.geom))/10000.0, 2) AS sobrep_ha
  FROM imovel_car a, imovel_car b
  WHERE a.cod_imovel < b.cod_imovel AND ST_Intersects(a.geom,b.geom)
  ORDER BY sobrep_ha DESC"

echo ">> Exportando camada de sobreposições para saida/sobreposicoes.geojson (EPSG:4674)..."
rm -f saida/sobreposicoes.geojson
ogr2ogr -f GeoJSON -t_srs EPSG:4674 saida/sobreposicoes.geojson "$DB" -dialect SQLite -sql "
  SELECT i.cod_imovel AS imovel, a.nome AS contra, 'assentamento' AS tipo,
         ROUND(ST_Area(ST_Intersection(i.geom,a.geom))/10000.0, 2) AS sobrep_ha,
         ST_Intersection(i.geom,a.geom) AS geom
  FROM imovel_car i, assentamento a
  WHERE ST_Intersects(i.geom,a.geom)" >/dev/null
echo ">> OK."
