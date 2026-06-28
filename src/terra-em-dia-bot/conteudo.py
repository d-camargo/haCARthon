"""Textos da conversa do Terra em Dia, na linguagem do Seu Raimundo.

São o roteiro determinístico (funciona sem LLM) e também o tom/base de regras
que o `llm.py` injeta no modelo. Princípios (Briefing + lives): frases curtas,
calorosas, exemplos concretos, zero juridiquês. O assistente ORIENTA, não executa.
"""
import unicodedata


def _n(x) -> str:
    """Número em PT-BR (vírgula decimal), sem zeros à toa: 89.6 -> '89,6'."""
    try:
        s = f"{float(x):.1f}".rstrip("0").rstrip(".")
        return s.replace(".", ",")
    except (TypeError, ValueError):
        return str(x)


SAUDACAO = (
    "Olá, Seu Raimundo! Seja muito bem-vindo. Me mande o *número do CAR* "
    "que está na sua carta. Se for mais fácil, pode mandar uma foto dela aqui."
)

RETOMADA = "Olá de novo, Seu Raimundo! Já estou com as informações da sua terra abertas aqui."

RECEBI_FOTO = "Recebi a foto! Só um instante que vou buscar os dados do seu sítio."

VENDO_CADASTRO = "Achei a sua terra! Vou te mandar um mapa para podermos olhar juntos."

CAPTION_ATUAL = "📍 O seu sítio hoje"
CAPTION_META = "🌳 Assim a beira do rio deve ficar: coberta de mato"
CAPTION_COMPARATIVO = "🔍 A beira do rio: hoje × coberta de mato"


def intro_sitio(an: dict) -> str:
    loc = f" em *{an['municipio']}/{an['uf']}*" if an.get("municipio") else ""
    return (
        f"Pronto, Seu Raimundo! O sítio fica{loc} e tem "
        f"*{_n(an['area_ha'])} hectares* de área."
    )


def resumo_imovel(an: dict) -> str:
    loc = f" em *{an['municipio']}/{an['uf']}*" if an.get("municipio") else ""
    partes = [
        "Não precisa decifrar essa carta sozinho, Seu Raimundo. Vamos por partes que isso fica mais simples.\n"
        f"Pela leitura do seu CAR, vi que seu sítio{loc} tem *{_n(an['area_ha'])} hectares*."
    ]
    
    partes.append("Eu olharia primeiro a *mata ciliar* (mato da beira do rio) e a *Reserva Legal*:")
    
    # 1. Mata Ciliar (APP)
    if an.get("tem_app"):
        partes.append(
            f"Na *beira do rio*, a lei pede para manter o mato numa faixa de *{an['faixa_app_m']} metros* de cada lado. "
            f"No seu sítio, essa faixa dá cerca de *{_n(an['app_mata_ciliar_ha'])} ha*. No mapa dá para ver onde ela fica — "
            "aí vale a pena olhar lá na terra quanto já está coberto de mato e quanto falta."
        )
    else:
        partes.append(
            f"Na *beira do rio*, a regra geral para rios de até 10 metros de largura pede uma faixa de *{an['faixa_app_m']} metros* de mato de cada lado para proteger a água. "
            "Como não tenho o desenho do rio da sua terra aqui, o ideal é você conferir como ficou a marcação no SICAR."
        )
        
    # 2. Reserva Legal (RL)
    if an.get("tem_rl"):
        if an.get("rl_deficit_ha", 0) and an["rl_deficit_ha"] > 0:
            partes.append(
                f"Na *Reserva Legal*, na sua declaração aparecem *{_n(an['rl_proposta_ha'])} ha* declarados. "
                f"Pela área do sítio, a lei pede perto de *{_n(an['rl_exigida_ha'])} ha*. "
                f"Então falta olhar cerca de *{_n(an['rl_deficit_ha'])} ha*."
            )
        else:
            partes.append(
                f"Na *Reserva Legal*, sua declaração aparece certinha e completa com *{_n(an['rl_proposta_ha'])} ha*."
            )
    else:
        partes.append(
            f"Para a *Reserva Legal*, pela área do sítio, a lei pede para guardar *{an['rl_exigida_pct']}%* da propriedade, "
            f"o que dá perto de *{_n(an['rl_exigida_ha'])} ha*. Como não vi uma Reserva declarada localmente para esse código, "
            "confira se ela foi desenhada ou declarada no SICAR."
        )
        
    partes.append("O ideal é conferir isso no mapa do seu imóvel e ajustar no SICAR se estiver diferente.")
    return "\n\n".join(partes)


def explica_mata(an: dict) -> str:
    if an.get("tem_app"):
        return (
            "A *mata ciliar* é aquela vegetação que fica na beira do rio, funcionando "
            "como os cílios dos nossos olhos para proteger a água.\n"
            f"A lei pede para manter o mato numa faixa de *{an['faixa_app_m']} metros* de cada lado do rio. "
            f"No seu sítio, essa faixa dá cerca de *{_n(an['app_mata_ciliar_ha'])} ha*. No mapa dá para ver onde ela fica — "
            "aí vale a pena olhar lá na terra quanto já está coberto de mato e quanto falta."
        )
    return (
        "A *mata ciliar* é aquela vegetação que fica na beira do rio, funcionando "
        "como os cílios dos nossos olhos para proteger a água.\n"
        f"Pela regra, a faixa exigida é de *{an['faixa_app_m']} metros* de mato de cada lado do rio. "
        "Como não temos o desenho desse rio na base local, vale a pena conferir a marcação dele no SICAR."
    )


def sugestao_rl(an: dict) -> str | None:
    if not an.get("tem_rl"):
        return None
    if an.get("rl_deficit_ha", 0) and an["rl_deficit_ha"] > 0:
        return (
            f"Sobre a *Reserva Legal*, vi que você declarou *{_n(an['rl_proposta_ha'])} hectares*.\n"
            f"Mas pela regra do Código Florestal, o esperado seria ter cerca de *{_n(an['rl_exigida_ha'])} hectares*.\n"
            f"Então falta a gente ver como regularizar cerca de *{_n(an['rl_deficit_ha'])} hectares*."
        )
    return (
        f"Olha, a sua *Reserva Legal* está excelente! O cadastro mostra "
        f"*{_n(an['rl_proposta_ha'])} hectares* declarados, cumprindo toda a regra."
    )


PERGUNTA_COMPREENSAO = (
    "Deixa eu te perguntar uma coisa, Seu Raimundo, só pra eu saber se "
    "expliquei direito 😅:\n\n"
    "*por que será que a lei pede pra deixar aquele mato na beira do rio?*\n"
    "(responde com suas palavras mesmo)"
)

ELOGIO_ENTENDEU = (
    "Isso. É por aí mesmo: esse mato protege a água e segura o barranco."
)

REEXPLICA = (
    "É o mato da beira do rio. Ele protege a água e segura a terra quando chove forte."
)


def guia_acao(an: dict) -> str:
    falta_rl = an["tem_rl"] and an["rl_deficit_ha"] > 0
    extra = (
        f"\n• Planejar a recuperação de *{_n(an['rl_deficit_ha'])} hectares* na Reserva Legal"
        if falta_rl else ""
    )
    return (
        "Para a gente resolver isso, o passo a passo é simples:\n"
        "1. Conferir a mata ciliar e as áreas verdes no mapa\n"
        "2. Fazer os ajustes necessários dentro do sistema do SICAR" + extra + "\n"
        "3. No final, *você* ou o seu técnico confirmam a retificação.\n\n"
        "Se quiser, posso te guiar mostrando onde olhar primeiro no sistema."
    )


NAO_ACHEI = (
    "Hmm, não consegui achar esse cadastro. Confere o *número do CAR* na carta "
    "e manda de novo, ou manda uma *foto* dela. 📄"
)

# Regras do Código Florestal em linguagem simples — base para o roteiro e para o LLM.
REGRAS = (
    "Regras (Código Florestal, Lei 12.651/2012), em linguagem simples:\n"
    "- APP de curso d'água (mata ciliar): rio com menos de 10 m de largura exige "
    "30 m de mato preservado em cada margem (art. 4º).\n"
    "- Reserva Legal: fora da Amazônia Legal (ex.: Mata Atlântica/PR) é 20% do "
    "imóvel guardado com vegetação (art. 12).\n"
    "- O aceite/retificação só vale DENTRO do SICAR — o produtor é quem confirma.\n"
    "- Não prometer liberação de crédito: é decisão do banco."
)


def resposta_curta(texto: str, an: dict) -> str:
    """Fallback deterministico para atendimento livre sem LLM."""
    t = _normaliza(texto)
    
    # 1. Objeções e dúvidas específicas de propriedade/posse ou plantio
    
    # Propriedade/posse: "mas a terra é minha", "sou dono"
    if any(p in t for p in ["terra e minha", "sou dono", "e minha terra", "e meu sitio", "sou o dono"]):
        return (
            "É sua mesmo, Seu Raimundo. O CAR é apenas o desenho do sítio no sistema para "
            "mostrar que a terra está regularizada. Primeiro a gente confere se o mapa está certo "
            "e, se precisar, orientamos os ajustes no SICAR."
        )
        
    # Plantio: "tenho que plantar arvore?", "vou ter que plantar?"
    if any(p in t for p in ["plantar arvore", "ter que plantar", "precisa plantar", "tenho que plantar"]):
        return (
            "Não necessariamente. Primeiro nós precisamos conferir se o desenho do seu CAR "
            "está correto. Pode ser apenas um ajuste de demarcação no SICAR. Se depois confirmarmos "
            "que falta mato mesmo, aí sim o técnico local planeja o plantio."
        )

    # Ajuda física com plantio: "voce vai ajudar a plantar?", "voce ajuda a plantar?"
    if any(p in t for p in ["voce vai plantar", "voce ajuda a plantar", "ajudar a plantar", "ajuda a plantar"]):
        return (
            "Eu não consigo plantar as árvores na terra, Seu Raimundo. Minha ajuda é para te mostrar "
            "onde olhar no mapa e orientar o que fazer no SICAR. Se depois precisar de ajuda para plantar, "
            "a Casa da Agricultura local pode apoiar."
        )

    # Perguntas genéricas sobre a propriedade, problemas, cartas, notificações ou ações gerais
    if any(p in t for p in ["como esta", "errado", "problema", "carta", "car", "resumo", "geral", "sitio", "propriedade", "terra", "notificacao", "fazer", "pendencia"]):
        if not any(p in t for p in ["mata", "ciliar", "app", "rio", "beira", "reserva", "legal", "rl", "floresta"]):
            return resumo_imovel(an)

    # 2. Perguntas específicas sobre os temas do CAR
    if any(p in t for p in ["mata", "ciliar", "app", "rio", "beira"]):
        return explica_mata(an)
    if any(p in t for p in ["reserva", "legal", "rl", "floresta"]):
        return sugestao_rl(an) or f"Não vi uma Reserva Legal declarada localmente. Pelo tamanho da terra, a lei pede perto de *{_n(an['rl_exigida_ha'])} ha* (20%). É bom conferir se ela foi desenhada ou declarada no SICAR."
    if any(p in t for p in ["sicar", "botao", "passo", "resolver", "regularizar"]):
        return guia_acao(an)
    if compreendeu(texto):
        return ELOGIO_ENTENDEU
    return (
        "Me conta, Seu Raimundo: você quer ver sobre a *mata ciliar*, a *Reserva Legal* "
        "ou os *passos no SICAR*?"
    )


def pediu_mapa(texto: str) -> bool:
    t = _normaliza(texto)
    return any(p in t for p in ["mapa", "desenho", "imagem", "foto da terra"])


def pediu_meta(texto: str) -> bool:
    t = _normaliza(texto)
    return any(
        p in t
        for p in [
            "deve ficar",
            "como fica",
            "como ficaria",
            "como deveria",
            "o certo",
            "corrigir",
            "arrumar",
            "depois",
            "segundo mapa",
            "mapa 2",
            "meta",
        ]
    )

_PALAVRAS_OK = [
    "agua", "proteg", "barranc", "eros", "rio", "nascente", "enchente",
    "seca", "desliz", "assorea", "terra cai", "chuva", "margem", "beira", "raiz",
]


def _normaliza(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


def compreendeu(resposta: str) -> bool:
    """Heurística determinística (reproduz a métrica sem custo de LLM)."""
    t = _normaliza(resposta)
    return any(p in t for p in _PALAVRAS_OK)
