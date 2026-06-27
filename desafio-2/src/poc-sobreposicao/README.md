# PoC — Detecção de sobreposição em PostGIS (Desafio 2 · recorte R2)

Prova de conceito técnica enxuta da entrega híbrida. Demonstra, de forma automática, a
**detecção de sobreposições** que hoje a Luana faz na mão (Jornada, etapa 5) — o gargalo nº 1
nomeado pelo estudo CPI/PUC-Rio (em Mato Grosso, ~30% dos cadastros têm sobreposições relevantes,
ver `docs/briefing.md` §2.1).

## O que ela faz
A partir de polígonos de imóveis do CAR e de assentamentos (INCRA), o motor espacial:
1. **detecta** quais imóveis sobrepõem assentamentos (CAR × assentamento);
2. **detecta** conflitos entre cadastros (CAR × CAR);
3. **quantifica** a área sobreposta em hectares e o % do imóvel;
4. monta uma **fila priorizada** com flags por imóvel (alimenta o painel R1);
5. exporta a **camada de sobreposições em GeoJSON** para o mapa Leaflet do painel.

## Stack
PostGIS (alinhado ao RER). Funções centrais: `ST_Intersects`, `ST_Overlaps`, `ST_Intersection`,
`ST_Area`. Índices GiST tornam a varredura da fila inteira viável em escala. CRS dos dados:
**SIRGAS 2000 (EPSG:4674)**, o oficial do CAR; área medida via `geography` (m² no elipsoide → ha).

## Estrutura
```
src/poc-sobreposicao/
├── docker-compose.yml      # PostGIS 16 / 3.4
├── run.sh                  # caminho canônico: roda tudo no PostGIS (precisa de Docker)
├── verificar_local.sh      # valida a lógica SEM Docker, via GDAL/Spatialite
├── sql/
│   ├── 01_schema.sql       # tabelas + índices espaciais
│   ├── 02_carga.sql        # dados sintéticos (ST_GeomFromText)
│   └── 03_deteccao.sql     # as 4 consultas + export GeoJSON
├── dados/                  # cenário sintético (FICTÍCIO) em GeoJSON / EPSG:4674
│   ├── imoveis_car.geojson      # 3 imóveis: 2 com conflito, 1 controle (sem sobreposição)
│   └── assentamentos.geojson    # 1 assentamento (PA Boa Vista)
└── saida/
    └── sobreposicoes.geojson    # resultado p/ o mapa (gerado)
```

## Como rodar

### Opção A — PostGIS (canônica, com Docker)
```bash
cd src/poc-sobreposicao
./run.sh            # sobe o PostGIS, cria, carrega e roda as consultas
# ... ao final:
docker compose down -v
```

### Opção B — sem Docker (validação rápida)
```bash
cd src/poc-sobreposicao
./verificar_local.sh   # usa GDAL/Spatialite (mesmas funções ST_*)
```
> A opção B reprojeta para EPSG:31982 (UTM 22S) para medir área em metros; o PostGIS mede via
> `geography`. Pequenas diferenças decimais entre as duas são esperadas e não afetam a detecção.

## Resultado esperado (dados sintéticos)
| Tipo | Imóvel | Conflita com | Sobreposição |
|---|---|---|---|
| CAR × assentamento | Fazenda Milho Verde IV | PA Boa Vista (INCRA) | **~85 ha (18,8%)** |
| CAR × CAR | Fazenda Milho Verde IV | Sítio Boa Esperança | **~82 ha** |
| controle | Fazenda Santa Fé | — | **nenhuma** (não sinalizada) |

## Próximos passos
- **Dados reais:** trocar o cenário sintético por um recorte municipal do SICAR
  (`ogr2ogr -f PostgreSQL PG:"..." imovel_AT.shp`) + base de assentamentos do INCRA.
  Registrar a **data de extração** em `data/README.md`.
- **Integração:** servir `saida/sobreposicoes.geojson` como camada no mapa Leaflet do painel
  (substitui os SVGs estáticos do wireframe), reusando o `map_component` do RER.
- **Escala:** validar o `ST_Intersects` com índice GiST sobre uma base estadual completa.

> ⚠️ Dados **fictícios** para demonstração. Não representam imóveis reais e não tocam produção.
