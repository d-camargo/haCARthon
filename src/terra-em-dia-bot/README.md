# Terra em Dia — bot de Telegram

Protótipo **funcional** do **Desafio 3** do haCARthon. O Seu Raimundo chama no
"Zap" (Telegram), manda o número do CAR; o bot:

1. **Consulta os dados reais** do imóvel no CAR (por `cod_imovel`).
2. **Manda um mapa** com as feições do cadastro (perímetro, mata ciliar, Reserva Legal).
3. **Explica em linguagem simples** o que a lei pede *naquela terra* (LLM, com
   fallback roteirizado) — APP de curso d'água e déficit de Reserva Legal.
4. Faz uma **pergunta despretensiosa** pra ver se entendeu → vira **métrica**.
5. **Guia o passo a passo** até o botão do SICAR (orienta, não executa).

## Como rodar

```bash
cd src/terra-em-dia-bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # osgeo (GDAL) vem do sistema, não do pip

cp .env.example .env                    # preencha:
#   TELEGRAM_TOKEN  (obrigatório, do @BotFather)
#   OPENAI_API_KEY  (opcional; sem ele, usa o roteiro determinístico)
#   TERRA_DEMO_COD  (cod_imovel de demonstração — ver data/exemplo-raimundo.local.md)
python bot.py
```

No Telegram, abra seu bot e mande `/start`. Use `/metricas` pra ver o KPI.

## Arquitetura
| Módulo | Papel |
|---|---|
| `bot.py` | Handlers do Telegram e fluxo da conversa |
| `cadastro.py` | Lê perímetro + APP + RL por `cod_imovel` (osgeo/GDAL) — motor de dados reais |
| `analise.py` | Regras do Código Florestal: faixa de APP, RL exigida × proposta, déficit |
| `mapa.py` | Renderiza o PNG do imóvel com as feições (matplotlib, offline) |
| `conteudo.py` | Textos na linguagem do Raimundo + roteiro de fallback + `compreendeu()` |
| `llm.py` | LLM **agnóstico** (interface OpenAI-compatible; `base_url` configurável) |
| `metricas.py` | Registro/agregação da compreensão (KPI "% que entendeu") |

## Notas
- **Dados reais** do SICAR (base oficial do Paraná, ver `data/`). O `cod_imovel`
  real fica só no `.env`/`data/` (gitignored); no código os números são anonimizados.
- **Agnóstico de modelo:** `OPENAI_BASE_URL` aponta para a OpenAI na demo ou para
  um modelo aberto/local (Ollama, vLLM) — coerente com o CAR como Bem Público Digital.
- **Funciona sem LLM:** sem `OPENAI_API_KEY`, o bot usa o roteiro de `conteudo.py`.
- O bot **orienta**, não executa: o aceite é sempre no SICAR.
