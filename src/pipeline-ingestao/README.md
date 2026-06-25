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
- **Assentamentos (INCRA):** opcional, para a detecção CAR × assentamento (ver `../poc-sobreposicao`).
  O acervo fundiário do INCRA expõe as camadas; confirmar o endpoint WFS vigente antes de depender
  (na verificação de 2026-06-25 o caminho testado não respondeu de forma estável).

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
```

## Arquivos
| Arquivo | Papel |
|---|---|
| `baixar.sh` | Baixa o recorte municipal do SICAR WFS (param. UF + município) e registra proveniência |
| `carregar.sh` | Carrega o GeoJSON no PostGIS (ogr2ogr), saneia e roda a detecção |
| `verificar_local.sh` | Mesma detecção sem Docker (GDAL/Spatialite) |
| `sql/10_schema_real.sql` | `ST_MakeValid` + índice GiST sobre a tabela carregada |
| `sql/11_deteccao_car.sql` | Detecção CAR × CAR com tolerância + export GeoJSON |

## Resultado real verificado (Itaguajé/PR, 2026-06-25)
- **364 imóveis** baixados (366 KB).
- **491 pares** com sobreposição acima de 100 m² (tolerância) — ou seja, conflitos reais que
  travariam a validação automática e cairiam na fila da Luana.
- Maiores sobreposições passam de **1.000 ha** — fortes candidatos a **cadastros duplicados /
  re-declarados** (exatamente o tipo de inconsistência que o motor precisa sinalizar e priorizar).

## Decisões técnicas
- **Tolerância de área:** divisas que apenas se tocam têm interseção de área ~0 e são ignoradas;
  o limite (default 100 m² / 0,01 ha) deve ser calibrado ao "limite legal de tolerância".
- **`ST_MakeValid`:** dados reais trazem geometrias inválidas (auto-interseção); saneamos antes de medir.
- **Área em hectares:** PostGIS mede via `geography` (elipsoide); a verificação local reprojeta para
  UTM 22S (EPSG:31982). Diferenças decimais entre os dois métodos não afetam a detecção.

## Próximos passos
- Acoplar a base de **assentamentos do INCRA** para reativar a detecção CAR × assentamento.
- Servir `saida/sobreposicoes_reais.geojson` como camada no **mapa Leaflet** do painel (R1).
- Rodar sobre uma **UF inteira** validando o desempenho do índice GiST.
