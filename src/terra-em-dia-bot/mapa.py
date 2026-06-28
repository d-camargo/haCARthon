"""Gera o mapa do imóvel (PNG) com as feições do cadastro, pra mandar no Zap.

Dois modos:
- "atual": como está hoje (perímetro + mata ciliar em azul + Reserva Legal).
- "meta":  como deve ficar — a faixa de mata ciliar em VERDE (coberta de mato).
           A localização da APP é dimensional (30 m da margem), então é "certa".

Lê os dados de `cadastro.carregar_imovel` (lon/lat, EPSG:4674) e desenha com
matplotlib — sem basemap online (funciona offline e em conexão ruim).
"""
from math import cos, radians
from pathlib import Path
import urllib.request
import urllib.parse
import io
from PIL import Image

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon as MplPolygon  # noqa: E402

ESTILO = {
    "perimetro": {"face": "#f5f5dc", "edge": "#333333", "lw": 2.0, "alpha": 0.5,
                  "label": "Seu imóvel"},
    "app": {"face": "#2563eb", "edge": "#1e3a8a", "lw": 0.6, "alpha": 0.65,
            "label": "Mata ciliar (beira do rio)"},
    "app_meta": {"face": "#15803d", "edge": "#14532d", "lw": 0.8, "alpha": 0.85,
                 "label": "Mata ciliar coberta de mato"},
    "rl": {"face": "#16a34a", "edge": "#14532d", "lw": 0.6, "alpha": 0.55,
           "label": "Reserva Legal"},
}


def _desenha(ax, polys, est, zorder=1, satelite=False):
    for ext, _furos in polys:
        if len(ext) >= 3:
            lw = est["lw"] * 1.5 if satelite else est["lw"]
            ax.add_patch(
                MplPolygon(ext, closed=True, facecolor=est["face"],
                           edgecolor=est["edge"], linewidth=lw, alpha=est["alpha"],
                           zorder=zorder)
            )


def _bounds(polys, b):
    for ext, _ in polys:
        for x, y in ext:
            b[0], b[1] = min(b[0], x), min(b[1], y)
            b[2], b[3] = max(b[2], x), max(b[3], y)
    return b


def gerar_mapa(imovel: dict, saida: str | Path, modo: str = "atual") -> Path:
    saida = Path(saida)
    meta = modo == "meta"
    fig, ax = plt.subplots(figsize=(8, 8), dpi=130)

    # 1. Calcula os limites (bbox) com margem
    b = [9e9, 9e9, -9e9, -9e9]
    _bounds(imovel["perimetro"], b)
    for f in imovel["app"] + imovel["rl"]:
        _bounds(f["polys"], b)
    mx = (b[2] - b[0]) * 0.08 + 1e-4
    my = (b[3] - b[1]) * 0.08 + 1e-4
    xmin = b[0] - mx
    ymin = b[1] - my
    xmax = b[2] + mx
    ymax = b[3] + my

    # 2. Tenta baixar a imagem de satélite (Esri World Imagery)
    import urllib.request
    import urllib.parse
    import io
    from PIL import Image

    img = None
    try:
        w = 1000
        aspect = (ymax - ymin) / (xmax - xmin) if (xmax - xmin) > 0 else 1.0
        aspect_corr = aspect * cos(radians((ymin + ymax) / 2))
        h = max(200, min(1500, int(w * aspect_corr)))
        
        params = {
            "bbox": f"{xmin},{ymin},{xmax},{ymax}",
            "bboxSR": "4326",
            "imageSR": "4326",
            "size": f"{w},{h}",
            "format": "jpg",
            "f": "image"
        }
        url = "https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/export?" + urllib.parse.urlencode(params)
        
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            img = Image.open(io.BytesIO(resp.read()))
    except Exception:
        # Fallback offline (fundo branco)
        img = None

    satelite_ok = img is not None
    if satelite_ok:
        ax.imshow(img, extent=[xmin, xmax, ymin, ymax], origin="upper", zorder=0)

    # 3. Desenha as feições
    _desenha(ax, imovel["perimetro"], ESTILO["perimetro"], zorder=1, satelite=satelite_ok)
    app_est = ESTILO["app_meta"] if meta else ESTILO["app"]
    for f in imovel["app"]:
        _desenha(ax, f["polys"], app_est, zorder=2, satelite=satelite_ok)
    if not meta:  # no mapa-meta, foco na mata ciliar
        for f in imovel["rl"]:
            _desenha(ax, f["polys"], ESTILO["rl"], zorder=2, satelite=satelite_ok)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect(1 / cos(radians((ymin + ymax) / 2)))

    handles = [plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["perimetro"]["face"],
                             edgecolor=ESTILO["perimetro"]["edge"], alpha=0.7,
                             label=ESTILO["perimetro"]["label"])]
    if imovel["app"]:
        handles.append(plt.Rectangle((0, 0), 1, 1, facecolor=app_est["face"],
                                     alpha=0.8, label=app_est["label"]))
    if imovel["rl"] and not meta:
        handles.append(plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["rl"]["face"],
                                     alpha=0.7, label=ESTILO["rl"]["label"]))
    ax.legend(handles=handles, loc="upper right", fontsize=9, framealpha=0.9)

    municipio = imovel["attrs"].get("municipio", "")
    uf = imovel["attrs"].get("uf", "")
    titulo = ("Como a beira do rio deve ficar"
              if meta else f"Seu imóvel hoje - {municipio}/{uf}".strip(" -/"))
    ax.set_title(titulo, fontsize=13, weight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    fig.tight_layout()
    fig.savefig(saida, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return saida


def gerar_comparativo(imovel: dict, saida: str | Path, feicao: str = "app") -> Path | None:
    saida = Path(saida)

    # 1. Calcula limites de zoom focados na feição escolhida
    b = [9e9, 9e9, -9e9, -9e9]
    for f in imovel.get(feicao, []):
        _bounds(f["polys"], b)
        
    if b[0] > 8e9:
        return None  # Feição vazia
        
    mx = (b[2] - b[0]) * 0.18 + 1e-4
    my = (b[3] - b[1]) * 0.18 + 1e-4
    xmin = b[0] - mx
    ymin = b[1] - my
    xmax = b[2] + mx
    ymax = b[3] + my

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), dpi=130)

    # 2. Tenta baixar a imagem de satélite para o bbox de zoom
    img = None
    try:
        w = 1000
        aspect = (ymax - ymin) / (xmax - xmin) if (xmax - xmin) > 0 else 1.0
        aspect_corr = aspect * cos(radians((ymin + ymax) / 2))
        h = max(200, min(1500, int(w * aspect_corr)))
        
        params = {
            "bbox": f"{xmin},{ymin},{xmax},{ymax}",
            "bboxSR": "4326",
            "imageSR": "4326",
            "size": f"{w},{h}",
            "format": "jpg",
            "f": "image"
        }
        url = "https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/export?" + urllib.parse.urlencode(params)
        
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            img = Image.open(io.BytesIO(resp.read()))
    except Exception:
        img = None

    satelite_ok = img is not None

    # Estilos customizados para contraste real
    est_hoje = ESTILO["app"].copy()
    est_hoje["face"] = "none"
    est_hoje["alpha"] = 1.0
    est_hoje["lw"] = 2.0  # contorno visível

    est_em_dia = ESTILO["app_meta"].copy()
    est_em_dia["alpha"] = 0.8  # verde sólido

    # 3. Painel da esquerda: "Hoje" (contorno/chão apenas)
    if satelite_ok:
        ax1.imshow(img, extent=[xmin, xmax, ymin, ymax], origin="upper", zorder=0)
    _desenha(ax1, imovel["perimetro"], ESTILO["perimetro"], zorder=1, satelite=satelite_ok)
    for f in imovel["app"]:
        _desenha(ax1, f["polys"], est_hoje, zorder=2, satelite=satelite_ok)

    # 4. Painel da direita: "Como deve ficar (Meta)" (verde sólido)
    if satelite_ok:
        ax2.imshow(img, extent=[xmin, xmax, ymin, ymax], origin="upper", zorder=0)
    _desenha(ax2, imovel["perimetro"], ESTILO["perimetro"], zorder=1, satelite=satelite_ok)
    for f in imovel["app"]:
        _desenha(ax2, f["polys"], est_em_dia, zorder=2, satelite=satelite_ok)

    # 5. Formatação dos eixos, proporção e títulos
    for ax in (ax1, ax2):
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.set_aspect(1 / cos(radians((ymin + ymax) / 2)))
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)

    ax1.set_title("Hoje: a beira do rio", fontsize=12, weight="bold")
    ax2.set_title("Em dia: coberta de mato 🌳", fontsize=12, weight="bold")

    # 6. Legendas curtas
    h1 = [plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["perimetro"]["face"],
                        edgecolor=ESTILO["perimetro"]["edge"], alpha=0.7,
                        label=ESTILO["perimetro"]["label"])]
    if imovel["app"]:
        h1.append(plt.Rectangle((0, 0), 1, 1, facecolor="none", edgecolor=est_hoje["edge"],
                                linewidth=2.0, label="Área que precisa de mata ciliar"))
    ax1.legend(handles=h1, loc="upper right", fontsize=8, framealpha=0.9)

    h2 = [plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["perimetro"]["face"],
                        edgecolor=ESTILO["perimetro"]["edge"], alpha=0.7,
                        label=ESTILO["perimetro"]["label"])]
    if imovel["app"]:
        h2.append(plt.Rectangle((0, 0), 1, 1, facecolor=est_em_dia["face"],
                                alpha=0.8, label=est_em_dia["label"]))
    ax2.legend(handles=h2, loc="upper right", fontsize=8, framealpha=0.9)

    municipio = imovel["attrs"].get("municipio", "")
    uf = imovel["attrs"].get("uf", "")
    fig.suptitle(f"Comparativo da beira do rio - {municipio}/{uf}".strip(" -/"), fontsize=13, weight="bold", y=0.98)

    fig.tight_layout()
    fig.savefig(saida, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return saida
