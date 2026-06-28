"""Memoria persistente simples do atendimento.

Grava contexto por usuario em `data/memoria_terra_em_dia.json`, que fica fora do
git. A ideia nao e guardar tudo para sempre: so o suficiente para o bot nao
voltar ao inicio a cada mensagem ou reinicio.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

_MEM_DB = {}
_MAX_HISTORICO = 16


def _agora() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ler_tudo() -> dict:
    # Para o protótipo de teste, a memória é mantida apenas em memória de processo
    return _MEM_DB


def _salvar_tudo(dados: dict) -> None:
    pass


def carregar(user_id: int) -> dict:
    return _ler_tudo().get(str(user_id), {})


def atualizar(user_id: int, **campos) -> dict:
    dados = _ler_tudo()
    atual = dados.get(str(user_id), {})
    atual.update(campos)
    atual["updated_at"] = _agora()
    dados[str(user_id)] = atual
    _salvar_tudo(dados)
    return atual


def adicionar_mensagem(user_id: int, role: str, content: str) -> list[dict]:
    dados = _ler_tudo()
    atual = dados.get(str(user_id), {})
    hist = atual.setdefault("historico", [])
    hist.append({"role": role, "content": content})
    atual["historico"] = hist[-_MAX_HISTORICO:]
    atual["updated_at"] = _agora()
    dados[str(user_id)] = atual
    _salvar_tudo(dados)
    return atual["historico"]


def limpar(user_id: int) -> None:
    dados = _ler_tudo()
    dados.pop(str(user_id), None)
    _salvar_tudo(dados)
