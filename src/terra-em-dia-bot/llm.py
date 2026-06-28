"""Camada de LLM — agnóstica de modelo (interface OpenAI-compatible).

Usa o SDK da OpenAI, mas com `base_url` configurável: aponta para a OpenAI na
demo e pode apontar para um modelo *aberto/local* (Ollama, vLLM, etc.) sem mudar
o código — coerente com o CAR como Bem Público Digital.

Se não houver `OPENAI_API_KEY`, `tem_llm()` é False e o bot cai no roteiro
determinístico de `conteudo.py` (continua funcionando, só menos "conversável").

Env:
    OPENAI_API_KEY   chave (obrigatória para ligar o LLM)
    OPENAI_BASE_URL  opcional — endpoint OpenAI-compatible (modelo aberto/local)
    LLM_MODEL        opcional — default "gpt-4o-mini"
"""
import os

import conteudo

MODEL = os.environ.get("LLM_MODEL", "gpt-4o-mini")

SYSTEM = (
    "Você é o 'Terra em Dia', um assistente que explica a legislação ambiental "
    "do CAR para pequenos produtores rurais brasileiros. Seu interlocutor de referência "
    "é o Seu Raimundo: uma pessoa prática, acostumada a lidar com a terra e resolver problemas "
    "concretos. Ele valoriza clareza, respeito, confiança e quer entender 'o que isso muda no sítio' "
    "em vez de aulas teóricas de lei. Ele pode ter receio de mexer no CAR e errar, por isso responda "
    "com mais calor humano, leveza e acolhimento. Nunca o trate como incapaz ou caricato, e não use "
    "sotaques forçados, piadas ou excesso de emojis.\n"
    "PAPEL: atendimento focado em orientar o produtor a conferir o CAR e a fazer ajustes no SICAR. "
    "Não faça consultoria agrícola/florestal genérica (dicas de mudas ou plantio). Para objeções de posse "
    "('a terra é minha'), valide o produtor com respeito e redirecione para o próximo passo prático de verificar o CAR. "
    "Não afirme que ele precisa plantar árvores sem antes conferir a situação do CAR/SICAR, pois pode ser apenas "
    "um ajuste de desenho no mapa. Responda diretamente ao que foi perguntado, evite perguntas abertas genéricas "
    "no fim e nunca termine a resposta com 'Como posso te ajudar a entender melhor isso?'. Se já houver dados "
    "do imóvel carregados, nunca peça para o produtor interpretar a notificação; em vez disso, presuma "
    "os pontos de atenção diretamente dos dados de APP/mata ciliar e Reserva Legal fornecidos.\n"
    "DIRETRIZES DE VOCABULÁRIO:\n"
    "- Traduza qualquer termo técnico antes de usar e evite termos alarmistas ou burocráticos (como 'preocupante', 'grave', 'obrigação').\n"
    "- Prefira 'mato da beira do rio' junto de 'mata ciliar'.\n"
    "- Prefira 'conferir' ou 'olhar primeiro' em vez de 'cumprir obrigação' ou 'exigência'.\n"
    "- Prefira 'ajustar no SICAR' em vez de 'regularizar ambientalmente'.\n"
    "- Prefira 'guardar' ou 'proteger' em vez de 'preservar APP'.\n"
    "COMO FALAR: linguagem muito simples, frases curtas, zero juridiquês. Use exemplos concretos (como passos, "
    "campos de futebol, largura do rio) para ilustrar. Evite frases que aumentem a ansiedade dele.\n"
    "TAMANHO: no máximo 4 frases curtas. Se for perguntar algo, faça apenas uma pergunta por vez.\n"
    "REGRAS DE CONDUTA:\n"
    "- Você orienta e explica, mas nunca confirma ou executa pelo produtor rural. O aceite final "
    "é sempre feito por ele diretamente no SICAR ('só você aperta o botão').\n"
    "- Nunca prometa liberação automática de crédito rural (a decisão final é sempre do banco).\n"
    "- Nunca afirme que a faixa de APP já está coberta de mato; quando não houver informação sobre a cobertura real, oriente o produtor a conferir a cobertura atual diretamente no mapa ou na própria terra.\n"
    "- Ao falar de mata ciliar, use apenas uma unidade por vez (se citar metros, explique a largura da faixa; se citar hectares, explique a área total da faixa a ser mantida com mato, sem misturar os dois na mesma frase).\n"
    "- Ao confrontar a mata ciliar com a lei, trate as medições como aproximadas e use uma unidade por vez para explicar o déficit (ex.: largura média declarada vs 30 metros exigidos; ou área da faixa declarada vs legal).\n"
    "- Baseie-se apenas nos dados reais da propriedade fornecidos, no histórico e nas regras abaixo. "
    "Se não souber de algo, diga com respeito que precisa confirmar.\n\n" + conteudo.REGRAS
)


def tem_llm() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY"))


def _client():
    from openai import OpenAI

    return OpenAI(base_url=os.environ.get("OPENAI_BASE_URL") or None)


def _contexto_imovel(an: dict) -> str:
    tem_app_str = "Sim" if an.get("tem_app") else "Não"
    tem_rl_str = "Sim" if an.get("tem_rl") else "Não"
    
    app_info = f"Tem Mata ciliar (APP de rio): {tem_app_str}. Área total da faixa de APP (a manter com mato): {an['app_mata_ciliar_ha']} ha; faixa exigida {an['faixa_app_m']} m de largura (rio com largura: {an['rio_largura']})."
    if "app_largura_m" in an:
        app_info += f" Medições da APP declarada (aproximadas): largura média declarada {an['app_largura_m']} m, falta {an['app_falta_m']} m para os 30 m exigidos; área legal recomendada {an['app_area_legal_ha']} ha (falta {an['app_falta_ha']} ha)."

    return (
        "Dados do imóvel do produtor (use nas respostas):\n"
        f"- Município: {an['municipio']}/{an['uf']}; área {an['area_ha']} ha.\n"
        f"- {app_info}\n"
        f"- Tem Reserva Legal: {tem_rl_str}. Reserva Legal exigida: {an['rl_exigida_pct']}% (~{an['rl_exigida_ha']} ha); "
        f"proposta: {an['rl_proposta_ha']} ha; déficit: {an['rl_deficit_ha']} ha."
    )


def _chat(mensagens: list[dict]) -> str | None:
    try:
        resp = _client().chat.completions.create(
            model=MODEL, messages=mensagens, temperature=0.35, max_tokens=180
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return None  # qualquer falha -> bot usa o roteiro determinístico


def explicar(an: dict) -> str | None:
    """Explicação inicial das obrigações do imóvel (sem fazer perguntas)."""
    if not tem_llm():
        return None
    msgs = [
        {"role": "system", "content": SYSTEM + "\n\n" + _contexto_imovel(an)},
        {
            "role": "user",
            "content": (
                "Explique, em 2 ou 3 parágrafos curtos, o que a lei pede na "
                "minha terra sobre a mata ciliar e a Reserva Legal. Não faça "
                "perguntas ainda; só explique."
            ),
        },
    ]
    return _chat(msgs)


def conversar(historico: list[dict], an: dict) -> str | None:
    """Resposta livre do assistente, com o contexto do imóvel."""
    if not tem_llm():
        return None
    msgs = [{"role": "system", "content": SYSTEM + "\n\n" + _contexto_imovel(an)}]
    msgs.extend(historico[-10:])
    return _chat(msgs)
