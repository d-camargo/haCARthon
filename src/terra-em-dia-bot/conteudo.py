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
    "Boa tarde, Seu Raimundo! 🌱 Eu sou o *Terra em Dia*.\n"
    "Pode tirar suas dúvidas do CAR aqui mesmo, no Zap.\n\n"
    "Pra começar, me manda o *número do seu CAR* (tá na carta que você "
    "recebeu) — ou uma *foto da carta* que eu dou um jeito. 📄"
)

RECEBI_FOTO = "Recebi a sua carta, obrigado! 📄 Já tô puxando aqui o seu cadastro..."

VENDO_CADASTRO = "Achei seu sítio ✅ Deixa eu te mandar o mapa dele..."

CAPTION_ATUAL = "📍 O seu sítio hoje"
CAPTION_META = "🌳 Assim a beira do rio deve ficar: coberta de mato"


def intro_sitio(an: dict) -> str:
    return (
        f"Esse é o seu sítio em *{an['municipio']}/{an['uf']}* — "
        f"*{_n(an['area_ha'])} hectares*. 👆"
    )


PERGUNTA_MOTIVO = (
    "Deixa eu te perguntar antes: você sabe *por que* recebeu essa carta? 🤔\n"
    "(pode chutar, sem medo)"
)

_MOTIVO_OK = ["mata", "ciliar", "reserva", "app", "ambient", "floresta", "rio",
              "arvore", "árvore", "verde", "lei"]


def reage_motivo(resposta: str) -> str:
    t = _normaliza(resposta)
    if any(p in t for p in _MOTIVO_OK):
        return "Isso, é bem por aí! 👏 Deixa eu te mostrar direitinho:"
    return "Tranquilo, é pra isso que eu tô aqui 🙂 Olha só:"


def explica_mata(an: dict) -> str:
    return (
        "A carta fala da *mata ciliar* 🌿 — a faixa de mato na beira do rio.\n"
        f"A lei pede *{an['faixa_app_m']} passos* de mato de cada lado, "
        f"porque o seu rio tem {an['rio_largura']}. É essa faixa do mapa 👇"
    )


def sugestao_rl(an: dict) -> str | None:
    if not an["tem_rl"]:
        return None
    if an["rl_deficit_ha"] > 0:
        return (
            f"Tem também a *Reserva Legal* 🌳: a lei pede uns *{_n(an['rl_exigida_ha'])} ha* "
            f"e hoje a sua tem *{_n(an['rl_proposta_ha'])} ha*.\n"
            f"Faltam uns *{_n(an['rl_deficit_ha'])} ha* — dá pra *ampliar a reserva que "
            "você já tem* ou *juntar com a mata do rio*, formando um corredor. "
            "A gente acha o melhor lugar com calma. 😉"
        )
    return f"Sua *Reserva Legal* já está completinha (~{_n(an['rl_proposta_ha'])} ha) 👏."


PERGUNTA_COMPREENSAO = (
    "Deixa eu te perguntar uma coisa, Seu Raimundo, só pra eu saber se "
    "expliquei direito 😅:\n\n"
    "*por que será que a lei pede pra deixar aquele mato na beira do rio?*\n"
    "(responde com suas palavras mesmo)"
)

ELOGIO_ENTENDEU = (
    "É isso aí! 👏 Você entendeu certinho. Esse mato protege a água e segura o "
    "barranco — sem ele, o rio assoreia e a terra escorrega."
)

REEXPLICA = (
    "Quase! Deixa eu dizer de outro jeito 😉\n"
    "esse mato na beira do rio serve pra *proteger a sua água* e *segurar o "
    "barranco*, pra terra não cair no rio quando chove forte. Faz sentido?"
)


def guia_acao(an: dict) -> str:
    falta_rl = an["tem_rl"] and an["rl_deficit_ha"] > 0
    extra = (
        f"\n• Completar uns *{_n(an['rl_deficit_ha'])} ha* de mato na Reserva Legal"
        if falta_rl else ""
    )
    return (
        "Agora o caminho pra ficar em dia 📋:\n"
        "• Confirmar a mata ciliar na beira do rio" + extra + "\n"
        "• Marcar isso no sistema do CAR (SICAR)\n\n"
        "No fim, *só você aperta o botão* no SICAR — é você que confirma, "
        "ninguém faz por você. 🤝\n\n"
        "Resolvendo, você fica regular e *entra na fila do crédito rural* 💰 "
        "(o banco ainda analisa, mas sem o CAR em dia nem dá pra começar).\n\n"
        "Quer que eu te mande o passo a passo com as telas? É só falar."
    )


FECHO = (
    "Tamo junto, Seu Raimundo! 🌳 Qualquer dúvida é só chamar aqui. "
    "*Terra em Dia* — o Código Florestal explicado pra *sua* terra."
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
