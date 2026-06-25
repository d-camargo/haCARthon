# Dados geoespaciais

Bases usadas no projeto. **Arquivos pesados não são versionados** (ver `.gitignore`) —
este README é o registro do que existe, de onde veio e **quando foi extraído**.

## Registro de extrações

| Base | Fonte | UF/recorte | Categoria(s) | Data de extração | Observações |
|---|---|---|---|---|---|
| `sicar/imoveis_pr_itaguaje.geojson` | SICAR WFS oficial (`geoserver.car.gov.br`) | PR / Itaguajé | imóveis (perímetro) | 2026-06-25 | 364 imóveis; baixado por `src/pipeline-ingestao/baixar.sh`; não versionado |
| _(exemplo)_ | Consulta Pública SICAR | — | perímetro/APP/RL | AAAA-MM-DD | — |

## Fontes oficiais preferenciais

- **Downloads SICAR (shapefile/KML):** Consulta Pública Federal, por estado/município.
  Campos-chave: `cod_imovel`, `ind_status` (`AT` ativo, `PE` pendente, `CA` cancelado).
  Exigem e-mail + captcha.
- **WMS/WFS oficial:** `https://geoserver.car.gov.br/geoserver/sicar/wfs` (disponibilidade
  variável — validar antes de depender).
- **Bases fundiárias de referência:** SNCR, SIGEF; **SNIF** para bases florestais.
- **Assentamentos (INCRA):** "Assentamento Brasil" — Acervo Fundiário do INCRA. ⚠️ Em 2026-06-25
  o acervo exigia **login** e os geoservers/i3geo estavam fora do ar; usar download manual ou um
  WFS estável quando disponível (ver `src/pipeline-ingestao/baixar_assentamentos.sh`).
- **Automação de download (comunidade):** `urbanogilson/SICAR` (OCR de captcha).
- **MapBiomas:** alternativa de uso/cobertura do solo (menos atualizada que a oficial).

> ⚠️ Verificar disponibilidade e atualização antes de assumir que funcionam.
> **Sempre registrar a data de extração** na tabela acima.
