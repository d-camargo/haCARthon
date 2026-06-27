"""Registro da métrica de eficácia: o produtor demonstrou entender?

Grava uma linha por conversa em `data/metricas_terra_em_dia.jsonl` (a pasta
`data/` é gitignored). Permite o KPI "% que entendeu" — o coração da prova de
que o método educa de verdade (o D3 pede "aumentar o entendimento").
"""
import json
from datetime import datetime, timezone
from pathlib import Path

_ARQUIVO = Path(__file__).resolve().parents[2] / "data" / "metricas_terra_em_dia.jsonl"


def registrar(user_id: int, entendeu: bool, tentativas: int = 1) -> None:
    _ARQUIVO.parent.mkdir(parents=True, exist_ok=True)
    linha = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "entendeu": bool(entendeu),
        "tentativas": tentativas,
    }
    with _ARQUIVO.open("a", encoding="utf-8") as f:
        f.write(json.dumps(linha, ensure_ascii=False) + "\n")


def resumo() -> dict:
    """(total, entenderam, pct) das conversas registradas."""
    total = entenderam = 0
    if _ARQUIVO.exists():
        for linha in _ARQUIVO.read_text(encoding="utf-8").splitlines():
            if not linha.strip():
                continue
            try:
                d = json.loads(linha)
            except json.JSONDecodeError:
                continue
            total += 1
            entenderam += 1 if d.get("entendeu") else 0
    pct = round(100 * entenderam / total) if total else 0
    return {"total": total, "entenderam": entenderam, "pct": pct}
