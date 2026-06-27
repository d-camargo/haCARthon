"""Textos da conversa do Terra em Dia, na linguagem do Seu Raimundo.

São o roteiro determinístico (funciona sem LLM) e também o tom/base de regras
que o `llm.py` injeta no modelo. Princípios (Briefing + lives): frases curtas,
calorosas, exemplos concretos, zero juridiquês. O assistente ORIENTA, não executa.
"""
import unicodedata

SAUDACAO = (
    "Boa tarde, Seu Raimundo! 🌱 Eu sou o *Terra em Dia*.\n"
    "Pode tirar suas dúvidas do CAR aqui mesmo, no Zap.\n\n"
    "Pra começar, me manda o *número do seu CAR* (tá na carta que você "
    "recebeu) — ou uma *foto da carta* que eu dou um jeito. 📄"
)

RECEBI_FOTO = "Recebi a sua carta, obrigado! 📄 Já tô puxando aqui o seu cadastro..."

VENDO_CADASTRO = "Achei seu sítio ✅ Deixa eu te mandar o mapa dele..."


def explicacao(an: dict) -> str:
    """Explica APP (mata ciliar) e Reserva Legal com os números reais do imóvel."""
    txt = (
        f"Esse é o seu sítio em *{an['municipio']}/{an['uf']}* — são "
        f"*{an['area_ha']} hectares* 👆\n\nVou te explicar com calma o que a "
        "lei pede aí na sua terra:\n\n"
    )
    if an["tem_app"]:
        txt += (
            "🔵 *Mata ciliar* (a faixa azul, na beira do rio): a lei pede "
            f"*{an['faixa_app_m']} passos* de mato de cada lado, porque o seu rio "
            f"tem {an['rio_largura']}. Dá uns *{an['campos_futebol']} campos de "
            "futebol* de faixa pra cuidar. Esse mato segura o barranco e protege "
            "a sua água 💧.\n\n"
        )
    if an["tem_rl"]:
        txt += (
            "🟢 *Reserva Legal* (a área verde): a lei pede *"
            f"{an['rl_exigida_pct']}%* do sítio guardado com mato — uns "
            f"*{an['rl_exigida_ha']} hectares*. Hoje a sua reserva proposta tem "
            f"*{an['rl_proposta_ha']} ha*"
        )
        if an["rl_deficit_ha"] > 0:
            txt += f", então *falta uns {an['rl_deficit_ha']} ha* pra completar.\n\n"
        else:
            txt += ", e já está completa 👏.\n\n"
    return txt.strip()


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
        f"\n• Completar uns *{an['rl_deficit_ha']} ha* de mato na Reserva Legal"
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
