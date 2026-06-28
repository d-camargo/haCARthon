# Checklist de entrega — Terra em Dia (Desafio 3)

> **Prazo: domingo, 28/06/2026, 23:59 (Brasília).** Uma pessoa entrega pela equipe; vale a última versão enviada.
> Três entregas complementares: **Ideação**, **Protótipo (vídeo 2 min)** e **Pitch (slides + voz 3 min)**.

## Visão geral — o que falta

| Entrega | Conteúdo pronto? | Falta fazer |
|---|---|---|
| **1. Ideação** | ✅ `docs/entregar/ideacao-terra-em-dia.md` (9 perguntas + 1 mentoria) | Colar na plataforma; (opcional) +1 mentoria |
| **2. Vídeo 2 min** | ✅ roteiro: `docs/entregar/entregar-terra-em-dia.md` | **Gravar a tela do bot** + exportar |
| **3. Pitch 3 min** | ✅ deck + narração: `docs/entregar/pitch-terra-em-dia.md` | Montar slides (Canva), **gravar voz humana**, subir YouTube |

---

## 1. Ideação — enviar
- [ ] Copiar as respostas de `ideacao-terra-em-dia.md` para o formulário oficial (uma a uma, nas 9 perguntas).
- [ ] Garantir o **feedback de mentoria** preenchido (≥1 é obrigatório — já temos; some outro se houver).
- [ ] Revisar que nada cita **dado sensível** (nº de CAR real, CPF) — não citar.

## 2. Vídeo de 2 min — gravar a tela do bot

**É protótipo funcional** — gravação de tela real no Telegram, seguindo o storyboard
(`entregar-terra-em-dia.md`). Não é mockup.

**Antes de gravar**
- [ ] Júnior terminou ACTION-004→006 (motor online + **satélite no mapa**). Gravar **depois** = vídeo mais rico.
- [ ] `.env` com `TELEGRAM_TOKEN` e `OPENAI_API_KEY` (para a conversa fluida) e `TERRA_DEMO_COD` apontando
      para **um dos 3 imóveis-demo** (o de ~89,6 ha / déficit RL ~9,6 ha do storyboard, se for um deles).
- [ ] Rodar `python bot.py` e fazer um **ensaio**: confirmar que os **2 mapas** saem (com satélite) e a
      conversa segue as cenas 2→7.
- [ ] Tela limpa: sem nome real do bot/usuário expondo dado pessoal; fonte do Telegram legível.

**Gravar (seguindo o storyboard)**
- [ ] Cenas 0–1: abertura em off (a carta + Casa da Agricultura — rotular como **ilustrativa/fictícia**).
- [ ] Cena 2: "oi" + número do CAR → bot acha o sítio.
- [ ] Cena 3: **mapa atual** + "você sabe por que recebeu a carta?".
- [ ] Cena 4: traduz mata ciliar (30 passos) + **mapa "como deve ficar"** + Reserva Legal (declarou × falta).
- [ ] Cena 5: confere o entendimento (pergunta simples).
- [ ] Cena 6: guia até o **botão do SICAR** ("só você aperta o botão").
- [ ] Cena 7: fecho + tagline.
- [ ] Duração **~2 min** (edição livre). Exportar.

**Não fazer**
- ❌ Não prometer liberação de crédito (é decisão do banco). ❌ Não dizer que o bot executa no SICAR.
- ❌ Não mostrar nº de CAR real legível na tela.

> **Live 08:** o **protótipo é só "como funciona"** (o bot funcionando). Problema, impacto e **validação**
> moram no **pitch**. Então mantenha as cenas 0–1 (carta/Casa da Agricultura) **curtas** — a locução
> ajuda a conduzir, mas o foco do vídeo é a conversa real com os 2 mapas.

## 3. Pitch de 3 min — slides + voz (regras da Live 08)
- [ ] Montar os **8 slides** de `pitch-terra-em-dia.md` no **Canva** (pouco texto; os 2 mapas + 1 print).
      **Slides ESTÁTICOS** — ⚠️ **sem GIF, sem vídeo, sem animação** (é PDF estático).
- [ ] Slides na **horizontal (16:9)**. Referência dos dados pequenininha no slide (slides 2 e 5).
- [ ] Gravar a **narração com voz de um integrante** (⚠️ **não pode ser IA**; **sem rosto**, só voz), nos tempos (fecha em 3:00).
- [ ] Ensaiar com **cronômetro**; **máx. 3:00** — passou, **desclassifica**.
- [ ] Subir no **YouTube** como **público ou "não listado"** (⚠️ **privado desclassifica**); **copiar o link**.
- [ ] Colar o link na entrega de pitch **+ descrever como a equipe usou IA** (campo da entrega: pesquisa,
      ideação, estruturação dos slides, arte — deixar claro que a **voz não foi IA**).
- [ ] Lembrar: os jurados veem **ideação → pitch → protótipo**; o pitch tem que se sustentar sozinho
      (problema, **insight**, solução, como funciona macro, **validação**, diferencial, impacto).

---

## Sequência sugerida para hoje
1. **Júnior:** motor online + satélite + ACTION-010 (dados na conversa + 2º mapa) **feitos**; falta a
   ACTION-011 (2º mapa proativo + nome do rio) para o vídeo ficar redondo.
2. **Em paralelo (equipe):** monta os slides do pitch no Canva e ensaia a narração.
3. **Depois do júnior:** grava a **tela do bot** (vídeo 2 min) com o bot já melhorado.
4. **Grava a voz** do pitch; sobe no YouTube.
5. **Envia tudo** na plataforma: respostas de ideação + vídeo + link do pitch. Conferir que entrou.

> Lembrete: vale a **última versão enviada**. Se der tempo, envie uma versão e atualize depois.
