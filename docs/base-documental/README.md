# Base documental do projeto

Material de referência **autoritativo do domínio**, organizado por tema. Os PDFs são pesados
e **não são versionados** (ver `.gitignore`) — ficam locais nesta pasta. Os arquivos `.md`
de referência são versionados. Consulte estes documentos antes de pesquisar fora.

## Organização das pastas

```
docs/base-documental/
├── manuais/        # Manuais operacionais do SICAR
├── legislacao/     # Leis e decretos que fundamentam as regras de negócio
├── metodologia/    # Edital, enunciado dos desafios, ideação, prototipação e pitch
├── estudos/        # Estudos e dados externos sobre a implementação do CAR/PRA
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

## metodologia/ — Edital, desafios, ideação, prototipação e pitch

| Arquivo | O que contém | Quando usar |
|---|---|---|
| `Edital haCARthon - Assinado - SEI_0993344_Edital_158.pdf` | Edital oficial ENAP nº 158/2026 — regras da maratona | Conferir regras, prazos e critérios de avaliação |
| `haCARthon - Briefing dos desafios - versão 2.pdf` | **Briefing oficial dos desafios (v2, 16 págs)** — contexto, os 3 desafios detalhados, **personas oficiais (Seu Raimundo, Luana)** e exemplos de soluções | Fonte oficial da persona e do enunciado do desafio |
| `esperado.md` | Enunciado oficial dos 3 desafios e soluções esperadas (extrato do briefing) | Escopo e aderência ao desafio escolhido (atual: **D3**) |
| `Resumo_haCARthon_Ideacao_Prototipacao.md` | Metodologia (Duplo Diamante), personas, formato de entrega | Conduzir ideação/prototipação |
| `pitch.md` | Resumo da Live 04 — como construir o pitch (estrutura, slides, gravação) | Montar o pitch e o vídeo |
| `Live_05_orientacoes-entrega-tiraduvidas.md` | Transcrição da Live 05 — orientações de entrega (ideação/protótipo/pitch), prazos e tira-dúvidas | Conferir regras de entrega e validações da coordenação |
| `Live_06_tiraduvidas-desafios.md` | Transcrição da Live 06 — tira-dúvidas exclusivo dos desafios (com a coordenação do CAR) | Validações de escopo do D3 (IA p/ legislação, aceite no SICAR, etc.) |
| `Identificacao_oportunidades.pdf` | Guia de identificação de oportunidades (imersão, jornada, JTBD) | Descobrir e enquadrar o problema |
| `ideacao_prototipacao.pdf` | Slides de ideação e prototipação (versão completa) | Apoiar a ideação |
| `ideacao_prototipacao_compressed.pdf` | Mesma apresentação, versão leve | Leitura rápida |
| `Hacarthon - Live de Pitch (2).pdf` | Slides da Live de Pitch | Apoiar a construção do pitch |

## estudos/ — Estudos e dados externos sobre a implementação do CAR/PRA

| Arquivo | O que contém | Quando usar |
|---|---|---|
| `Onde-Estamos-2025.pdf` | CPI/PUC-Rio — "Onde Estamos na Implementação do Código Florestal? Radiografia do CAR e do PRA nos Estados, Ed. 2025". Dados de inscrição/análise por estado (nov/2025) | Dimensionar o problema, fundamentar o pitch (ver `desafio-2/docs/briefing.md` seção 2.1) |
| `LEG-Consultada-OE-2025.pdf` | Apêndice "Legislação Consultada" do estudo acima | Rastrear a legislação estadual consultada |

## ecossistema/ — Sistemas do CAR e acesso ao ambiente de testes

| Arquivo | O que contém | Quando usar |
|---|---|---|
| `CAR DPG - Sistemas, plataformas e repositórios do CAR_V4.docx.pdf` | Lista de sistemas/plataformas/repositórios do CAR | Mapear ecossistema, evitar retrabalho |
| `Meu-Imovel-Rural.md` | Transcrição do vídeo oficial do **Meu Imóvel Rural** (cruza CAR+SNCR+SIGEF, painel "Tô em Dia") | **Evidência do diferencial do D3**: as ferramentas oficiais traduzem a checklist de crédito, não as obrigações ambientais por feição |
| `Acesso ao Módulo de Cadastro Pré- Preenchido.pdf` | Credenciais e acesso ao ambiente de testes | Acessar ambiente de testes ⚠️ ver segurança |

> ⚠️ O PDF de **acesso** contém credenciais do ambiente de testes — **não** copiar CPFs/SNCR/senhas
> para arquivos versionados. Manter segredos apenas no `.env` local.

> Briefing oficial dos desafios: arquivo local em `metodologia/haCARthon - Briefing dos desafios - versão 2.pdf`
> (online: https://repositorio.enap.gov.br/bitstream/1/9909/5/haCARthon%20-%20Briefing%20dos%20desafios%20-%20vers%c3%a3o%202.pdf)
