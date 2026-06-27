# Jornada da Luana — analista ambiental (validação de cadastro CAR)

> Ferramenta da fase **Descobrir/Definir**. Mapeia, passo a passo, o trabalho da persona
> primária ao validar **um** cadastro, com os atritos e a emoção em cada etapa.
> Base: persona do `CLAUDE.md` + mecanismo da Retificação/Análise Dinamizada (`Manual_Retificacao_Dinamizada.pdf`).
> ⚠️ Etapas marcadas **[inferida]** precisam de validação com uma analista real (ver Dúvidas D1/D4/D6 na Matriz CSD).

## Contexto
Luana cuida da **fila de validação do estado inteiro** (~12.000 análises pendentes). A maioria
dos casos que chega à mão dela é, por definição, o que a **automação não resolveu** (imóveis sem
base de referência, sobreposições, RL averbada, compensação, etc. — ver Matriz CSD C3).

## Mapa da jornada

| Etapa | O que a Luana faz | Atrito (dor) | Emoção | Oportunidade (Desafio 2) |
|---|---|---|---|---|
| **1. Triagem da fila** | Escolhe o próximo cadastro a analisar entre milhares | Fila não priorizada por risco/complexidade; tudo parece igual de urgente | 😩 Sobrecarga | Priorizar a fila por **risco ambiental** e por **tipo de exceção** (sem base, sobreposição) |
| **2. Abrir o caso** | Levanta o cadastro declarado, recibo, polígonos | Dados espalhados; precisa abrir o cadastro em um sistema e os anexos em outro | 😐 Atrito inicial | Painel **único** que reúne declaração + referência + histórico |
| **3. Buscar base fundiária** [inferida] | Consulta SNCR/SIGEF para conferir domínio/limites | **Troca de sistema** (sai do SICAR, entra na base fundiária) | 😤 Interrupção | Integração das bases fundiárias **no mesmo painel** |
| **4. Conferir imagem/base de referência** | Compara polígono declarado com imagem de satélite e cobertura do solo | Base de referência **ausente** (caso nem entra na automação) ou **desatualizada** → divergência pode ser "falsa" | 😟 Insegurança | **Gerar/atualizar** base de referência; mostrar **data** da base e da imagem |
| **5. Detectar sobreposição** | Verifica se o imóvel sobrepõe outro imóvel, assentamento ou área protegida | Detecção **manual/visual**, caso a caso; fácil passar despercebido | 😰 Medo de errar | **Detecção automática de sobreposição** com alerta priorizável |
| **6. Comparar declarado × referência** | Avalia divergência por feição (RVN, consolidada, curso d'água, APP, RL) | Faz "na mão" o que a RD faz automático — mas aqui a RD **não cobre** | 🧮 Trabalho repetitivo | Estender o motor **declarado × referência** (modelo RD) para os casos manuais |
| **7. Redigir parecer** | Escreve a justificativa técnica da decisão | Sem template; reescreve raciocínio parecido a cada caso | 😮‍💨 Cansaço | **Templates inteligentes** de parecer com memória de cálculo pré-preenchida |
| **8. Devolver / notificar** | Aprova, exige retificação ou indefere; notifica o proprietário | Linguagem técnica/jurídica; proprietário (Seu Raimundo) tem dificuldade de entender | 🤝 Frustração mútua | Saída em **linguagem simples** para o produtor (ponte com Desafio 1) |

## Picos de dor (onde concentrar a solução)
1. **Etapa 5 — sobreposições manuais.** Alto risco de erro, alto esforço, e é exatamente uma "solução esperada" do Desafio 2.
2. **Etapa 4 — base de referência ausente/desatualizada.** É a **causa-raiz**: sem base, o caso nem é pré-validado e cai inteiro na fila (Matriz CSD C3/S3).
3. **Etapas 2–3 — fragmentação (4 sistemas).** Atrito constante; o painel integrado ataca isso.

## Momento "uau" desejado
> Luana abre **um** painel, vê o cadastro já **pré-analisado** (declarado × referência atualizado),
> com **sobreposições destacadas** e a fila **ordenada por risco** — e gasta o tempo dela só onde
> o julgamento humano realmente importa.

## Pontes com as personas/desafios
- **Seu Raimundo / Desafio 1:** etapa 8 (linguagem simples na devolução).
- **Desafio 2 (foco):** etapas 4, 5 e 6 — base de referência, sobreposição e motor de comparação.
