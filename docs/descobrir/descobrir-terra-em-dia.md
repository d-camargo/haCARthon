# Descobrir — Terra em Dia (Desafio 3)

> Fase 1 do Duplo Diamante. Conhecer o usuário, a dor, o contexto e o que já existe.
> Persona primária: **Seu Raimundo** (pequeno/médio produtor). Data: 2026-06-27.

## Desk Research — o que já existe (e o buraco)

- **"Meu Imóvel Rural" / "Tô em Dia"** (vídeo oficial; ambiente demo em localhost): cruza CAR+SNCR+SIGEF, mostra **status** do CAR e uma **checklist de crédito** (Manual de Crédito Rural, item 2.9 / Cap. 2 Seção 9), com "Entenda a Regra" e "Fique em Dia" (passo a passo) — **aplicados às restrições de crédito**, e lê dados "via API". *Fonte: `docs/base-documental/ecossistema/Meu-Imovel-Rural.md` + prints do vídeo.*
- **🕳️ O buraco:** nenhuma ferramenta oficial **traduz as obrigações ambientais do Código Florestal por feição** (APP, déficit de RL, área a recompor) em linguagem do produtor, com o *porquê* e o *como*. Os números existem, mas trancados no **demonstrativo técnico**.
- **Retificação Dinamizada (RD):** o SICAR já compara **declarado × base de referência** e gera divergências por feição com memória de cálculo — insumo técnico que ninguém traduz para o produtor.
- **Estudo CPI/PUC-Rio (2025):** ~8 mi de imóveis; gargalo nº 1 nomeado pela coordenação = **proprietário não volta para retificar** (não sabe / não entende a notificação).

## Matriz CSD

### ✅ Certezas (com evidência)
*Comportamento / contexto (Live 06 + estudo):*
- O produtor **tem medo de mexer no CAR e ser punido**; depende de técnico por não entender a lei. *(Live 06)*
- O motivo nº 1 de não retificar é **não saber que precisa / não entender a notificação**. *(Live 06)*
- **Crédito rural** é o maior driver para o produtor agir. *(Live 06)*

*Persona oficial — confirmadas pelo Briefing (Persona 1, Seu Raimundo):*
- **Canais que usa:** informa-se por **rádio, televisão, WhatsApp e TikTok**. *(Briefing)*
- **Confia via intermediários:** decide ouvindo **vizinhos, sindicatos, cooperativas, líderes comunitários, técnicos agrícolas e gerentes de banco** — não confia "no abstrato". *(Briefing)*
- **Prefere exemplos concretos a orientações abstratas.** → valida o "na sua terra" vs. cartilha genérica. *(Briefing)*
- **Feições que mais geram insegurança:** definição dos **limites do imóvel, APP e Reserva Legal**. *(Briefing)*
- **Maiores medos:** perda da terra, falta de recursos, incerteza; quer evitar multas/embargos. *(Briefing)*

*Técnico / estratégico:*
- As ferramentas oficiais traduzem **crédito e status**, não **obrigações ambientais por feição**. *(vídeo Meu Imóvel Rural)*
- O **aceite/retificação só vale dentro do SICAR**. *(Live 06)*
- **IA generativa para traduzir a legislação é permitida** (sem restrição). *(Live 06)*
- Existe **leitura de dados do imóvel via API**. *(prints Meu Imóvel Rural)*
- **D3 é a pista menos disputada** (mentor: 15/15 equipes em D1/D2).

### ❓ Suposições (ainda a validar)
- A **checagem de entendimento** (perguntas) aumenta confiança/ação — e não vira fricção chata.
- Explicação personalizada **reduz o medo** mais que só informar (o briefing confirma a *preferência* por exemplos concretos; falta confirmar o *efeito sobre o medo/ação*).
- Ele **tem o número do CAR** à mão (ou acha fácil) para iniciar a conversa.

### 🔎 Dúvidas (perguntas abertas)
- Como entrar pelos **canais/intermediários de confiança** dele (cooperativa, sindicato, técnico) em vez de ser "mais um app de terceiro"?
- Quão personalizada a explicação pode ser **só com dados públicos / sem escrita**?
- Até onde a "execução assistida" vai **antes do botão do SICAR**?
- Entre **APP e RL** (as duas que assustam), qual vira a **feição-herói** da demo?
- Como lidar com o Raimundo que **discorda da base de referência**?

## Mapa de Empatia — Seu Raimundo

- **Pensa & sente:** "será que fiz errado e vou ser multado?"; insegurança com o juridiquês; quer crédito mas não sabe se está regular; medo de perder a terra.
- **Vê:** uma notificação que não entende; o SICAR cheio de mapas e termos técnicos; o filho mexendo no celular por ele.
- **Ouve:** o técnico que fez o cadastro (e sumiu); vizinhos, **sindicato, cooperativa e líderes comunitários**; o gerente do banco exigindo CAR regular; **rádio e TV**. *(canais/influências confirmados no Briefing)*
- **Fala & faz:** "deixa pra depois"; adia mexer no CAR; pede ajuda ao filho ou paga um técnico; busca info no **WhatsApp/TikTok**.
- **Dores:** linguagem técnica · medo de errar · internet instável · dependência de terceiros.
- **Ganhos:** entender **com segurança** o que precisa fazer · regularizar sem advogado · destravar **crédito** · **trabalhar tranquilo e garantir o futuro da família** *(definição de sucesso no Briefing)*.
