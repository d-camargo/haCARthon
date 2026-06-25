#!/usr/bin/env bash
# Gera dados/dados_mapa.js (camadas do mapa Leaflet) a partir dos dados reais do pipeline.
# Pré-requisito: ter baixado os dados:
#   (cd ../../src/pipeline-ingestao && ./baixar.sh PR "Querência do Norte" && ./baixar_assentamentos.sh incra pr)
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$(cd ../.. && pwd)"
IM="$ROOT/data/sicar/imoveis_pr_querencia_do_norte.geojson"
AS="$ROOT/data/assentamentos/assentamentos_pr.geojson"
DB="$(mktemp -u).sqlite"; mkdir -p dados

ogr2ogr -f SQLite -dsco SPATIALITE=YES "$DB" "$IM" -nln imovel -t_srs EPSG:31982 -lco GEOMETRY_NAME=geom -nlt MULTIPOLYGON >/dev/null
ogr2ogr -f SQLite -update "$DB" "$AS" -nln assentamento -t_srs EPSG:31982 -lco GEOMETRY_NAME=geom -nlt MULTIPOLYGON >/dev/null

# imóveis (4674, simplificados) com flag de conflito + área sobreposta
ogr2ogr -f GeoJSON -t_srs EPSG:4674 /tmp/_im.geojson "$DB" -dialect SQLite -sql "
SELECT i.cod_imovel AS cod_imovel, i.municipio AS municipio,
  ROUND(COALESCE(c.sobrep_ha,0),2) AS sobrep_ha,
  CASE WHEN c.sobrep_ha>0 THEN 1 ELSE 0 END AS conflito,
  c.assentamento AS assentamento,
  ST_SimplifyPreserveTopology(ST_MakeValid(i.geom),25) AS geom
FROM imovel i LEFT JOIN (
  SELECT i2.cod_imovel AS cod,
         SUM(ST_Area(ST_Intersection(ST_MakeValid(i2.geom),ST_MakeValid(a.geom)))/10000.0) AS sobrep_ha,
         MAX(a.nome) AS assentamento
  FROM imovel i2, assentamento a
  WHERE ST_Intersects(i2.geom,a.geom)
    AND ST_Area(ST_Intersection(ST_MakeValid(i2.geom),ST_MakeValid(a.geom)))>1000
  GROUP BY i2.cod_imovel) c ON c.cod=i.cod_imovel" >/dev/null

ogr2ogr -f GeoJSON -t_srs EPSG:4674 /tmp/_as.geojson "$AS" -where "municipio LIKE '%QUEREN%'" -nlt MULTIPOLYGON >/dev/null

python3 - <<'PY'
import json
im=json.load(open('/tmp/_im.geojson')); a=json.load(open('/tmp/_as.geojson'))
out='// GERADO por gerar_dados_mapa.sh — dados REAIS (SICAR + INCRA), Querência do Norte/PR.\n'
out+='window.DADOS = '+json.dumps({'imoveis':im,'assentamentos':a},ensure_ascii=False)+';\n'
open('dados/dados_mapa.js','w').write(out)
print('dados/dados_mapa.js gerado:', round(len(out)/1024),'KB')
PY
rm -f "$DB" /tmp/_im.geojson /tmp/_as.geojson
