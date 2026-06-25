# Matriz CSD — Desafio 2 (Certezas, Suposições, Dúvidas)

> Ferramenta da fase **Descobrir**. Separa o que sabemos do que precisamos validar.
> Fonte primária: `Manual_Retificacao_Dinamizada.pdf` (SFB, 2023) + personas do `CLAUDE.md`.
> Cada item marca a origem: **[manual]** fundamentado · **[persona]** material do projeto · **[inferência]** a confirmar.
> Data de levantamento: 2026-06-25.

## ✅ Certezas (fundamentadas)

| # | Certeza | Origem |
|---|---|---|
| C1 | A **Análise/Retificação Dinamizada** compara automaticamente o **declarado × base de referência** e gera **divergência por feição**: RVN, área consolidada, curso d'água, APP de cursos d'água/nascentes e Reserva Legal. | [manual] |
| C2 | Se o proprietário **aceita** a sugestão, a retificação é **automática**; se **rejeita** (ou o caso é complexo), o cadastro vai para a **análise técnica do órgão estadual** — a mesa da Luana. | [manual] |
| C3 | Há casos que **a automação não resolve** e que **obrigatoriamente** vão para análise manual: imóveis **sem base de referência**; com **Área de Uso Restrito**; **sobreposição com assentamentos**; **RL averbada / aprovada não averbada**; compensação ambiental; alteração de área após 22/07/2008; antropização não consolidada pós-2008; assentamentos (AST) e povos/comunidades tradicionais (PCT). | [manual, pág. 39] |
| C4 | A Retificação/Análise Dinamizada é **habilitada município a município**, conforme interesse do órgão estadual competente. Cobertura é **desigual** pelo país. | [manual, pág. 39] |
| C5 | A base de referência vem de **arquivos temáticos** de cobertura do solo e hidrografia **obtidos de imagens de satélite**. | [manual] |
| C6 | Existe **memória de cálculo** por feição, ancorada na lei (Arts. 12, 67 e 68 da Lei 12.651/2012); o Art. 68 nunca é sugerido automaticamente (exige comprovação documental). | [manual] |
| C7 | A persona primária (Luana) enfrenta **fila de ~12.000 análises**, **sobreposições difíceis de detectar** e **troca constante entre 4 sistemas**. | [persona] |

## 🤔 Suposições (a validar)

| # | Suposição | Como testar |
|---|---|---|
| S1 | A fila da Luana é dominada pelos casos que a automação **não** cobre (sem base de referência + sobreposição), não por volume "simples". | Cruzar composição da fila por motivo de exceção (C3) com um órgão estadual. |
| S2 | Base de referência **desatualizada/ausente** gera divergências "falsas" e retrabalho — e é o gargalo de origem do Desafio 2. | Comparar data da base de referência vs. data da imagem; medir % de divergências revertidas na análise. |
| S3 | **Ampliar e atualizar** a base de referência (cobertura por município) reduz **diretamente** o tamanho da fila manual. | Estimar quantos casos da fila se enquadram em "sem base de referência" (C3). |
| S4 | A "troca entre 4 sistemas" decorre de dados **fragmentados** (SICAR, SNCR/SIGEF, imagens, bases fundiárias) sem painel único. | Mapear com a Luana quais sistemas e qual dado busca em cada um. |
| S5 | Sobreposições hoje são detectadas de forma **manual/visual**, caso a caso. | Confirmar o procedimento atual de detecção de sobreposição no órgão. |

## ❓ Dúvidas (a pesquisar)

| # | Dúvida | Onde buscar |
|---|---|---|
| D1 | Quais são exatamente os **4 sistemas** que a Luana alterna e o que busca em cada um? | Entrevista com analista / manuais do órgão estadual. |
| D2 | Qual a **cobertura atual** da base de referência? Quantos municípios têm RD/AD habilitada? | Painel CAR, SFB, órgãos estaduais. |
| D3 | Com que **frequência** a base de uso/cobertura do solo é atualizada hoje? (o desafio pede atualização **anual**) | SFB / MapBiomas / base oficial. |
| D4 | Qual o **gargalo dominante** da fila: volume, complexidade jurídica ou ausência de base? | Dados do órgão estadual. |
| D5 | Sobreposições: entre imóveis CAR×CAR, CAR×assentamento, CAR×unidade de conservação? Qual o caso mais comum? | Base SICAR + análise espacial. |
| D6 | Que parte da análise é **documental** (não-geométrica) e, portanto, fora do alcance de solução geoespacial? | Manual de análise / entrevista. |

> **Leitura para a fase Definir:** as certezas C3 e C4 conectam o problema da Luana diretamente
> às soluções esperadas do Desafio 2 — *geração/atualização de bases de referência* e *detecção
> de sobreposições*. As suposições S2/S3 são a **hipótese central** a validar antes de fixar o recorte.
