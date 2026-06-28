"""Módulo de integração WFS para consulta aos dados do CAR.

Busca perímetro e atributos do imóvel de qualquer UF do Brasil diretamente
do geoserver oficial do SICAR.
"""
import urllib.parse
from osgeo import gdal, ogr

# Configurações HTTP do GDAL
gdal.SetConfigOption("GDAL_HTTP_TIMEOUT", "25")
gdal.SetConfigOption("GDAL_HTTP_USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

# OGR exceptions
ogr.UseExceptions()


def _anel(ring) -> list[tuple[float, float]]:
    return [(ring.GetX(i), ring.GetY(i)) for i in range(ring.GetPointCount())]


def _poligonos(geom) -> list[tuple[list, list]]:
    """Achata POLYGON/MULTIPOLYGON em [(anel_externo, [furos])]."""
    out: list[tuple[list, list]] = []
    if geom is None:
        return out
    nome = geom.GetGeometryName()
    if nome == "POLYGON":
        ext = _anel(geom.GetGeometryRef(0))
        furos = [_anel(geom.GetGeometryRef(i)) for i in range(1, geom.GetGeometryCount())]
        out.append((ext, furos))
    elif nome in ("MULTIPOLYGON", "GEOMETRYCOLLECTION"):
        for i in range(geom.GetGeometryCount()):
            out.extend(_poligonos(geom.GetGeometryRef(i)))
    return out


def buscar_perimetro(cod: str) -> tuple[list, dict] | tuple[None, None]:
    """Busca o perímetro e atributos de qualquer imóvel no WFS do SICAR.
    Retorna (polys, attrs) ou (None, None) se falhar/não achar.
    """
    cod = (cod or "").strip()
    if not cod or len(cod) < 5:
        return None, None
        
    uf = cod[:2].lower()
    typeName = f"sicar:sicar_imoveis_{uf}"
    
    # Escape de aspas simples
    cod_escaped = cod.replace("'", "''")
    cql_filter = f"cod_imovel='{cod_escaped}'"
    
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeName": typeName,
        "CQL_FILTER": cql_filter,
        "outputFormat": "application/json",
        "srsName": "EPSG:4674",
        "count": "1"
    }
    
    url = "https://geoserver.car.gov.br/geoserver/sicar/wfs?" + urllib.parse.urlencode(params)
    
    try:
        ds = ogr.Open("/vsicurl/" + url)
        if ds is None:
            return None, None
        
        lyr = ds.GetLayer(0)
        if lyr is None or lyr.GetFeatureCount() == 0:
            return None, None
            
        feat = lyr.GetNextFeature()
        if feat is None:
            return None, None
            
        # Parse geometry
        geom = feat.GetGeometryRef()
        polys = _poligonos(geom)
        
        # Parse attributes
        attrs = {
            feat.GetFieldDefnRef(i).GetName(): feat.GetField(i)
            for i in range(feat.GetFieldCount())
        }
        
        return polys, attrs
    except Exception:
        return None, None
