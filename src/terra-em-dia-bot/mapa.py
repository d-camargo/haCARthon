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


def _desenha(ax, polys, est, zorder=1, satelite=False, transform=None):
    for ext, _furos in polys:
        if len(ext) >= 3:
            lw = est["lw"] * 1.5 if satelite else est["lw"]
            ax.add_patch(
                MplPolygon(ext, closed=True, facecolor=est["face"],
                           edgecolor=est["edge"], linewidth=lw, alpha=est["alpha"],
                           zorder=zorder, transform=transform)
            )


def _rotate_pt(x, y, cx, cy, theta_deg):
    import math
    rad = math.radians(theta_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    rx = cx + (x - cx) * cos_a - (y - cy) * sin_a
    ry = cy + (x - cx) * sin_a + (y - cy) * cos_a
    return rx, ry


def _rotate_polys(polys, cx, cy, theta):
    rotated = []
    for ext, furos in polys:
        ext_rot = [_rotate_pt(tx, ty, cx, cy, theta) for tx, ty in ext]
        furos_rot = [[_rotate_pt(tx, ty, cx, cy, theta) for tx, ty in f] for f in furos]
        rotated.append((ext_rot, furos_rot))
    return rotated


def _calcular_rotacao(imovel: dict, perimetro_utm: list, app_utm: list):
    import numpy as np
    import math
    
    pts = []
    for ext, _ in perimetro_utm:
        for x, y in ext:
            pts.append((x, y))
            
    if not pts:
        return 0.0, 0.0, 0.0
        
    pts = np.array(pts)
    cx, cy = np.mean(pts, axis=0)
    
    pts_centered = pts - [cx, cy]
    if len(pts_centered) < 2:
        return cx, cy, 0.0
        
    cov = np.cov(pts_centered.T)
    if cov.shape != (2, 2) or np.any(np.isnan(cov)) or np.any(np.isinf(cov)):
        return cx, cy, 0.0
        
    evals, evecs = np.linalg.eigh(cov)
    idx_max = np.argmax(evals)
    v_principal = evecs[:, idx_max]
    
    angle_base = math.degrees(math.atan2(v_principal[1], v_principal[0]))
    candidatos = [angle_base, angle_base + 90, angle_base + 180, angle_base + 270]
    
    app_pts = []
    for f in app_utm:
        for ext, _ in f["polys"]:
            for x, y in ext:
                app_pts.append((x, y))
                
    if not app_pts:
        return cx, cy, 90.0 - angle_base
        
    app_pts = np.array(app_pts)
    app_cx, app_cy = np.mean(app_pts, axis=0)
    
    v_app = np.array([app_cx - cx, app_cy - cy])
    
    melhor_theta = 0.0
    menor_y = 1e18
    
    for theta in candidatos:
        rot_deg = 90.0 - theta
        rad = math.radians(rot_deg)
        y_rot = v_app[0] * math.sin(rad) + v_app[1] * math.cos(rad)
        if y_rot < menor_y:
            menor_y = y_rot
            melhor_theta = rot_deg
            
    return cx, cy, melhor_theta


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

    # Calcula rotação inteligente e centróide
    cx, cy, theta = _calcular_rotacao(imovel, perimetro_utm, app_utm)

    # Define o que desenhar para a APP
    if meta:
        app_desenhar = _gerar_buffer_app(app_utm, perimetro_utm)
    else:
        app_desenhar = []
        for f in app_utm:
            app_desenhar.extend(f["polys"])

    # Rotaciona para calcular o bounding box correto em coordenadas rotacionadas
    perimetro_rot = _rotate_polys(perimetro_utm, cx, cy, theta)
    app_rot = _rotate_polys(app_desenhar, cx, cy, theta)
    rl_rot = []
    if not meta:
        for f in rl_utm:
            rl_rot.extend(_rotate_polys(f["polys"], cx, cy, theta))

    b_rot = [9e9, 9e9, -9e9, -9e9]
    _bounds(perimetro_rot, b_rot)
    _bounds(app_rot, b_rot)
    _bounds(rl_rot, b_rot)

    mx = (b_rot[2] - b_rot[0]) * 0.08 + 1e-4
    my = (b_rot[3] - b_rot[1]) * 0.08 + 1e-4
    xmin_rot = b_rot[0] - mx
    ymin_rot = b_rot[1] - my
    xmax_rot = b_rot[2] + mx
    ymax_rot = b_rot[3] + my

    # 1. Calcula os limites do download em coordenadas não rotacionadas com margem maior (evitar cantos brancos)
    import math
    dist_max = 100.0
    for ext, _ in perimetro_utm:
        for x, y in ext:
            dist_max = max(dist_max, math.hypot(x - cx, y - cy))

    mx_dl = dist_max * 1.5
    xmin_dl = cx - mx_dl
    ymin_dl = cy - mx_dl
    xmax_dl = cx + mx_dl
    ymax_dl = cy + mx_dl

    # 2. Tenta baixar a imagem de satélite (Esri World Imagery)
    import urllib.request
    import urllib.parse
    import io
    from PIL import Image

    img = None
    try:
        # A escala é baseada nas dimensões do download real
        aspect = (ymax_dl - ymin_dl) / (xmax_dl - xmin_dl) if (xmax_dl - xmin_dl) > 0 else 1.0
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
            "bbox": f"{xmin_dl},{ymin_dl},{xmax_dl},{ymax_dl}",
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

    # Aplica transformação afim no Matplotlib para rotação
    import matplotlib.transforms as mtransforms
    t = mtransforms.Affine2D().translate(-cx, -cy).rotate_deg(theta).translate(cx, cy) + ax.transData

    if satelite_ok:
        ax.imshow(img, extent=[extent_real["xmin"], extent_real["xmax"], extent_real["ymin"], extent_real["ymax"]],
                  origin="upper", zorder=0, transform=t)

    # 3. Desenha as feições
    _desenha(ax, perimetro_utm, ESTILO["perimetro"], zorder=1, satelite=satelite_ok, transform=t)
    app_est = ESTILO["app_meta"] if meta else ESTILO["app"]

    _desenha(ax, app_desenhar, app_est, zorder=2, satelite=satelite_ok, transform=t)
    if not meta:  # no mapa-meta, foco na mata ciliar
        for f in rl_utm:
            _desenha(ax, f["polys"], ESTILO["rl"], zorder=2, satelite=satelite_ok, transform=t)

    ax.set_xlim(xmin_rot, xmax_rot)
    ax.set_ylim(ymin_rot, ymax_rot)
    ax.set_aspect("equal")

    # Seta do Norte com Rosa dos Ventos de imagem asset (ACTION-030)
    from matplotlib.offsetbox import OffsetImage, AnnotationBbox
    try:
        caminho_seta = Path(__file__).parent / "assets" / "seta_norte.png"
        img_seta = Image.open(caminho_seta)
        img_girada = img_seta.rotate(theta, expand=True)
        imagebox = OffsetImage(img_girada, zoom=0.15)
        ab = AnnotationBbox(imagebox, (0.92, 0.85), xycoords='axes fraction', frameon=False, zorder=5)
        ax.add_artist(ab)
    except Exception:
        pass

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

    # Legenda fora do mapa (margem inferior) (ACTION-028)
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.07), ncol=2, fontsize=9, framealpha=0.9)

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
    fig.subplots_adjust(bottom=0.15)
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

    # Calcula rotação inteligente e centróide
    cx, cy, theta = _calcular_rotacao(imovel, perimetro_utm, app_utm)

    # Se a feição for 'app', geramos a APP ideal via Buffer + Intersect no Perímetro (ACTION-020)
    app_meta_polys = _gerar_buffer_app(app_utm, perimetro_utm) if feicao == "app" else []
    if feicao != "app":
        for f in app_utm:
            app_meta_polys.extend(f["polys"])

    # 1. Calcula limites de zoom focados na feição escolhida no espaço rotacionado
    b_rot = [9e9, 9e9, -9e9, -9e9]
    if feicao == "app":
        app_rot = []
        for f in app_utm:
            app_rot.extend(_rotate_polys(f["polys"], cx, cy, theta))
        _bounds(app_rot, b_rot)
    else:
        rl_rot = []
        for f in rl_utm:
            rl_rot.extend(_rotate_polys(f["polys"], cx, cy, theta))
        _bounds(rl_rot, b_rot)
        
    if b_rot[0] > 8e9:
        return None  # Feição vazia
        
    mx = (b_rot[2] - b_rot[0]) * 0.18 + 1e-4
    my = (b_rot[3] - b_rot[1]) * 0.18 + 1e-4
    xmin_rot = b_rot[0] - mx
    ymin_rot = b_rot[1] - my
    xmax_rot = b_rot[2] + mx
    ymax_rot = b_rot[3] + my

    # Rotaciona de volta as 4 quinas do bbox de zoom rotacionado para saber a bbox de download original
    corners_rot = [
        (xmin_rot, ymin_rot),
        (xmax_rot, ymin_rot),
        (xmin_rot, ymax_rot),
        (xmax_rot, ymax_rot)
    ]
    corners_unrot = [_rotate_pt(tx, ty, cx, cy, -theta) for tx, ty in corners_rot]
    xmin_dl = min(x for x, y in corners_unrot)
    ymin_dl = min(y for x, y in corners_unrot)
    xmax_dl = max(x for x, y in corners_unrot)
    ymax_dl = max(y for x, y in corners_unrot)

    # Adiciona margem de segurança no download para evitar cantos brancos ao girar
    mx_dl = (xmax_dl - xmin_dl) * 0.15 + 1e-4
    my_dl = (ymax_dl - ymin_dl) * 0.15 + 1e-4
    xmin_dl -= mx_dl
    ymin_dl -= my_dl
    xmax_dl += mx_dl
    ymax_dl += my_dl

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), dpi=130)

    # 2. Tenta baixar a imagem de satélite para o bbox de zoom original
    img = None
    import math
    import urllib.request
    import urllib.parse
    import io
    from PIL import Image
    try:
        aspect = (ymax_dl - ymin_dl) / (xmax_dl - xmin_dl) if (xmax_dl - xmin_dl) > 0 else 1.0
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
            "bbox": f"{xmin_dl},{ymin_dl},{xmax_dl},{ymax_dl}",
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

    # Cria transforms afins para cada eixo
    import matplotlib.transforms as mtransforms
    t1 = mtransforms.Affine2D().translate(-cx, -cy).rotate_deg(theta).translate(cx, cy) + ax1.transData
    t2 = mtransforms.Affine2D().translate(-cx, -cy).rotate_deg(theta).translate(cx, cy) + ax2.transData

    # 3. Painel da esquerda: "Hoje" (contorno/chão apenas)
    if satelite_ok:
        ax1.imshow(img, extent=[extent_real["xmin"], extent_real["xmax"], extent_real["ymin"], extent_real["ymax"]],
                  origin="upper", zorder=0, transform=t1)
    _desenha(ax1, perimetro_utm, ESTILO["perimetro"], zorder=1, satelite=satelite_ok, transform=t1)
    for f in app_utm:
        _desenha(ax1, f["polys"], est_hoje, zorder=2, satelite=satelite_ok, transform=t1)

    # 4. Painel da direita: "Como deve ficar (Meta)" (verde sólido com buffer ideal)
    if satelite_ok:
        ax2.imshow(img, extent=[extent_real["xmin"], extent_real["xmax"], extent_real["ymin"], extent_real["ymax"]],
                  origin="upper", zorder=0, transform=t2)
    _desenha(ax2, perimetro_utm, ESTILO["perimetro"], zorder=1, satelite=satelite_ok, transform=t2)
    _desenha(ax2, app_meta_polys, est_em_dia, zorder=2, satelite=satelite_ok, transform=t2)

    # Adiciona a cota visual de 30m no painel da solução (ax2) no centro rotacionado
    cx_anno = (xmin_rot + xmax_rot) / 2
    cy_anno = (ymin_rot + ymax_rot) / 2
    ax2.annotate(
        "Faixa legal:\n30m da margem",
        xy=(cx_anno, cy_anno),
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
        ax.set_xlim(xmin_rot, xmax_rot)
        ax.set_ylim(ymin_rot, ymax_rot)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)

        # Seta do Norte com Rosa dos Ventos de imagem asset (ACTION-030)
        from matplotlib.offsetbox import OffsetImage, AnnotationBbox
        try:
            caminho_seta = Path(__file__).parent / "assets" / "seta_norte.png"
            img_seta = Image.open(caminho_seta)
            img_girada = img_seta.rotate(theta, expand=True)
            imagebox = OffsetImage(img_girada, zoom=0.15)
            ab = AnnotationBbox(imagebox, (0.92, 0.85), xycoords='axes fraction', frameon=False, zorder=5)
            ax.add_artist(ab)
        except Exception:
            pass

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

    # 6. Legendas curtas (ACTION-028)
    h1 = [plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["perimetro"]["face"],
                        edgecolor=ESTILO["perimetro"]["edge"], alpha=0.7,
                        label=ESTILO["perimetro"]["label"])]
    if imovel["app"]:
        h1.append(plt.Rectangle((0, 0), 1, 1, facecolor="none", edgecolor=est_hoje["edge"],
                                linewidth=2.0, label=label_hoje))
    ax1.legend(handles=h1, loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=8, framealpha=0.9)

    h2 = [plt.Rectangle((0, 0), 1, 1, facecolor=ESTILO["perimetro"]["face"],
                        edgecolor=ESTILO["perimetro"]["edge"], alpha=0.7,
                        label=ESTILO["perimetro"]["label"])]
    if imovel["app"]:
        h2.append(plt.Rectangle((0, 0), 1, 1, facecolor=est_em_dia["face"],
                                alpha=0.8, label=label_meta))
    ax2.legend(handles=h2, loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=8, framealpha=0.9)

    # Inserção do Quadro de Áreas (ACTION-031)
    import analise
    an = analise.analisar(imovel)
    if feicao == "app":
        q_decl = an.get("app_area_decl_ha", 0.0)
        q_legal = an.get("app_area_legal_ha", 0.0)
        q_falta = an.get("app_falta_ha", 0.0)
        texto_quadro = (
            "RESUMO DA ÁREA (Beira do Rio)\n"
            f"• O que você tem hoje: {q_decl} ha\n"
            f"• O que a lei exige: {q_legal} ha\n"
            f"• Falta recuperar: {q_falta} ha"
        )
    else:
        q_decl = an.get("rl_proposta_ha", 0.0)
        q_legal = an.get("rl_exigida_ha", 0.0)
        q_falta = an.get("rl_deficit_ha", 0.0)
        texto_quadro = (
            "RESUMO DA ÁREA (Reserva Legal)\n"
            f"• O que você tem hoje: {q_decl} ha\n"
            f"• O que a lei exige: {q_legal} ha\n"
            f"• Falta recuperar: {q_falta} ha"
        )

    fig.text(0.5, 0.03, texto_quadro, ha="center", va="bottom", fontsize=10, 
             bbox=dict(facecolor='#f0f0f0', alpha=0.9, edgecolor='#cccccc', boxstyle='round,pad=0.6'))

    municipio = imovel["attrs"].get("municipio", "")
    uf = imovel["attrs"].get("uf", "")
    fig.suptitle(f"Comparativo da beira do rio - {municipio}/{uf}".strip(" -/"), fontsize=13, weight="bold", y=0.98)

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.25)
    fig.savefig(saida, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return saida
