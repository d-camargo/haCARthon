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

Conversa de WhatsApp ("Zap"). Voz em off + balões na tela. Imóvel real anonimizado de **Querência do Norte/PR** (~3 módulos; mata ciliar ~2 ha).

| Cena | Tempo | Visual | Conteúdo |
|---|---|---|---|
| **0. A carta** | 0:00–0:15 | Raimundo na varanda com um **papel** na mão (notificação dos Correios), cara de dúvida | Off: *"Seu Raimundo recebeu uma carta sobre o CAR. Não entendeu o que era pra fazer — e ficou com medo de perder a terra."* |
| **1. A Casa da Agricultura** | 0:15–0:30 | Fachada simples "**Casa da Agricultura**" (prefeitura — fictício); um técnico aponta o celular | Off: *"Foi até a Casa da Agricultura da prefeitura. Lá disseram: 'isso você tira no Zap, com o Terra em Dia'."* |
| **2. O primeiro oi** | 0:30–0:45 | Tela do WhatsApp abrindo | **Raimundo:** "Boa tarde! Recebi essa carta aqui do CAR 📄 e não entendi nada. Pode me ajudar?" (envia **foto da carta**) · **Terra em Dia:** "Boa tarde, Seu Raimundo! 🌱 Posso sim. Me confirma o número do seu CAR (tá na carta) que eu já vejo o seu sítio." |
| **3. Educa (na terra dele)** | 0:45–1:15 | Mapa simples do sítio com a **faixa do rio destacada** | **Terra em Dia:** "Achei seu sítio em Querência do Norte ✅. A carta fala da **mata ciliar** — aquela faixa de mato na beira do rio. A lei pede **30 passos (30 m)** de mato de cada lado, porque o seu rio é estreito. Hoje você tem cerca de **2 campos de futebol** dessa faixa pra cuidar. Ela segura o barranco e protege a sua água 💧." |
| **4. Conversa pra ver se entendeu** | 1:15–1:40 | Balões normais (sem "quiz") | **Terra em Dia:** "Deixa eu te perguntar uma coisa, Seu Raimundo, só pra eu saber se expliquei direito 😅: por que será que a lei pede pra deixar esse mato na beira do rio?" · **Raimundo:** "Ah… pra água não secar e o barranco não cair, né?" · **Terra em Dia:** "É isso aí! 👏 Entendeu certinho." |
| **5. Guia a ação** | 1:40–2:00 | Print do SICAR com o botão destacado | **Terra em Dia:** "Agora o caminho: confirmar essa faixa no sistema e cuidar do que faltar de mato. Eu te mostro o passo a passo 📋. No fim, **só você aperta o botão no SICAR** — é rapidinho. Resolvido isso, você destrava o **crédito rural** 💰. Quer que eu te acompanhe?" |
| **6. Fecho** | 2:00–2:10 | Raimundo aliviado, sorrindo pro celular | Off + tagline: *"Sem juridiquês. Sem advogado. No canal que ele já confia. **Terra em Dia — o Código Florestal explicado pra sua terra.**"* |

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
1. **Telas do protótipo** (mockup do WhatsApp) a partir deste storyboard — ferramenta a definir (Figma/HTML).
2. **Roteiro de ideação** (respostas às perguntas oficiais) — puxar de Descobrir→Entregar.
3. **Pitch** (slides + voz, 3 min) — problema, buraco, solução, diferencial, impacto.
