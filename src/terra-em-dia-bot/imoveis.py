"""Leitura dos dados do imóvel a partir do número do CAR.

No protótipo, simula a consulta de leitura (a interface oficial do CAR já lê
"via API"). Usa um imóvel real de Querência do Norte/PR **anonimizado** — o
cod_imovel verdadeiro fica só em `data/` (gitignored), não aqui.
"""

# Exemplo-âncora (Querência do Norte/PR) — números reais, identidade anonimizada.
IMOVEL_EXEMPLO = {
    "nome": "seu sítio",
    "municipio": "Querência do Norte",
    "uf": "PR",
    "bioma": "Mata Atlântica",
    "modulos_fiscais": 2.98,
    "area_ha": 53.7,            # ~2,98 módulos x 18 ha/módulo (a confirmar)
    "app_mata_ciliar_ha": 2.0,  # APP de rio <= 10 m (faixa de 30 m)
    "rio_largura_texto": "menos de 10 metros de largura",
    "faixa_app_m": 30,
    "rl_proposta_ha": 8.25,
    "rl_exigida_pct": 20,       # Mata Atlântica: Reserva Legal de 20% (art. 12)
}


def buscar_imovel(texto: str) -> dict | None:
    """Devolve os dados do imóvel para o texto informado (nº do CAR).

    Protótipo: qualquer entrada parecida com um código/identificador retorna o
    imóvel-exemplo. Em produção, aqui entraria a consulta real por `cod_imovel`.
    """
    if texto and len(texto.strip()) >= 3:
        return dict(IMOVEL_EXEMPLO)
    return None
