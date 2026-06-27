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
- **Assentamentos (INCRA):** para a detecção CAR × assentamento. Endpoint que **funciona**
  (verificado 2026-06-25, via Acervo Fundiário do INCRA):
  `https://acervofundiario.incra.gov.br/i3geo/ogc.php?tema=assentamentos_<uf>` — MapServer WFS 1.0.0,
  uma camada por UF, campos ricos (`nome_projeto`, `municipio`, `num_familias`, `fase`, `cd_sipra`…).
  ⚠️ **Devolve coordenadas em ordem lat,lon** — `baixar_assentamentos.sh incra <uf>` corrige o eixo
  automaticamente. *(O geoserver "oficial" do INCRA e a INDE não serviram — só o i3geo respondeu;
  a fragilidade de acesso a dados de referência é, ela própria, o problema do Desafio 2.)*

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
./baixar_assentamentos.sh incra pr                 # baixa os 309 PAs do PR (i3geo, eixo corrigido)
./baixar.sh PR "Querência do Norte"                # município com muitos assentamentos
./verificar_assentamento_local.sh \
    ../../data/sicar/imoveis_pr_querencia_do_norte.geojson \
    ../../data/assentamentos/assentamentos_pr.geojson 1000
#  (alternativas: 'local <arquivo_incra> <imoveis>' ou 'exemplo <imoveis>')
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
- **CAR × assentamento com dados 100% reais** (Querência do Norte/PR, 548 imóveis × 309 PAs do INCRA):
  **69 imóveis CAR sobrepõem 10 assentamentos reais**, a maioria a **100%** (imóvel inteiro dentro do
  PA — ex.: PA Chico Mendes, PA Che Guevara, PA Pontal do Tigre/331 famílias). É exatamente o caso que
  o manual da Retificação Dinamizada cita como bloqueador da validação automática.

## Decisões técnicas
- **Tolerância de área:** divisas que apenas se tocam têm interseção de área ~0 e são ignoradas;
  o limite (default 100 m² / 0,01 ha) deve ser calibrado ao "limite legal de tolerância".
- **`ST_MakeValid`:** dados reais trazem geometrias inválidas (auto-interseção); saneamos antes de medir.
- **Área em hectares:** PostGIS mede via `geography` (elipsoide); a verificação local reprojeta para
  UTM 22S (EPSG:31982). Diferenças decimais entre os dois métodos não afetam a detecção.

## Próximos passos
- Servir `saida/sobreposicoes_*.geojson` como camadas no **mapa Leaflet** do painel (R1).
- Rodar sobre uma **UF inteira** validando o desempenho do índice GiST.
- Cruzar também com `parcelageo_<uf>` (SIGEF) e `quilombolas_<uf>` do mesmo i3geo do INCRA.
