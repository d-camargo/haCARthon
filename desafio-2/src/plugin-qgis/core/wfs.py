# -*- coding: utf-8 -*-
"""
Carregamento das camadas do SICAR e do INCRA.

Rede: usamos a pilha do PRÓPRIO QGIS (QgsBlockingNetworkRequest) e o GDAL/OGR, e NÃO o
`urllib` do Python — o Python embarcado (ex.: Flatpak) pode falhar no handshake SSL com o
GeoServer (SSLV3_ALERT_HANDSHAKE_FAILURE), enquanto a rede do QGIS respeita a config de
SSL/proxy do aplicativo.

- SICAR : GET do GeoServer em GeoJSON (QgsBlockingNetworkRequest; fallback GDAL /vsicurl/).
- INCRA : driver WFS do GDAL/OGR (prefixo "WFS:"). O i3geo (MapServer WFS 1.0.0) devolve
          lat,lon — o eixo é corrigido no algoritmo de download.
"""
from qgis.core import QgsVectorLayer, QgsBlockingNetworkRequest
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest
import urllib.parse
import tempfile
from datetime import datetime

SICAR_WFS_BASE = "https://geoserver.car.gov.br/geoserver/sicar/wfs"
INCRA_WFS_BASE = "https://acervofundiario.incra.gov.br/i3geo/ogc.php"
_UA = "PreValCAR-QGIS/0.1 (+haCARthon)"


def _invalid(layer_name, msg):
    layer = QgsVectorLayer("", layer_name, "ogr")
    layer.error_msg = msg
    return layer


def _layer_from_geojson_bytes(data, layer_name):
    tmp = tempfile.NamedTemporaryFile(suffix='.geojson', delete=False)
    tmp.write(data)
    tmp.close()
    return QgsVectorLayer(tmp.name, layer_name, "ogr")


def load_sicar_layer(uf, municipio, layer_name=None):
    """Imóveis do SICAR (GeoJSON via rede do QGIS), filtrados por município (CQL_FILTER)."""
    if not layer_name:
        layer_name = f"CAR - {municipio} ({uf})"

    municipio_cql = municipio.replace("'", "''")  # escapa aspa simples no CQL
    params = {
        'service': 'WFS', 'version': '2.0.0', 'request': 'GetFeature',
        'typeNames': f'sicar:sicar_imoveis_{uf.lower()}',
        'srsName': 'EPSG:4674', 'outputFormat': 'application/json',
        'CQL_FILTER': f"municipio='{municipio_cql}'",
    }
    url = SICAR_WFS_BASE + '?' + urllib.parse.urlencode(params)

    # 1) Pilha de rede do QGIS (respeita SSL/proxy do app)
    erro_rede = None
    try:
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"User-Agent", _UA.encode("utf-8"))
        blocking = QgsBlockingNetworkRequest()
        blocking.get(request, True)
        reply = blocking.reply()
        data = bytes(reply.content())
        if data:
            layer = _layer_from_geojson_bytes(data, layer_name)
            if layer.isValid():
                layer.setCustomProperty("data_extracao", datetime.now().strftime("%Y-%m-%d"))
                layer.setCustomProperty("fonte", "SICAR WFS (GeoJSON)")
                return layer
            erro_rede = "GeoJSON recebido, mas o GDAL não abriu a camada."
        else:
            erro_rede = reply.errorString() or "resposta vazia"
    except Exception as e:
        erro_rede = f"{type(e).__name__}: {e}"

    # 2) Fallback: GDAL/libcurl via /vsicurl/
    layer = QgsVectorLayer(f"/vsicurl/{url}", layer_name, "ogr")
    if layer.isValid():
        layer.setCustomProperty("data_extracao", datetime.now().strftime("%Y-%m-%d"))
        layer.setCustomProperty("fonte", "SICAR WFS (GeoJSON/vsicurl)")
        return layer

    return _invalid(layer_name, f"Falha de rede ao baixar o SICAR. {erro_rede or ''}".strip())


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
