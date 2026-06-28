"""Análise legal do imóvel (Código Florestal) a partir dos dados do cadastro.

Transforma as geometrias/atributos de `cadastro.carregar_imovel` em números
amigáveis para a explicação e o mapa: faixa de APP, Reserva Legal exigida ×
proposta e o déficit. Pura e testável (sem rede).
"""

# Reserva Legal fora da Amazônia Legal (Mata Atlântica/PR): 20% (art. 12, Lei 12.651/2012).
RL_PCT_PADRAO = 20


def _num(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def analisar(imovel: dict) -> dict:
    a = imovel.get("attrs", {})
    area = _num(a.get("area"))
    modulos = _num(a.get("m_fiscal"))

    # Mata ciliar (APP de rio <= 10 m): usa o tema app_rio_ate_10 se houver.
    app = imovel.get("app", [])
    mata = next((f for f in app if f["tipo"] == "app_rio_ate_10"), app[0] if app else None)
    app_ha = _num(mata.get("area_ha")) if mata else 0.0

    tem_rl = bool(imovel.get("rl"))
    rl_proposta = sum(_num(f.get("area_ha")) for f in imovel.get("rl", []))
    rl_exigida = round(area * RL_PCT_PADRAO / 100, 1)
    deficit = round(max(0.0, rl_exigida - rl_proposta), 1) if tem_rl else None

    res = {
        "municipio": a.get("municipio", ""),
        "uf": a.get("uf", ""),
        "area_ha": round(area, 1),
        "modulos": round(modulos, 2),
        "tem_app": bool(app),
        "app_mata_ciliar_ha": round(app_ha, 1),
        "campos_futebol": max(1, round(app_ha)) if app_ha else 0,
        "faixa_app_m": 30,
        "rio_largura": "menos de 10 metros",
        "tem_rl": tem_rl,
        "rl_proposta_ha": round(rl_proposta, 1),
        "rl_exigida_pct": RL_PCT_PADRAO,
        "rl_exigida_ha": rl_exigida,
        "rl_deficit_ha": deficit,
    }

    try:
        import geo_app
        m = geo_app.medir_app(imovel)
        if m:
            res.update(m)
    except Exception:
        pass

    return res
