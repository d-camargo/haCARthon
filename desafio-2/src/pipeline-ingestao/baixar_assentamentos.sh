#!/usr/bin/env bash
# Pipeline — assentamentos (INCRA). Saída sempre em EPSG:4674, com campo `nome` padronizado.
#
# Modos:
#   ./baixar_assentamentos.sh incra   <uf>                       # INCRA i3geo WFS (RECOMENDADO)
#   ./baixar_assentamentos.sh local   <arquivo.{shp,zip,gpkg,geojson}> <imoveis.geojson>
#   ./baixar_assentamentos.sh exemplo <imoveis.geojson>          # stand-in p/ demonstrar
#
# Fonte (verificada em 2026-06-25, via Acervo Fundiário do INCRA):
#   https://acervofundiario.incra.gov.br/i3geo/ogc.php?tema=assentamentos_<uf>
#   MapServer WFS 1.0.0. ⚠️ Devolve coordenadas em ordem lat,lon — este script CORRIGE o eixo.
#   Campos reais: nome_projeto, municipio, num_familias, fase, area_hectare_declarada, cd_sipra...
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$(cd ../.. && pwd)"
OUT_DIR="$ROOT/data/assentamentos"; mkdir -p "$OUT_DIR"

MODE="${1:?modos: incra | local | exemplo}"

bbox_de() {
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
  incra)
    UF="${2:?uso: ./baixar_assentamentos.sh incra <uf>}"
    ufl="$(echo "$UF" | tr 'A-Z' 'a-z')"
    OUT="$OUT_DIR/assentamentos_${ufl}.geojson"
    TMP="$(mktemp -u).geojson"
    URL="https://acervofundiario.incra.gov.br/i3geo/ogc.php?tema=assentamentos_${ufl}"
    echo ">> Baixando assentamentos do INCRA (i3geo WFS) — ${UF}..."
    ogr2ogr -f GeoJSON "$TMP" "WFS:${URL}" "assentamentos_${ufl}" >/dev/null
    # Corrige eixo (lat,lon -> lon,lat), padroniza `nome`/`fonte` e fixa CRS 4674.
    python3 - "$TMP" "$OUT" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
def sw(c):
    return [c[1],c[0]] if isinstance(c[0],(int,float)) else [sw(x) for x in c]
for f in d['features']:
    f['geometry']['coordinates']=sw(f['geometry']['coordinates'])
    p=f['properties']; p['nome']=p.get('nome_projeto'); p['fonte']='INCRA (i3geo Acervo Fundiário)'
d['crs']={'type':'name','properties':{'name':'urn:ogc:def:crs:EPSG::4674'}}
json.dump(d,open(sys.argv[2],'w'))
PY
    rm -f "$TMP"
    FONTE="INCRA i3geo (assentamentos_${ufl}, eixo corrigido)"
    ;;
  local)
    SRC="${2:?arquivo do INCRA}"; IMOV="${3:?geojson de imóveis (p/ recorte)}"
    read -r xmin ymin xmax ymax < <(bbox_de "$IMOV")
    OUT="$OUT_DIR/assentamentos_recorte.geojson"; rm -f "$OUT"
    ogr2ogr -f GeoJSON "$OUT" "$SRC" -t_srs EPSG:4674 -nlt MULTIPOLYGON \
      -clipdst "$xmin" "$ymin" "$xmax" "$ymax"
    # padroniza `nome` se houver nome_projeto
    python3 - "$OUT" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
for f in d['features']:
    p=f['properties']; p.setdefault('nome', p.get('nome_projeto') or p.get('nome'))
json.dump(d,open(sys.argv[1],'w'))
PY
    FONTE="INCRA (arquivo local: $(basename "$SRC"))"
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
dx=(xmax-xmin)*0.3; dy=(ymax-ymin)*0.3
ax0,ax1=xmin+dx,xmax-dx; ay0,ay1=ymin+dy,ymax-dy
fc={"type":"FeatureCollection","name":"assentamentos",
 "crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:EPSG::4674"}},
 "features":[{"type":"Feature","properties":{
   "nome":"PA Exemplo (stand-in)","fonte":"EXEMPLO — substituir pela base real do INCRA"},
   "geometry":{"type":"Polygon","coordinates":[[
     [ax0,ay0],[ax1,ay0],[ax1,ay1],[ax0,ay1],[ax0,ay0]]]}}]}
json.dump(fc,open(sys.argv[2],"w")); print("gerado:",sys.argv[2])
PY
    FONTE="EXEMPLO (stand-in gerado — NÃO é dado real)"
    ;;
  *) echo "modo inválido: $MODE (use incra | local | exemplo)"; exit 1;;
esac

N="$(python3 -c "import json;print(len(json.load(open('$OUT'))['features']))")"
printf '%s\t%s\t%s feições\t%s\n' "$(date +%F)" "$FONTE" "$N" "$OUT" >> "$OUT_DIR/EXTRACOES.log"
echo ">> OK: $N feições -> $OUT  [$FONTE]"
