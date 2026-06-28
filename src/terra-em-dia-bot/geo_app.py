import math
from osgeo import osr

def medir_app(imovel: dict) -> dict | None:
    # 1. Encontra a camada app_rio_ate_10
    app_camada = None
    for f in imovel.get("app", []):
        if f.get("tipo") == "app_rio_ate_10":
            app_camada = f
            break
            
    if not app_camada or not app_camada.get("polys"):
        return None

    polys = app_camada["polys"]
    
    # 2. Pega a longitude de referência do 1º ponto para calcular a zona UTM
    try:
        lon_ref = polys[0][0][0][0]
    except (IndexError, TypeError):
        return None

    zona = int((lon_ref + 180) / 6) + 1
    epsg_utm = 31960 + zona

    src = osr.SpatialReference()
    src.ImportFromEPSG(4674)
    src.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    
    dst = osr.SpatialReference()
    dst.ImportFromEPSG(epsg_utm)
    dst.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    
    transform = osr.CoordinateTransformation(src, dst)

    total_area_m2 = 0.0
    total_perimetro_m = 0.0

    for ext, furos in polys:
        # Reprojeta anel externo
        ext_utm = []
        for x, y in ext:
            px, py, _ = transform.TransformPoint(x, y)
            ext_utm.append((px, py))
            
        # Reprojeta furos
        furos_utm = []
        for f in furos:
            f_utm = []
            for x, y in f:
                px, py, _ = transform.TransformPoint(x, y)
                f_utm.append((px, py))
            furos_utm.append(f_utm)

        # Calcula área do anel externo
        n_ext = len(ext_utm)
        if n_ext >= 3:
            a_ext = 0.0
            for i in range(n_ext):
                x1, y1 = ext_utm[i]
                x2, y2 = ext_utm[(i + 1) % n_ext]
                a_ext += x1 * y2 - x2 * y1
            area_p = abs(a_ext) / 2.0
            
            # Subtrai furos
            for f_utm in furos_utm:
                n_f = len(f_utm)
                if n_f >= 3:
                    a_f = 0.0
                    for i in range(n_f):
                        x1, y1 = f_utm[i]
                        x2, y2 = f_utm[(i + 1) % n_f]
                        a_f += x1 * y2 - x2 * y1
                    area_p -= abs(a_f) / 2.0
            total_area_m2 += max(0.0, area_p)

        # Calcula perímetro do anel externo (para a largura média)
        if n_ext >= 2:
            if ext_utm[0] == ext_utm[-1]:
                p_p = sum(math.hypot(ext_utm[i+1][0] - ext_utm[i][0], ext_utm[i+1][1] - ext_utm[i][1]) for i in range(n_ext - 1))
            else:
                p_p = sum(math.hypot(ext_utm[i+1][0] - ext_utm[i][0], ext_utm[i+1][1] - ext_utm[i][1]) for i in range(n_ext - 1))
                p_p += math.hypot(ext_utm[0][0] - ext_utm[-1][0], ext_utm[0][1] - ext_utm[-1][1])
            total_perimetro_m += p_p

    if total_perimetro_m <= 0.0:
        return None

    area_decl_ha = total_area_m2 / 10000.0
    largura_media = 2.0 * total_area_m2 / total_perimetro_m
    
    # Escala para 30 m
    area_legal_ha = area_decl_ha * 30.0 / largura_media if largura_media > 0.0 else 0.0

    largura_media_m = round(largura_media, 1)
    app_falta_m = round(max(0.0, 30.0 - largura_media), 1)
    
    area_decl_ha_r = round(area_decl_ha, 1)
    area_legal_ha_r = round(area_legal_ha, 1)
    app_falta_ha_r = round(max(0.0, area_legal_ha - area_decl_ha), 1)

    return {
        "app_largura_m": largura_media_m,
        "app_faixa_legal_m": 30,
        "app_area_decl_ha": area_decl_ha_r,
        "app_area_legal_ha": area_legal_ha_r,
        "app_falta_m": app_falta_m,
        "app_falta_ha": app_falta_ha_r,
    }
