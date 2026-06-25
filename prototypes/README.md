# Protótipos

Wireframes e mockups da solução. Fidelidade sobe **só até onde precisar**
(papel → wireframe → mockup → Figma), conforme a metodologia do projeto.

## painel-luana/ — Painel de Pré-validação da Luana (recorte R1+R2)

Wireframe **lo-fi** da tela principal do recorte escolhido: a fila de análise priorizada por
risco + o detalhe do cadastro com comparação declarado × referência e detecção de sobreposição.

- **Arquivo:** `painel-luana/index.html` (autocontido, sem dependências).
- **Como abrir:** dê duplo clique no arquivo ou abra no navegador.
- **Print:** `painel-luana/preview.png` (gerado com Chrome headless).

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
- [ ] Validar o wireframe com a jornada futura (storyboard) da Luana.
- [ ] Subir fidelidade para **mockup** (cores, tipografia) — ou migrar para **Figma** se for o canal do pitch.
- [ ] Conectar a **PoC de sobreposição** (PostGIS) a este painel — substituir os SVGs por mapa **Leaflet** real (reusar `map_component` do RER).
