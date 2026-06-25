# Base documental do projeto

Material de referência **autoritativo do domínio**, organizado por tema. Os PDFs são pesados
e **não são versionados** (ver `.gitignore`) — ficam locais nesta pasta. Os arquivos `.md`
de referência são versionados. Consulte estes documentos antes de pesquisar fora.

## Organização das pastas

```
docs/base-documental/
├── manuais/        # Manuais operacionais do SICAR
├── legislacao/     # Leis e decretos que fundamentam as regras de negócio
├── metodologia/    # Enunciado dos desafios, ideação e prototipação
└── ecossistema/    # Sistemas/plataformas do CAR e acesso ao ambiente de testes
```

## manuais/ — Manuais operacionais do SICAR

| Arquivo | O que contém | Quando usar |
|---|---|---|
| `manual_modulo_cadastro.pdf` | Módulo de Cadastro v3.7 (etapa Geo, 5 passos, imagens de satélite, vetorização) | Fluxo geoespacial atual e atritos |
| `manual_modulo_cadastro_pre_preenchido.pdf` | Módulo Pré-Preenchido (consulta SNCR/SIGEF, retificação) | Pré-preenchimento e bases fundiárias |
| `Manual_Retificacao_Dinamizada.pdf` | Retificação Dinamizada do SICAR (2023) — declarado × referência | Mecanismo de validação e divergências |
| `Manual_Central_do_Proprietario_Possuidor.pdf` | Central do Proprietário/Possuidor | Canal de atendimento/notificação |

## legislacao/ — Base legal

| Arquivo | O que contém | Quando usar |
|---|---|---|
| `L12651.pdf` | Lei nº 12.651/2012 — Código Florestal | APP, Reserva Legal, uso restrito |
| `Decreto nº 7830.pdf` | Decreto nº 7.830/2012 — institui o SICAR | Regras do sistema |

## metodologia/ — Desafios, ideação e prototipação

| Arquivo | O que contém | Quando usar |
|---|---|---|
| `esperado.md` | Enunciado oficial dos 3 desafios e soluções esperadas | Escopo e aderência ao Desafio 2 |
| `Resumo_haCARthon_Ideacao_Prototipacao.md` | Metodologia (Duplo Diamante), personas, formato de entrega | Conduzir ideação/prototipação |
| `Identificacao_oportunidades.pdf` | Guia de identificação de oportunidades (imersão, jornada, JTBD) | Descobrir e enquadrar o problema |
| `ideacao_prototipacao.pdf` | Slides de ideação e prototipação (versão completa) | Apoiar a ideação |
| `ideacao_prototipacao_compressed.pdf` | Mesma apresentação, versão leve | Leitura rápida |

## ecossistema/ — Sistemas do CAR e acesso ao ambiente de testes

| Arquivo | O que contém | Quando usar |
|---|---|---|
| `CAR DPG - Sistemas, plataformas e repositórios do CAR_V4.docx.pdf` | Lista de sistemas/plataformas/repositórios do CAR | Mapear ecossistema, evitar retrabalho |
| `Acesso ao Módulo de Cadastro Pré- Preenchido.pdf` | Credenciais e acesso ao ambiente de testes | Acessar ambiente de testes ⚠️ ver segurança |

> ⚠️ O PDF de **acesso** contém credenciais do ambiente de testes — **não** copiar CPFs/SNCR/senhas
> para arquivos versionados. Manter segredos apenas no `.env` local.

> Briefing oficial dos desafios (online): https://repositorio.enap.gov.br/bitstream/1/9909/5/haCARthon%20-%20Briefing%20dos%20desafios%20-%20vers%c3%a3o%202.pdf
