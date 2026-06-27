# Entregar — Terra em Dia (Desafio 3)

> Fase 4 do Duplo Diamante. Priorizar, prototipar e contar a história.
> Saída: **storyboard** (vira o vídeo de 2 min) + telas do protótipo.

## Priorização — Impacto × Esforço (para o MVP do protótipo)

| Funcionalidade | Impacto | Esforço (protótipo) | No MVP? |
|---|---|---|---|
| Traduzir **APP (mata ciliar)** por imóvel, em linguagem simples | 🔴 Alto | 🟢 Baixo | ✅ herói |
| **Checagem de entendimento** (1–2 perguntas) | 🔴 Alto | 🟢 Baixo | ✅ diferencial |
| **"Antes/depois" visual** da faixa do rio | 🟠 Médio | 🟢 Baixo | ✅ |
| Guiar **até o botão do SICAR** | 🔴 Alto | 🟢 Baixo | ✅ |
| Entrada via **Casa da Agricultura → WhatsApp** | 🔴 Alto | 🟢 Baixo (encenado) | ✅ (abertura) |
| Reserva Legal / déficit | 🟠 Médio | 🟠 Médio | 🚲 próximo |
| Multicanal (Telegram, caixa Gov.br) | 🟠 Médio | 🟢 Baixo (citar) | 🚲 próximo |
| Leitura real por API do CAR | 🔴 Alto | 🔴 Alto | 🚲 próximo (citar viabilidade) |
| Painel da Luana (escala) | 🟠 Médio | 🟠 Médio | 🚲 pitch (1 frase) |

> RICE não muda a conclusão: o MVP é **APP + checagem + guia**, com alto *reach* (toda APP de curso d'água é a feição mais comum) e alta *confidence* (validado nas lives/Briefing).

## Storyboard — "A carta do Seu Raimundo" (vídeo ~2 min)

**Gravação de tela do bot real no Telegram** (a conversa de verdade, com os **2 mapas**). Imóvel real anonimizado de **Querência do Norte/PR** (~3 módulos; 89,6 ha; mata ciliar ~2 ha; déficit de RL ~9,6 ha). Cenas 0–1 são abertura em off; **2–7 são a tela do bot**.

| Cena | Tempo | Visual | Conteúdo |
|---|---|---|---|
| **0. A carta** | 0:00–0:12 | Raimundo na varanda com um **papel** na mão (notificação dos Correios), cara de dúvida | Off: *"Seu Raimundo recebeu uma carta sobre o CAR. Não entendeu o que era pra fazer — e ficou com medo de perder a terra."* |
| **1. A Casa da Agricultura** | 0:12–0:25 | Fachada "**Casa da Agricultura**" (prefeitura — fictício); técnico aponta o celular | Off: *"Foi à Casa da Agricultura da prefeitura. Lá disseram: 'isso você tira no Zap, com o Terra em Dia'."* |
| **2. O primeiro oi** | 0:25–0:40 | Tela do Telegram | **Raimundo:** "Boa tarde! Recebi essa carta do CAR 📄 e não entendi nada." (manda o **número do CAR**) · **Terra em Dia:** "Achei seu sítio ✅ Deixa eu te mandar o mapa dele..." |
| **3. O mapa + o porquê** | 0:40–1:05 | **Mapa atual** do sítio (perímetro + mata ciliar azul + RL) | **Terra em Dia:** "Esse é o seu sítio em *Querência do Norte/PR* — *89,6 hectares* 👆. Deixa eu te perguntar antes: você sabe *por que* recebeu essa carta? 🤔" · **Raimundo:** "Sei lá, não entendi direito…" |
| **4. Educa + como deve ficar** | 1:05–1:35 | **2º mapa "como deve ficar"** (mata ciliar em verde) | **Terra em Dia:** "Tranquilo 🙂 A carta fala da *mata ciliar* — a faixa de mato na beira do rio. A lei pede *30 passos* de cada lado. É essa faixa 👇" · *(manda o mapa-meta)* · "Tem também a *Reserva Legal*: faltam uns *9,6 ha* — dá pra ampliar a sua ou formar um corredor com a mata do rio. 😉" |
| **5. Confere se entendeu** | 1:35–1:55 | Balões normais | **Terra em Dia:** "Só pra eu saber se expliquei direito 😅: por que será que a lei pede esse mato na beira do rio?" · **Raimundo:** "Pra água não secar e o barranco não cair, né?" · **Terra em Dia:** "É isso aí! 👏" |
| **6. Guia a ação** | 1:55–2:10 | Print do SICAR com o botão | **Terra em Dia:** "Agora é confirmar no SICAR e cuidar do que faltar de mato 📋. No fim, *só você aperta o botão* — ninguém faz por você. Aí você entra na fila do *crédito rural* 💰." |
| **7. Fecho** | 2:10–2:20 | Raimundo aliviado, sorrindo pro celular | Off + tagline: *"Sem juridiquês. Sem advogado. No canal que ele já confia. **Terra em Dia — o Código Florestal explicado pra sua terra.**"* |

### Métrica de eficácia — "educação que se mede"
A checagem **não é um teste**: é uma **pergunta despretensiosa** ("por que você acha que a lei pede esse mato?"). O bot infere pela resposta se o produtor **demonstrou entender** e registra (sim/não). Isso vira um **KPI**:

> *De 30 produtores que conversaram, 20 entenderam na 1ª explicação → **67% de compreensão**.*

**Por que importa:** o D3 pede literalmente "**aumentar o entendimento**". A maioria das soluções só *afirma* que educa — a nossa **mede** o entendimento e melhora com o tempo (A/B nas explicações). Raro num hackathon; a coordenação valoriza impacto demonstrável (Live 06).

### Notas de produção
- **Tom:** caloroso, frases curtas, **exemplos concretos** (passos, campo de futebol) — o Briefing diz que o Raimundo confia mais em concreto que em abstrato.
- **Checagem conversacional** (sem botões de quiz): pergunta aberta; o bot reconhece a ideia certa (proteger água/barranco/erosão) e, se não vier, **reexplica** com outras palavras.
- **Honestidade:** o assistente **orienta**, não executa; o aceite é sempre no SICAR (Live 06). Não prometer liberação automática de crédito (é critério do banco — Live 06).
- **Casa da Agricultura** é **fictícia** (representa o canal de confiança / ATER local) — rotular como ilustrativa.
- **Antes/depois:** usar o mapa real do imóvel (geometria do `data/`), anonimizado.

## Próximos passos da entrega (até domingo 28/06, 23:59)
1. **Gravar a tela do bot real** (Telegram) usando este storyboard como roteiro de demonstração — é protótipo **funcional**, não mockup.
2. **Ideação** (respostas às perguntas oficiais) — puxar do Duplo Diamante (`docs/descobrir|definir|desenvolver|entregar`).
3. **Pitch** (slides + voz, 3 min) — problema, buraco, solução, diferencial, impacto.
