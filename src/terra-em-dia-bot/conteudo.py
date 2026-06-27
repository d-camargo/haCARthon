"""Textos da conversa do Terra em Dia, na linguagem do Seu Raimundo.

Princípios (do Briefing e das lives): frases curtas, calorosas, **exemplos
concretos** (passos, campo de futebol), sem juridiquês. O assistente **orienta**,
não executa — o aceite é sempre no SICAR.
"""
import unicodedata

SAUDACAO = (
    "Boa tarde, Seu Raimundo! 🌱 Eu sou o *Terra em Dia*.\n"
    "Pode me mandar suas dúvidas do CAR aqui mesmo, no Zap.\n\n"
    "Pra começar, me confirma o *número do seu CAR* (tá na carta que você "
    "recebeu) — ou manda uma *foto da carta* que eu dou um jeito. 📄"
)

RECEBI_FOTO = (
    "Recebi a sua carta, obrigado! 📄 Já tô vendo aqui o seu cadastro..."
)


def explicacao_app(imovel: dict) -> str:
    """Explica a APP de curso d'água (mata ciliar) na terra do produtor."""
    campos = max(1, round(imovel["app_mata_ciliar_ha"]))
    return (
        f"Achei o {imovel['nome']} em *{imovel['municipio']}/{imovel['uf']}* ✅\n\n"
        "A carta fala da *mata ciliar* — aquela faixa de mato na *beira do rio*.\n\n"
        f"A lei pede *{imovel['faixa_app_m']} passos* "
        f"(uns {imovel['faixa_app_m']} metros) de mato de *cada lado* do rio, "
        f"porque o seu rio tem {imovel['rio_largura_texto']}.\n\n"
        f"No seu caso, isso dá uns *{campos} campos de futebol* de faixa pra "
        "cuidar. Esse mato segura o barranco e protege a sua água 💧."
    )

PERGUNTA_COMPREENSAO = (
    "Deixa eu te perguntar uma coisa, Seu Raimundo, só pra eu saber se "
    "expliquei direito 😅:\n\n"
    "*por que será que a lei pede pra deixar esse mato na beira do rio?*\n"
    "(responde com suas palavras mesmo)"
)

ELOGIO_ENTENDEU = (
    "É isso aí! 👏 Você entendeu certinho. Esse mato protege a água e segura "
    "o barranco — sem ele, o rio assoreia e a terra escorrega."
)

REEXPLICA = (
    "Quase! Deixa eu dizer de outro jeito: 😉\n"
    "esse mato na beira do rio serve pra *proteger a sua água* e *segurar o "
    "barranco*, pra terra não cair dentro do rio quando chove forte.\n"
    "Faz sentido?"
)


def guia_acao(imovel: dict) -> str:
    """Passo a passo até o botão do SICAR + o benefício."""
    return (
        "Agora o caminho pra ficar em dia, bem rapidinho 📋:\n\n"
        "1️⃣ Confirmar essa faixa de mato no sistema do CAR (SICAR)\n"
        "2️⃣ Cuidar do que faltar de mato na beira do rio\n"
        "3️⃣ No fim, *só você aperta o botão* no SICAR — é você que confirma, "
        "ninguém faz por você.\n\n"
        "Resolvendo isso, você fica regular e *destrava o crédito rural* 💰 "
        "(o banco ainda analisa, mas sem o CAR em dia nem entra na fila).\n\n"
        "Quer que eu te mande o passo a passo com as telas? É só falar *sim*."
    )

FECHO = (
    "Tamo junto, Seu Raimundo! 🌳\n"
    "Qualquer dúvida, é só chamar aqui no Zap. *Terra em Dia* — o Código "
    "Florestal explicado pra *sua* terra."
)

NAO_ACHEI = (
    "Hmm, não consegui ler esse número. Tenta de novo: digita o *número do "
    "CAR* que tá na carta, ou manda uma *foto* dela. 📄"
)


# Palavras que indicam que o produtor entendeu a função da mata ciliar.
_PALAVRAS_OK = [
    "agua", "proteg", "barranc", "eros", "rio", "nascente", "enchente",
    "seca", "desliz", "assorea", "terra cai", "chuva", "margem", "beira",
]


def _normaliza(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto or "")
    t = "".join(c for c in t if not unicodedata.combining(c))
    return t.lower()


def compreendeu(resposta: str) -> bool:
    """Heurística simples: a resposta cita alguma ideia central correta.

    (No upgrade com LLM, esta função vira uma chamada agnóstica de modelo.)
    """
    t = _normaliza(resposta)
    return any(p in t for p in _PALAVRAS_OK)
