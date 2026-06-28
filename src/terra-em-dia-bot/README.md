# Terra em Dia — bot de Telegram

Protótipo **funcional** do **Desafio 3** do haCARthon. O Seu Raimundo chama no
"Zap" (Telegram), manda o número do CAR; o bot:

1. **Consulta os dados reais** do imóvel no CAR (por `cod_imovel`).
2. **Manda um mapa** com as feições do cadastro (perímetro, mata ciliar, Reserva Legal).
3. Guarda uma **memória local em memória de processo** durante a execução do bot, para não começar do zero a cada mensagem.
4. Responde em linguagem simples ao que o produtor perguntar: mata ciliar, Reserva Legal,
   mapa ou passo no SICAR.
5. **Guia o passo a passo** quando o produtor pedir (orienta, não executa).

## Como rodar

```bash
cd src/terra-em-dia-bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # osgeo (GDAL) vem do sistema, não do pip

cp .env.example .env                    # preencha:
#   TELEGRAM_TOKEN  (obrigatório, do @BotFather)
#   OPENAI_API_KEY  (opcional; sem ele, usa o roteiro determinístico)
#   TERRA_DEMO_COD  (cod_imovel de demonstração — ver data/exemplo-raimundo.local.md)
python bot.py
```

No Telegram, abra seu bot e mande `/start`.

**Fluxo de Botões (Telegram Inline Keyboard):**
Ao carregar um imóvel do CAR, o bot oferece proativamente botões interativos para guiar o produtor rural:
- 🌳 **Ver como fica em dia:** Envia o mapa-meta de como a beira do rio/reserva deve ficar.
- 🔍 **Comparar agora × depois:** Envia um comparativo visual com dois painéis lado a lado, dando **zoom automático** focado diretamente na beira do rio (APP) para manter as faixas nítidas e visíveis. A Reserva Legal, por não possuir demarcação geométrica futura pré-definida, é informada de maneira transparente via texto/anotação na conversa para evitar dados fictícios.
- 📋 **Passos no SICAR:** Manda o passo a passo resumido do que fazer.

**Atalhos e Comandos (para fallback/uso direto):**
- **Mapa atual (Situação hoje):** Envie mensagens naturais como `"me manda o mapa"`, `"quero ver o mapa"` ou use o comando `/mapa`.
- **Mapa meta (Como deve ficar):** Envie mensagens naturais como `"como deve ficar?"`, `"como fica depois?"`, `"o certo"`, `"depois"` ou use o comando `/comofica` (ou `/mapadepois`).

Use o comando `/metricas` para ver a eficácia de compreensão acumulada (KPI).

## Demonstração e Simulação

O projeto permite selecionar imóveis de demonstração da base local e simular conversas via linha de comando (sem precisar de chaves do Telegram):

1. **Selecionar imóveis de demonstração:**
   Rode o script abaixo para selecionar deterministicamente 3 imóveis locais de Querência do Norte/PR com perfis contrastantes, restringindo a seleção apenas a pequenas e médias propriedades rurais (até 15 módulos fiscais, segundo o art. 3º da Lei 12.651/2012):
   ```bash
   PYTHONPATH=. .venv/bin/python selecionar_demo.py --forcar
   ```
   Os códigos reais desses imóveis serão gravados em `data/imoveis_teste.local.txt` (ignorados pelo git) e a tabela completa em `data/candidatos_demo.local.txt`.

2. **Simular atendimento via CLI:**
   Você pode simular o atendimento a um imóvel (resumo e respostas) usando:
   ```bash
   # Apresentar o resumo da primeira propriedade de teste
   PYTHONPATH=. .venv/bin/python simular.py
   
   # Simular resposta a uma pergunta para a propriedade de teste
   PYTHONPATH=. .venv/bin/python simular.py "o que é essa mata da beira do rio?"
   
   # Simular para um código específico (real ou fictício)
   PYTHONPATH=. .venv/bin/python simular.py PR-4121000-0007CEC715174E48B38AAE0537AEB789 "qual é minha pendência?"
   ```

## Arquitetura
| Módulo | Papel |
|---|---|
| `bot.py` | Handlers do Telegram e fluxo da conversa |
| `cadastro.py` | Lê perímetro + APP + RL por `cod_imovel` (osgeo/GDAL) — motor de dados reais |
| `analise.py` | Regras do Código Florestal: faixa de APP, RL exigida × proposta, déficit |
| `geo_app.py` | Medição geométrica da largura média e área legal da APP (GDAL/OGR) |
| `mapa.py` | Renderiza o PNG do imóvel com as feições (matplotlib, offline) |
| `conteudo.py` | Textos na linguagem do Raimundo + roteiro de fallback + `compreendeu()` |
| `llm.py` | LLM **agnóstico** (interface OpenAI-compatible; `base_url` configurável) |
| `memoria.py` | Memória persistente por usuário em arquivo local gitignored |
| `metricas.py` | Registro/agregação da compreensão (KPI "% que entendeu") |

## Notas
- **Dados reais** do SICAR (base oficial do Paraná/Brasil). O acesso aos dados é centralizado em `cadastro.carregar_imovel(cod)`. O motor tenta primeiro consultar a API WFS oficial em tempo real para obter o perímetro e atributos de qualquer imóvel do Brasil. Caso a consulta falhe ou não haja conexão, o motor cai de forma automática para a base local offline. Para imóveis que não possuem dados de APP/RL declarados na base local, a análise do bot opera de forma dimensional (mata ciliar de 30 m) e não calcula déficit de Reserva Legal. **O bot presume os pontos de atenção a partir dos dados do CAR carregados**, eliminando a necessidade do produtor decifrar ou interpretar a notificação sozinho.
- **Mapas com imagem de satélite:** Os mapas gerados para o produtor rural (`mapa.py`) utilizam a imagem de satélite **Esri World Imagery** como fundo, com alinhamento universal de vetores. A requisição de exportação de satélite é feita solicitando o formato `f=json` ao Esri para ler o `extent` geográfico real de posicionamento da imagem retornada, usando-o no parâmetro `extent` da plotagem `imshow` do Matplotlib. Isso garante um alinhamento perfeito dos vetores sobre o satélite, mesmo em propriedades extremamente estreitas ou longas que ativariam limites de proporção de imagem. O mapa comparativo também apresenta uma cota e seta indicativas sobre o painel da solução, reforçando graficamente a regra de "Faixa legal: 30m da margem" para a mata ciliar.
- **Medição da APP e Base Legal:** O módulo `geo_app.py` realiza a reprojeção dos polígonos de APP de EPSG:4674 para UTM SIRGAS 2000 (zona dependente da longitude do imóvel) com ordem tradicional GIS para calcular a área real (Shoelace) e o perímetro do anel externo em metros. A largura média é estimada pela heurística `largura_media ≈ 2 * área / perímetro`. A área legal recomendada (escala para os 30 metros de largura mínima exigidos da margem pelo Código Florestal, Lei 12.651/12, Art. 4º, I, alínea 'a' para rios de até 10 metros) é projetada proporcionalmente. Esses valores são aproximados e auxiliam no confronto de déficit de mata ciliar.
- **Agnóstico de modelo:** `OPENAI_BASE_URL` aponta para a OpenAI na demo ou para
  um modelo aberto/local (Ollama, vLLM) — coerente com o CAR como Bem Público Digital.
- **Funciona sem LLM:** sem `OPENAI_API_KEY`, o bot usa o roteiro de `conteudo.py`.
- O bot **orienta**, não executa: o aceite é sempre no SICAR. Além disso, ele não substitui assistência técnica de campo nem programas de plantio; sua função é ajudar a interpretar o CAR e guiar o produtor rural até o passo correto no SICAR.
- A memória é mantida em processo (zera ao reiniciar o bot) e também pode ser limpa para aquele chat com `/cancel`.
