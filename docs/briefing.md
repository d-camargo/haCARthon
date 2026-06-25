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
