"""Leitura dos dados reais do imóvel no CAR, por cod_imovel.

Reusa o conceito do motor do Desafio 2 (consulta à base oficial do SICAR), aqui
com a base oficial do Paraná já extraída em `data/` (registrar data de extração)
e leitura via GDAL/OGR (osgeo) — sem dependências pesadas.

Camadas:
- Perímetro do imóvel  → data/sicar/imoveis_pr_*.geojson
- APP (por tipo)       → data/Área de Preservação Permanente/*.shp
- Reserva Legal        → data/Reserva Legal/*.shp

`carregar_imovel(cod)` devolve as geometrias (em lon/lat, EPSG:4674) e os
atributos prontos para o mapa e para a explicação do assistente.
"""
import os
from pathlib import Path

os.environ.setdefault("SHAPE_ENCODING", "ISO-8859-1")
from osgeo import ogr  # noqa: E402

ogr.UseExceptions()

DATA = Path(__file__).resolve().parents[2] / "data"
PERIM_DIR = DATA / "sicar"
APP_DIR = DATA / "Área de Preservação Permanente"
RL_DIR = DATA / "Reserva Legal"


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


def _ler(caminho: Path, cod: str, campo: str = "cod_imovel"):
    """Polígonos e atributos da 1ª feição com aquele cod_imovel no arquivo."""
    ds = ogr.Open(str(caminho))
    if ds is None:
        return [], None
    lyr = ds.GetLayer(0)
    lyr.SetAttributeFilter(f"{campo}='{cod}'")
    polys, attrs = [], None
    for feat in lyr:
        polys.extend(_poligonos(feat.GetGeometryRef()))
        if attrs is None:
            attrs = {
                feat.GetFieldDefnRef(i).GetName(): feat.GetField(i)
                for i in range(feat.GetFieldCount())
            }
    return polys, attrs


def _camadas(pasta: Path, cod: str) -> list[dict]:
    feicoes = []
    for shp in sorted(pasta.glob("*.shp")):
        polys, attrs = _ler(shp, cod)
        if polys:
            feicoes.append(
                {
                    "tipo": shp.stem,
                    "polys": polys,
                    "area_ha": (attrs or {}).get("nu_area_im"),
                }
            )
    return feicoes


def carregar_imovel(cod: str) -> dict | None:
    """Junta perímetro + APP + RL do imóvel. None se não achar o perímetro."""
    perimetro, attrs = [], None
    for gj in sorted(PERIM_DIR.glob("imoveis_pr_*.geojson")):
        perimetro, attrs = _ler(gj, cod)
        if perimetro:
            break
    if not perimetro:
        return None

    return {
        "cod": cod,
        "perimetro": perimetro,
        "attrs": attrs or {},
        "app": _camadas(APP_DIR, cod),
        "rl": _camadas(RL_DIR, cod),
    }
