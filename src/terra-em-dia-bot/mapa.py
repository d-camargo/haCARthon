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
from matplotlib.lines import Line2D

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


def _obter_hidrografia_externa(xmin: float, ymin: float, xmax: float, ymax: float, epsg_utm: int) -> list:
    """Consulta a API REST do GeoPR (IAT) para obter linhas de hidrografia no bbox, em UTM."""
    import urllib.request
    import urllib.parse
    import json
    import ssl
    
    linhas = []
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        params = {
            "geometry": f"{xmin},{ymin},{xmax},{ymax}",
            "geometryType": "esriGeometryEnvelope",
            "inSR": str(epsg_utm),
            "spatialRel": "esriSpatialRelIntersects",
            "outSR": str(epsg_utm),
            "f": "json",
            "returnGeometry": "true",
            "outFields": "rio"
        }
        url = "https://geopr.iat.pr.gov.br/server/rest/services/00_PUBLICACOES/zee_rios/MapServer/0/query?" + urllib.parse.urlencode(params)
        
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            for feat in res.get("features", []):
                geom = feat.get("geometry", {})
                for path in geom.get("paths", []):
                    pts = [(pt[0], pt[1]) for pt in path]
                    if pts:
                        linhas.append(pts)
    except Exception:
        # Silencioso e defensivo
        pass
    return linhas


def gerar_mapa(imovel: dict, saida: str | Path, modo: str = "atual") -> Path:
    saida = Path(saida)
    meta = modo == "meta"
    fig, ax = plt.subplots(figsize=(8, 8), dpi=130)

    import geo_app
    epsg_utm = geo_app.obter_epsg_utm_imovel(imovel)

    # Reprojeta as camadas locais para UTM
    perimetro_utm = geo_app.reprojetar_poligonos_utm(imovel["perimetro"], epsg_utm)
    app_utm = []
    for f in imovel["app"]:
        app_utm.append({
            "tipo": f["tipo"],
            "polys": geo_app.reprojetar_poligonos_utm(f["polys"], epsg_utm),
            "area_ha": f.get("area_ha")
        })
    rl_utm = []
    for f in imovel["rl"]:
        rl_utm.append({
            "tipo": f["tipo"],
            "polys": geo_app.reprojetar_poligonos_utm(f["polys"], epsg_utm),
            "area_ha": f.get("area_ha")
        })

    # 1. Calcula os limites (bbox) com margem em metros
    b = [9e9, 9e9, -9e9, -9e9]
    _bounds(perimetro_utm, b)
    for f in app_utm + rl_utm:
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
        aspect = (ymax - ymin) / (xmax - xmin) if (xmax - xmin) > 0 else 1.0
        MAXDIM = 1400
        if aspect >= 1:
            h = MAXDIM
            w = int(MAXDIM / aspect)
        else:
            w = MAXDIM
            h = int(MAXDIM * aspect)
        w = max(200, w)
        h = max(200, h)
        
        import json
        params = {
            "bbox": f"{xmin},{ymin},{xmax},{ymax}",
            "bboxSR": str(epsg_utm),
            "imageSR": str(epsg_utm),
            "size": f"{w},{h}",
            "format": "jpg",
            "f": "json"
        }
        url = "https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/export?" + urllib.parse.urlencode(params)
        
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            dados_json = json.loads(resp.read().decode("utf-8"))
            
        href = dados_json["href"]
        extent_real = dados_json["extent"]
        
        req_img = urllib.request.Request(
            href,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req_img, timeout=20) as resp_img:
            img = Image.open(io.BytesIO(resp_img.read()))
    except Exception:
        # Fallback offline (fundo branco)
        img = None
        extent_real = None

    satelite_ok = img is not None and extent_real is not None
    if satelite_ok:
        ax.imshow(img, extent=[extent_real["xmin"], extent_real["xmax"], extent_real["ymin"], extent_real["ymax"]], origin="upper", zorder=0)

    # 3. Desenha as feições
    _desenha(ax, perimetro_utm, ESTILO["perimetro"], zorder=1, satelite=satelite_ok)
    app_est = ESTILO["app_meta"] if meta else ESTILO["app"]
    for f in app_utm:
        _desenha(ax, f["polys"], app_est, zorder=2, satelite=satelite_ok)
    if not meta:  # no mapa-meta, foco na mata ciliar
        for f in rl_utm:
            _desenha(ax, f["polys"], ESTILO["rl"], zorder=2, satelite=satelite_ok)

    # 4. Desenha a hidrografia externa (se houver)
    linhas_rio = _obter_hidrografia_externa(xmin, ymin, xmax, ymax, epsg_utm)
    desenhou_rio = False
    for path in linhas_rio:
        xs = [pt[0] for pt in path]
        ys = [pt[1] for pt in path]
        ax.plot(xs, ys, color="#0ea5e9", linewidth=2.5, zorder=3)
        desenhou_rio = True

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")

    handles = [plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["perimetro"]["face"],
                             edgecolor=ESTILO["perimetro"]["edge"], alpha=0.7,
                             label=ESTILO["perimetro"]["label"])]
    if imovel["app"]:
        handles.append(plt.Rectangle((0, 0), 1, 1, facecolor=app_est["face"],
                                     alpha=0.8, label=app_est["label"]))
    if imovel["rl"] and not meta:
        handles.append(plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["rl"]["face"],
                                     alpha=0.7, label=ESTILO["rl"]["label"]))
    if desenhou_rio:
        handles.append(Line2D([0], [0], color="#0ea5e9", linewidth=2.5, label="Rio / Drenagem (Ref)"))

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

    import geo_app
    epsg_utm = geo_app.obter_epsg_utm_imovel(imovel)

    # Reprojeta as camadas locais para UTM
    perimetro_utm = geo_app.reprojetar_poligonos_utm(imovel["perimetro"], epsg_utm)
    app_utm = []
    for f in imovel["app"]:
        app_utm.append({
            "tipo": f["tipo"],
            "polys": geo_app.reprojetar_poligonos_utm(f["polys"], epsg_utm),
            "area_ha": f.get("area_ha")
        })
    rl_utm = []
    for f in imovel["rl"]:
        rl_utm.append({
            "tipo": f["tipo"],
            "polys": geo_app.reprojetar_poligonos_utm(f["polys"], epsg_utm),
            "area_ha": f.get("area_ha")
        })

    # 1. Calcula limites de zoom focados na feição escolhida em UTM
    b = [9e9, 9e9, -9e9, -9e9]
    camada_alvo = app_utm if feicao == "app" else rl_utm
    for f in camada_alvo:
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
        aspect = (ymax - ymin) / (xmax - xmin) if (xmax - xmin) > 0 else 1.0
        MAXDIM = 1400
        if aspect >= 1:
            h = MAXDIM
            w = int(MAXDIM / aspect)
        else:
            w = MAXDIM
            h = int(MAXDIM * aspect)
        w = max(200, w)
        h = max(200, h)
        
        import json
        params = {
            "bbox": f"{xmin},{ymin},{xmax},{ymax}",
            "bboxSR": str(epsg_utm),
            "imageSR": str(epsg_utm),
            "size": f"{w},{h}",
            "format": "jpg",
            "f": "json"
        }
        url = "https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/export?" + urllib.parse.urlencode(params)
        
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            dados_json = json.loads(resp.read().decode("utf-8"))
            
        href = dados_json["href"]
        extent_real = dados_json["extent"]
        
        req_img = urllib.request.Request(
            href,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req_img, timeout=20) as resp_img:
            img = Image.open(io.BytesIO(resp_img.read()))
    except Exception:
        img = None
        extent_real = None

    satelite_ok = img is not None and extent_real is not None

    # Estilos customizados para contraste real
    est_hoje = ESTILO["app"].copy()
    est_hoje["face"] = "none"
    est_hoje["alpha"] = 1.0
    est_hoje["lw"] = 2.0  # contorno visível

    est_em_dia = ESTILO["app_meta"].copy()
    est_em_dia["alpha"] = 0.8  # verde sólido

    # 3. Painel da esquerda: "Hoje" (contorno/chão apenas)
    if satelite_ok:
        ax1.imshow(img, extent=[extent_real["xmin"], extent_real["xmax"], extent_real["ymin"], extent_real["ymax"]], origin="upper", zorder=0)
    _desenha(ax1, perimetro_utm, ESTILO["perimetro"], zorder=1, satelite=satelite_ok)
    for f in app_utm:
        _desenha(ax1, f["polys"], est_hoje, zorder=2, satelite=satelite_ok)

    # 4. Painel da direita: "Como deve ficar (Meta)" (verde sólido)
    if satelite_ok:
        ax2.imshow(img, extent=[extent_real["xmin"], extent_real["xmax"], extent_real["ymin"], extent_real["ymax"]], origin="upper", zorder=0)
    _desenha(ax2, perimetro_utm, ESTILO["perimetro"], zorder=1, satelite=satelite_ok)
    for f in app_utm:
        _desenha(ax2, f["polys"], est_em_dia, zorder=2, satelite=satelite_ok)

    # 4b. Desenha a hidrografia externa (se houver)
    linhas_rio = _obter_hidrografia_externa(xmin, ymin, xmax, ymax, epsg_utm)
    desenhou_rio = False
    for path in linhas_rio:
        xs = [pt[0] for pt in path]
        ys = [pt[1] for pt in path]
        ax1.plot(xs, ys, color="#0ea5e9", linewidth=2.5, zorder=3)
        ax2.plot(xs, ys, color="#0ea5e9", linewidth=2.5, zorder=3)
        desenhou_rio = True

    # Adiciona a cota visual de 30m no painel da solução (ax2)
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    ax2.annotate(
        "Faixa legal:\n30m da margem",
        xy=(cx, cy),
        xytext=(0, 20),
        textcoords="offset points",
        ha="center", va="center",
        fontsize=10, weight="bold", color="black",
        arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.85, edgecolor="none"),
        zorder=4
    )

    # 5. Formatação dos eixos, proporção e títulos
    for ax in (ax1, ax2):
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)

    ax1.set_title("Hoje: a beira do rio", fontsize=12, weight="bold")
    ax2.set_title("Em dia: faixa de 30m coberta 🌳", fontsize=12, weight="bold")

    # 6. Legendas curtas
    h1 = [plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["perimetro"]["face"],
                        edgecolor=ESTILO["perimetro"]["edge"], alpha=0.7,
                        label=ESTILO["perimetro"]["label"])]
    if imovel["app"]:
        h1.append(plt.Rectangle((0, 0), 1, 1, facecolor="none", edgecolor=est_hoje["edge"],
                                linewidth=2.0, label="Área que precisa de mata ciliar"))
    if desenhou_rio:
        h1.append(Line2D([0], [0], color="#0ea5e9", linewidth=2.5, label="Rio / Drenagem (Ref)"))
    ax1.legend(handles=h1, loc="upper right", fontsize=8, framealpha=0.9)

    h2 = [plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["perimetro"]["face"],
                        edgecolor=ESTILO["perimetro"]["edge"], alpha=0.7,
                        label=ESTILO["perimetro"]["label"])]
    if imovel["app"]:
        h2.append(plt.Rectangle((0, 0), 1, 1, facecolor=est_em_dia["face"],
                                alpha=0.8, label=est_em_dia["label"]))
    if desenhou_rio:
        h2.append(Line2D([0], [0], color="#0ea5e9", linewidth=2.5, label="Rio / Drenagem (Ref)"))
    ax2.legend(handles=h2, loc="upper right", fontsize=8, framealpha=0.9)

    municipio = imovel["attrs"].get("municipio", "")
    uf = imovel["attrs"].get("uf", "")
    fig.suptitle(f"Comparativo da beira do rio - {municipio}/{uf}".strip(" -/"), fontsize=13, weight="bold", y=0.98)

    fig.tight_layout()
    fig.savefig(saida, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return saida
