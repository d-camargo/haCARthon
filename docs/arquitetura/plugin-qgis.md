# Arquitetura — Plugin QGIS de pré-validação do CAR (lado da Luana)

> Documento de arquitetura **antes de codar**. Define escopo, componentes, fluxo e decisões do plugin
> que entrega o recorte R1+R2 (detecção de sobreposição + priorização da fila) dentro do QGIS.
> Nome de trabalho (provisório, ver item aberto #3 do CLAUDE.md): **"Pré-Val CAR"** (codinome `prevalcar`).
> Data: 2026-06-25.

## 1. Objetivo e posicionamento

Dar à analista ambiental estadual (persona **Luana**) a pré-validação geoespacial **dentro da
ferramenta que ela já usa** (QGIS) — atacando a raiz do Gap C ("não criar mais um sistema").

**Complementar ao [GeoCAR](https://github.com/OpenGeoOne/GeoCAR), não concorrente:**

| | GeoCAR (existe) | Pré-Val CAR (este) |
|---|---|---|
| Lado | Entrada/preparação do cadastro (cadastrante) | **Análise/validação** (analista) |
| Faz | baixar CAR, APP por altitude/declividade, exportar SHP/ZIP/KML | **detecção de sobreposição** (CAR×CAR, CAR×assentamento), **fila priorizada**, **parecer/RAT** |

Reaproveita o **pipeline já validado** (`src/pipeline-ingestao/`): WFS do SICAR + INCRA i3geo + lógica de
detecção (ver `docs/referencias.md` para endpoints).

## 2. O que a ferramenta precisa cobrir (do trabalho real da Luana)

Fonte: `definir/opcao-entrega-qgis-vs-web.md` §1 (Fig. 8 do estudo). A Luana: analisa → detecta
inconsistências → **notifica** o proprietário / atesta conformidade / encaminha passivos ao **PRA**.
Logo, o MVP vai **da detecção até o rascunho de parecer/notificação (RAT)** — não para na detecção.

## 3. Decisões de arquitetura (fechadas em 2026-06-25)

| # | Decisão | Implicação |
|---|---|---|
| D1 | **Plugin novo e complementar** ao GeoCAR | mesmo padrão (Processing), sem acoplar ao código deles |
| D2 | **Native-first**: Processing provider **+ UX nativa do QGIS** (tabela de atributos, formulário de feição, estilo por regra, Layout+Atlas, Actions). **Sem dockwidget custom no MVP** | mínimo de código de GUI; menor manutenção; UX que a analista já conhece |
| D3 | **QGIS puro** (QgsGeometry), **PostGIS opcional** | roda offline na máquina dela; PostGIS só p/ escala (UF) |
| D4 | **MVP = detecção + fila + parecer/RAT** | entrega fim-a-fim, fiel ao fluxo da analista |

## 4. Visão de componentes

```
QGIS
 ├── Processing Provider "Pré-Val CAR"  ──────────────► usável em modelos/batch
 │     ├── alg: Baixar imóveis CAR (município)
 │     ├── alg: Baixar assentamentos INCRA (UF)   [corrige eixo lat,lon]
 │     ├── alg: Detectar sobreposição (CAR×CAR, CAR×assentamento)
 │     ├── alg: Priorizar fila (grava score na camada)
 │     └── (opcional) Modelo que encadeia os 4 num clique
 │
 └── UX NATIVA do QGIS (sem código de GUI próprio)  ──► experiência da analista
       ├── Tabela de atributos   = a "fila" (ordena por score, filtra conflito=1)
       ├── Estilo por regra       = conflitos em vermelho no mapa
       ├── Formulário de feição   = detalhe (sobreposições, %, memória)
       ├── Action de camada       = botão "Gerar parecer" na feição
       └── Print Layout + Atlas   = parecer/RAT em PDF (1 página por imóvel)
                 │
                 ▼
  core/ (lógica pura, testável fora do QGIS — espelha o pipeline)
       ├── wfs.py        clientes SICAR / INCRA (+ axis-fix)
       ├── detector.py   interface + estratégias  ◄── QGIS puro | PostGIS
       ├── priorizacao.py  score de risco / ordenação da fila
       └── parecer.py    monta o contexto do Atlas/parecer
```

**Princípio-chave:** os algoritmos Processing são **camadas finas** sobre o `core/`, e a experiência
da analista é montada com **recursos nativos do QGIS** (config, não código). O `core/` não importa
nada de GUI — dá para testar detecção/priorização sem abrir o QGIS (reusa a lógica do pipeline).
Nada de dockwidget custom no MVP → **a superfície de código de interface é praticamente zero**.

### 4.1 UX nativa — cada necessidade → recurso do QGIS (não código)
| Necessidade | Recurso nativo do QGIS | Esforço |
|---|---|---|
| Fila priorizada | **Tabela de atributos** ordenada por `score`, filtro `conflito=1` | config |
| Destaque no mapa | **Estilo baseado em regra** (QML versionado) | template |
| Zoom ao selecionar | *Zoom to selection* / *Flash* / **Action** | config |
| Detalhe do imóvel | **Formulário de feição** (form designer + widget HTML/expressão) | template |
| Botão "Gerar parecer" | **Action de camada** (dispara o Atlas) | config + script curto |
| Parecer/RAT em PDF | **Print Layout + Atlas** (1 página/imóvel) | template de layout |
| Encadear o fluxo | **Modelo do Processing** (Graphical Modeler) | config |

> Só vira código nosso: os **algoritmos Processing** (finos), o **`core/`**, o **template de Layout/Atlas**,
> o **QML de estilo** e 1–2 **Actions**. Reavaliar um painel custom **só** se a UX nativa falhar em teste real.

### Backend de cálculo (D3) — padrão Strategy
```
detector.DetectorSobreposicao (interface)
 ├── DetectorQGIS     usa QgsSpatialIndex + QgsGeometry.intersection + QgsDistanceArea (área elipsoidal → ha)
 └── DetectorPostGIS  (opcional) executa o SQL de 11_/12_deteccao via conexão PostGIS existente no QGIS
```
- Default **QGIS puro**: sem infra, funciona com as camadas já carregadas. Área via `QgsDistanceArea`
  com elipsoide SIRGAS 2000 = equivalente ao `geography` do PostGIS (mesma medida em ha).
- **PostGIS** entra quando a base é grande (UF inteira) e já há um banco — só troca a estratégia.

## 5. Fluxo de uso (jornada futura da Luana, no QGIS)

1. **Obter dados** (algoritmo ou painel): baixa o recorte municipal do CAR + assentamentos do INCRA
   (ou usa camadas que ela já tem abertas). Reprojeta p/ 4674, corrige eixo do INCRA, sane geometrias.
2. **Detectar**: roda a detecção → gera a camada `conflitos` (CAR×CAR e CAR×assentamento) com
   `sobrep_ha`, `pct_imovel`, `tipo`, `contra`.
3. **Triar**: a **tabela de atributos** (ordenada pelo `score`, filtro `conflito=1`) **é a fila**; ela
   clica numa linha → o mapa foca o imóvel e o **formulário de feição** abre o detalhe. (UX nativa.)
4. **Decidir**: inspeciona a sobreposição e a **memória de cálculo**; decide notificar / conformidade / PRA.
5. **Gerar parecer (RAT)**: rascunho pré-preenchido (imóvel, divergências, enquadramento legal, recomendação)
   → exporta PDF/HTML para ela revisar e assinar.

## 6. Módulos detalhados

### 6.1 Aquisição (`core/wfs.py`)
- SICAR: `sicar:sicar_imoveis_<uf>` por `CQL_FILTER=municipio`. Campos: `cod_imovel`, `status_imovel`,
  `condicao`, `municipio`, `area`, `m_fiscal`.
- INCRA: `assentamentos_<uf>` (i3geo) — **corrige ordem de eixo lat,lon → lon,lat**, padroniza `nome`.
- Implementação: `QgsVectorLayer` (provider WFS) ou `QgsBlockingNetworkRequest` (sem dependências pip).
- Registra **data de extração** (proveniência), coerente com `data/README.md`.

### 6.2 Detecção (`core/detector.py`)
- CAR×CAR: pares `cod_imovel a < b` com `ST_Intersects` e área de interseção **> tolerância**
  (default 0,01 ha — ajustável; lembrar que **o SICAR admite sobreposições na inscrição**, então
  classifica-se, não se trata todo overlap como erro).
- CAR×assentamento: imóvel × assentamento INCRA, com `pct_imovel`.
- Usa `QgsSpatialIndex` para viabilidade em escala.

### 6.3 Priorização (`core/priorizacao.py`)
- `score = w1·norm(sobrep_ha) + w2·pct_imovel + w3·peso_tipo(assentamento>CAR×CAR) + w4·sinal_social(num_familias)`.
- Pesos configuráveis. Saída: fila ordenada (o que falta hoje — a fila não é priorizada).

### 6.4 Parecer/RAT — **Print Layout + Atlas (nativo)**
- O parecer é um **template de Print Layout** com o Atlas ligado à camada de imóveis (1 página por
  imóvel). Campos via **expressões/HTML frame**: identificação, **lista de sobreposições** (com quem,
  ha, %), **memória de cálculo** (inspirada na Retificação Dinamizada), **enquadramento legal**
  (Lei 12.651/2012) e **recomendação** (notificar / conformidade / encaminhar PRA). Exporta PDF nativo.
- `core/parecer.py` só **prepara o contexto** (campos calculados/atributos) que o Atlas consome — não
  gera PDF na mão. Disparável por uma **Action** na feição.
- É **rascunho assistido**: a analista revisa e assina. Não automatiza a decisão.

## 7. Estrutura de pastas proposta
```
src/plugin-qgis/
├── metadata.txt          # name, qgisMinimumVersion=3.40, version, about, tags
├── __init__.py           # classFactory()
├── plugin.py             # registra provider + dockwidget
├── provider.py           # QgsProcessingProvider
├── processing/           # algoritmos (camada fina sobre core/)
│   ├── baixar_sicar.py
│   ├── baixar_assentamentos_incra.py
│   ├── detectar_sobreposicao.py
│   └── gerar_parecer.py
├── core/                 # lógica pura, testável sem QGIS  (espelha src/pipeline-ingestao)
│   ├── wfs.py
│   ├── detector.py
│   ├── priorizacao.py
│   └── parecer.py        # prepara o contexto do Atlas (não gera PDF na mão)
├── recursos_qgis/        # artefatos NATIVOS versionados (config, não código de GUI)
│   ├── parecer_rat.qpt   # template de Print Layout (Atlas) do parecer
│   ├── estilo_conflito.qml  # estilo baseado em regra (conflitos em vermelho)
│   ├── form_imovel.ui    # formulário de feição (detalhe)
│   └── actions.json      # Actions de camada (ex.: "Gerar parecer")
├── modelos/              # (opcional) modelo do Processing que encadeia o fluxo
├── resources/ (ícones)
└── tests/  (testa core/ com os dados de Querência do Norte)
# Sem dockwidget custom no MVP (ver D2).
```

## 8. Mapeamento: pipeline atual → plugin
| Hoje (`src/pipeline-ingestao/`) | Vira no plugin |
|---|---|
| `baixar.sh` | `processing/baixar_sicar.py` → `core/wfs.py` |
| `baixar_assentamentos.sh incra` (axis-fix) | `processing/baixar_assentamentos_incra.py` → `core/wfs.py` |
| `sql/11_deteccao_car.sql`, `sql/12_deteccao_assentamento.sql` | `core/detector.py` (QGIS puro) **ou** `DetectorPostGIS` |
| `verificar_*_local.sh` | `tests/` (mesmos dados, mesmas asserções) |
| (novo) | `core/priorizacao.py`, `core/parecer.py` + recursos nativos (`.qpt`/`.qml`/Actions) |

## 9. Compatibilidade, dependências e distribuição
- **QGIS ≥ 3.40** (alinha ao mínimo do GeoCAR para coexistir), PyQGIS + PyQt.
- **Sem dependências pip externas** no caminho padrão (usa GDAL/QGIS embutidos); PostGIS é opcional.
- Distribuição pelo **repositório oficial de plugins do QGIS** (DPG/GPL-3.0), versionado.
- i18n PT-BR (e EN no `about`, como o GeoCAR).

## 10. Restrições e segurança (alinhado ao CLAUDE.md)
- **Somente leitura/análise** — nunca escreve em produção do SICAR.
- Os campos do WFS não trazem CPF; ainda assim, tratar `cod_imovel`/dados como sensíveis (não logar/expor).
- Registrar **data de extração** de toda base baixada.

## 11. Riscos e mitigação
| Risco | Mitigação |
|---|---|
| API PyQGIS muda entre versões | **native-first (D2): zero dockwidget custom** + lógica no `core/` (sem QGIS) → superfície de GUI mínima; testes em `tests/` |
| Proficiência variável em QGIS | curso ENAP (ver "O Pedido", `opcao-entrega-qgis-vs-web.md` §5) |
| Endpoints externos instáveis (INCRA) | tolerância a falha + modo "usar camadas já carregadas" + cache local |
| Escala (UF inteira) trava QGIS puro | estratégia PostGIS opcional (D3) |
| Sobreposição "legal" tratada como erro | tolerância + **classificação** (não decide, sinaliza) |

## 12. Itens em aberto (a decidir antes/durante o código)
- Nome definitivo + ícone (item #3 do CLAUDE.md).
- Pesos do score de priorização (validar com analista — "O Pedido" §1).
- Formato final do parecer (HTML/PDF; campos obrigatórios do RAT do órgão).
- Reaproveitar a função `baixarCAR` do GeoCAR como referência de implementação do WFS?
