# Ideação — Terra em Dia (Desafio 3)

> Respostas às perguntas oficiais da entrega de Ideação (haCARthon, Live 05).
> Objetivas e diretas. Fundamentadas em `docs/descobrir|definir|desenvolver|entregar`.

## 1. Processo de brainstorm (como escolhemos a ideia)
Começamos no Desafio 2 (geoespacial), não foi muito um brainstorm, mas como um fio condutor, afunilando o que conheciamos do CAR, as informações, enfim... A solução era integrada com o QGIS (SIG Open Source) e tinha como alvo a Luana. Contudo, após mentoria e as lives de tira-dúvidas, percebemos que o que estavamos fazendo não era 100% alinhado ao objetivo de D3. A mentoria mencionou que o **D3 estava pouco disputado**, e com as lives a coordenação comentou mais sobre D1 e D3 ("comunicação, foco no usuário"). Pivotamos e rodamos o **Duplo Diamante**: Matriz CSD, mapa de empatia e jornada do Seu Raimundo, How Might We, benchmark e SCAMPER. Para D3 pegamos algumas sugestões da mentoria, portanto, também não teve um "brainstorm".

Ideias consideradas: (a) Sistema de score para priorização de análise da Luana (sobreposição de área CARxCAR e CARxAssentamentos INCRA). Além do sistema de priorização, a Luana desenvolvia seu trabalho todo pelo QGIS, sem trocar de sistema; (b) **"a lei na sua terra"** — explicar a legislação **personalizada pelo imóvel**. Pivotamos para a (b), batizada **Terra em Dia**, porque é a única que ocupa um **buraco real**: as ferramentas oficiais (vídeo disponibilizado do "Meu Imóvel Rural") traduzem a checklist de crédito, mas **não traduzem as obrigações ambientais do Código Florestal por feição** (mata ciliar, Reserva Legal, área a recompor).

## 2. Qual problema queremos resolver
Pequenos e médios produtores **não entendem o que o Código Florestal exige da terra deles**. Recebem uma notificação (em papel) que não compreendem, têm **medo de errar e ser punidos** e dependem de um técnico que nem sempre está por perto. Quase sempre deixam de responder as notificações e o sistema para.
- **Quem enfrenta:** o produtor rural (Seu Raimundo) e, no atendimento, o analista ambiental (Luana).
- **O que acontece hoje:** a lei está em manuais densos; o produtor não sabe que precisa retificar, ou não entende a notificação → **não age**. A coordenação nomeou isso como **gargalo nº 1** (a retificação que não é atendida).
- **Por que importa:** sem entender, não há regularização, não há acesso a crédito e **não há preservação/recuperação florestal** — exatamente o que o D3 busca. Sem o Seu Raimundo entender o que precisa fazer o sistema para.

## 3. A solução
**Terra em Dia** — um assistente conversacional (no protótipo, Telegram) que fala a língua do produtor:
1. A partir do **número do CAR** (pode ser alterado pelo número de CPF, por exemplo), consulta os **dados reais** do imóvel e **manda um mapa** com as feições (perímetro, mata ciliar, Reserva Legal, pode ser ampliado).
2. **Explica em linguagem simples** o que a lei pede *naquela terra* — mata ciliar (faixa de 30 m, art. 4º) e **déficit de Reserva Legal** — com o porquê e o benefício, e um 2º mapa de **"como deve ficar"**.
3. **Confere se o produtor entendeu** com uma pergunta despretensiosa — o que vira **métrica de compreensão**.
4. **Guia o passo a passo** até o botão do SICAR (orienta; **não executa** — o aceite é sempre no SICAR).

## 4. Para quem é a solução
- **Primária — Seu Raimundo** (pequeno/médio produtor): é a persona oficial do briefing, informa-se por WhatsApp/rádio/TV e confia em exemplos concretos e em canais locais (cooperativa, sindicato, técnico).
- **Secundária — Luana** (analista do órgão estadual): o mesmo motor gera o material que ela usa para **explicar** ao produtor (branch "suporte ao analista" do D3).
- **Por que esse público:** 98% dos processos parados aguardando reposta da notificação são para pequenos/médios produtores.

## 5. Impacto e resultados esperados
- **Produtor entende e age com segurança** → mais retificações atendidas → ataca o gargalo nº 1 → mais regularização → o sistema caminha para mudanças concretas.
- **Educação que se mede:** KPI de **% de compreensão** (ex.: 20 de 30 produtores entenderam = 67%). O D3 pede "aumentar o entendimento" — e a gente **mede** isso. Outros KPI's podem ser implementados.
- **Escala** pelos canais de confiança (cooperativas, sindicatos, ATER) e, para a gestão, padroniza a explicação que a Luana dá.

## 6. Diferencial
- Hoje a lei vive em **manuais densos**; as ferramentas oficiais ("Tô em Dia"/"Meu Imóvel Rural") traduzem só a **checklist de crédito** e mostram **status** — não as obrigações ambientais por feição (conforme o vídeo oficial de demonstração).
- O Terra em Dia **traduz a obrigação ambiental na terra do produtor**, com **mapa "atual × como deve ficar"**, e o sistema vem preparado para medir o entendimento do produtor quanto as mudanças que são necessárias na sua declaração do CAR, assim como em sua terra.
- Chega pelo **canal que ele já confia** (o "Zap"), não como "mais um app".

## 7. Viabilidade (legal, técnica, operacional) e tempo
- **Legal:** respeita o Código Florestal (Lei 12.651/2012); o aceite/retificação só vale **dentro do SICAR**; não promete liberação de crédito (é decisão do banco).
- **Técnica:** **já funciona** — protótipo em Python lê dados oficiais do CAR de **qualquer imóvel do Brasil pelo serviço aberto do SICAR** (WFS oficial, `geoserver.car.gov.br`, consultado pelo número do CAR), gera os mapas (com **imagem de satélite de fundo**) e conversa com LLM treinado para um atendimento acolhedor e com linguagem simplificada. As feições declaradas (mata ciliar/Reserva Legal) vêm do dado oficial do imóvel; a leitura é o ponto único `cadastro.carregar_imovel(cod)`. Para o protótipo os dados da cidade de Querência do Norte - Paraná, estão em base local (download feito pelo portal do https://consulta.car.gov.br/geoservices), contudo, entende-se que o sistema do Ministério já tenha essa base de dados para todo o Brasil e com fácil acesso.
- **Operacional:** multicanal por princípio (Telegram/WhatsApp/caixa Gov.br); distribuição via cooperativas/sindicatos/ATER.
- **Tempo:** protótipo pronto (já lê qualquer imóvel pelo serviço oficial). Para um **piloto real** (um município/cooperativa): ~6–10 semanas. Etapas: (1) ampliar as **feições declaradas por API/derivação** (mata ciliar e RL para todo o país, hoje completas no recorte do piloto); (2) cobrir mais estados; (3) multicanal; (4) **piloto com ATER**; (5) painel da Luana, recebendo os KPI's do seu estado.

## 8. Código aberto (como pode ser compartilhada)
- **Licenciável como GPL-3.0**, arquitetura **modular** (dados, análise legal, mapa, conversa, LLM) — reaproveitável por **qualquer estado ou órgão**.
- **Agnóstico de modelo:** a camada de LLM é OpenAI-compatible e troca por um **modelo aberto/local** sem mudar o código — coerente com o CAR como **Bem Público Digital**. É completamente possível usar um servidor local com LLM local e Open Source.
- Usa **dados abertos oficiais** e pode **integrar ao ecossistema** (Meu Imóvel Rural / RER) em vez de competir. A lógica "declarado × referência → tradução por feição" serve a **outros países** com cadastros semelhantes.

## 9. Mentoria (feedback coletado)
- **Mentor (durante o evento):** sugeriu pivotar para o D3 (menos disputado) e o conceito de **atendimento por mensageria + checagem de entendimento + execução assistida**. **Incorporado** — é o coração do Terra em Dia. Apresentou discussões sobre o D2 e a ideia que atualmente estavamos trabalhando. Foi uma conversa boa.
