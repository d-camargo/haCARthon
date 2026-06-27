"""Gera o mapa do imóvel (PNG) com as feições do cadastro, pra mandar no Zap.

Lê os dados de `cadastro.carregar_imovel` (lon/lat, EPSG:4674) e desenha com
matplotlib — sem basemap online (funciona offline e em conexão ruim). Estilo
pensado para o Seu Raimundo: poucas cores, legenda em linguagem simples.
"""
from math import cos, radians
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon as MplPolygon  # noqa: E402

# Cores por camada (legenda em linguagem do produtor)
ESTILO = {
    "perimetro": {"face": "#f5f5dc", "edge": "#333333", "lw": 2.0, "alpha": 0.5,
                  "label": "Seu imóvel"},
    "app": {"face": "#2563eb", "edge": "#1e3a8a", "lw": 0.6, "alpha": 0.65,
            "label": "Mata ciliar (beira do rio)"},
    "rl": {"face": "#16a34a", "edge": "#14532d", "lw": 0.6, "alpha": 0.55,
           "label": "Reserva Legal"},
}


def _desenha(ax, polys, est):
    for ext, _furos in polys:
        if len(ext) >= 3:
            ax.add_patch(
                MplPolygon(ext, closed=True, facecolor=est["face"],
                           edgecolor=est["edge"], linewidth=est["lw"], alpha=est["alpha"])
            )


def _bounds(polys, b):
    for ext, _ in polys:
        for x, y in ext:
            b[0], b[1] = min(b[0], x), min(b[1], y)
            b[2], b[3] = max(b[2], x), max(b[3], y)
    return b


def gerar_mapa(imovel: dict, saida: str | Path) -> Path:
    saida = Path(saida)
    fig, ax = plt.subplots(figsize=(8, 8), dpi=130)

    _desenha(ax, imovel["perimetro"], ESTILO["perimetro"])
    for f in imovel["app"]:
        _desenha(ax, f["polys"], ESTILO["app"])
    for f in imovel["rl"]:
        _desenha(ax, f["polys"], ESTILO["rl"])

    # Limites + aspecto correto para lon/lat
    b = [9e9, 9e9, -9e9, -9e9]
    _bounds(imovel["perimetro"], b)
    for f in imovel["app"] + imovel["rl"]:
        _bounds(f["polys"], b)
    mx = (b[2] - b[0]) * 0.08 + 1e-4
    my = (b[3] - b[1]) * 0.08 + 1e-4
    ax.set_xlim(b[0] - mx, b[2] + mx)
    ax.set_ylim(b[1] - my, b[3] + my)
    lat_med = (b[1] + b[3]) / 2
    ax.set_aspect(1 / cos(radians(lat_med)))

    # Legenda só com as camadas presentes
    handles = [plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["perimetro"]["face"],
                             edgecolor=ESTILO["perimetro"]["edge"], alpha=0.7,
                             label=ESTILO["perimetro"]["label"])]
    if imovel["app"]:
        handles.append(plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["app"]["face"],
                                     alpha=0.7, label=ESTILO["app"]["label"]))
    if imovel["rl"]:
        handles.append(plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["rl"]["face"],
                                     alpha=0.7, label=ESTILO["rl"]["label"]))
    ax.legend(handles=handles, loc="upper right", fontsize=9, framealpha=0.9)

    municipio = imovel["attrs"].get("municipio", "")
    uf = imovel["attrs"].get("uf", "")
    ax.set_title(f"Seu imóvel — {municipio}/{uf}".strip(" —/"), fontsize=13, weight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    fig.tight_layout()
    fig.savefig(saida, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return saida
