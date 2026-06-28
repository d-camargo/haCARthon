# Ideação — Terra em Dia (Desafio 3)

> Respostas às perguntas oficiais da entrega de Ideação (haCARthon, Live 05).
> Objetivas e diretas. Fundamentadas em `docs/descobrir|definir|desenvolver|entregar`.

## 1. Processo de brainstorm (como escolhemos a ideia)
Começamos no Desafio 2 (geoespacial). Após mentoria e as lives de tira-dúvidas, percebemos que o **D3 estava pouco disputado** e era onde a coordenação mais espera ver soluções ("comunicação, foco no usuário"). Pivotamos e rodamos o **Duplo Diamante**: Matriz CSD, mapa de empatia e jornada do Seu Raimundo, How Might We, benchmark e SCAMPER.

Ideias consideradas: (a) tradutor genérico do Código Florestal; (b) calculadora de benefícios da regularidade; (c) kit para multiplicadores; (d) **"a lei na sua terra"** — explicar a legislação **personalizada pelo imóvel**. Escolhemos a (d), batizada **Terra em Dia**, porque é a única que ocupa um **buraco real**: as ferramentas oficiais traduzem a checklist de crédito, mas **não traduzem as obrigações ambientais do Código Florestal por feição** (mata ciliar, Reserva Legal, área a recompor).

## 2. Qual problema queremos resolver
Pequenos e médios produtores **não entendem o que o Código Florestal exige da terra deles**. Recebem uma notificação (em papel) que não compreendem, têm **medo de errar e ser punidos** e dependem de um técnico que nem sempre está por perto.
- **Quem enfrenta:** o produtor rural (Seu Raimundo) e, no atendimento, o analista ambiental (Luana).
- **O que acontece hoje:** a lei está em manuais densos; o produtor não sabe que precisa retificar, ou não entende a notificação → **não age**. A coordenação nomeou isso como **gargalo nº 1** (a retificação que não é atendida).
- **Por que importa:** sem entender, não há regularização, não há acesso a crédito e **não há preservação/recuperação florestal** — exatamente o que o D3 busca.

## 3. A solução
**Terra em Dia** — um assistente conversacional (no protótipo, Telegram) que fala a língua do produtor:
1. A partir do **número do CAR**, consulta os **dados reais** do imóvel e **manda um mapa** com as feições (perímetro, mata ciliar, Reserva Legal).
2. **Explica em linguagem simples** o que a lei pede *naquela terra* — mata ciliar (faixa de 30 m, art. 4º) e **déficit de Reserva Legal** — com o porquê e o benefício, e um 2º mapa de **"como deve ficar"**.
3. **Confere se o produtor entendeu** com uma pergunta despretensiosa — o que vira **métrica de compreensão**.
4. **Guia o passo a passo** até o botão do SICAR (orienta; **não executa** — o aceite é sempre no SICAR).

## 4. Para quem é a solução
- **Primária — Seu Raimundo** (pequeno/médio produtor): é a persona oficial do briefing, informa-se por WhatsApp/rádio/TV e confia em exemplos concretos e em canais locais (cooperativa, sindicato, técnico).
- **Secundária — Luana** (analista do órgão estadual): o mesmo motor gera o material que ela usa para **explicar** ao produtor (branch "suporte ao analista" do D3).
- **Por que esse público:** é quem o D3 nomeia, é a pista menos disputada e é onde está o maior impacto (autonomia + segurança destravam a ação).

## 5. Impacto e resultados esperados
- **Produtor entende e age com segurança** → mais retificações atendidas → ataca o gargalo nº 1 → mais regularização → **mais preservação e recuperação florestal**.
- **Educação que se mede:** KPI de **% de compreensão** (ex.: 20 de 30 produtores entenderam = 67%). O D3 pede "aumentar o entendimento" — e a gente **mede** isso.
- **Escala** pelos canais de confiança (cooperativas, sindicatos, ATER) e, para a gestão, padroniza a explicação que a Luana dá.

## 6. Diferencial
- Hoje a lei vive em **manuais densos**; as ferramentas oficiais ("Tô em Dia"/"Meu Imóvel Rural") traduzem só a **checklist de crédito** e mostram **status** — não as obrigações ambientais por feição (conforme o vídeo oficial de demonstração).
- O Terra em Dia **traduz a obrigação ambiental na terra do produtor**, com **mapa "atual × como deve ficar"**, e é o único que **mede o entendimento**.
- Chega pelo **canal que ele já confia** (o "Zap"), não como "mais um app".

## 7. Viabilidade (legal, técnica, operacional) e tempo
- **Legal:** respeita o Código Florestal (Lei 12.651/2012); o aceite/retificação só vale **dentro do SICAR**; não promete liberação de crédito (é decisão do banco).
- **Técnica:** **já funciona** — protótipo em Python lê dados oficiais do CAR de **qualquer imóvel do Brasil pelo serviço aberto do SICAR** (WFS oficial, `geoserver.car.gov.br`, consultado pelo número do CAR), gera os mapas (com **imagem de satélite de fundo**) e conversa com LLM **agnóstico de modelo**. As feições declaradas (mata ciliar/Reserva Legal) vêm do dado oficial do imóvel; a leitura é o ponto único `cadastro.carregar_imovel(cod)`.
- **Operacional:** multicanal por princípio (Telegram/WhatsApp/caixa Gov.br); distribuição via cooperativas/sindicatos/ATER.
- **Tempo:** protótipo pronto (já lê qualquer imóvel pelo serviço oficial). Para um **piloto real** (um município/cooperativa): ~8–12 semanas. Etapas: (1) ampliar as **feições declaradas por API/derivação** (mata ciliar e RL para todo o país, hoje completas no recorte do piloto); (2) cobrir mais estados; (3) multicanal; (4) **piloto com ATER**; (5) painel da Luana.

## 8. Código aberto (como pode ser compartilhada)
- **Licenciável como GPL-3.0**, arquitetura **modular** (dados, análise legal, mapa, conversa, LLM) — reaproveitável por **qualquer estado ou órgão**.
- **Agnóstico de modelo:** a camada de LLM é OpenAI-compatible e troca por um **modelo aberto/local** sem mudar o código — coerente com o CAR como **Bem Público Digital**.
- Usa **dados abertos oficiais** e pode **integrar ao ecossistema** (Meu Imóvel Rural / RER) em vez de competir. A lógica "declarado × referência → tradução por feição" serve a **outros países** com cadastros semelhantes.

## 9. Mentoria (feedback coletado)
- **Mentor (durante o evento):** sugeriu pivotar para o D3 (menos disputado) e o conceito de **atendimento por mensageria + checagem de entendimento + execução assistida**. **Incorporado** — é o coração do Terra em Dia.
- *(Atualizar com feedbacks adicionais de mentoria antes do envio.)*
