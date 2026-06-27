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
    "do CAR para pequenos produtores rurais brasileiros (o Seu Raimundo).\n"
    "COMO FALAR: linguagem MUITO simples e calorosa, frases curtas, zero "
    "juridiquês. Use exemplos concretos (passos, campos de futebol, beira do "
    "rio). Trate por 'você'.\n"
    "REGRAS DE CONDUTA:\n"
    "- Você ORIENTA, nunca executa: o aceite/retificação é sempre no SICAR "
    "('só você aperta o botão').\n"
    "- Nunca prometa crédito automático (é decisão do banco).\n"
    "- Baseie-se só nos dados do imóvel e nas regras informadas. Se não souber, "
    "diga que vai confirmar.\n\n" + conteudo.REGRAS
)


def tem_llm() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY"))


def _client():
    from openai import OpenAI

    return OpenAI(base_url=os.environ.get("OPENAI_BASE_URL") or None)


def _contexto_imovel(an: dict) -> str:
    return (
        "Dados do imóvel do produtor (use nas respostas):\n"
        f"- Município: {an['municipio']}/{an['uf']}; área {an['area_ha']} ha.\n"
        f"- Mata ciliar (APP de rio): {an['app_mata_ciliar_ha']} ha; faixa exigida "
        f"{an['faixa_app_m']} m (rio {an['rio_largura']}).\n"
        f"- Reserva Legal: exigida {an['rl_exigida_pct']}% (~{an['rl_exigida_ha']} ha); "
        f"proposta {an['rl_proposta_ha']} ha; déficit {an['rl_deficit_ha']} ha."
    )


def _chat(mensagens: list[dict]) -> str | None:
    try:
        resp = _client().chat.completions.create(
            model=MODEL, messages=mensagens, temperature=0.4, max_tokens=400
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
