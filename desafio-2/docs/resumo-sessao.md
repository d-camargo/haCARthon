# Resumo da sessão — do zero ao plugin funcional

> Linha do tempo da conversa que construiu o **Pré-Val CAR**. Serve de referência para retomar.
> Repositório: github.com/d-camargo/haCARthon.

## Fase 1 — Descobrir/Definir (Duplo Diamante)
- Confirmado o **Desafio 2** (acesso a dados geoespaciais do CAR); persona primária **Luana**.
- Estruturado o repo, organizada a base documental por tema, lido o **Manual da Retificação Dinamizada**
  e o estudo **CPI/PUC-Rio "Onde Estamos 2025"** (dados nacionais que fundamentam o problema).
- Artefatos: `docs/descobrir/matriz-csd.md`, `docs/descobrir/jornada-luana.md`,
  `docs/definir/sintese-oportunidades.md`, `docs/briefing.md`.
- **Recorte escolhido (R1+R2):** painel de pré-validação da Luana + **detecção de sobreposição**.

## Fase 2 — Provas de conceito (entrega híbrida)
- **Wireframe** lo-fi do painel (`prototypes/painel-luana/index.html`).
- **PoC PostGIS** de detecção de sobreposição (`src/poc-sobreposicao/`), verificada via GDAL/Spatialite.
- **Pipeline de dados reais** (`src/pipeline-ingestao/`): baixa do **SICAR WFS** e do **INCRA i3geo WFS**,
  detecta CAR×CAR e CAR×assentamento. Validado: Itaguajé (491 pares) e **Querência do Norte (69 imóveis ×
  10 assentamentos reais)**. Endpoints salvos na memória do projeto.
- **Painel web** funcional com Leaflet e dados reais (`prototypes/painel-luana/painel.html`).

## Fase 3 — Decisão de canal: plugin QGIS
- Validado que **a Luana usa QGIS** (plugin GeoCAR existente, SFB/ENAP ensinam QGIS p/ CAR).
  Ver `docs/definir/opcao-entrega-qgis-vs-web.md` e `docs/referencias.md`.
- Decisão **híbrida, liderando pelo plugin QGIS** (native-first; única GUI custom = painel/KPIs).
- Arquitetura em `docs/arquitetura/plugin-qgis.md`. (GeoCAR foi só pesquisa — não é régua.)

## Fase 4 — Construção do plugin (`src/plugin-qgis/`, instalar como `prevalcar`)
Estrutura: `metadata.txt`, `plugin.py`, `provider.py`, `compat.py`, `processing/` (baixar SICAR/INCRA,
detectar, gerar parecer), `core/` (wfs, detector, priorizacao, parecer, municipios, layout_parecer),
`gui/kpis_dock.py` (painel), `estilos.py`, `icon.svg`.

### Bugs/lições resolvidos em sequência (todos commitados)
1. **Compat 3.x/4.x** (PyQt5↔PyQt6): `QVariant`→`QMetaType`, `Qgis.GeometryType/WkbType`,
   `QgsFeatureSink.Flag.FastInsert`, etc. → centralizados em `compat.py`.
2. **Ícone** 1,1MB → SVG; **`qgisMaximumVersion=4.99`** (sem isso o QGIS barrava a 4.0).
3. **WFS:** provider nativo expirava → **SICAR** via `QgsBlockingNetworkRequest` (GeoJSON; o `urllib` do
   Python do Flatpak falhava no **SSL**); **INCRA** via **GDAL WFS** + `swapXy()` (eixo lat,lon) e
   reprojeção para **4674**.
4. **parameterAsSink** exige `QgsFields` (não `list`).
5. **Geometria inválida:** `context.setInvalidGeometryCheck(GEOM_NO_CHECK)` + `makeValid()`.
6. **Área zerada → zero conflitos → KPIs zerados:** `setEllipsoid('GRS80')` (era `'EPSG:4674'`, que é CRS).
7. **UX:** consolidado em **1 painel** com botões (baixar / detectar / parecer), KPIs calculados direto
   das camadas; **estilo automático** (conflitos em vermelho, fila graduada por score).
8. **Município:** resolução da grafia via **IBGE** (aceita "querencia do norte", "MARINGA") + notificação.
9. **Nomes de camada** padronizados com o município.
10. **Parecer/RAT:** Print Layout + **Atlas** (2 páginas A4 retrato por imóvel). Sem WebKit →
    `QgsLayoutItemLabel` HTML + tabela capada. Ver `docs/arquitetura/parecer-layout.md`.

## Estado atual
Cadeia completa dentro do QGIS: **baixar → detectar/priorizar → KPIs/estilo → parecer PDF**, em uma janela.

## Tópicos abertos (separados em arquivos próprios)
- **Parecer/layout:** `docs/arquitetura/parecer-layout.md` (inclui plano de migrar para template `.qpt`).
- **Pitch:** `docs/pitch.md`.
- Calibragens finas do layout; piloto com órgão estadual; publicação do plugin.
