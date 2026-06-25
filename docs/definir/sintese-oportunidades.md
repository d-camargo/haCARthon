# Síntese e How Might We — fase Definir (Desafio 2)

> Fecha o 1º losango: agrupa os atritos (Descobrir) em **gaps de oportunidade**, transforma-os
> em perguntas **How Might We** e aponta candidatos a **recorte** com um pré-juízo de Impacto × Esforço.
> Entradas: [matriz-csd](../descobrir/matriz-csd.md) · [jornada-luana](../descobrir/jornada-luana.md).
> Data: 2026-06-25.

## 1. Diagrama de afinidade — atritos agrupados em 3 gaps

### Gap A — Base de referência ausente/desatualizada (causa-raiz)
Imóveis **sem base de referência não passam pela automação** e caem inteiros na fila manual
(Matriz CSD C3). A base vem de imagens de satélite, mas a cobertura é **desigual** (habilitada
município a município, C4) e a atualização é lenta — enquanto o desafio pede atualização **anual**.

### Gap B — Sobreposições detectadas na mão
A detecção de sobreposição (imóvel × imóvel, × assentamento, × área protegida) é **manual e visual**
(Jornada, etapa 5). Alto risco de passar despercebido; é uma "solução esperada" explícita do Desafio 2.

### Gap C — Dados fragmentados, sem painel único
A analista alterna entre ~4 sistemas (SICAR, bases fundiárias SNCR/SIGEF, imagens, anexos) e refaz
"na mão" a comparação declarado × referência que a RD já automatiza nos casos cobertos (Jornada 2–3–6).

## 2. How Might We (perguntas de ideação)

**Gap A — base de referência**
- HMW **gerar e atualizar automaticamente** a base de referência de uso e cobertura do solo, por município, com **periodicidade anual**?
- HMW deixar **explícito para a Luana** quão atual é a base (data da base × data da imagem) para ela confiar/descartar uma divergência?
- HMW **ampliar a cobertura** da pré-validação para os municípios que hoje não têm base de referência?

**Gap B — sobreposições**
- HMW **detectar e destacar sobreposições automaticamente** no momento em que o cadastro entra na fila?
- HMW **priorizar a fila** por risco (sobreposição + risco ambiental) em vez de ordem de chegada?

**Gap C — painel integrado**
- HMW **consolidar declaração + referência + bases fundiárias** num único painel de análise?
- HMW **estender o motor "declarado × referência" (modelo RD)** para os casos que hoje são 100% manuais, com memória de cálculo e template de parecer?

## 3. Candidatos a recorte × Impacto × Esforço (pré-triagem)

| Recorte candidato | Cobre gaps | Impacto p/ Luana | Esforço (protótipo) | Aderência Desafio 2 |
|---|---|---|---|---|
| **R1. Painel de pré-validação + priorização da fila** (declarado×referência + sobreposição destacada + fila por risco) | A·B·C | 🟢 Alto | 🟡 Médio (mockup forte + PoC pequena) | "dados integrados, fluxo e correções rápidas" |
| **R2. Motor de detecção de sobreposições** (alerta automático priorizável) | B | 🟢 Alto | 🟢 Baixo/Médio (PostGIS faz o cálculo) | "dados georreferenciados vetorizados / uso restrito" |
| **R3. Pipeline de atualização da base de referência** (ingestão + atualização anual) | A | 🟢 Alto (causa-raiz) | 🔴 Alto (dados + processamento) | "geração automatizada de bases" / "atualização de mapas" |
| **R4. Desenho via celular/drone** (Seu Raimundo) | — | 🟡 Médio | 🔴 Alto | "desenho georreferenciado acessível" |

### ✅ Recorte escolhido (2026-06-25)
**R1 — Painel de pré-validação com priorização da fila**, usando **R2 (detecção de sobreposição)**
como a prova de conceito técnica enxuta da entrega híbrida. _(Confirmado pela equipe.)_

**Por quê:**
- Ataca os **três gaps** ao mesmo tempo e o **pico de dor #1** da Luana (sobreposição) com o **#3** (fragmentação).
- A entrega híbrida fica natural: **mockup** do painel (Figma) + **PoC** de detecção de sobreposição em **PostGIS** sobre polígonos reais do SICAR (encaixa na pilha do RER, sem reinventar).
- R3 (base de referência) é a causa-raiz, mas é alto esforço de dados; entra como **roadmap/visão**, não como protótipo inicial — o painel já mostra "data da base" preparando o terreno.

## 4. Próximos passos (entrar no 2º losango: Desenvolver)
- [ ] Validar a recomendação de recorte com a equipe (ou rodar AskUserQuestion).
- [ ] Rascunhar a **jornada futura** da Luana com o painel (storyboard).
- [ ] Esboçar o **wireframe** do painel (fila priorizada + comparação declarado×referência + alerta de sobreposição).
- [x] Validar viabilidade da **PoC de sobreposição** — feita em `src/poc-sobreposicao/` (PostGIS + `ST_Intersects`/`ST_Intersection`; verificada localmente via GDAL/Spatialite). Detecta CAR×assentamento e CAR×CAR, quantifica em ha e exporta GeoJSON para o mapa.
- [x] **Pipeline de ingestão de dados reais** — `src/pipeline-ingestao/` baixa recorte municipal do **SICAR WFS oficial** e roda a detecção. Validado em **Itaguajé/PR (364 imóveis → 491 pares conflitantes reais)**. Dados em `data/` (não versionados; data de extração registrada).
- [ ] Confirmar no RER o que já existe (map_component/Leaflet, calc_engine) para **estender** em vez de recriar.
