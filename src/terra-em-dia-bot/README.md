# Terra em Dia — bot de Telegram

Protótipo funcional do **Desafio 3** do haCARthon. O Seu Raimundo chama no "Zap"
(Telegram), manda o número do CAR, e o bot **explica a obrigação ambiental do
imóvel dele em linguagem simples**, faz uma **pergunta despretensiosa** pra ver
se entendeu (vira métrica) e o **guia até o botão do SICAR**.

## Como rodar

```bash
cd src/terra-em-dia-bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Crie um bot com o @BotFather no Telegram (/newbot) e pegue o token:
cp .env.example .env        # cole o token em TELEGRAM_TOKEN
python bot.py
```

No Telegram, abra seu bot e mande `/start`.

## Fluxo da conversa
1. `/start` → saudação; pede o nº do CAR (ou foto da carta).
2. Recebe o nº → **explica a mata ciliar (APP de curso d'água)** com os números
   reais do imóvel-exemplo (Querência do Norte/PR, anonimizado).
3. Pergunta *"por que a lei pede esse mato na beira do rio?"* → avalia a resposta.
4. Registra se entendeu (métrica) → guia o passo a passo até o **botão do SICAR**.

## Métrica de eficácia
Cada conversa grava `entendeu: sim/não` em `data/metricas_terra_em_dia.jsonl`
(pasta gitignored). Veja o KPI com o comando `/metricas`:

> Conversas: 30 · Entenderam: 20 · **Compreensão: 67%**

## Arquivos
- `bot.py` — handlers e fluxo (ConversationHandler).
- `conteudo.py` — textos na linguagem do Raimundo + `compreendeu()`.
- `imoveis.py` — "leitura" do imóvel por nº do CAR (simula a API).
- `metricas.py` — registro/agregação da compreensão.

## Notas
- **Determinístico/roteirizado** (sem chave de LLM) → reprodutível e open source.
  `compreendeu()` é o ponto de upgrade para uma LLM **agnóstica de modelo**.
- O bot **orienta**, não executa: o aceite/retificação é sempre no SICAR.
- **Segurança:** o token fica só no `.env` (gitignored). O `cod_imovel` real
  fica só em `data/` (gitignored); aqui os números aparecem anonimizados.
