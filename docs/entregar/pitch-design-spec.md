# Spec de design do pitch — Terra em Dia (para o Claude Design)

> Companheiro de `pitch-terra-em-dia.md` (que tem a **narração**). Aqui está o **visual**:
> sistema de design + os **8 slides** detalhados (layout, texto exato na tela, imagens, uso do ícone).
> **Formato:** 16:9, 1920×1080 (Canva "Apresentação"). **Pouco texto por slide** — a voz conta a história.
> **Marca-d'água do edital:** rodapé discreto "haCARthon · Desafio 3" em todos os slides (menos a capa).

---

## 1. Sistema de design

### Logo / ícone
- Arquivos na **raiz do projeto**: `icon.png` (1024², fundo transparente) e `icon.svg` (vetor — preferir o SVG para escalar sem perder nitidez).
- O ícone é um **brasão verde**: folha + mapa dobrado com grade + pin lima + campos.
- **Uso:** ele é o logo do produto. Aparece grande na **capa (slide 1)** e pequeno no **rodapé/canto** dos demais. Nunca distorça (manter proporção) nem coloque sobre fundo verde-escuro sem o contorno branco que ele já tem.
- **Lockup do nome:** ao lado/abaixo do ícone, "**Terra em Dia**" em verde-floresta; subtítulo fino "O Código Florestal explicado pra sua terra".

### Paleta (derivada do ícone + dos mapas do bot)
| Token | Hex | Uso |
|---|---|---|
| Verde-floresta (contorno/título) | `#14532d` | títulos, contornos, texto sobre claro |
| Verde-primário | `#16a34a` | destaques, selos, barras |
| Verde-folha | `#4d9e3f` | apoio, blocos secundários |
| Lima/pin (acento) | `#c4d92e` | **acento de destaque** (números, realce) — usar com parcimônia |
| Azul-mata-ciliar | `#2563eb` | só no mapa "atual" (já é a cor da APP no bot) |
| Verde-meta | `#15803d` | só no mapa "como deve ficar" |
| Bege-perímetro | `#f5f5dc` | fundos de cartão suaves |
| Off-white (fundo) | `#faf9f4` | fundo padrão dos slides |
| Tinta (texto) | `#1c2b1f` | corpo de texto sobre claro |

- **Fundos:** padrão claro `#faf9f4`. Slides de virada (3 "o buraco" e 8 "fecho") podem ser **verde-floresta `#14532d` com texto off-white** para dar ritmo.
- **Contraste:** garantir AA (texto ≥ 4.5:1). Lima `#c4d92e` **não** serve para texto pequeno sobre branco — usar só em número grande/realce com peso.

### Tipografia (disponíveis no Canva)
- **Títulos:** Poppins **SemiBold/Bold** (ou Montserrat). Tamanho 44–60 pt.
- **Corpo/legendas:** Inter ou Source Sans, 20–28 pt.
- **Número-herói** (estatística): Poppins Bold 120–160 pt, em verde-primário ou lima.
- Máximo **2 famílias**. Frases curtas, sem ponto final em títulos.

### Grid e composição
- Margem de segurança de **8%** nas bordas. Coluna única ou 2 colunas (texto | imagem).
- **Regra de 1 ideia por slide.** No máx. 3 bullets curtos; nada de parágrafo.
- Imagens dos mapas com **canto arredondado 16 px** e sombra suave.

### Estilo de ícones (pictogramas)
- Linha simples, 2–3 px, cor verde-floresta, mesmo peso. (Carta, mapa, balão de conversa, folha, cifrão, escudo/lei.) Canva "linha/outline", não 3D.

### Rodapé padrão (slides 2–8)
- Faixa inferior fina: à esquerda `icon.svg` mini + "Terra em Dia"; à direita "haCARthon · Desafio 3". 14–16 pt, cor `#4d9e3f`.

### Assets reais a usar (não usar placeholder genérico onde houver o real)
- **Mapa "atual"** e **mapa "como deve ficar"**: gerados pelo bot (`mapa.gerar_mapa`, modos `atual`/`meta`) — agora **com satélite de fundo**. Exportar 2 PNGs do imóvel-demo e usar nos slides 5 (e 1, como textura sutil).
- **Print do bot** (conversa real no Telegram) — 1 recorte vertical limpo para o slide 5.
- **Foto do produtor** (slide 1) e **fachada "Casa da Agricultura"** (se usar) — **stock do Canva** (produtor rural brasileiro, +50, chapéu/camisa simples). Rotular a Casa da Agricultura como **ilustrativa**.

---

## 2. Slides (8) — layout + texto exato

> "Texto na tela" = **só o que aparece no slide** (curto). A fala completa está em `pitch-terra-em-dia.md`.

### Slide 1 — Capa / O problema
- **Fundo:** off-white com o mapa "atual" bem suave (10% opacidade) sangrando à direita.
- **Centro-esquerda:** `icon.svg` grande (~280 px) + lockup:
  - **Terra em Dia** (Poppins Bold 60, `#14532d`)
  - "O Código Florestal explicado pra sua terra" (Inter 26, `#1c2b1f`)
- **Faixa inferior:** foto do Seu Raimundo segurando um **papel** (a carta), com leve gradiente para o texto respirar.
- **Texto na tela:** só o lockup. (A dor vem na narração.)
- **Sem rodapé** (é capa).

### Slide 2 — O tamanho do problema
- **Layout:** número-herói centralizado, com uma linha de escala embaixo.
- **Texto na tela:**
  - Número-herói: **1,1 milhão** (Poppins Bold 150, `#16a34a`)
  - Linha sob o número: "imóveis parados esperando o produtor responder"
  - Linha de escala (menor, `#1c2b1f`): "de **8,29 mi** cadastrados (13%) · **154 mi ha** travados (21% da área)"
  - Selo/fonte (rodapé do slide, 14 pt): "Painel de Regularização Ambiental — SFB · jun/2026"
- **Visual:** silhueta do mapa do Brasil em `#4d9e3f` 15% atrás do número. Opcional: um pequeno bloco "1 em cada 8 imóveis" como reforço visual do 13%.
- **Acento lima** pode realçar o "1,1 milhão" ou a palavra "parados".
- **Dado confirmado** (Painel SFB, 28/06/2026): 1.107.749 de 8.292.805 imóveis (13,4%); 153,8 mi ha (21,4%). Memória de cálculo e fonte em `evidencias-pitch.md`. ⚠️ Conferir se o painel mudou no dia da gravação.

### Slide 3 — O buraco (slide de virada)
- **Fundo:** verde-floresta `#14532d`, texto off-white.
- **Layout:** 2 colunas.
  - **Esquerda:** print/ícone "Tô em Dia / Meu Imóvel Rural" com etiqueta "traduz o **crédito** ✓".
  - **Direita:** trecho do Código Florestal (textura de lei) com etiqueta "obrigação ambiental por feição ✗".
- **Texto na tela (título):** "As ferramentas oficiais traduzem o **crédito** — não a **obrigação ambiental**."
- **Selo no rodapé do slide:** "conforme o vídeo oficial de demonstração" (itálico, pequeno).

### Slide 4 — A solução
- **Fundo:** off-white. Volta a respirar depois do slide escuro.
- **Centro:** `icon.svg` médio + nome **Terra em Dia**.
- **Abaixo:** balão de conversa estilizado (verde-primário) com a frase:
  - "Manda o número do CAR. Eu te explico o que a lei pede **na sua terra**."
- **Texto na tela (1 linha):** "Um assistente de conversa — **no Zap que ele já confia**."
- **Mini-ícones em linha:** 📨 conversa · 🗺️ mapa · 🌱 linguagem simples.

### Slide 5 — Como funciona (o coração) — slide mais visual
- **Layout:** 3 zonas.
  - **Faixa superior — 4 passos** (pictogramas em linha, numerados):
    1. Mostra a terra → 2. Traduz a lei → 3. Confere o entendimento → 4. Guia até o SICAR.
  - **Centro — o "antes/depois":** os **2 mapas lado a lado** com seta entre eles:
    - Esquerda: **"como está"** (mapa `atual`, mata ciliar azul).
    - Direita: **"como deve ficar"** (mapa `meta`, faixa verde).
  - **Direita/canto — print do bot** (recorte vertical curto da conversa real).
- **Texto na tela:** títulos "como está" / "como deve ficar" sobre os mapas; nada mais.
- **Micro-destaque:** sob os mapas, uma linha: "Reserva Legal: **você declarou X · a lei pede Y · falta Z**" (preencher com os números do imóvel-demo).

### Slide 6 — Diferencial
- **Layout:** 3 cartões iguais (bege `#f5f5dc`, ícone no topo).
  - **Cartão 1 — Personalizado pelo imóvel** (ícone mapa/pin) — "a lei na **sua** terra, não um texto genérico".
  - **Cartão 2 — Mede o entendimento** (ícone gráfico) — "**KPI de % de compreensão** — raro num app de lei". Destacar com lima.
  - **Cartão 3 — Qualquer imóvel do Brasil** (ícone Brasil) — "lê direto da **base oficial do SICAR** pelo nº do CAR".
- **Texto na tela (título):** "Três coisas que ninguém junta."

### Slide 7 — Impacto, viabilidade e abertura
- **Layout:** 3 colunas com ícone + 1 linha cada.
  - ⚖️ **Legal:** "o aceite é sempre **dentro do SICAR**".
  - 🛠️ **Técnico:** "protótipo **funcional** · **open source** (GPL) · **troca de LLM** sem reescrever".
  - 🌱 **Escala:** "cooperativas, sindicatos e **ATER** — e apoia o analista do estado".
- **Faixa inferior:** "coerente com o CAR como **Bem Público Digital**".
- **Texto na tela (título):** "Dá pra rodar hoje — e crescer."

### Slide 8 — Fecho (slide de virada)
- **Fundo:** verde-floresta `#14532d`.
- **Centro:** `icon.svg` + **tagline grande** off-white:
  - "**Terra em Dia**"
  - "O Código Florestal explicado pra sua terra."
- **Acima, fininho:** "Sem juridiquês. Sem advogado. No canal que ele já confia."
- **Canto:** foto do Raimundo aliviado, olhando o celular (opcional, recorte pequeno).

---

## 3. Notas finais para o Claude Design
- **Consistência:** mesmo rodapé, mesma família tipográfica e mesma posição do logo em todos.
- **Ritmo de cor:** claro (1,2) → escuro (3) → claro (4,5,6,7) → escuro (8). Dá respiro e ênfase.
- **Acento lima** só em: número-herói (slide 2) e cartão "mede o entendimento" (slide 6). Não espalhar.
- **Exportar** como apresentação 16:9; a equipe grava a narração por cima (voz humana, ≤3:00).
- **Pendências de conteúdo** marcadas com ⚠️: números X/Y/Z da Reserva Legal do slide 5 — preencher com o imóvel-demo (herói) antes de gravar. (O número do slide 2 já está fechado — ver `evidencias-pitch.md`.)
