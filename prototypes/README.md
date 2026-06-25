# Protótipos

Wireframes e mockups da solução. Fidelidade sobe **só até onde precisar**
(papel → wireframe → mockup → Figma), conforme a metodologia do projeto.

## painel-luana/ — Painel de Pré-validação da Luana (recorte R1+R2)

Duas fidelidades da mesma tela:

| Arquivo | Fidelidade | Dados |
|---|---|---|
| `painel-luana/index.html` | **Wireframe lo-fi** (SVGs estáticos, sem dependências) | fictícios |
| `painel-luana/painel.html` | **Protótipo funcional** com **mapa Leaflet** | **REAIS** (SICAR + INCRA) |

- **Abrir:** duplo clique no `.html` (o `painel.html` usa Leaflet via CDN + tiles OSM → precisa de internet).
- **Prints:** `preview.png` (wireframe) e `preview_painel.png` (funcional).
- **Dados do mapa:** `dados/dados_mapa.js` (Querência do Norte/PR — 548 imóveis, 69 em conflito com
  10 assentamentos do INCRA). Regenerável com `./gerar_dados_mapa.sh` após rodar o pipeline.

### O que o painel funcional mostra
Fila priorizada pelas sobreposições reais detectadas pelo pipeline, KPIs (imóveis, em conflito,
assentamentos, ha em conflito) e o mapa com imóveis CAR, **conflitos em vermelho** e **assentamentos
do INCRA**. Clicar na fila ou no mapa inspeciona o imóvel e mostra qual assentamento ele sobrepõe.

### O que o wireframe demonstra (e como liga aos gaps)
| Elemento da tela | Gap atacado | Origem |
|---|---|---|
| KPIs "com sobreposição" e "sem base de referência" | A + B | Achados do manual RD (pág. 39) |
| Fila ordenada por **score de risco** + filtros por exceção | C (triagem) | Jornada, etapa 1 |
| Selo **"Base de referência: atualizada em…"** | A | Jornada, etapa 4 |
| Dois mapas lado a lado (declaração × referência) | C | Modelo Retificação Dinamizada |
| Camada de **sobreposição destacada** + alerta automático | B | Jornada, etapa 5 |
| Tabela de **divergência por feição** + memória de cálculo | C | Manual RD (Figuras 4–5) |
| Ações: **gerar parecer (template)** / aprovar / exigir retificação | C | Jornada, etapas 7–8 |

> Dados são **fictícios** (demo). Não representa cadastro real e não toca o ambiente de produção.

### Regenerar o print
```bash
cd prototypes/painel-luana
google-chrome-stable --headless --disable-gpu --no-sandbox \
  --hide-scrollbars --window-size=1280,1400 \
  --screenshot=preview.png "file://$PWD/index.html"
```

### Próximos passos de prototipação
- [x] Conectar a detecção de sobreposição a um **mapa Leaflet** real → `painel.html` (dados reais SICAR + INCRA).
- [ ] Validar o painel funcional com a jornada futura (storyboard) da Luana.
- [ ] Subir fidelidade visual / migrar para **Figma** se for o canal do pitch.
- [ ] Reusar o `map_component` do RER no lugar do Leaflet puro, ao integrar com a plataforma.
