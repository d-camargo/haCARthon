# Desenvolver — Terra em Dia (Desafio 3)

> Fase 3 do Duplo Diamante. Gerar e estruturar soluções para o problema definido.
> Insumo: jornada e gaps de `docs/definir/definir-terra-em-dia.md`.

## How Might We (Como poderíamos...)

Dores da jornada → perguntas abertas:
- **HMW-1** Como poderíamos explicar a obrigação ambiental do imóvel em **linguagem que o Raimundo entende**, usando a **terra dele** como exemplo?
- **HMW-2** Como poderíamos dar **segurança** ao Raimundo de que ele **entendeu** antes de agir (vencer o medo de errar)?
- **HMW-3** Como poderíamos chegar ao Raimundo pelos **canais que ele já confia** (cooperativa, sindicato, técnico → WhatsApp), em vez de "mais um app"?
- **HMW-4** Como poderíamos **guiar** o Raimundo até resolver **no SICAR** sem ele se perder?
- **HMW-5** Como poderíamos transformar o **demonstrativo técnico** (números trancados) em uma **conversa** que conecta regra → porquê → benefício → ação?

> Foco do MVP: **HMW-1 + HMW-2** (tradução por feição + checagem). HMW-3/4/5 entram como contexto e próximos passos.

## Benchmark (o que existe e onde para)

| Solução | Linguagem simples? | Personalizado pelo imóvel? | Obrigações **ambientais** por feição? | Testa entendimento? | Guia até a ação? |
|---|---|---|---|---|---|
| **Meu Imóvel Rural / Tô em Dia** | ✅ (regra de **crédito**) | ✅ (status/checklist) | ❌ (só crédito/status) | ❌ | parcial ("Fique em Dia", crédito) |
| **Demonstrativo do CAR** | ❌ (técnico) | ✅ (números do imóvel) | ✅ (números crus, sem traduzir) | ❌ | ❌ |
| **Cartilhas / vídeos do Código Florestal** | ✅ | ❌ (genérico) | ✅ (genérico) | ❌ | ❌ |
| **Chatbots jurídicos genéricos** | ✅ | ❌ | parcial (abstrato) | ❌ | ❌ |
| **🟢 Terra em Dia** | ✅ | ✅ (nº do CAR, leitura) | ✅ **(o buraco)** | ✅ **(diferencial)** | ✅ (até o botão do SICAR) |

**Leitura:** o cruzamento "personalizado pelo imóvel × obrigações ambientais por feição × testa entendimento" é uma **coluna vazia** no mercado. Ninguém ocupa as três ao mesmo tempo.

## SCAMPER (refinar a ideia)

- **S — Substituir:** texto jurídico → **conversa**; cartilha genérica → **caso real da terra dele**; PDF do demonstrativo → mensagem falada.
- **C — Combinar:** dados do CAR (leitura via API) **+** regras do Código Florestal (APP/RL) **+** LLM tradutora (agnóstica) **+** checagem pedagógica.
- **A — Adaptar:** pegar o padrão **"Entenda a Regra / Fique em Dia"** do Tô em Dia (que já funciona para crédito) e **adaptá-lo para as obrigações ambientais**.
- **M — Modificar/ampliar:** acrescentar a **checagem de entendimento** (1–3 perguntas) — vira o diferencial pedagógico; e o **"antes/depois" visual** da APP (a Giovanna disse que destrava).
- **P — Propor outro uso:** o **mesmo motor** gera o material que a **Luana** usa para explicar (escala / "suporte ao analista" do D3) e pode virar conteúdo para **multiplicadores**.
- **E — Eliminar:** elimina a **dependência de advogado/técnico só para entender**; elimina o **juridiquês** e a tela técnica do SICAR como porta de entrada.
- **R — Reverter:** em vez de o produtor **ir até** o sistema técnico, o sistema **vai até ele** no WhatsApp; em vez de **notificar e esperar**, **explica e acompanha** até a ação.

## Conceito refinado + escopo de MVP (skate → bike)

**🛹 MVP (skate) — o que vira o protótipo/vídeo:** uma **conversa** que, a partir do nº do CAR (encenado com o imóvel real de Querência do Norte):
1. **Educa 1 feição** — APP de curso d'água: *"seu imóvel tem ~2 ha de mata ciliar ao longo do rio; a lei (art. 4º) pede 30 m de cada lado porque o rio tem menos de 10 m"* + o benefício (crédito/PRA).
2. **Testa o entendimento** — 1–2 perguntas simples; se errar, reexplica.
3. **Guia o próximo passo** — mostra o "antes/depois" e leva **até o botão do SICAR** (ou o que subir).

**🚲 Próximos incrementos:** + Reserva Legal (déficit) · multicanal (Telegram/caixa Gov.br) · entrada via cooperativa/sindicato · leitura real por API · painel da Luana (escala).

> Mantém o princípio do MVP: cada incremento já resolve a dor central (entender e agir sobre **uma** obrigação), nunca uma "parte inútil".
