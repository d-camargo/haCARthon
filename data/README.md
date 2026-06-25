# Dados geoespaciais

Bases usadas no projeto. **Arquivos pesados não são versionados** (ver `.gitignore`) —
este README é o registro do que existe, de onde veio e **quando foi extraído**.

## Registro de extrações

| Base | Fonte | UF/recorte | Categoria(s) | Data de extração | Observações |
|---|---|---|---|---|---|
| `sicar/imoveis_pr_itaguaje.geojson` | SICAR WFS oficial (`geoserver.car.gov.br`) | PR / Itaguajé | imóveis (perímetro) | 2026-06-25 | 364 imóveis; `baixar.sh`; não versionado |
| `sicar/imoveis_pr_querencia_do_norte.geojson` | SICAR WFS oficial | PR / Querência do Norte | imóveis (perímetro) | 2026-06-25 | 548 imóveis; `baixar.sh`; não versionado |
| `assentamentos/assentamentos_pr.geojson` | INCRA i3geo WFS (`acervofundiario.incra.gov.br`) | PR | assentamentos (PA) | 2026-06-25 | 309 PAs; `baixar_assentamentos.sh incra pr`; eixo corrigido; não versionado |
| _(exemplo)_ | Consulta Pública SICAR | — | perímetro/APP/RL | AAAA-MM-DD | — |

## Fontes oficiais preferenciais

- **Downloads SICAR (shapefile/KML):** Consulta Pública Federal, por estado/município.
  Campos-chave: `cod_imovel`, `ind_status` (`AT` ativo, `PE` pendente, `CA` cancelado).
  Exigem e-mail + captcha.
- **WMS/WFS oficial:** `https://geoserver.car.gov.br/geoserver/sicar/wfs` (disponibilidade
  variável — validar antes de depender).
- **Bases fundiárias de referência:** SNCR, SIGEF; **SNIF** para bases florestais.
- **Assentamentos (INCRA):** Acervo Fundiário — **i3geo WFS por UF** (✅ funciona, verificado 2026-06-25):
  `https://acervofundiario.incra.gov.br/i3geo/ogc.php?tema=assentamentos_<uf>` (MapServer WFS 1.0.0).
  ⚠️ Devolve coordenadas em ordem **lat,lon** — `baixar_assentamentos.sh incra <uf>` já corrige o eixo.
  Outros temas úteis no mesmo padrão: `parcelageo_<uf>`, `certificada_sigef_*_<uf>`, `quilombolas_<uf>`.
- **Automação de download (comunidade):** `urbanogilson/SICAR` (OCR de captcha).
- **MapBiomas:** alternativa de uso/cobertura do solo (menos atualizada que a oficial).

> ⚠️ Verificar disponibilidade e atualização antes de assumir que funcionam.
> **Sempre registrar a data de extração** na tabela acima.
