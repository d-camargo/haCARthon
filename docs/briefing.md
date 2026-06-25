# Briefing do projeto — haCARthon Desafio 2

> Documento vivo. Registra decisões e o enquadramento do problema. Atualizar conforme avançamos.

## 1. Decisões tomadas (2026-06-25)

| Tema | Decisão | Observação |
|---|---|---|
| Desafio | **Desafio 2 — Melhorar o acesso a dados geoespaciais do CAR** | Definido no CLAUDE.md |
| Persona primária | **Luana** (analista ambiental estadual) | Secundária: Seu Raimundo |
| Formato de entrega | **Híbrido**: mockup/protótipo + vídeo de pitch **+ prova de conceito técnica enxuta** | Código é opcional na avaliação; a PoC serve para dar credibilidade |
| Recorte da solução | **Em exploração** | Será fixado após a fase Descobrir/Definir |
| Primeiro passo | Estruturar repositório + docs e iniciar git | Concluído |

## 2. Próximos passos — fase Descobrir/Definir

O recorte ainda **não** está fixado de propósito: vamos escolher com base em evidência,
seguindo o Duplo Diamante, antes de investir em protótipo.

- [ ] **Matriz CSD** (Certezas, Suposições, Dúvidas) sobre o Desafio 2.
- [ ] **Jornada da Luana** — mapear passo a passo a validação de um cadastro e os atritos
      (troca entre 4 sistemas, detecção de sobreposições, fila de ~12.000).
- [ ] **Extrair atritos reais dos manuais** — Módulo de Cadastro e Retificação Dinamizada
      (declarado × referência) como base do mecanismo de validação.
- [ ] **Mapear o ecossistema** (RER + sistemas oficiais) para não recriar o que já existe.
- [ ] **How Might We** — transformar as dores priorizadas em perguntas de ideação.
- [ ] **Escolher o recorte** entre as soluções esperadas do Desafio 2 (ver seção 4).

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
