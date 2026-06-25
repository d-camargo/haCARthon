# Briefing do projeto — haCARthon Desafio 2

> Documento vivo. Registra decisões e o enquadramento do problema. Atualizar conforme avançamos.

## 1. Decisões tomadas (2026-06-25)

| Tema | Decisão | Observação |
|---|---|---|
| Desafio | **Desafio 2 — Melhorar o acesso a dados geoespaciais do CAR** | Definido no CLAUDE.md |
| Persona primária | **Luana** (analista ambiental estadual) | Secundária: Seu Raimundo |
| Formato de entrega | **Híbrido**: mockup/protótipo + vídeo de pitch **+ prova de conceito técnica enxuta** | Código é opcional na avaliação; a PoC serve para dar credibilidade |
| Recorte da solução | **R1 + R2 — Painel de pré-validação da Luana** (fila priorizada por risco + comparação declarado×referência) **com detecção de sobreposição em PostGIS como PoC técnica** | Definido em 2026-06-25 após a fase Descobrir/Definir |
| Primeiro passo | Estruturar repositório + docs e iniciar git | Concluído |
| Canal de entrega | **Híbrido: plugin QGIS (analista) + painel web (gestão)**; plugin novo e complementar ao GeoCAR; **native-first** (Processing + UX nativa do QGIS, sem dockwidget custom); QGIS puro com PostGIS opcional; MVP = detecção + fila + parecer/RAT | Decidido 2026-06-25 — arquitetura em `docs/arquitetura/plugin-qgis.md`; análise em `docs/definir/opcao-entrega-qgis-vs-web.md` |

## 2. Fase Descobrir/Definir — andamento

O recorte é escolhido com base em evidência, seguindo o Duplo Diamante, antes de prototipar.
Artefatos produzidos em `docs/descobrir/` e `docs/definir/`.

- [x] **Matriz CSD** — `docs/descobrir/matriz-csd.md`
- [x] **Jornada da Luana** — `docs/descobrir/jornada-luana.md`
- [x] **Extrair atritos dos manuais** — lido `Manual_Retificacao_Dinamizada.pdf` (págs. 1-20 e 35-40);
      mecanismo declarado × referência e, sobretudo, **quais casos a automação não cobre** (pág. 39).
- [x] **How Might We** + síntese — `docs/definir/sintese-oportunidades.md`
- [ ] **Mapear o ecossistema/RER** com mais profundidade (o que estender vs. recriar).
- [x] **Recorte escolhido (2026-06-25):** **R1 painel de pré-validação + R2 detecção de
      sobreposição como PoC**. Entramos no 2º losango (Desenvolver/Prototipar).

### Achados fundamentados (manual RD, pág. 39) — por que importam ao Desafio 2
- **Imóveis sem base de referência não passam pela pré-validação** → caem inteiros na fila manual.
  Ampliar/atualizar a base de referência encolhe a fila da Luana (causa-raiz).
- **Sobreposição** (com assentamentos) e **Área de Uso Restrito** desviam da automação.
- A Retificação/Análise Dinamizada é habilitada **município a município** → cobertura desigual.

## 2.1 Dados do estudo CPI/PUC-Rio — "Onde Estamos na Implementação do Código Florestal? Ed. 2025"

> Fonte: `docs/base-documental/estudos/Onde-Estamos-2025.pdf` (CPI/PUC-Rio, 2025; dados dos órgãos
> estaduais e Painel SFB de nov/2025). **Data de extração: 2026-06-25.** Esses números **dimensionam
> e validam** o problema da Luana com dados nacionais recentes.

### A escala da fila é nacional e enorme
- **~8 milhões** de imóveis inscritos no CAR (+5,6% no ano). Maiores bases: Bahia (1.245 mil) e Minas Gerais (1.140 mil). *(Sumário Exec. p.17–18, Fig. 2)*
- **Análise iniciada:** subiu de 15% → **24% da base** em um ano (~1,9 milhão). Ou seja, **~76% dos cadastros ainda nem tiveram análise iniciada.** *(p.20–23, Fig. 3)*
- **Análise concluída (validada):** ~**724 mil = 9% da base** (era 3,3% no ano anterior — quase triplicou). **Nove UFs não chegam a 1% validado.** *(p.25–27, Fig. 4)*
- Heterogeneidade enorme: % validado vai de **ES 65% / SP 45% / PR 40%** até resíduos <1% na maioria das UFs.

### O estudo confirma nossas suposições (ver Matriz CSD)
- **S1/S5 — sobreposições travam a análise (CONFIRMADA):** *"cadastros com sobreposições acima do limite legal de tolerância não podem avançar na análise — seja por automação ou por equipe técnica — sem retificação pelos produtores"*. Em **Mato Grosso, ~30% dos cadastros têm sobreposições relevantes**. *(p.14, p.21)*
- **S2/S3 — base de referência é entrave/causa-raiz (CONFIRMADA):** *"a ausência de informações fundiárias verificáveis no CAR começa a se consolidar como um dos principais entraves à continuidade das análises"*. Onde há **bases cartográficas de alta resolução**, a validação destrava (SP dobrou validação para 45%; MT "CAR Digital" **delimita automaticamente APP, RL, vegetação remanescente e área consolidada**). *(p.14, Box 1 p.24)*

### Respostas a dúvidas em aberto
- **D4 (gargalo dominante):** o estudo nomeia **dois gargalos estruturais** — (1) **situação fundiária / sobreposições** e (2) **comunicação com o proprietário** ("aguardando atendimento à notificação"). *(p.14, p.28)*
- **D3 (atualização):** a análise dinamizada gera "saltos semanais"; MS faz **reanálise com bases cartográficas mais recentes** → reforça a importância de **atualizar a base de referência**. *(p.20–21)*
- **D2 (cobertura):** confirma cobertura **desigual** e habilitação por estado/município; só ~9 estados adotam análise automatizada de forma relevante. *(Fig. 1 p.16, Fig. 3)*

### Implicação para o recorte (R1+R2)
Os dados **reforçam** o recorte: o gargalo nº 1 nomeado pelo estudo (**sobreposições**) é exatamente o
que a PoC R2 ataca, e o ganho comprovado vem de **bases de referência melhores + pré-validação** — o
coração do painel R1. O painel pode, inclusive, exibir esses indicadores (% validado, % com sobreposição)
como contexto. *Pendência para aprofundar: Fig. 8 "Etapas da Análise Dinamizada" (p.84).*

## 2.2 Fragmentação de sistemas (Gap C) — dado do estudo (Tabela 4, p.63-65)

> Fundamenta a dor "muitos sistemas" da Luana com dado real do estudo CPI/PUC-Rio (2025).
> A fragmentação tem **duas camadas**.

**Camada 1 — entre estados (não existe "um" sistema do CAR).** O Código Florestal deixou cada
estado escolher entre usar o SICAR direto ou ter sistema próprio (Tabela 4):
- **SICAR direto (16 UFs):** AL, AP, AM, CE, DF, MA, MG, PB, PR, PE, PI, RJ, RN, RS, RR, SE.
- **Sistema estadual próprio (11 UFs):** AC, BA, ES, GO, MT, MS, PA, RO, SC, SP, TO.

Vários estaduais são **versões antigas do SICAR customizadas ("forkadas")** que, segundo o estudo,
viram *"plataformas independentes, sem governança federal e sem alinhamento automático"* → **perda
de sincronia**, *"lacunas ou atrasos na atualização"*. A integração SICAR↔SNCR/SIGEF **só começou em
2025** (puxada pela ADPF 743) — antes, eram silos.

**Camada 2 — dentro da análise (o dia a dia da Luana).** Para validar **um** cadastro ela cruza
fontes em sistemas separados: o sistema de análise (SICAR/estadual) + bases fundiárias (SNCR, SIGEF)
+ INCRA (assentamentos, quilombolas) + bases cartográficas/satélite + painéis de BI (Power BI).
O estudo confirma: a maioria dos estados *"não possui mecanismos de transparência… dados de difícil acesso"*.

**Evidência de 1ª mão (nosso pipeline):** para sobrepor só **duas** camadas (SICAR + INCRA) lidamos com
**duas tecnologias** (GeoServer WFS × i3geo/MapServer), **dois CRS/ordens de eixo** (4674 lon/lat × 4326
lat/lon invertido), **dois esquemas de campos** e **dois regimes de acesso** (aberto × login). É o Gap C
em miniatura — multiplicado pelas 5-6 fontes da Luana, a cada cadastro, vezes a fila.

> **Implicação:** o valor do nosso recorte é **fazer a integração entre sistemas uma vez** (pipeline) e
> entregar o resultado consolidado num só lugar — alinhado ao movimento real do **CAR Pré-Preenchido**
> (que já puxa SNCR/SIGEF na *entrada*; nós propomos o mesmo na *análise*).

## 3. Personas (resumo)

- **Luana** — analista ambiental (geógrafa). Dores: fila de ~12.000 análises; sobreposições
  geométricas difíceis de detectar; troca constante entre 4 sistemas. Ganhos esperados:
  pré-validação automatizada; dados integrados num painel; templates de parecer.
- **Seu Raimundo** — pequeno/médio produtor. Dores: internet instável, dependência de
  terceiros, linguagem técnica, medo de errar. Ganhos: regularizar sem advogado, pelo celular.

## 4. Soluções esperadas do Desafio 2 (candidatas a recorte)

1. Sistemas de **dados integrados**, com fluxo e correções rápidas.
2. **Dados georreferenciados vetorizados** de feições naturais (rios, rochas), APP e uso restrito.
3. **Geração automatizada de bases de referência**.
4. **Atualização de mapas de uso e cobertura do solo**.
5. **Desenho georreferenciado** dos imóveis via tecnologias acessíveis (fotos, celulares, drones).

> Toda tarefa deve se conectar a pelo menos um destes pontos. Ao iniciar uma tarefa,
> declarar a qual ela contribui.

## 5. Conceito-âncora: Retificação Dinamizada (RD)

Compara o que o proprietário **declarou** com as **informações de referência** e aponta
**divergências por feição** (RVN, área consolidada, curso d'água, APP, Reserva Legal), com
memória de cálculo. É o coração das soluções de "dados integrados" e "pré-validação" que o
Desafio 2 pede — boas oportunidades giram em torno de **melhorar bases de referência, sua
atualização e a forma de apresentar/priorizar divergências**.
