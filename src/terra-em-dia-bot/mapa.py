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


def _gerar_buffer_app(app_utm: list, perimetro_utm: list) -> list:
    """Gera o buffer de 13m da APP declarada restrita ao perímetro do imóvel."""
    if not app_utm:
        return []
    try:
        from osgeo import ogr
        
        # 1. Converte perímetro para OGR geometry
        geom_perimetro = ogr.Geometry(ogr.wkbMultiPolygon)
        for ext, furos in perimetro_utm:
            poly = ogr.Geometry(ogr.wkbPolygon)
            ring_ext = ogr.Geometry(ogr.wkbLinearRing)
            for x, y in ext:
                ring_ext.AddPoint(x, y)
            if ext and (ext[0] != ext[-1]):
                ring_ext.AddPoint(ext[0][0], ext[0][1])
            poly.AddGeometry(ring_ext)
            for f in furos:
                ring_f = ogr.Geometry(ogr.wkbLinearRing)
                for x, y in f:
                    ring_f.AddPoint(x, y)
                if f and (f[0] != f[-1]):
                    ring_f.AddPoint(f[0][0], f[0][1])
                poly.AddGeometry(ring_f)
            geom_perimetro.AddGeometry(poly)

        # 2. Converte todas as APPs locais para OGR geometry
        geom_app = ogr.Geometry(ogr.wkbMultiPolygon)
        for f in app_utm:
            for ext, furos in f["polys"]:
                poly = ogr.Geometry(ogr.wkbPolygon)
                ring_ext = ogr.Geometry(ogr.wkbLinearRing)
                for x, y in ext:
                    ring_ext.AddPoint(x, y)
                if ext and (ext[0] != ext[-1]):
                    ring_ext.AddPoint(ext[0][0], ext[0][1])
                poly.AddGeometry(ring_ext)
                for f_fur in furos:
                    ring_f = ogr.Geometry(ogr.wkbLinearRing)
                    for x, y in f_fur:
                        ring_f.AddPoint(x, y)
                    if f_fur and (f_fur[0] != f_fur[-1]):
                        ring_f.AddPoint(f_fur[0][0], f_fur[0][1])
                    poly.AddGeometry(ring_f)
                geom_app.AddGeometry(poly)

        # 3. Faz o buffer de 13 metros
        geom_app_buffer = geom_app.Buffer(13.0)
        
        # 4. Intersecção com o perímetro
        geom_app_ideal = geom_app_buffer.Intersection(geom_perimetro)
        
        # 5. Converte de volta para a lista de polys
        def _geom_to_polys(g: ogr.Geometry) -> list:
            p_list = []
            if g is None or g.IsEmpty():
                return p_list
            g_name = g.GetGeometryName()
            if g_name == 'MULTIPOLYGON':
                for idx in range(g.GetGeometryCount()):
                    p_list.extend(_geom_to_polys(g.GetGeometryRef(idx)))
            elif g_name == 'POLYGON':
                ext_pts = []
                furos_pts = []
                for ring_idx in range(g.GetGeometryCount()):
                    ring = g.GetGeometryRef(ring_idx)
                    pts = []
                    for pt_idx in range(ring.GetPointCount()):
                        pt = ring.GetPoint(pt_idx)
                        pts.append((pt[0], pt[1]))
                    if ring_idx == 0:
                        ext_pts = pts
                    else:
                        furos_pts.append(pts)
                if ext_pts:
                    p_list.append((ext_pts, furos_pts))
            elif g_name == 'GEOMETRYCOLLECTION':
                for idx in range(g.GetGeometryCount()):
                    p_list.extend(_geom_to_polys(g.GetGeometryRef(idx)))
            return p_list

        return _geom_to_polys(geom_app_ideal)
    except Exception:
        fallback = []
        for f in app_utm:
            fallback.extend(f["polys"])
        return fallback


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

    if meta:
        app_desenhar = _gerar_buffer_app(app_utm, perimetro_utm)
    else:
        app_desenhar = []
        for f in app_utm:
            app_desenhar.extend(f["polys"])

    _desenha(ax, app_desenhar, app_est, zorder=2, satelite=satelite_ok)
    if not meta:  # no mapa-meta, foco na mata ciliar
        for f in rl_utm:
            _desenha(ax, f["polys"], ESTILO["rl"], zorder=2, satelite=satelite_ok)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")

    res_app = geo_app.medir_app(imovel)
    if res_app:
        ha_decl = res_app.get("app_area_decl_ha", 0.0)
        ha_legal = res_app.get("app_area_legal_ha", 0.0)
        label_hoje = f"Área a recuperar: ~{ha_decl} ha"
        label_meta = f"Área meta (30m): ~{ha_legal} ha"
    else:
        label_hoje = ESTILO["app"]["label"]
        label_meta = ESTILO["app_meta"]["label"]

    label_app = label_meta if meta else label_hoje

    handles = [plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["perimetro"]["face"],
                             edgecolor=ESTILO["perimetro"]["edge"], alpha=0.7,
                             label=ESTILO["perimetro"]["label"])]
    if imovel["app"]:
        handles.append(plt.Rectangle((0, 0), 1, 1, facecolor=app_est["face"],
                                     alpha=0.8, label=label_app))
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

    # Se a feição for 'app', geramos a APP ideal via Buffer + Intersect no Perímetro (ACTION-020)
    app_meta_polys = _gerar_buffer_app(app_utm, perimetro_utm) if feicao == "app" else []
    if feicao != "app":
        for f in app_utm:
            app_meta_polys.extend(f["polys"])

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

    # 4. Painel da direita: "Como deve ficar (Meta)" (verde sólido com buffer ideal)
    if satelite_ok:
        ax2.imshow(img, extent=[extent_real["xmin"], extent_real["xmax"], extent_real["ymin"], extent_real["ymax"]], origin="upper", zorder=0)
    _desenha(ax2, perimetro_utm, ESTILO["perimetro"], zorder=1, satelite=satelite_ok)
    _desenha(ax2, app_meta_polys, est_em_dia, zorder=2, satelite=satelite_ok)

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

    res_app = geo_app.medir_app(imovel)
    if res_app:
        ha_decl = res_app.get("app_area_decl_ha", 0.0)
        ha_legal = res_app.get("app_area_legal_ha", 0.0)
        label_hoje = f"Área a recuperar: ~{ha_decl} ha"
        label_meta = f"Área meta (30m): ~{ha_legal} ha"
    else:
        label_hoje = "Área que precisa de mata ciliar"
        label_meta = est_em_dia["label"]

    # 6. Legendas curtas
    h1 = [plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["perimetro"]["face"],
                        edgecolor=ESTILO["perimetro"]["edge"], alpha=0.7,
                        label=ESTILO["perimetro"]["label"])]
    if imovel["app"]:
        h1.append(plt.Rectangle((0, 0), 1, 1, facecolor="none", edgecolor=est_hoje["edge"],
                                linewidth=2.0, label=label_hoje))
    ax1.legend(handles=h1, loc="upper right", fontsize=8, framealpha=0.9)

    h2 = [plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["perimetro"]["face"],
                        edgecolor=ESTILO["perimetro"]["edge"], alpha=0.7,
                        label=ESTILO["perimetro"]["label"])]
    if imovel["app"]:
        h2.append(plt.Rectangle((0, 0), 1, 1, facecolor=est_em_dia["face"],
                                alpha=0.8, label=label_meta))
    ax2.legend(handles=h2, loc="upper right", fontsize=8, framealpha=0.9)

    municipio = imovel["attrs"].get("municipio", "")
    uf = imovel["attrs"].get("uf", "")
    fig.suptitle(f"Comparativo da beira do rio - {municipio}/{uf}".strip(" -/"), fontsize=13, weight="bold", y=0.98)

    fig.tight_layout()
    fig.savefig(saida, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return saida
