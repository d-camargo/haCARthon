#!/usr/bin/env bash
# Pipeline de ingestão — passo 1: BAIXAR recorte municipal do SICAR (WFS oficial).
# Fonte: GeoServer do CAR (verificado no ar em 2026-06-25). CRS de saída: EPSG:4674.
# Uso: ./baixar.sh <UF> "<Município>"      ex.: ./baixar.sh PR "Itaguajé"
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$(cd ../.. && pwd)"

UF="${1:?uso: ./baixar.sh <UF> \"<Município>\"}"
MUNI="${2:?uso: ./baixar.sh <UF> \"<Município>\"}"
ufl="$(echo "$UF" | tr 'A-Z' 'a-z')"
slug="$(echo "$MUNI" | iconv -f utf8 -t ascii//TRANSLIT 2>/dev/null | tr 'A-Z ' 'a-z_' | tr -cd 'a-z0-9_')"
menc="$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))' "$MUNI")"

OUT_DIR="$ROOT/data/sicar"
mkdir -p "$OUT_DIR"
OUT="$OUT_DIR/imoveis_${ufl}_${slug}.geojson"

BASE="https://geoserver.car.gov.br/geoserver/sicar/wfs"
URL="${BASE}?service=WFS&version=2.0.0&request=GetFeature&typeNames=sicar:sicar_imoveis_${ufl}&outputFormat=application/json&srsName=EPSG:4674&CQL_FILTER=municipio='${menc}'"

echo ">> Baixando ${UF}/${MUNI} do SICAR WFS..."
curl -fsS -m 180 "$URL" -o "$OUT"
N="$(python3 -c "import json;print(len(json.load(open('$OUT'))['features']))")"

# Registro de proveniência (data de extração) — exigência do projeto.
printf '%s\tSICAR WFS\t%s/%s\t%s imóveis\t%s\n' "$(date +%F)" "$UF" "$MUNI" "$N" "$OUT" >> "$OUT_DIR/EXTRACOES.log"
echo ">> OK: $N imóveis -> $OUT"
echo ">> Proveniência registrada em data/sicar/EXTRACOES.log (atualize também data/README.md)."
