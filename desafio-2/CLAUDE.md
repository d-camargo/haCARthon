# CLAUDE.md

Orientações para o Claude Code trabalhar neste projeto. Leia este arquivo no início de cada sessão.

## Contexto do projeto

Este é um projeto desenvolvido no contexto do **haCARthon**, hackathon cuja finalidade é desenvolver **soluções inovadoras** que fortaleçam o Sistema de Cadastro Ambiental Rural (**SICAR**) e consolidem o Cadastro Ambiental Rural (**CAR**) como um **Bem Público Digital (DPG)**, em modelo de **código aberto**.

> 🎯 **Esta equipe se inscreveu no DESAFIO 2 — Melhorar o acesso a dados geoespaciais do CAR.** Todo o foco do projeto é este desafio.

O CAR é o registro público eletrônico, de âmbito nacional, obrigatório para imóveis rurais brasileiros, criado pela Lei nº 12.651/2012 (Código Florestal) e operacionalizado pelo SICAR (Decreto nº 7.830/2012). O projeto deve respeitar esse arcabouço legal e o ecossistema já existente — **não reinventar o que o governo já construiu**.

### Importante sobre o formato da entrega
**Não é obrigatório apresentar software funcional ou código-fonte.** O foco é a **construção e validação de uma solução**. A entrega pode ser protótipo, wireframe, fluxograma, apresentação, mockup ou vídeo de pitch. Código funcional é bem-vindo, mas opcional. **Priorize validar a ideia antes de investir em implementação.**

### Princípio orientador

> **Comece pelo problema (e pela pessoa), não pela solução.**
> Toda solução que ignora o contexto real do usuário vira mais um sistema que ninguém usa.

Antes de propor ou codar qualquer coisa, valide: que dor real resolve, para qual persona, e se já existe nas plataformas oficiais.

## O Desafio 2 em detalhe

**Pergunta-desafio:** Como podemos atualizar anualmente, com rapidez e acurácia, o mapeamento de uso e cobertura do solo de todos os estados brasileiros, melhorando a atualização dos cadastros e propiciando o aumento na quantidade e qualidade das análises do CAR?

### Soluções esperadas (tipos de entrega que pontuam)
- Sistemas de **dados integrados**, com fluxo e correções rápidas.
- Sistemas de dados **georreferenciados vetorizados** de feições naturais (rios, rochas), Áreas de Preservação Permanente (APP) e outras áreas de uso restrito.
- Soluções para **geração automatizada de bases de referência**.
- Soluções para **atualização de mapas de uso e cobertura do solo**.
- Sistemas que permitam o **desenho georreferenciado dos imóveis** a partir de tecnologias acessíveis (fotos, celulares e drones).

> Toda tarefa deve poder ser justificada como contribuição direta a pelo menos um desses pontos. Ao iniciar uma tarefa, declare a qual deles ela se conecta.

## Personas

A persona primária do Desafio 2 é a **Luana**, mas soluções de desenho/coleta acessível também tocam o **Seu Raimundo**.

### Luana — analista ambiental do órgão estadual (geógrafa) — PERSONA PRIMÁRIA
Cuida da fila de validação de cadastros do estado inteiro.
- **Ganhos esperados:** pré-validação automatizada; dados integrados num só painel; templates inteligentes de parecer.
- **Dores:** fila de ~12.000 análises pendentes; sobreposições geométricas difíceis de detectar; troca constante entre 4 sistemas diferentes.

### Seu Raimundo — pequeno/médio produtor rural
Depende da propriedade para renda e sustento da família.
- **Ganhos esperados:** regularizar sem advogado; acessar crédito rural verde; resolver pelo celular.
- **Dores:** internet instável e dependência do filho para usar tecnologia; linguagem técnica; medo de errar e perder o cadastro.

### Pontos de dor mapeados (relevantes ao Desafio 2)
- Custo alto e dependência de terceiros para georreferenciamento.
- Sobreposições de imóveis passam despercebidas.
- Dados fragmentados entre múltiplos sistemas; falta de integração.
- Bases de referência desatualizadas, atrasando análises.

## Conceitos técnicos do domínio (do material oficial)

Domine estes conceitos — são a base do Desafio 2. Detalhes nos manuais do projeto (ver "Base documental").

### Georreferenciamento do imóvel — os 5 passos (Etapa "Geo" do Módulo de Cadastro)
O cadastro consiste no desenho georreferenciado do imóvel e suas feições. São 5 passos:
1. **Imóvel** — perímetro do imóvel (obrigatório).
2. **Cobertura do solo** — áreas consolidadas, remanescente de vegetação nativa (RVN), etc.
3. **Servidão administrativa** — infraestrutura/utilidade pública, reservatório de abastecimento.
4. **APP / Uso Restrito** — Áreas de Preservação Permanente, definidas por parâmetros dimensionais do Código Florestal (faixas de curso d'água, nascentes, etc.).
5. **Reserva Legal (RL)** — proposta, averbada, aprovada e não averbada, ou vinculada a compensação.

### Imagens de satélite e desenho
- O módulo usa imagens de satélite (ex.: **Landsat** — mais leves/menor resolução; **RapidEye** — resolução até 5 m). Importável "Da Internet" ou de disco, por UF/município.
- Ferramentas de **vetorização/desenho** de geometrias no mapa por feição.
- **Oportunidade do desafio:** tornar o desenho georreferenciado viável a partir de fotos, celulares e drones (mais acessível que georreferenciamento profissional).

### Retificação Dinamizada (RD) — conceito central de "dados declarados vs. referência"
A **Análise Dinamizada / Retificação Dinamizada** compara o que o proprietário **declarou** com as **informações de referência** geoespaciais e aponta **divergências por feição** (RVN, área consolidada, curso d'água, APP de cursos d'água e nascentes, Reserva Legal). Exemplo do manual: declaração de 26,79 ha de curso d'água vs. 0,03 ha de referência → divergência de 26,76 ha. A RD oferece **memória de cálculo** e permite retificação automática, por etapas, ou manter o cadastro.

> 💡 Este mecanismo (comparar declaração × base de referência e gerar divergências priorizáveis) é o coração de soluções de "dados integrados com correções rápidas" e "pré-validação automatizada" que o Desafio 2 pede. Boas oportunidades giram em torno de **melhorar bases de referência, sua atualização e a forma de apresentar/priorizar divergências**.

### Siglas essenciais
CAR (Cadastro Ambiental Rural) · SICAR (Sistema Nacional de CAR) · APP (Área de Preservação Permanente) · AUR (Área de Uso Restrito) · RL (Reserva Legal) · RVN (Remanescente de Vegetação Nativa) · IR (Imóvel Rural) · MRA (Módulo de Regularização Ambiental) · PRA (Programa de Regularização Ambiental) · RD (Retificação Dinamizada) · AD (Análise Dinamizada) · SFB (Serviço Florestal Brasileiro) · SNCR / SIGEF (bases fundiárias consultadas no cadastro).

## Base documental do projeto

> 📁 **Estes documentos estão na pasta `docs/base-documental/`, organizados por tema** (`manuais/`, `legislacao/`, `metodologia/`, `estudos/`, `ecossistema/`) e acessíveis ao Claude Code. Consulte-os antes de pesquisar fora — são a fonte autoritativa do domínio. Índice completo em `docs/base-documental/README.md`. Os PDFs ficam locais (não versionados); os `.md` de referência são versionados.

| Documento | O que contém | Quando usar |
|---|---|---|
| `docs/base-documental/metodologia/Edital haCARthon - Assinado - SEI_0993344_Edital_158.pdf` | Edital oficial ENAP nº 158/2026 — regras da maratona | Conferir regras, prazos e critérios de avaliação |
| `docs/base-documental/metodologia/esperado.md` | Enunciado oficial dos 3 desafios e soluções esperadas | Definir escopo e validar aderência ao Desafio 2 |
| `docs/base-documental/metodologia/Resumo_haCARthon_Ideacao_Prototipacao.md` | Metodologia (Duplo Diamante), personas, formato de entrega | Conduzir ideação e prototipação |
| `docs/base-documental/metodologia/pitch.md` | Resumo da Live 04 — como construir o pitch (estrutura, slides, gravação) | Montar o pitch e o vídeo |
| `docs/base-documental/metodologia/Hacarthon - Live de Pitch (2).pdf` | Slides da Live de Pitch | Apoiar a construção do pitch |
| `docs/base-documental/estudos/Onde-Estamos-2025.pdf` | CPI/PUC-Rio — Radiografia do CAR e do PRA nos Estados (Ed. 2025); dados de inscrição/análise por estado (nov/2025) | Dimensionar o problema e fundamentar o pitch (ver `docs/briefing.md` §2.1) |
| `docs/base-documental/estudos/LEG-Consultada-OE-2025.pdf` | Apêndice "Legislação Consultada" do estudo acima | Rastrear a legislação estadual consultada |
| `docs/base-documental/manuais/manual_modulo_cadastro.pdf` | Manual do Módulo de Cadastro v3.7 (etapa Geo, 5 passos, baixar imagens de satélite, vetorização) | Entender o fluxo geoespacial atual e seus atritos |
| `docs/base-documental/manuais/manual_modulo_cadastro_pre_preenchido.pdf` | Manual do Módulo Pré-Preenchido (consulta automática SNCR/SIGEF, retificação) | Entender pré-preenchimento e integração com bases fundiárias |
| `docs/base-documental/manuais/Manual_Retificacao_Dinamizada.pdf` | Manual da Retificação Dinamizada do SICAR (2023) — comparação declarado×referência | Entender o mecanismo de validação e divergências |
| `docs/base-documental/manuais/Manual_Central_do_Proprietario_Possuidor.pdf` | Manual da Central do Proprietário/Possuidor | Entender o canal de atendimento/notificação ao proprietário |
| `docs/base-documental/ecossistema/Acesso ao Módulo de Cadastro Pré- Preenchido.pdf` | Credenciais e passos de acesso ao ambiente de testes | Acessar o ambiente de testes (ver avisos de segurança) |
| `docs/base-documental/ecossistema/CAR DPG - Sistemas, plataformas e repositórios do CAR_V4.docx.pdf` | Lista de sistemas, plataformas e repositórios do CAR | Mapear o ecossistema e evitar retrabalho |
| `docs/base-documental/metodologia/Identificacao_oportunidades.pdf` | Guia de identificação de oportunidades (imersão, jornada, JTBD) | Descobrir e enquadrar o problema |
| `docs/base-documental/metodologia/ideacao_prototipacao.pdf` (+ `ideacao_prototipacao_compressed.pdf`) | Slides de ideação e prototipação (versão completa + versão leve) | Apoiar a fase de ideação |
| `docs/base-documental/legislacao/L12651.pdf` | Lei nº 12.651/2012 — Código Florestal | Fundamentar regras de negócio (APP, RL, uso restrito) |
| `docs/base-documental/legislacao/Decreto nº 7830.pdf` | Decreto nº 7.830/2012 — institui o SICAR | Fundamentar regras do sistema |

## Plataforma de referência: RER (Rural Environmental Registry)

O **RER** é a versão moderna e open source do CAR, mantida como **Bem Público Digital**. É a base técnica de referência — antes de criar do zero, verifique se o RER já oferece o que precisa, e prefira estender/integrar.

- **Organização GitHub:** https://github.com/Rural-Environmental-Registry
- **Licença:** GPL-3.0 em todos os repositórios.

### Repositórios
| Repositório | Conteúdo | Stack | Imagem Docker |
|---|---|---|---|
| [core](https://github.com/Rural-Environmental-Registry/core) | Orquestrador de deploy (docker-compose, scripts, docs) | Shell / Docker | — |
| [gateway](https://github.com/Rural-Environmental-Registry/gateway) | API Gateway (roteamento, CORS, auth relay) | Java / Spring Cloud Gateway | `rer-gateway` |
| [frontend](https://github.com/Rural-Environmental-Registry/frontend) | SPA principal | TypeScript / Vue.js 3 | `rer-core-frontend` |
| [backend](https://github.com/Rural-Environmental-Registry/backend) | API REST principal (migrations Flyway) | Java / Spring Boot 3 | `rer-core-backend` |
| [authentication](https://github.com/Rural-Environmental-Registry/authentication) | Keycloak + portal admin | Java / Spring Boot + Keycloak | `rer-auth-*` |
| [calc_engine](https://github.com/Rural-Environmental-Registry/calc_engine) | Motor de cálculo ambiental | Java / Spring Boot WebFlux | `rer-calc-engine` |
| [map_component](https://github.com/Rural-Environmental-Registry/map_component) | Biblioteca de mapa (Leaflet) | Vue / npm | — (npm) |

### Arquitetura e stack (RER)
```
NGINX (:80)
  ├── /geoserver  → GeoServer (WMS/WFS)
  └── /*          → Spring Cloud Gateway (:8080)
                      ├── core-frontend (Vue 3)
                      ├── core-backend (Spring Boot 3) ── core-backend-db (PostGIS)
                      ├── authentication (Keycloak) ──── auth-db (PostgreSQL 15)
                      └── calc_engine (Spring Boot WebFlux) ── PostgreSQL 17 + PostGIS 17
```
- **Backend:** Java 21, Spring Boot 3.4.x, Spring Cloud Gateway, WebFlux.
- **Frontend:** Vue.js 3 + TypeScript; mapas com **Leaflet**.
- **Dados/GIS:** PostgreSQL 15/17 + **PostGIS**; **GeoServer 2.28 (WMS/WFS)**.
- **Auth:** Keycloak (SSO/OAuth2). **Infra:** Docker/docker-compose, Nginx, Flyway.

> Para o Desafio 2, o RER já oferece a espinha geoespacial (PostGIS + GeoServer + Leaflet). Soluções de "dados integrados" e "bases de referência" se encaixam naturalmente nessa pilha.

### Rodando o RER localmente (se houver implementação)
Requisitos: Linux, 8 GB RAM (16 recomendado), 20 GB de disco, 4 vCPUs, Docker.
```bash
curl -fsSL https://raw.githubusercontent.com/Rural-Environmental-Registry/core/main/install.sh | bash
# ou, no diretório do core:
docker compose up -d && docker compose ps && docker compose logs -f core-backend
docker compose down -v   # reset total
```
Serviços (padrão `localhost`): app em `http://localhost`, Keycloak `/keycloak/admin`, GeoServer `/geoserver/`. Config no `.env`. **Troque todas as credenciais padrão antes de qualquer exposição.**

## Ecossistema oficial do CAR

**Reutilize o que já existe antes de criar.**

| Recurso | Endereço | Descrição |
|---|---|---|
| Portal do CAR | https://car.gov.br | Site oficial |
| Consulta pública | https://consultapublica.car.gov.br | Consulta de imóveis no SICAR |
| Painel de dados | https://painel.car.gov.br | Dados e estatísticas |
| RER (DPG) | https://rer.dataprev.gov.br | Plataforma open source |
| GitHub do RER | https://github.com/Rural-Environmental-Registry | Código-fonte |

## Fontes de dados geoespaciais e microdados (núcleo do Desafio 2)

Prefira fontes oficiais; alternativas comunitárias servem como apoio/automação.

- **Downloads oficiais por estado (shapefile/KML):** base de downloads da Consulta Pública do SICAR Federal, por estado/município. Polígonos separados por categoria (perímetro, APP, Reserva Legal, uso consolidado). Exigem e-mail + captcha. Campos-chave: `cod_imovel` (identificação) e `ind_status` — `AT` (ativo), `PE` (pendente), `CA` (cancelado).
- **Serviço WMS/WFS oficial:** GeoServer do CAR — conecta a base direto em GIS (QGIS/ArcGIS). Endpoint conhecido: `https://geoserver.car.gov.br/geoserver/sicar/wfs` (disponibilidade variável; validar antes de depender).
- **Bases fundiárias para referência/pré-preenchimento:** **SNCR** e **SIGEF** (o módulo pré-preenchido já consulta automaticamente). **SNIF** (Sistema Nacional de Informações Florestais) para bases florestais de referência.
- **Biblioteca Python da comunidade (automação de download):** [`urbanogilson/SICAR`](https://github.com/urbanogilson/SICAR) — baixa bases estaduais por categoria de polígono, com OCR (Tesseract/Paddle) para o captcha. Útil para pipelines de ingestão.
- **MapBiomas:** fonte alternativa de uso/cobertura do solo (mais limitada e menos atualizada que a oficial).

> ⚠️ **Verifique disponibilidade e atualização antes de assumir que funcionam** — endpoints WMS/WFS e o portal já ficaram fora do ar; bases de terceiros costumam estar desatualizadas. **Sempre registre a data de extração** de qualquer dado usado.

### Painel de BI (Power BI) — referência de visualização
`https://app.powerbi.com/view?r=eyJrIjoiMjQ5Mjc2M2MtN2E3MS00MzU5LTgzZTUtZGU5YTU4MzAwMWNhIiwidCI6IjNlYzkyOTY5LTVhNTEtNGYxOC04YWM5LWVmOThmYmFmYTk3OCJ9`
> É um relatório interativo (SPA), **não** uma fonte de microdados — não há exportação direta pelo link. Use-o para entender métricas e recortes existentes; para dados brutos, use as fontes acima.

## Base legal

- **Lei nº 12.651/2012** (Código Florestal) — define APP, Reserva Legal, uso restrito. Arquivo: `docs/base-documental/legislacao/L12651.pdf`.
- **Decreto nº 7.830/2012** — institui o SICAR. Arquivo: `docs/base-documental/legislacao/Decreto nº 7830.pdf`.

Toda regra de negócio sobre dimensões de APP, percentuais de RL e classificação de feições deve ser fundamentada nesses textos (disponíveis no projeto).

## Ambiente de testes (SICAR)

> ⚠️ **CRÍTICO:** cadastro/envio **exclusivamente no ambiente de testes**. **Nunca** enviar ao ambiente de produção do Sicar — gera registros indevidos no sistema oficial. Trate integração de escrita com produção como bloqueada por padrão.

- Dados são **fictícios** (usuários e cadastros de teste).
- **Módulo Pré-Preenchido:** https://car-sus.dataprev.gov.br/#/baixar → "Acesse o módulo de cadastro pré-preenchido".
- **Módulo Offline:** mesmo endereço → "Baixe o módulo de cadastro offline" (exige código **SNCR** conforme o CPF).
- **Envio (somente teste):** https://car-sus.dataprev.gov.br/#/enviar
- **Central do Proprietário/Possuidor:** https://car-sus.dataprev.gov.br/#/central/acesso
- Login via **Gov.br** com credenciais de teste (detalhes em `docs/base-documental/ecossistema/Acesso ao Módulo de Cadastro Pré- Preenchido.pdf`).

> 🔐 **Não commitar credenciais, CPFs ou códigos SNCR** (mesmo fictícios) em texto plano. Mantenha em `.env`/gerenciador de segredos, fora do controle de versão.

## Metodologia de trabalho (Duplo Diamante)

1. **Descobrir** — usuário, dor, contexto e o que já existe (brainstorming, matriz CSD, desk research, persona, mapa de empatia).
2. **Definir** — briefing claro: desafio, usuário, dor, proposta de valor (jornada do usuário, JTBD, diagrama de afinidade, opportunity gaps).
3. **Desenvolver** — gerar soluções (How Might We, benchmark, SCAMPER).
4. **Entregar** — triar e priorizar (RICE / Impacto×Esforço), prototipar e testar. Saída: protótipo validado + **vídeo de pitch**.

### Histórias de usuário (JTBD)
> Quando **[situação]**, quero **[motivação]**, para que **[resultado esperado]**.

### How Might We
Ex.: "Como poderíamos priorizar a fila de Luana por risco ambiental real?" / "Como poderíamos sinalizar conflitos geométricos no momento do cadastro?"

### Escala de fidelidade
Suba a fidelidade **só até onde precisar**: papel → wireframe → mockup → protótipo interativo (Figma) → MVP funcional. Ferramentas: Excalidraw, Figma, tldraw. **Lembre-se: código funcional é opcional na entrega.**

### Mentalidade de MVP
Incrementos que já entregam valor (skate → patinete → bike → moto → carro), nunca partes inúteis até o final.

## Diretrizes para o Claude Code

### Idioma e comunicação
- Documentação, comentários e commits em **português do Brasil**.
- **Linguagem simples e acessível** em qualquer texto voltado ao usuário final — jargão técnico/jurídico é uma dor central do projeto.

### Antes de codar ou prototipar
1. Confirme a contribuição ao **Desafio 2** (qual "solução esperada" ela atende).
2. **Consulte a base documental do projeto primeiro** (manuais, leis) — é a fonte autoritativa.
3. Verifique se já existe no **RER** ou no ecossistema oficial; prefira **integrar/estender** a recriar.
4. Para dados, prefira **bases abertas oficiais** (downloads SICAR, WMS/WFS, SNCR, SIGEF, SNIF) e registre a data de extração.
5. Pergunte se a melhor entrega é **protótipo/mockup** em vez de código — frequentemente é.

### Ao implementar (se houver código)
- Alinhe-se à pilha geoespacial do RER: **PostGIS** no banco, **GeoServer (WMS/WFS)** para servir camadas, **Leaflet** no front.
- Para validação/divergências, inspire-se no modelo da **Retificação Dinamizada** (declarado × referência, com memória de cálculo).
- **Mobile-first** e tolerante a conexão instável (Seu Raimundo no celular, internet ruim).
- Para a Luana: priorize **automação de validação**, **detecção de sobreposições** e **consolidação num único painel**.
- Mantenha tudo **open source** (licenciável como GPL-3.0), documentado e reaproveitável.

### Convenções (alinhadas ao RER, se integrar)
- Backend **Java 21 + Spring Boot 3**; frontend **Vue 3 + TypeScript**; migrations **Flyway**; **Docker**.
- Branches do RER: `develop` (dev) → `staging` (QA) → `demo` (pré-prod) → `main` (prod). PRs contra `develop`.

### Restrições rígidas
- ❌ Nunca enviar dados a **produção** do SICAR.
- ❌ Nunca commitar credenciais/CPFs/códigos (mesmo de teste) em texto plano.
- ✅ Sempre respeitar Código Florestal (Lei 12.651/2012) e Decreto 7.830/2012.
- ✅ Sempre registrar a data de extração de bases externas.

## Stack deste projeto

> ⚠️ A definir. Se a entrega for só protótipo, esta seção pode permanecer enxuta. Preencha quando decidir.

- **Tipo de entrega:** _(protótipo/mockup/vídeo  •  ou  •  software funcional)_
- **Linguagem/runtime:** _(ex.: Java 21 / Node 20 / Python 3.12)_
- **Backend:** _(ex.: Spring Boot 3 / FastAPI)_
- **Frontend:** _(ex.: Vue 3 + TypeScript)_
- **Banco / GIS:** _(ex.: PostgreSQL + PostGIS; GeoServer WMS/WFS; Leaflet)_
- **Infra / pacotes:** _(ex.: Docker; Maven / npm / pip)_
- **Prototipação:** _(ex.: Figma / Excalidraw)_

## Estrutura sugerida do repositório

```
/
├── CLAUDE.md
├── README.md              # Visão do projeto, decisões e restrições
├── docs/                  # Pesquisa de usuário, decisões, briefing
│   ├── briefing.md        # Decisões e enquadramento do problema
│   ├── base-documental/   # Manuais, leis e metodologia (PDFs locais, não versionados)
│   │   ├── README.md      #   índice da base documental
│   │   └── manuais/  legislacao/  metodologia/  estudos/  ecossistema/
│   └── acesso-ambiente-testes.md   # (se criado) NÃO versionar credenciais reais
├── prototypes/            # Wireframes, mockups, storyboards
├── data/                  # Bases (registrar data de extração; NÃO versionar dados pesados)
├── src/                   # Código-fonte (se houver)
└── .env.example
```

## Comandos

> ⚠️ A definir conforme o stack. Exemplos:
```bash
# npm install / mvn install / pip install -r requirements.txt
# npm run dev / mvn spring-boot:run
# npm test / mvn test / pytest
# docker compose up -d
```

---

## Itens em aberto (a confirmar)

1. **Formato da entrega** — protótipo/mockup (sem código) ou software funcional? Define "Stack" e "Comandos".
2. **Recorte da solução** — qual das "soluções esperadas" do Desafio 2 será o foco (ex.: vetorização de feições naturais, geração automatizada de bases de referência, desenho via celular/drone, painel de dados integrados)?
3. **Nome e proposta de valor** da solução, se já houver, para o topo do documento.
4. **Stack/ferramentas de prototipação** preferidas (Figma, Excalidraw, etc.).
