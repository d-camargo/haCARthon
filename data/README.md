# Dados geoespaciais

Bases usadas no projeto. **Arquivos pesados não são versionados** (ver `.gitignore`) —
este README é o registro do que existe, de onde veio e **quando foi extraído**.

## Registro de extrações

| Base | Fonte | UF/recorte | Categoria(s) | Data de extração | Observações |
|---|---|---|---|---|---|
| _(exemplo)_ | Consulta Pública SICAR | — | perímetro/APP/RL | AAAA-MM-DD | — |

## Fontes oficiais preferenciais

- **Downloads SICAR (shapefile/KML):** Consulta Pública Federal, por estado/município.
  Campos-chave: `cod_imovel`, `ind_status` (`AT` ativo, `PE` pendente, `CA` cancelado).
  Exigem e-mail + captcha.
- **WMS/WFS oficial:** `https://geoserver.car.gov.br/geoserver/sicar/wfs` (disponibilidade
  variável — validar antes de depender).
- **Bases fundiárias de referência:** SNCR, SIGEF; **SNIF** para bases florestais.
- **Automação de download (comunidade):** `urbanogilson/SICAR` (OCR de captcha).
- **MapBiomas:** alternativa de uso/cobertura do solo (menos atualizada que a oficial).

> ⚠️ Verificar disponibilidade e atualização antes de assumir que funcionam.
> **Sempre registrar a data de extração** na tabela acima.
