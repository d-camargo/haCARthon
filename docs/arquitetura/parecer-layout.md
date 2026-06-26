# Contexto — Parecer/RAT (Print Layout + Atlas) do plugin Pré-Val CAR

> Documento para **retomar o tópico do parecer** depois. Resume o que existe, como funciona,
> as restrições e os próximos passos — incluindo o plano de usar um **template `.qpt`**.

## O que é
O 3º passo do plugin gera, para cada imóvel em conflito, um **parecer técnico em PDF** (a "RAT"),
via **Print Layout + Atlas** do QGIS. O Atlas itera os imóveis e produz **2 páginas A4 retrato** por imóvel.

## Onde está o código
| Arquivo | Papel |
|---|---|
| `src/plugin-qgis/processing/gerar_parecer.py` | Algoritmo `prevalcar:preparar_pareceres` — lê `json_sobreposicoes` da fila e cria o campo **`parecer_html`** |
| `src/plugin-qgis/core/parecer.py` | `formatar_memoria_html()` — monta o HTML do parecer (tabela + recomendação) |
| `src/plugin-qgis/core/layout_parecer.py` | `criar_layout_parecer()` — **monta o layout programaticamente** e configura o Atlas |
| `src/plugin-qgis/gui/kpis_dock.py` → `acao_parecer()` | roda o algoritmo, chama `criar_layout_parecer`, abre o designer e liga o preview do Atlas |

## Como o layout está hoje (montado em código)
- **Atlas:** camada de cobertura = "Fila c/ Parecer"; filtro `"conflito" = 1`; ordena por `"score"` desc.
- **Página 1 (identificação + mapa):** logo no **canto superior direito** (60×60); título e identificação
  (`cod_imovel · municipio · score`) **centralizados**; **mapa grande** (190×210) mostrando **apenas a
  camada "Fila Priorizada"** (estilo graduado por score); **legenda** + **escala gráfica e numérica**.
- **Página 2 (memória de cálculo):** logo (50×50); cabeçalho **"MEMÓRIA DE CÁLCULO"** centralizado (18pt);
  o **parecer HTML**.

## Restrições importantes (já aprendidas na marra)
- **Sem WebKit:** o QGIS 4.0.3 do usuário foi compilado **sem WebKit** → `QgsLayoutItemHtml` fica em
  branco. Por isso o parecer usa **`QgsLayoutItemLabel` em modo HTML** (Qt rich text), que:
  - renderiza um **subconjunto** de HTML/CSS (tabelas e estilos simples ok);
  - **não pagina** → por isso a tabela é **limitada a 12 linhas** (`_LIMITE_LINHAS` em `parecer.py`) + linha-resumo.
- **Expressões em rótulo:** usar campos **sem aspas duplas** (`[% cod_imovel %]`); com aspas viram `&quot;`
  e quebram a expressão (aparece o código cru).
- **Retrato:** forçar `page(0).setPageSize('A4', PORTRAIT)` — o `initializeDefaults()` pode criar paisagem.
- **Campos exigidos** na camada de cobertura: `parecer_html`, `cod_imovel`, `municipio`, `score`, `conflito`.
- Compat de enums Qt5/Qt6 tratada no topo de `layout_parecer.py` (MM, MAP_AUTO, LABEL_HTML, PIC_ZOOM, PORTRAIT, HCENTER).

## Próximo passo planejado — usar um TEMPLATE `.qpt`
**Ideia do usuário:** desenhar o layout no **designer do QGIS** (com calma, ajustando visualmente) e
**salvar como template `.qpt`**, em vez de manter o layout em código.

Plano para isso:
1. No designer, montar as 2 páginas (cabeçalho, mapa, legenda, escalas, parecer) e configurar o **Atlas**.
2. Nos itens de texto, usar as **mesmas expressões** (`[% cod_imovel %]`, `[% parecer_html %]` etc.).
3. **Layout → Salvar como template** → arquivo `.qpt`. Guardar em `src/plugin-qgis/recursos_qgis/parecer_rat.qpt`.
4. Trocar `criar_layout_parecer()` para **carregar o template** em vez de construir item a item:
   ```python
   from qgis.PyQt.QtXml import QDomDocument
   from qgis.core import QgsReadWriteContext
   doc = QDomDocument(); doc.setContent(open(caminho_qpt).read())
   layout = QgsPrintLayout(project)
   layout.loadFromTemplate(doc, QgsReadWriteContext())
   # depois: setar coverage do atlas, layers do mapa, e o nome com o município
   ```
5. Pontos de atenção ao carregar template: **re-apontar** a camada de cobertura do Atlas e os **layers do
   mapa** (o `.qpt` não guarda as camadas do projeto atual); e o **caminho do logo** (usar caminho relativo
   ou re-setar a imagem após carregar).

> Quando o usuário salvar o `.qpt`, ele compartilha o arquivo e eu adapto `criar_layout_parecer()`
> para carregá-lo (mantendo a ligação de Atlas/camadas/logo no código).

## Itens em aberto / calibragem
- Ajuste fino de milímetros (altura do mapa, posição de legenda/escala, tamanho do logo).
- Melhorar o HTML do parecer dentro do que o Qt rich text renderiza bem (evitar CSS não suportado).
- Eventualmente expor `_LIMITE_LINHAS` como parâmetro.
- Considerar um rodapé com data/responsável e espaço para assinatura (futuro).
