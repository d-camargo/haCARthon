# Referências e fontes externas

Fontes consultadas no projeto, com **data de acesso** (disciplina de rastreabilidade do projeto).
Os documentos-base (manuais, leis, edital, estudo) estão em `docs/base-documental/` — aqui ficam os
**links externos** (web, endpoints, estudos online) usados nas decisões.

## Validação de uso de QGIS pela persona (ver `definir/opcao-entrega-qgis-vs-web.md`)
Acesso em 2026-06-25.

| Fonte | Para quê | Link |
|---|---|---|
| **GeoCAR** — plugin QGIS para CAR | Precedente de plugin de CAR no QGIS (extensão, não invenção) | https://plugins.qgis.org/plugins/geocar/ |
| **Saberes da Floresta** (SFB) — geoprocessamento p/ notificações do CAR em QGIS | Ecossistema oficial já usa QGIS na análise | https://saberes.florestal.gov.br/mod/page/view.php?id=11845 |
| **ENAP** — Geoprocessamento Aplicado às Políticas Públicas (intro a QGIS) | Gancho de capacitação (curso do próprio organizador) | https://suap.enap.gov.br/vitrine/curso/1822/ |
| **CONTECC 2025** — Análise de sobreposição do CAR com base do SIGEF | Detecção de sobreposição em QGIS é prática estabelecida | https://www.confea.org.br/midias/uploads-imce/CONTECC2025/AGRO/AN%C3%81LISE_DE_SOBREPOSI%C3%87%C3%83O_NO_CADASTRO_AMBIENTAL_RURAL_(CAR)_COM_USO_DA_BASE_FUNDI%C3%81RIA_DO_SIGEF.pdf |
| **ResearchGate** — metodologia p/ análise e remoção de sobreposição no CAR | Metodologias de remoção de sobreposição a partir dos dados brutos do SICAR | https://researchgate.net/publication/381993179 |

## Endpoints de dados geoespaciais (usados em `src/pipeline-ingestao/`)
Verificados no ar em 2026-06-25. Detalhes em `data/README.md`.

| Fonte | Endpoint | Observação |
|---|---|---|
| **SICAR — imóveis (WFS oficial)** | https://geoserver.car.gov.br/geoserver/sicar/wfs | camada `sicar:sicar_imoveis_<uf>`; EPSG:4674; `CQL_FILTER` por município |
| **INCRA — assentamentos (i3geo WFS)** | https://acervofundiario.incra.gov.br/i3geo/ogc.php?tema=assentamentos_<uf> | MapServer WFS 1.0.0; ⚠️ eixo lat,lon (corrigido no pipeline) |

## Estudo de referência
| Fonte | Link |
|---|---|
| **CPI/PUC-Rio — "Onde Estamos na Implementação do Código Florestal?" (Ed. 2025)** | arquivo local em `docs/base-documental/estudos/Onde-Estamos-2025.pdf` |
| Briefing oficial dos desafios (ENAP) | https://repositorio.enap.gov.br/bitstream/1/9909/5/haCARthon%20-%20Briefing%20dos%20desafios%20-%20vers%c3%a3o%202.pdf |

## Ecossistema oficial do CAR (referência permanente)
Portal CAR https://car.gov.br · Consulta pública https://consultapublica.car.gov.br ·
Painel de dados https://painel.car.gov.br · RER (DPG) https://github.com/Rural-Environmental-Registry

> ⚠️ Endpoints e páginas externas mudam/saem do ar. Sempre **reverificar** antes de depender e
> **atualizar a data de acesso** ao reusar.
