# Pipeline de ingestão — dados reais do SICAR → PostGIS → detecção

Substitui os dados sintéticos da PoC (`../poc-sobreposicao`) por **dados reais e abertos do
SICAR**, baixados por município, e roda a detecção de sobreposição sobre eles. Caminho:

```
SICAR WFS oficial  ──baixar.sh──►  data/sicar/*.geojson  ──carregar.sh──►  PostGIS  ──►  detecção + GeoJSON
                                                          └─ verificar_local.sh (sem Docker, GDAL/Spatialite)
```

## Fonte dos dados
- **SICAR — WFS oficial:** `https://geoserver.car.gov.br/geoserver/sicar/wfs`
  - Uma camada por UF: `sicar:sicar_imoveis_<uf>` (ex.: `sicar_imoveis_pr`).
  - Campos: `cod_imovel`, `status_imovel` (AT/PE/CA), `condicao`, `municipio`, `cod_municipio_ibge`, `area`, `m_fiscal`, `tipo_imovel`.
  - Geometria **MultiPolygon** em **EPSG:4674** (SIRGAS 2000). Suporta `CQL_FILTER` (filtro por município).
  - ✅ Verificado no ar em **2026-06-25** (o PR retornou 548.159 imóveis — bate com os "548 mil" do estudo CPI/PUC-Rio).
- **Assentamentos (INCRA):** para a detecção CAR × assentamento. ⚠️ **Verificado em 2026-06-25:**
  a base de Projetos de Assentamento do INCRA **não tem endpoint aberto/scriptável estável** — o
  Acervo Fundiário exige login e os geoservers/i3geo estavam fora do ar (a INDE só tem
  "assentamentos precários" urbanos do MPOG, que **não** servem). Por isso a aquisição é
  **fonte-agnóstica** (`baixar_assentamentos.sh`): aceita arquivo local do INCRA, um WFS configurável,
  ou um polígono de **exemplo** para demonstrar o pipeline. *(Esta dificuldade de acesso é, ela
  própria, evidência do problema do Desafio 2: dados de referência fragmentados e inacessíveis.)*

> ⚠️ Sempre **registrar a data de extração** (feito automaticamente em `data/sicar/EXTRACOES.log`
> e manualmente em `data/README.md`). Dados baixados ficam em `data/` e **não são versionados**.

## Como usar

```bash
cd src/pipeline-ingestao

# 1) Baixar um recorte municipal (parametrizável)
./baixar.sh PR "Itaguajé"          # -> data/sicar/imoveis_pr_itaguaje.geojson

# 2a) Validar a lógica SEM Docker (rápido)
./verificar_local.sh ../../data/sicar/imoveis_pr_itaguaje.geojson 100

# 2b) Caminho canônico em PostGIS (requer Docker)
(cd ../poc-sobreposicao && docker compose up -d)     # sobe um PostGIS
./carregar.sh ../../data/sicar/imoveis_pr_itaguaje.geojson

# 3) Assentamentos (INCRA) — detecção CAR x assentamento
#    Modo real (recomendado): baixe "Assentamento Brasil" do INCRA e use 'local':
./baixar_assentamentos.sh local /caminho/Assentamento_Brasil.zip ../../data/sicar/imoveis_pr_itaguaje.geojson
#    Ou WFS: ASSENT_WFS_URL=... ASSENT_LAYER=... ./baixar_assentamentos.sh wfs <imoveis.geojson>
#    Ou exemplo (demonstra o pipeline sem dado real):
./baixar_assentamentos.sh exemplo ../../data/sicar/imoveis_pr_itaguaje.geojson
#    Detecção (sem Docker):
./verificar_assentamento_local.sh ../../data/sicar/imoveis_pr_itaguaje.geojson \
    ../../data/assentamentos/assentamentos_exemplo.geojson 100
```

## Arquivos
| Arquivo | Papel |
|---|---|
| `baixar.sh` | Baixa o recorte municipal do SICAR WFS (param. UF + município) e registra proveniência |
| `baixar_assentamentos.sh` | Obtém assentamentos do INCRA (modos `local` / `wfs` / `exemplo`), recortados ao município |
| `carregar.sh` | Carrega o GeoJSON no PostGIS (ogr2ogr), saneia e roda a detecção |
| `verificar_local.sh` | Detecção CAR × CAR sem Docker (GDAL/Spatialite) |
| `verificar_assentamento_local.sh` | Detecção CAR × assentamento sem Docker |
| `sql/10_schema_real.sql` | `ST_MakeValid` + índice GiST sobre a tabela carregada |
| `sql/11_deteccao_car.sql` | Detecção CAR × CAR com tolerância + export GeoJSON |
| `sql/12_deteccao_assentamento.sql` | Detecção CAR × assentamento + export GeoJSON |

## Resultado real verificado (Itaguajé/PR, 2026-06-25)
- **364 imóveis** baixados (366 KB).
- **491 pares** com sobreposição acima de 100 m² (tolerância) — ou seja, conflitos reais que
  travariam a validação automática e cairiam na fila da Luana.
- Maiores sobreposições passam de **1.000 ha** — fortes candidatos a **cadastros duplicados /
  re-declarados** (exatamente o tipo de inconsistência que o motor precisa sinalizar e priorizar).
- **CAR × assentamento** (com o PA de exemplo): vários imóveis reais sobrepõem o assentamento,
  com até **90% da área do imóvel** dentro do PA — o caso que o manual da RD cita como bloqueador
  da validação automática. Trocar o exemplo pela base real do INCRA não muda o código, só o dado.

## Decisões técnicas
- **Tolerância de área:** divisas que apenas se tocam têm interseção de área ~0 e são ignoradas;
  o limite (default 100 m² / 0,01 ha) deve ser calibrado ao "limite legal de tolerância".
- **`ST_MakeValid`:** dados reais trazem geometrias inválidas (auto-interseção); saneamos antes de medir.
- **Área em hectares:** PostGIS mede via `geography` (elipsoide); a verificação local reprojeta para
  UTM 22S (EPSG:31982). Diferenças decimais entre os dois métodos não afetam a detecção.

## Próximos passos
- Substituir o assentamento de **exemplo** pela base real do **INCRA** (modo `local`/`wfs`) quando
  houver acesso a um endpoint/arquivo estável.
- Servir `saida/sobreposicoes_*.geojson` como camadas no **mapa Leaflet** do painel (R1).
- Rodar sobre uma **UF inteira** validando o desempenho do índice GiST.
