#!/usr/bin/env bash
# Pipeline — assentamentos (INCRA), recortados ao município dos imóveis.
#
# IMPORTANTE (verificado em 2026-06-25): a base de Projetos de Assentamento do INCRA
# NÃO tem endpoint aberto/scriptável estável — o Acervo Fundiário exige login e os
# geoservers/i3geo estavam fora do ar. Por isso este script é FONTE-AGNÓSTICO:
#
#   ./baixar_assentamentos.sh local  <arquivo_incra.{shp,zip,gpkg,geojson}> <imoveis.geojson>
#   ./baixar_assentamentos.sh wfs    <imoveis.geojson>     # usa $ASSENT_WFS_URL e $ASSENT_LAYER
#   ./baixar_assentamentos.sh exemplo <imoveis.geojson>    # gera um PA de EXEMPLO p/ demonstrar
#
# Para dados reais: baixe "Assentamento Brasil" do INCRA (Acervo Fundiário, requer login,
# ou dados.gov.br) e use o modo 'local'. Saída sempre em EPSG:4674.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$(cd ../.. && pwd)"
OUT_DIR="$ROOT/data/assentamentos"; mkdir -p "$OUT_DIR"

MODE="${1:?modos: local | wfs | exemplo}"

bbox_de() {  # imprime "xmin ymin xmax ymax" do geojson de imóveis
  python3 - "$1" <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); xs=[];ys=[]
def w(c):
    if isinstance(c[0],(int,float)): xs.append(c[0]); ys.append(c[1])
    else:
        for x in c: w(x)
for f in d['features']: w(f['geometry']['coordinates'])
print(min(xs),min(ys),max(xs),max(ys))
PY
}

case "$MODE" in
  local)
    SRC="${2:?arquivo do INCRA}"; IMOV="${3:?geojson de imóveis (p/ recorte)}"
    read -r xmin ymin xmax ymax < <(bbox_de "$IMOV")
    OUT="$OUT_DIR/assentamentos_recorte.geojson"; rm -f "$OUT"
    ogr2ogr -f GeoJSON "$OUT" "$SRC" -t_srs EPSG:4674 -nlt MULTIPOLYGON \
      -clipdst "$xmin" "$ymin" "$xmax" "$ymax"
    FONTE="INCRA (arquivo local: $(basename "$SRC"))"
    ;;
  wfs)
    IMOV="${2:?geojson de imóveis}"
    : "${ASSENT_WFS_URL:?defina ASSENT_WFS_URL}"; : "${ASSENT_LAYER:?defina ASSENT_LAYER}"
    read -r xmin ymin xmax ymax < <(bbox_de "$IMOV")
    OUT="$OUT_DIR/assentamentos_recorte.geojson"; rm -f "$OUT"
    ogr2ogr -f GeoJSON "$OUT" "WFS:${ASSENT_WFS_URL}" "$ASSENT_LAYER" \
      -t_srs EPSG:4674 -nlt MULTIPOLYGON -spat "$xmin" "$ymin" "$xmax" "$ymax"
    FONTE="INCRA WFS: $ASSENT_WFS_URL ($ASSENT_LAYER)"
    ;;
  exemplo)
    IMOV="${2:?geojson de imóveis}"
    OUT="$OUT_DIR/assentamentos_exemplo.geojson"
    python3 - "$IMOV" "$OUT" <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); xs=[];ys=[]
def w(c):
    if isinstance(c[0],(int,float)): xs.append(c[0]); ys.append(c[1])
    else:
        for x in c: w(x)
for f in d['features']: w(f['geometry']['coordinates'])
xmin,ymin,xmax,ymax=min(xs),min(ys),max(xs),max(ys)
# retângulo central (40% da extensão) para sobrepor vários imóveis reais
dx=(xmax-xmin)*0.3; dy=(ymax-ymin)*0.3
ax0,ax1=xmin+dx,xmax-dx; ay0,ay1=ymin+dy,ymax-dy
fc={"type":"FeatureCollection","name":"assentamentos",
 "crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:EPSG::4674"}},
 "features":[{"type":"Feature","properties":{
   "codigo":"EXEMPLO-PA-01","nome":"PA Exemplo (stand-in)",
   "fonte":"EXEMPLO — substituir pela base real do INCRA"},
   "geometry":{"type":"Polygon","coordinates":[[
     [ax0,ay0],[ax1,ay0],[ax1,ay1],[ax0,ay1],[ax0,ay0]]]}}]}
json.dump(fc,open(sys.argv[2],"w")); print("gerado:",sys.argv[2])
PY
    FONTE="EXEMPLO (stand-in gerado — NÃO é dado real)"
    ;;
  *) echo "modo inválido: $MODE (use local | wfs | exemplo)"; exit 1;;
esac

N="$(python3 -c "import json;print(len(json.load(open('$OUT'))['features']))")"
printf '%s\t%s\t%s feições\t%s\n' "$(date +%F)" "$FONTE" "$N" "$OUT" >> "$OUT_DIR/EXTRACOES.log"
echo ">> OK: $N feições -> $OUT  [$FONTE]"
