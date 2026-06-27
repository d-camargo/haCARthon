# haCARthon — Desafio 2: Melhorar o acesso a dados geoespaciais do CAR

Projeto da equipe para o **haCARthon**, focado em fortalecer o SICAR e consolidar o
CAR como **Bem Público Digital**, em modelo de **código aberto**.

> 🎯 **Desafio escolhido:** **DESAFIO 2 — Melhorar o acesso a dados geoespaciais do CAR.**
> Pergunta-desafio: como atualizar anualmente, com rapidez e acurácia, o mapeamento de
> uso e cobertura do solo de todos os estados, melhorando os cadastros e a qualidade das
> análises do CAR?

## Onde estamos

- **Fase (Duplo Diamante):** Descobrir / Definir.
- **Recorte da solução:** **Painel de pré-validação da Luana** (fila priorizada por risco +
  comparação declarado×referência) **+ detecção de sobreposição em PostGIS como PoC técnica**.
- **Formato de entrega:** **híbrido** — protótipo/mockup + vídeo de pitch, acompanhado de
  uma prova de conceito técnica enxuta para dar credibilidade.
- **Persona primária:** Luana (analista ambiental — fila de ~12.000 análises).
  Secundária: Seu Raimundo (produtor rural — celular, internet instável).

## Princípio orientador

> **Comece pelo problema (e pela pessoa), não pela solução.**

Antes de prototipar ou codar, validamos: que dor real resolve, para qual persona, e se já
existe nas plataformas oficiais (SICAR / RER).

## Estrutura do repositório

```
/
├── CLAUDE.md               # Orientações de trabalho (ler no início de cada sessão)
├── README.md               # Este arquivo
├── docs/                   # Pesquisa, decisões, briefing
│   ├── briefing.md         # Decisões e enquadramento do problema
│   ├── referencias.md      # Fontes externas (links) com data de acesso
│   └── base-documental/    # Manuais, leis e material da metodologia (PDFs locais, não versionados)
│       ├── README.md       #   índice da base documental
│       ├── manuais/  legislacao/  metodologia/  ecossistema/
├── prototypes/             # Wireframes, mockups, storyboards
├── data/                   # Bases geoespaciais (registrar data de extração; não versionar pesados)
├── src/                    # Código-fonte da prova de conceito (se houver)
└── .env.example            # Modelo de variáveis de ambiente (segredos só no .env local)
```

## Restrições rígidas

- ❌ Nunca enviar dados à **produção** do SICAR (cadastro/envio só no ambiente de testes).
- ❌ Nunca commitar credenciais / CPFs / códigos SNCR (mesmo de teste).
- ✅ Respeitar o Código Florestal (Lei 12.651/2012) e o Decreto 7.830/2012.
- ✅ Registrar a data de extração de qualquer base externa.

## Ecossistema de referência

- **RER (versão open source do CAR):** https://github.com/Rural-Environmental-Registry
  — pilha geoespacial PostGIS + GeoServer (WMS/WFS) + Leaflet. Preferir **estender/integrar**.
- Portal CAR: https://car.gov.br · Consulta pública: https://consultapublica.car.gov.br
