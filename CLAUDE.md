# CLAUDE.md — Terra em Dia

Orientações para o Claude Code trabalhar neste projeto. Leia este arquivo no início de cada sessão.

> 📦 **Projeto anterior arquivado.** A equipe começou no **Desafio 2** (painel de pré-validação da Luana + detecção de sobreposição em PostGIS/QGIS). Esse trabalho foi **preservado em `desafio-2/`** e **não deve ser sobrescrito**. A partir de 2026-06-27 a equipe **pivotou para o Desafio 3** (pivô confirmado com a organização). Parte do motor geo do D2 pode ser **reaproveitada como "cérebro"** desta solução (ver §"A solução").

## Contexto do projeto

Projeto do **haCARthon**, maratona para desenvolver **soluções inovadoras** que fortaleçam o **SICAR** e consolidem o **CAR** como **Bem Público Digital (DPG)**, em **código aberto**. O CAR é o registro público eletrônico, nacional e obrigatório dos imóveis rurais, criado pela Lei nº 12.651/2012 (Código Florestal) e operacionalizado pelo SICAR (Decreto nº 7.830/2012). Respeitar o arcabouço legal e o ecossistema existente — **não reinventar o que o governo já construiu**.

> 🎯 **Esta equipe se inscreveu no DESAFIO 3 — Aumentar o entendimento das legislações do CAR.** Todo o foco do projeto é este desafio.

### Importante sobre o formato da entrega
**Não é obrigatório software funcional ou código-fonte.** O foco é **construir e validar a solução**. A entrega pode ser protótipo, wireframe, fluxograma, mockup ou vídeo. **Priorize validar a ideia antes de implementar.**

### Princípio orientador
> **Comece pelo problema (e pela pessoa), não pela solução.**
> Antes de propor ou codar qualquer coisa, valide: que dor real resolve, para qual persona, e se já existe nas plataformas oficiais.

## O Desafio 3 em detalhe

**Pergunta-desafio:** Como podemos aumentar o conhecimento e entendimento da legislação ambiental associada ao CAR pelos **pequenos e médios proprietários rurais**, para promover a preservação e recuperação florestal?

### Soluções esperadas (do edital) — marcadas as que atacamos
- ✅ **Simplificação da linguagem**: transformar termos jurídicos em orientações claras e exemplos concretos.
- ✅ **Educação e engajamento**: fazer o produtor entender os benefícios da regularidade (crédito, incentivos).
- ✅ **Análise automatizada de dados/imagens** que interprete a **legislação aplicada a cada imóvel**.
- ✅ **Ciência de dados** que faça **interpretações automáticas da legislação** para apoiar o proprietário.
- ◻️ Suporte aos analistas (ferramentas que facilitem a explicação) — *secundário* (ver persona Luana).
- ◻️ Tradução do Código Florestal para linguagem ampla/viral; plataformas de comunicação; formação de multiplicadores; acessibilidade de informações sobre benefícios.

> Toda tarefa deve poder ser justificada como contribuição direta a pelo menos um item ✅. Ao iniciar uma tarefa, declare a qual ela se conecta.

## Personas

### Seu Raimundo — pequeno/médio produtor rural — PERSONA PRIMÁRIA
Depende da propriedade para renda e sustento da família.
- **Dores:** internet instável e dependência do filho para usar tecnologia; **linguagem técnica/jurídica**; **medo de errar e ser punido** (motivo nº 1 para não mexer no CAR, confirmado na Live 06); depende de técnico por não entender a lei.
- **Ganhos esperados:** entender o que a lei quer da **sua** terra; regularizar sem advogado; acessar crédito rural verde; resolver pelo celular, com segurança.

### Luana — analista ambiental do órgão estadual — PERSONA SECUNDÁRIA (escala)
Atende proprietários para explicar notificações e legislação (confirmado na Live 06). Entra como **canal de escala**: o mesmo motor que personaliza a conversa do Raimundo **gera o material que a Luana usa para explicar** (branch "suporte ao analista" do D3). **Sem telas próprias no MVP** — aparece como argumento de escala no pitch.

## A solução: "Terra em Dia"

Assistente **conversacional** (mensageria, multicanal) que, a partir do **número do CAR** do imóvel (consulta de **leitura** — a interface oficial já lê os dados "via API", confirmado nos prints do vídeo do Meu Imóvel Rural), conduz o Raimundo por **três momentos**:

1. **Educa** — explica, em linguagem simples e **personalizada pelo imóvel dele**, o que o Código Florestal exige naquela terra (APP de curso d'água/nascente, déficit de Reserva Legal, área a recompor), com o **porquê** dimensional e o **benefício** (crédito/PRA).
2. **Testa o entendimento** — faz perguntas curtas para confirmar que o Raimundo entendeu **antes** de deixá-lo agir (ataca o medo de errar). É o **diferencial pedagógico**.
3. **Execução assistida** — guia o passo a passo e **termina no botão do SICAR** (ou gera o arquivo que ele sobe). **Não executa por ele** — o aceite/retificação só vale dentro do SICAR (Live 06).

### Diferencial (provado pelo vídeo oficial)
As ferramentas oficiais ("Tô em Dia" / "Meu Imóvel Rural") traduzem a **checklist de crédito** (Manual de Crédito Rural, item 2.9 / Cap. 2 Seção 9) e mostram o **status** do CAR — mas **não traduzem as obrigações ambientais do Código Florestal por feição** (APP / déficit de RL / área a recompor). **Esse é o nosso buraco.** Evidência: `docs/base-documental/ecossistema/Meu-Imovel-Rural.md` + prints do vídeo. No pitch, citar como *"conforme o vídeo oficial de demonstração"* — **não** afirmar teste ao vivo.

### Conceito-âncora reaproveitado: Retificação Dinamizada (RD)
A RD compara **declarado × base de referência** e aponta **divergências por feição** com **memória de cálculo**. É a lógica que alimenta o momento "Educa": o motor (que pode reusar o do `desafio-2/`) calcula o passivo; o **Terra em Dia traduz** isso para linguagem de gente. O motor é **encanamento invisível** — a face do produto é 100% Raimundo/D3.

## Conceitos técnicos do domínio (base do D3)

Fundamente toda regra no Código Florestal (`docs/base-documental/legislacao/L12651.pdf`).
- **APP — Áreas de Preservação Permanente (art. 4º):** faixas dimensionais (mata ciliar por largura do curso d'água, raio de nascente, topo de morro). Regra clara e fácil de explicar/ilustrar (boa candidata a feição-herói da demo).
- **Reserva Legal (art. 12):** percentual por região/bioma (ex.: 20% em boa parte do país; 80% em área de floresta na Amazônia Legal; variações por **ZEE**). **Déficit de RL** = falta de vegetação na RL declarada.
- **Área consolidada:** área convertida **antes de 22/07/2008** (tem regras próprias de regularização).
- **Demonstrativo do CAR / "quadro área":** documento (público) com as áreas por feição — APP, RVN/vegetação nativa, área consolidada, RL, **área a recompor**. É o insumo técnico que traduzimos.
- **Aceite no SICAR:** retificação só vale **dentro do SICAR** ("entrar e apertar o botão"). Notificar/explicar por fora é ok.
- **Regras estaduais:** podem ser **mais restritivas** que a federal (ex.: Piauí RL 30%; ZEE da Amazônia). **Base = Código Florestal federal**; podemos focar **1 estado** sem cobrir os 27.

### Siglas
CAR · SICAR · APP (Área de Preservação Permanente) · AUR (Área de Uso Restrito) · RL (Reserva Legal) · RVN (Remanescente de Vegetação Nativa) · PRA (Programa de Regularização Ambiental) · RD/AD (Retificação/Análise Dinamizada) · MCR (Manual de Crédito Rural, BACEN) · CRA (Cota de Reserva Ambiental) · SFB · SNCR/SIGEF (bases fundiárias) · SNIF (bases florestais de referência) · ZEE (Zoneamento Ecológico-Econômico) · ZARC (Zoneamento Agrícola de Risco Climático).

## Restrições rígidas

- ❌ **Nunca** enviar dados à **produção** do SICAR. Escrita em produção é bloqueada por padrão.
- ❌ **Nunca** commitar credenciais, CPFs, números de CAR ou códigos SNCR (mesmo de teste) em texto plano — usar `.env`/local gitignored.
- ✅ **Agnóstico de plataforma e de modelo (LLM):** não depender de software fechado/pago (Google Earth Engine, ArcGIS) nem de uma LLM específica. Framear como model-agnostic (a dúvida "precisa ser LLM gratuita?" ficou sem resposta oficial).
- ✅ **Multicanal:** WhatsApp é o canal natural, mas a solução não pode depender só dele (pensar Telegram, caixa postal Gov.br).
- ✅ **Aceite só no SICAR**; a solução orienta, não executa por ele.
- ✅ **Linguagem simples** em todo texto voltado ao produtor — jargão técnico/jurídico é a dor central.
- ✅ Respeitar Código Florestal (12.651/2012) e Decreto 7.830/2012. Registrar **data de extração** de bases externas. Tudo **open source** (GPL-3.0 compatível).

## Base documental

> 📁 Em `docs/base-documental/`, por tema (`manuais/`, `legislacao/`, `metodologia/`, `estudos/`, `ecossistema/`). Índice em `docs/base-documental/README.md`. PDFs ficam locais (não versionados); os `.md` de referência são versionados. **Consulte antes de pesquisar fora.**

Destaques para o D3:
- `metodologia/haCARthon - Briefing dos desafios - versão 2.pdf` — **Briefing oficial**: enunciado do D3 + **persona oficial do Seu Raimundo** (canais, confiança, medos). **Fonte autoritativa da persona.**
- `legislacao/L12651.pdf` — Código Florestal (APP, RL, área consolidada). **Fonte autoritativa das regras.**
- `manuais/Manual_Retificacao_Dinamizada.pdf` — mecanismo declarado × referência + memória de cálculo (estrutura do "quadro área").
- `ecossistema/Meu-Imovel-Rural.md` — transcrição do vídeo oficial; **evidência do diferencial** (Tô em Dia = crédito, não obrigação ambiental).
- `metodologia/Live_05_orientacoes-entrega-tiraduvidas.md` e `Live_06_tiraduvidas-desafios.md` — orientações de entrega + tira-dúvidas com a coordenação (validações citadas neste doc).
- `manuais/Manual_Central_do_Proprietario_Possuidor.pdf` — canal de notificação ao proprietário.

## Ecossistema oficial e fontes de dados (reutilize antes de criar)

| Recurso | Endereço | Uso |
|---|---|---|
| Consulta pública | https://consultapublica.car.gov.br | Consultar imóvel e **baixar demonstrativo (público)** |
| Meu Imóvel Rural | (vídeo oficial; ambiente demo em localhost) | Referência do que **já existe** (e do buraco que deixa) |
| Painel SFB Regularização | painel do SFB | Dados atuais (~10% validados) |
| RER (DPG) / GitHub | https://github.com/Rural-Environmental-Registry | Plataforma open source de referência |
| Downloads SICAR (shapefile/KML) | base da Consulta Pública | Geometrias por estado/município (`cod_imovel`, `ind_status`: AT/PE/CA) |
| SNCR · SIGEF · SNIF | bases oficiais | Fundiário e bases florestais de referência |

> ⚠️ Verifique disponibilidade antes de depender de qualquer endpoint. **Registre a data de extração.**

## A entrega (haCARthon)

**Prazo final: domingo, 28/06/2026, 23:59 (Brasília).** Uma pessoa entrega pela equipe; vale a última versão enviada. Três entregas complementares:
1. **Ideação** — perguntas objetivas (brainstorm, problema/quem sofre, solução, para quem, impacto, diferencial, viabilidade legal/técnica/operacional, tempo de implementação, como vira código aberto) + **feedback de mentoria (obrigatório, ≥1)**.
2. **Protótipo** — **vídeo de 2 min** das telas (mockup de conversa; sem código). Edição livre.
3. **Pitch** — **slides + voz, máx. 3 min**, gravar (Canva sugerido), subir no YouTube, colar link. **Áudio não pode ser IA** — voz de um integrante.

## Metodologia (Duplo Diamante)
1. **Descobrir** → 2. **Definir** (briefing: desafio, usuário, dor, proposta de valor) → 3. **Desenvolver** (How Might We, benchmark) → 4. **Entregar** (priorizar, prototipar, testar; saída = protótipo + vídeo de pitch).
- **JTBD:** Quando **[situação]**, quero **[motivação]**, para que **[resultado]**.
- **Fidelidade:** suba só até onde precisar (papel → wireframe → mockup → protótipo). Código é opcional.

## Diretrizes para o Claude Code
1. Confirme a contribuição ao **D3** (qual solução esperada ✅).
2. **Consulte a base documental primeiro** (Código Florestal, manuais, lives) — fonte autoritativa.
3. Verifique se já existe no ecossistema oficial (Meu Imóvel Rural, RER); prefira **estender/integrar** a recriar.
4. Pergunte se a melhor entrega é **protótipo/mockup** em vez de código — frequentemente é.
5. Documentação, comentários e commits em **português do Brasil**. **Linguagem simples** em qualquer texto voltado ao usuário final.

## Stack deste projeto

> Entrega **protótipo funcional** (bot de Telegram) + vídeo + pitch.
- **Tipo de entrega:** **bot de Telegram funcional** (`src/terra-em-dia-bot/`) + vídeo de 2 min + pitch.
- **Linguagem/runtime:** **Python 3.12**.
- **Lib:** **`python-telegram-bot`** (v21+, async). Token via `.env` (**nunca** versionar).
- **Fluxo da conversa:** **roteirizado/determinístico** (sem chave de API, reprodutível e open source). **Hook de LLM** opcional como upgrade — **agnóstico de modelo**.
- **Dados do imóvel:** exemplo real **anonimizado** de Querência do Norte/PR, lido localmente (`src/.../imoveis.py`), **simulando** a leitura por API do CAR. cod_imovel real só em `data/` (gitignored).
- **Métrica:** registro de compreensão (sim/não) em arquivo local gitignored → KPI "% que entendeu".
- **Motor de cálculo (opcional, reaproveitável):** lógica declarado × referência do `desafio-2/` (PostGIS/QGIS) como "cérebro" para os números por feição.

## Estrutura do repositório
```
/
├── CLAUDE.md              # este arquivo (Terra em Dia · D3)
├── README.md              # visão do projeto D3
├── docs/
│   ├── base-documental/   # COMPARTILHADO (manuais, leis, metodologia, lives) — não versionar PDFs
│   └── (briefing, descobrir, definir, prototipo do D3)
├── desafio-2/             # ARQUIVO do projeto anterior (NÃO sobrescrever)
├── data/                  # bases (registrar data de extração; não versionar pesados)
└── .env.example
```

## Itens em aberto
1. **Feição-herói da demo** — APP de curso d'água (recomendada) ou déficit de RL?
2. **Estado-foco** do exemplo (regras federais como base).
3. **Imóvel-exemplo** — representativo "Seu Raimundo" (ilustrativo) vs. imóvel público real (Consulta Pública); cuidar de privacidade.
4. **Ferramenta de protótipo** (Figma / HTML / outro) e canal simulado (WhatsApp/Telegram).
