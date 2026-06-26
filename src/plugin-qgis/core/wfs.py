# -*- coding: utf-8 -*-
"""
Carregamento das camadas do SICAR e do INCRA.

Decisão (após teste): o provider WFS NATIVO do QGIS expirava (~60s) no endpoint i3geo do
INCRA. Adotamos os caminhos comprovados no pipeline (`src/pipeline-ingestao/`):
- SICAR : GET direto do GeoServer em GeoJSON (outputFormat=application/json) + CQL_FILTER.
- INCRA : driver WFS do GDAL/OGR (prefixo "WFS:"), rápido e estável. O i3geo (MapServer
          WFS 1.0.0) devolve lat,lon — o eixo é corrigido no algoritmo de download.
"""
from qgis.core import QgsVectorLayer
import urllib.parse
import urllib.request
import tempfile
from datetime import datetime

SICAR_WFS_BASE = "https://geoserver.car.gov.br/geoserver/sicar/wfs"
INCRA_WFS_BASE = "https://acervofundiario.incra.gov.br/i3geo/ogc.php"
_UA = "PreValCAR-QGIS/0.1 (+haCARthon)"


def _invalid(layer_name, msg):
    layer = QgsVectorLayer("", layer_name, "ogr")
    layer.error_msg = msg
    return layer


def load_sicar_layer(uf, municipio, layer_name=None):
    """Imóveis do SICAR (GeoJSON via HTTP), filtrados por município (CQL_FILTER)."""
    if not layer_name:
        layer_name = f"CAR - {municipio} ({uf})"

    params = {
        'service': 'WFS', 'version': '2.0.0', 'request': 'GetFeature',
        'typeNames': f'sicar:sicar_imoveis_{uf.lower()}',
        'srsName': 'EPSG:4674', 'outputFormat': 'application/json',
        'CQL_FILTER': f"municipio='{municipio}'",
    }
    url = SICAR_WFS_BASE + '?' + urllib.parse.urlencode(params)

    try:
        req = urllib.request.Request(url, headers={'User-Agent': _UA})
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = resp.read()
        tmp = tempfile.NamedTemporaryFile(suffix='.geojson', delete=False)
        tmp.write(data)
        tmp.close()
        layer = QgsVectorLayer(tmp.name, layer_name, "ogr")
    except Exception as e:
        return _invalid(layer_name, f"{type(e).__name__}: {e}")

    if not layer.isValid():
        return _invalid(layer_name, "GeoJSON baixado, mas o GDAL não conseguiu abrir a camada.")

    layer.setCustomProperty("data_extracao", datetime.now().strftime("%Y-%m-%d"))
    layer.setCustomProperty("fonte", "SICAR WFS (GeoJSON)")
    return layer


def load_incra_layer(uf, layer_name=None):
    """Assentamentos do INCRA via driver WFS do GDAL/OGR (eixo corrigido no algoritmo)."""
    if not layer_name:
        layer_name = f"Assentamentos INCRA - {uf}"

    src = f"WFS:{INCRA_WFS_BASE}?tema=assentamentos_{uf.lower()}"
    layer = QgsVectorLayer(src, layer_name, "ogr")

    if not layer.isValid():
        return _invalid(
            layer_name,
            "GDAL não conseguiu abrir o WFS do INCRA "
            "(acervofundiario.incra.gov.br/i3geo). Verifique a conectividade."
        )

    layer.setCustomProperty("data_extracao", datetime.now().strftime("%Y-%m-%d"))
    layer.setCustomProperty("fonte", "INCRA i3geo (GDAL WFS)")
    return layer
