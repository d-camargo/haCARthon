# ACTIONS.md - Tarefas do planejador para o executor junior

Este arquivo e o canal operacional entre o planejador senior e o executor
junior.

- O planejador senior escreve aqui as tarefas prontas para execucao.
- O executor junior le este arquivo, escolhe a proxima tarefa marcada como
  `status: pronta`, executa exatamente o que foi pedido e reporta o resultado.
- Nenhuma tarefa deve ser executada se estiver como `rascunho`, `bloqueada` ou
  `concluida`.

O executor junior tambem deve ler `INSTRUCTIONS.md` antes de executar qualquer
tarefa. Em caso de conflito, siga esta ordem de prioridade:

1. instrucao direta mais recente do usuario;
2. tarefa especifica em `ACTIONS.md`;
3. regras de execucao em `INSTRUCTIONS.md`;
4. regras de planejamento em `AGENTS.md`.

## Como usar este arquivo

O planejador deve registrar cada tarefa no formato abaixo.

````md
## ACTION-000 - Titulo curto

status: pronta
tipo: codigo | documentacao | validacao | pesquisa
prioridade: alta | media | baixa

### Objetivo

Uma frase dizendo o resultado esperado.

### Contexto

Explique somente o necessario para o junior nao interpretar errado.

### Arquivos permitidos

- caminho/permitido.py

### Arquivos proibidos

- .env
- data/**
- desafio-2/**

### Passos

1. Faca exatamente isto.
2. Depois faca aquilo.
3. Nao faca nada alem disso.

### Comandos de validacao

```bash
comando exato
```

### Criterios de aceite

- Criterio verificavel 1.
- Criterio verificavel 2.

### Forma errada provavel

- Nao confundir X com Y.
- Nao alterar arquivo Z.

### Resultado do executor

Preencher depois da execucao.
````

## Fila de acoes

## ACTION-001 - Deixar o atendimento mais natural e usar todos os dados do imovel

status: concluida
tipo: codigo
prioridade: alta

### Objetivo

Melhorar a conversa do bot para soar mais amigavel e rural, garantir que ele
traga tanto mata ciliar quanto Reserva Legal quando falar da propriedade, e
fazer a memoria de teste zerar toda vez que o bot subir.

### Contexto

O usuario testou o bot e achou a conversa monotona. O bot tambem falou apenas
de Reserva Legal, embora o imovel de teste tenha problema/tema relevante de
mata ciliar.

Descreva o produtor rural de referencia assim ao ajustar tom e prompt:

- pessoa pratica, acostumada a resolver problema concreto;
- valoriza clareza, confianca e exemplo da propria terra;
- pode ter medo de mexer no CAR e fazer errado;
- nao quer aula de lei, quer entender "o que isso muda no meu sitio";
- prefere conversa respeitosa, simples e direta;
- nao deve ser tratado como incapaz ou caricato.

O bot deve ter mais vida, mas sem virar personagem exagerado. Use acolhimento
leve, linguagem de atendimento e exemplos concretos. Nao usar piadas, caipires,
estereotipo ou excesso de emoji.

Hoje a leitura do imovel ja existe em `cadastro.py`:

- perimetro em `data/sicar`;
- APP em `data/Área de Preservação Permanente`;
- Reserva Legal em `data/Reserva Legal`.

Para a demo, continue usando a base local. Para preparar a ideia de tempo real,
organize o codigo para deixar claro que `cadastro.carregar_imovel(cod)` e o
ponto unico de acesso aos dados da propriedade. Nao implemente rede, API real
do CAR nem scraping agora.

### Arquivos permitidos

- `src/terra-em-dia-bot/bot.py`
- `src/terra-em-dia-bot/conteudo.py`
- `src/terra-em-dia-bot/llm.py`
- `src/terra-em-dia-bot/memoria.py`
- `src/terra-em-dia-bot/README.md`

### Arquivos proibidos

- `src/terra-em-dia-bot/.env`
- `.env`
- `.env.*`, exceto `.env.example`
- `data/**`, exceto se for arquivo temporario criado e apagado pelo proprio teste
- `desafio-2/**`
- `docs/base-documental/**`
- arquivos `.sqlite`
- arquivos `.pdf`

### Passos

1. Leia `bot.py`, `conteudo.py`, `llm.py`, `memoria.py` e `README.md`.
2. Nao altere `cadastro.py` nem `analise.py` nesta tarefa. Eles ja entregam os
   dados necessarios para o bot: APP e Reserva Legal.
3. Em `conteudo.py`, crie uma funcao de resumo da propriedade, por exemplo
   `resumo_imovel(an)`, que sempre apresente os principais pontos disponiveis:
   municipio/UF, area, mata ciliar se `tem_app` for verdadeiro, e Reserva Legal
   se `tem_rl` for verdadeiro.
4. Esse resumo deve ser curto e conversado. Nao pode ser uma lista juridica
   longa. Exemplo de direcao, nao copie literalmente se os dados pedirem ajuste:
   "Olhei seu sitio em Querencia do Norte. Tem dois pontos pra conferir: a mata
   da beira do rio e a Reserva Legal. A mata ciliar precisa guardar 30 metros de
   cada lado; na Reserva Legal, aparecem X ha e a conta pede perto de Y ha."
5. Ajuste `resposta_curta(texto, an)` para que perguntas genericas como
   "como esta minha propriedade?", "o que tem de errado?", "recebi uma carta",
   "me explica meu CAR" ou "qual o problema?" respondam com o resumo completo
   APP + RL, nao apenas com Reserva Legal.
6. Mantenha respostas especificas funcionando: se o usuario perguntar so sobre
   "mata", responder mata ciliar; se perguntar so sobre "reserva", responder RL;
   se pedir mapa, enviar mapa.
7. Ajuste `SAUDACAO`, `RETOMADA`, `VENDO_CADASTRO`, `intro_sitio`,
   `explica_mata`, `sugestao_rl` e `guia_acao` para ficarem mais amigaveis e
   menos secos. Nao aumentar demais: cada resposta deve continuar curta.
8. Em `llm.py`, ajuste o `SYSTEM` para descrever o produtor rural de forma
   respeitosa e orientar o modelo a responder com mais calor humano, mas sem
   estereotipo e sem aula juridica.
9. Ainda em `llm.py`, garanta que `_contexto_imovel(an)` exponha claramente os
   dados de APP/mata ciliar e Reserva Legal para a conversa. O modelo precisa
   ver os dois temas quando existirem.
10. Em `bot.py`, depois de `_apresentar`, use o novo resumo do imovel em vez de
    apenas `intro_sitio(an)`, para o primeiro retorno ja mencionar os pontos
    relevantes da propriedade.
11. Em `memoria.py`, altere a memoria para o modo de teste atual: ela deve zerar
    a cada vez que o processo do bot subir. Forma recomendada: manter historico
    em memoria de processo, sem persistir em `data/memoria_terra_em_dia.json`.
12. Se preferir manter o arquivo como opcao futura, tudo bem, mas nesta tarefa o
    comportamento padrao deve ser: reiniciou o bot, perdeu a memoria anterior.
13. Atualize `README.md` para explicar que, neste prototipo de teste, a memoria
    e apenas da sessao do processo e zera ao reiniciar o bot. Explique tambem
    que `cadastro.carregar_imovel(cod)` e o ponto que hoje le base local e no
    futuro pode ser trocado por consulta em tempo real ao CAR.
14. Nao implemente chamada real ao CAR, WFS, API externa, scraping, captcha ou
    rede. Esta tarefa e organizacao do comportamento e da conversa.
15. Nao mexa em dados locais, `.env` ou `desafio-2/`.

### Comandos de validacao

```bash
python -m py_compile src/terra-em-dia-bot/*.py
```

```bash
PYTHONPATH=src/terra-em-dia-bot python - <<'PY'
import conteudo, memoria
an = {
    "municipio": "QUERENCIA DO NORTE", "uf": "PR", "area_ha": 89.6,
    "faixa_app_m": 30, "tem_app": True, "app_mata_ciliar_ha": 2.0,
    "tem_rl": True, "rl_deficit_ha": 1.2,
    "rl_proposta_ha": 8.0, "rl_exigida_ha": 9.2,
}
resumo = conteudo.resposta_curta("o que tem de errado na minha propriedade?", an).lower()
assert "mata" in resumo or "ciliar" in resumo
assert "reserva" in resumo
assert "30" in resumo
memoria.atualizar(-1, cod="TESTE", historico=[])
memoria.adicionar_mensagem(-1, "user", "teste")
assert memoria.carregar(-1)["cod"] == "TESTE"
memoria.limpar(-1)
assert memoria.carregar(-1) == {}
print("ok")
PY
```

### Criterios de aceite

- Pergunta generica sobre a propriedade retorna resumo com mata ciliar e Reserva
  Legal quando ambos existirem em `an`.
- Pergunta especifica sobre mata ciliar continua respondendo mata ciliar.
- Pergunta especifica sobre Reserva Legal continua respondendo Reserva Legal.
- O primeiro retorno apos carregar o CAR nao fica seco; ele deve apresentar a
  propriedade e os pontos principais de forma amigavel.
- O tom fica mais humano e acolhedor, sem estereotipo de produtor rural.
- O bot nao despeja legislacao nem cita artigo sem necessidade.
- A memoria nao persiste entre reinicios do processo do bot.
- O README explica claramente a memoria de sessao e o ponto futuro de integracao
  com dados reais do CAR.
- Os comandos de validacao passam.

### Forma errada provavel

- Nao resolver criando texto enorme sobre legislacao.
- Nao tratar produtor rural como caricatura.
- Nao colocar sotaque forçado, "caipires" ou piadas rurais.
- Nao remover o suporte sem LLM.
- Nao implementar API real do CAR agora.
- Nao abrir `.env`.
- Nao alterar `data/**`.
- Nao mexer em `desafio-2/**`.
- Nao fazer a memoria persistir em arquivo como comportamento padrao neste
  prototipo de teste.
- Nao deixar pergunta generica cair so em Reserva Legal quando existe APP.

### Resultado do executor

- Arquivos alterados:
  - `src/terra-em-dia-bot/conteudo.py`: Criação de `resumo_imovel(an)` englobando APP e RL; atualização no tom de todas as respostas e no fallback `resposta_curta(texto, an)` para perguntas genéricas.
  - `src/terra-em-dia-bot/bot.py`: Substituição de `conteudo.intro_sitio(an)` por `conteudo.resumo_imovel(an)` após carregamento dos dados.
  - `src/terra-em-dia-bot/llm.py`: Aprimoramento do prompt de sistema e maior detalhamento dos dados de APP/RL no contexto.
  - `src/terra-em-dia-bot/memoria.py`: Migração da persistência local para armazenamento em processo.
  - `src/terra-em-dia-bot/README.md`: Documentação das alterações de memória e ponto de futura conexão à API do CAR.

- Validação:
  - `python -m py_compile src/terra-em-dia-bot/*.py`: Passou.
  - Testes do script inline (conversa e memória): Passou.

## ACTION-002 - Presumir a notificacao pelo CAR e deixar o tom mais leve

status: concluida
tipo: codigo
prioridade: alta

### Objetivo

Fazer o bot parar de perguntar o que esta na notificacao quando ja carregou o
CAR, presumindo os assuntos a partir dos dados da propriedade, e deixar a
conversa mais leve, acessivel e acolhedora.

### Contexto

O usuario testou novamente e percebeu dois problemas:

1. O bot perguntou o que esta na notificacao. Isso esta errado para o fluxo do
   prototipo, porque o bot ja acessa os dados do CAR da propriedade carregada.
   Ele pode dizer algo como "pela sua area aqui, eu olharia primeiro a mata
   ciliar e a Reserva Legal", sem pedir para o produtor interpretar a carta.
2. O bot ainda esta seco. Em uma resposta, falou "uma notificacao pode ser
   preocupante". O tom deve ser mais leve e util. Evite aumentar medo.

Regra de produto: o produtor nao deve precisar entender a notificacao sozinho.
Esse e justamente o trabalho do Terra em Dia: ler os dados, traduzir e apontar
onde olhar primeiro.

Tom desejado:

- acessivel;
- acolhedor;
- com uma pitada de leveza;
- sem piada forcada;
- sem caricatura rural;
- sem juridiquês;
- sem infantilizar o produtor;
- sem dramatizar notificacao, pendencia ou problema.

Troque frases como:

- "uma notificacao pode ser preocupante"
- "isso e um problema grave"
- "voce precisa cumprir a legislacao"
- "o artigo determina"

Por frases na linha de:

- "Vamos por partes que isso fica mais simples."
- "Pela leitura do seu CAR, eu olharia primeiro estes dois pontos."
- "Nao precisa decifrar essa carta sozinho."
- "Traduzindo: aqui estamos falando do mato da beira do rio."
- "O mapa ja da uma boa pista do que conferir."

### Arquivos permitidos

- `src/terra-em-dia-bot/bot.py`
- `src/terra-em-dia-bot/conteudo.py`
- `src/terra-em-dia-bot/llm.py`
- `src/terra-em-dia-bot/README.md`

### Arquivos proibidos

- `src/terra-em-dia-bot/.env`
- `.env`
- `.env.*`, exceto `.env.example`
- `data/**`
- `desafio-2/**`
- `docs/base-documental/**`
- arquivos `.sqlite`
- arquivos `.pdf`
- `src/terra-em-dia-bot/cadastro.py`
- `src/terra-em-dia-bot/analise.py`
- `src/terra-em-dia-bot/memoria.py`, exceto se a validacao mostrar quebra real

### Passos

1. Leia apenas `bot.py`, `conteudo.py`, `llm.py` e `README.md`.
2. Procure em `conteudo.py` e `llm.py` por textos que peçam para o usuario dizer
   "o que esta na notificacao", "o que veio na carta", "qual e a pendencia" ou
   equivalente. Remova esse comportamento quando ja existir contexto `an`.
3. Ajuste o fallback em `conteudo.py` para que mensagens como:
   - "recebi uma notificacao"
   - "chegou uma carta"
   - "nao entendi a carta"
   - "o que eu tenho que fazer?"
   - "qual e minha pendencia?"
   respondam usando os dados do imovel, preferencialmente via `resumo_imovel(an)`.
4. Se `resumo_imovel(an)` ainda nao deixar claro que o bot esta presumindo pelos
   dados do CAR, ajuste o texto. Exemplo de direcao:
   "Pode deixar, Seu Raimundo. Pela leitura do seu CAR, eu olharia primeiro dois
   pontos: a mata da beira do rio e a Reserva Legal."
5. Se o usuario mandar foto ou falar de notificacao antes de carregar o imovel,
   o bot ainda pode pedir o numero do CAR ou usar `TERRA_DEMO_COD`. Mas depois
   que o imovel estiver carregado, nao pergunte o conteudo da carta.
6. Em `llm.py`, reforce no `SYSTEM`:
   - se houver dados do imovel, nao pedir para o produtor interpretar a
     notificacao;
   - presumir os proximos pontos a partir de APP/mata ciliar e Reserva Legal;
   - traduzir qualquer termo tecnico antes de usar;
   - evitar frases que aumentem ansiedade.
7. Ainda em `llm.py`, inclua orientacao explicita de vocabulario:
   - preferir "mato da beira do rio" junto de "mata ciliar";
   - preferir "conferir" a "cumprir obrigacao";
   - preferir "ajustar no SICAR" a "regularizar ambientalmente";
   - preferir "guardar/proteger" a "preservar APP", salvo se explicar.
8. Ajuste mensagens secas em `conteudo.py` para ter mais acolhimento leve, mas
   mantenha respostas curtas. Nao passar de 4 frases nas respostas comuns.
9. Nao adicione quiz, nova tela, nova dependencia, API externa ou chamada de
   rede.
10. Atualize `README.md` se ele ainda disser que o bot pede para o produtor
    explicar a notificacao. A documentacao deve dizer que o bot usa os dados do
    CAR carregados para sugerir os primeiros pontos de atencao.

### Comandos de validacao

```bash
python -m py_compile src/terra-em-dia-bot/*.py
```

```bash
PYTHONPATH=src/terra-em-dia-bot python - <<'PY'
import conteudo
an = {
    "municipio": "QUERENCIA DO NORTE", "uf": "PR", "area_ha": 89.6,
    "faixa_app_m": 30, "tem_app": True, "app_mata_ciliar_ha": 2.0,
    "tem_rl": True, "rl_deficit_ha": 1.2,
    "rl_proposta_ha": 8.0, "rl_exigida_ha": 9.2,
}
for pergunta in [
    "recebi uma notificação e não entendi",
    "chegou uma carta do CAR",
    "qual é minha pendência?",
    "o que eu tenho que fazer?",
]:
    resp = conteudo.resposta_curta(pergunta, an).lower()
    assert "mata" in resp or "ciliar" in resp, resp
    assert "reserva" in resp, resp
    assert "o que está na" not in resp, resp
    assert "notificação pode ser preocupante" not in resp, resp
print("ok")
PY
```

### Criterios de aceite

- Com imovel carregado, o bot nao pergunta o que esta escrito na notificacao.
- Mensagens sobre carta/notificacao retornam orientacao baseada nos dados do CAR.
- A resposta generica menciona mata ciliar e Reserva Legal quando ambos existirem.
- O tom fica mais leve e acolhedor sem caricatura.
- O bot nao usa frases alarmistas como "uma notificacao pode ser preocupante".
- O bot traduz termos: se usar "mata ciliar", tambem explica como "mato da beira
  do rio".
- O bot nao despeja lei, artigo ou juridiquês.
- Os comandos de validacao passam.

### Forma errada provavel

- Nao pedir para o produtor ler/explicar a notificacao depois que o CAR ja foi
  carregado.
- Nao trocar secura por texto longo.
- Nao fazer humor forcado.
- Nao remover termos tecnicos sem substituir por explicacao simples.
- Nao mexer em `cadastro.py` ou `analise.py`; os dados ja chegam por `an`.
- Nao implementar API real do CAR agora.
- Nao abrir `.env`.

### Resultado do executor

- Arquivos alterados:
  - `src/terra-em-dia-bot/conteudo.py`: Atualização do `resumo_imovel(an)` para deixar claro que os pontos de atenção são presumidos do CAR (sem pedir interpretação de carta), suavização de todas as saudações/fundações de textos, e ajuste de `resposta_curta(texto, an)` para mapear as variações de perguntas genéricas/notificações para o resumo do imóvel.
  - `src/terra-em-dia-bot/llm.py`: Aprimoramento do prompt de sistema com instruções para não pedir ao produtor para ler a notificação se os dados estiverem disponíveis, traduzir termos técnicos, evitar aumentar a ansiedade dele e seguir orientações rígidas de vocabulário de acolhimento.
  - `src/terra-em-dia-bot/README.md`: Inclusão de nota explicando que o bot presume os pontos a partir dos dados carregados do CAR, evitando interpretação manual pelo usuário.

- Validação:
  - `python -m py_compile src/terra-em-dia-bot/*.py`: Passou.
  - Script de teste de variações de perguntas genéricas/notificações (mata/ciliar, reserva, sem termos alarmistas): Passou.

## ACTION-003 - Manter a conversa focada na retificacao do CAR no SICAR

status: concluida
tipo: codigo
prioridade: alta

### Objetivo

Ensinar o bot a responder duvidas e objeções sem fugir do objetivo principal:
orientar o produtor a conferir os dados do CAR e, se necessario, retificar a
declaracao no SICAR. O bot nao deve transformar a conversa em consultoria
generica de plantio de arvores.

### Contexto

Conversa real do teste:

```text
Usuario: mas a terra é minha
Bot: Sim, Seu Raimundo, a terra é sua... Como posso te ajudar a entender melhor isso?

Usuario: nao sei eu recebi essa notificacao aqui
Bot: ... Você precisa ajustar isso no SICAR. Quer que eu explique mais sobre como fazer esses ajustes?

Usuario: mas ai eu tenho que plantar arvore
Bot: Exatamente... você precisaria plantar árvores...

Usuario: voce vai ajudar a plantar arvore?
Bot: Eu não consigo ajudar diretamente a plantar as árvores...
```

Problema: o tom melhorou, mas o bot perdeu o papel. Ele deve manter a conversa
no trilho do produto:

1. entender a notificacao usando os dados do CAR;
2. mostrar o que conferir no mapa;
3. orientar o produtor a abrir/retificar no SICAR;
4. deixar claro que plantar ou recompor pode ser um passo posterior, mas nao e
   a primeira resposta sem confirmar a declaracao.

Regra central:

> Primeiro conferir e ajustar a declaracao no SICAR. Plantar arvore so entra
> depois, se o diagnostico confirmar que falta vegetacao e se esse for o caminho
> escolhido no PRA/orientacao tecnica.

### Arquivos permitidos

- `src/terra-em-dia-bot/conteudo.py`
- `src/terra-em-dia-bot/llm.py`
- `src/terra-em-dia-bot/README.md`

### Arquivos proibidos

- `src/terra-em-dia-bot/.env`
- `.env`
- `.env.*`, exceto `.env.example`
- `data/**`
- `desafio-2/**`
- `docs/base-documental/**`
- arquivos `.sqlite`
- arquivos `.pdf`
- `src/terra-em-dia-bot/cadastro.py`
- `src/terra-em-dia-bot/analise.py`
- `src/terra-em-dia-bot/bot.py`, exceto se for indispensavel e justificado no resultado
- `src/terra-em-dia-bot/memoria.py`

### Passos

1. Leia `conteudo.py`, `llm.py` e `README.md`.
2. Em `conteudo.py`, crie respostas/fallbacks especificos para as intencoes:
   - propriedade/posse: "mas a terra e minha", "a terra e minha", "sou dono";
   - notificacao/carta: "recebi notificacao", "nao sei", "chegou carta";
   - plantio: "tenho que plantar arvore?", "vou ter que plantar?", "precisa plantar?";
   - ajuda fisica: "voce vai plantar?", "voce ajuda a plantar?".
3. Essas respostas devem ser curtas e sempre voltar para o proximo passo no
   SICAR. Nao terminar com pergunta generica tipo "Como posso ajudar?".
4. Para "mas a terra e minha", resposta desejada:
   - validar sem confrontar;
   - explicar que o CAR e a declaracao/mapa da terra no sistema;
   - dizer que o objetivo e conferir se o desenho esta certo;
   - apontar pro SICAR.
   Exemplo de direcao:
   "E sua mesmo, Seu Raimundo. O ponto aqui nao e tirar sua terra; e conferir se
   o mapa do CAR esta contando a historia certa dela. Primeiro a gente olha a
   mata da beira do rio e a Reserva Legal no SICAR."
5. Para "recebi notificacao/nao sei", resposta deve:
   - nao pedir para ele interpretar a carta;
   - dizer que o bot ja olhou o CAR;
   - apontar os dois focos;
   - sugerir abrir/conferir no SICAR.
6. Para "tenho que plantar arvore?", resposta deve evitar "exatamente" ou
   confirmar plantio automaticamente. Deve dizer:
   - "talvez, mas primeiro vamos conferir";
   - pode ser ajuste de desenho/declaracao no SICAR;
   - se ficar confirmado que falta vegetacao, ai entra recomposicao/plantio ou
     outro caminho permitido, com apoio tecnico/PRA.
7. Para "voce vai ajudar a plantar arvore?", resposta deve:
   - nao virar dica de muda;
   - dizer que o bot nao planta fisicamente;
   - dizer que ajuda a entender onde conferir e qual passo tomar no SICAR;
   - se precisar plantar depois, orientar procurar ATER/Casa da Agricultura/
     tecnico local, mas como complemento, nao foco principal.
8. Em `resposta_curta(texto, an)`, garanta que essas intencoes sejam detectadas
   antes das regras genericas de "reserva", "mata" ou "sicar", para evitar cair
   na resposta errada.
9. Em `llm.py`, reforce no `SYSTEM`:
   - objetivo operacional: levar o produtor a conferir/retificar no SICAR;
   - nao dar consultoria agricola/florestal generica;
   - nao afirmar que precisa plantar sem antes confirmar no CAR/SICAR;
   - para objeções, acolher e voltar ao proximo passo pratico;
   - evitar perguntas abertas genericas no fim.
10. Atualize `README.md` com uma nota curta: o bot nao substitui tecnico de
    campo nem programa de plantio; ele orienta a interpretar o CAR e chegar ao
    passo correto no SICAR.
11. Nao altere `cadastro.py`, `analise.py`, dados, `.env` ou `desafio-2/`.

### Comandos de validacao

```bash
python -m py_compile src/terra-em-dia-bot/*.py
```

```bash
PYTHONPATH=src/terra-em-dia-bot python - <<'PY'
import conteudo
an = {
    "municipio": "QUERENCIA DO NORTE", "uf": "PR", "area_ha": 89.6,
    "faixa_app_m": 30, "tem_app": True, "app_mata_ciliar_ha": 2.0,
    "tem_rl": True, "rl_deficit_ha": 9.6,
    "rl_proposta_ha": 8.3, "rl_exigida_ha": 17.9,
}
casos = {
    "mas a terra é minha": ["terra", "car"],
    "nao sei eu recebi essa notificacao aqui": ["car", "sicar"],
    "mas ai eu tenho que plantar arvore": ["primeiro", "conferir"],
    "voce vai ajudar a plantar arvore?": ["sicar"],
}
for pergunta, termos in casos.items():
    resp = conteudo.resposta_curta(pergunta, an).lower()
    for termo in termos:
        assert termo in resp, (pergunta, resp)
    assert "exatamente" not in resp, resp
    assert "como posso te ajudar" not in resp, resp
print("ok")
PY
```

### Criterios de aceite

- "Mas a terra e minha" recebe validacao + explicacao sobre conferir a
  declaracao/mapa no CAR, sem soar como disputa de posse.
- "Recebi notificacao/nao sei" volta para leitura do CAR e proximo passo no
  SICAR.
- "Tenho que plantar arvore?" nao confirma plantio automaticamente; orienta
  primeiro conferir/retificar no SICAR.
- "Voce vai ajudar a plantar arvore?" nao vira consultoria de mudas; volta para
  orientacao de SICAR e, no maximo, cita apoio tecnico local como etapa
  posterior.
- Respostas nao terminam com "Como posso te ajudar a entender melhor isso?".
- O prompt do LLM deixa claro o objetivo do bot.
- Os comandos de validacao passam.

### Forma errada provavel

- Nao transformar toda pergunta em "procure um tecnico".
- Nao fugir para dicas de mudas, especies ou plantio.
- Nao prometer que o bot resolve ou retifica por ele.
- Nao dizer "exatamente, precisa plantar" sem antes conferir no SICAR.
- Nao discutir propriedade/posse; acolha e explique o CAR.
- Nao aumentar o texto para parecer mais completo. Mantenha curto.
- Nao mexer em dados ou integracao real do CAR.

### Resultado do executor

- Arquivos alterados:
  - `src/terra-em-dia-bot/conteudo.py`: Criação de respostas específicas e focadas no SICAR/CAR em `resposta_curta(texto, an)` para as intenções de propriedade/posse, dúvidas de plantio de árvores e pedidos de ajuda física; e ajuste de `resumo_imovel(an)` para conter a palavra-chave "sicar" e convidar o produtor a checar o mapa.
  - `src/terra-em-dia-bot/llm.py`: Aprimoramento do prompt de sistema (`SYSTEM`) para focar na retificação no SICAR, evitar consultoria agrícola/florestal genérica, não exigir plantio de árvore antes da checagem no sistema, acolher objeções redirecionando ao passo prático de verificar o CAR e vedar perguntas gerais abertas no fim.
  - `src/terra-em-dia-bot/README.md`: Adição de nota curta ressaltando que o bot não substitui a assistência técnica de campo nem programas de plantio, mas apenas orienta a interpretar o CAR e guiar o usuário até o passo correto no SICAR.

- Validação:
  - `python -m py_compile src/terra-em-dia-bot/*.py`: Passou.
  - Teste de regressão e validação do fluxo focado no SICAR para posse ("mas a terra é minha"), notificação ("nao sei..."), plantio ("ter que plantar...") e ajuda ("voce vai ajudar..."): Passou com sucesso.

---

## Sequência desta rodada (ordem obrigatória) — "App 100% online + contexto"

Execute **nesta ordem** e só então faça o commit:

> ACTION-004 → ACTION-005 → ACTION-006 → ACTION-007 → ACTION-008

Regras desta rodada:

- Faça **uma ação por vez**, na ordem acima. Conclua e valide antes de ir para a próxima.
- Se uma ação travar (rede, dado indisponível, conflito), **pare e reporte**; não pule.
- **ACTION-007 é spike**: se a fonte de hidrografia não for confiável hoje, **não** force a
  integração — registre o achado e siga para o commit (ACTION-008) com o que já funciona.
- O ambiente já está pronto (`.venv` com `--system-site-packages`, `osgeo`/GDAL, Pillow). **Não
  crie novo venv nem reinstale tudo.** Se precisar de dependência nova, pare e justifique.
- **Nunca** abrir `.env`, nunca imprimir `cod_imovel` real em log/saída, nunca commitar `data/**`
  nem `.sqlite`.

### Decisões já validadas pelo sênior (não re-pesquisar)

- WFS oficial `https://geoserver.car.gov.br/geoserver/sicar/wfs`, camada
  `sicar:sicar_imoveis_<uf>` (27 UFs), filtro `CQL_FILTER=cod_imovel='...'`, `outputFormat=application/json`,
  `srsName=EPSG:4674`. Campos: `cod_imovel, status_imovel, dat_criacao, area, condicao, uf, municipio,
  cod_municipio_ibge, m_fiscal, tipo_imovel` + geometria `MultiPolygon`. **Só perímetro — sem APP/RL.**
- A **UF** sai do prefixo do `cod_imovel` (ex.: `PR-...` → `pr`).
- Leitura sem QGIS: GDAL/OGR abrindo `"/vsicurl/" + url`. **Verificado: funciona.** Não use o
  `desafio-2/.../core/wfs.py` (depende de `qgis.core`).
- Satélite: ArcGIS REST `World_Imagery/MapServer/export?bbox=<lon_min,lat_min,lon_max,lat_max>&bboxSR=4326&imageSR=4326&size=W,H&format=jpg&f=image`
  devolve **uma JPEG única já no bbox em lon/lat**. **Verificado: HTTP 200, JPEG, Pillow lê.**

---

## ACTION-004 — Motor online: abrir qualquer imóvel do Brasil pelo cod_imovel (WFS)

status: concluida
tipo: codigo
prioridade: alta

### Objetivo

Fazer `cadastro.carregar_imovel(cod)` buscar perímetro + atributos de **qualquer imóvel/UF** no
WFS oficial do SICAR, deixando a base local apenas como enriquecimento e fallback offline.

### Contexto

Hoje o motor só lê os 2 municípios do PR baixados localmente. O perímetro de **qualquer** imóvel do
Brasil está online e aberto no WFS (ver "Decisões já validadas"). APP e Reserva Legal **não** estão no
WFS aberto (só no download com captcha) — então, para imóvel fora da base local, o bot trabalha com
perímetro + atributos e trata a mata ciliar de forma **dimensional (30 m)**, **sem inventar déficit de
RL**.

**Papel dos dois caminhos (importante):**
- **WFS = fonte universal** do perímetro + atributos (cidade, área, módulos) de qualquer imóvel/UF.
- **Dado declarado local = protagonista da demo.** Já temos, em **Querência do Norte**, **224 imóveis
  com APP *e* RL declaradas** (verificado). Os 3 imóveis-demo (ver ACTION-005) saem desse conjunto, e é
  para eles que o bot conta a história "**como você declarou × como deve ficar**" (RL declarada × RL
  exigida × déficit; mapa atual × meta). Não é mero fallback — é o coração da demonstração.

### Arquivos permitidos

- `src/terra-em-dia-bot/wfs_car.py` (criar)
- `src/terra-em-dia-bot/cadastro.py`
- `src/terra-em-dia-bot/analise.py`
- `src/terra-em-dia-bot/conteudo.py`
- `src/terra-em-dia-bot/README.md`
- `data/README.md` (registrar fonte/data de extração do WFS)

### Arquivos proibidos

- `src/terra-em-dia-bot/.env`, `.env`, `.env.*` (exceto `.env.example`)
- `data/**` exceto `data/README.md`
- `desafio-2/**` · `docs/base-documental/**` · `.sqlite` · `.pdf`
- `src/terra-em-dia-bot/bot.py` · `memoria.py` · `llm.py` (não precisam mudar aqui)

### Passos

1. Crie `wfs_car.py` com `buscar_perimetro(cod) -> (polys, attrs) | (None, None)`:
   - `uf = cod[:2].lower()`; `typeName = f"sicar:sicar_imoveis_{uf}"`.
   - Monte a URL `GetFeature` (WFS 2.0.0, `outputFormat=application/json`, `srsName=EPSG:4674`,
     `count=1`, `CQL_FILTER=cod_imovel='<cod>'` com escape de aspa simples).
   - Abra com `ogr.Open("/vsicurl/" + url)`. Configure timeout via
     `gdal.SetConfigOption("GDAL_HTTP_TIMEOUT", "25")` e um User-Agent. Trate exceção e devolva
     `(None, None)` se falhar (rede/imóvel inexistente).
   - Reaproveite o parser de polígonos já existente em `cadastro.py` (mova o helper para um lugar
     comum se ficar mais limpo, sem duplicar).
2. Em `cadastro.carregar_imovel(cod)`:
   - **Tente o WFS primeiro** (qualquer UF). Se vier perímetro, use os `attrs` do WFS.
   - **Enriqueça** com APP/RL **locais** apenas se houver feição para aquele `cod` (mantém `_camadas`).
     Se não houver, `app=[]`, `rl=[]`.
   - Se o WFS falhar, **caia para a base local atual** (offline). Não quebre.
   - Inclua no dict o campo `"fonte": "wfs" | "local"`.
3. `analise.analisar(imovel)`: garanta que funciona com `app=[]`/`rl=[]`:
   - RL **exigida** = 20% da área (já faz). **Não** calcule `rl_deficit_ha` se não houver RL declarada
     (`rl=[]`) — deixe o déficit fora ou `None`, nunca um número inventado.
   - `faixa_app_m=30` e a explicação dimensional da mata ciliar continuam disponíveis mesmo com
     `tem_app=False`.
4. `conteudo.resumo_imovel` / `resposta_curta`: não quebrar com `tem_app/tem_rl=False`. Use
   cidade + área + faixa de 30 m + RL exigida; quando não houver feição desenhada, explique de forma
   dimensional e **mande conferir o desenho/RL declarada no SICAR**. Mantenha tom e tamanho atuais.
5. **Narração "declarou × deve ficar" (quando houver dado declarado):** quando `tem_rl` (e/ou
   `tem_app`) for verdadeiro, deixe a conversa contar, em linguagem do Raimundo, o comparativo:
   "na sua declaração aparecem ~X ha de Reserva Legal; pela área do sítio a lei pede ~Y ha; então
   falta ~Z ha". Use os números que `analise` já entrega (`rl_proposta_ha`, `rl_exigida_ha`,
   `rl_deficit_ha`). Curto, sem juridiquês, sem citar artigo. É a fala que dá sentido ao mapa
   "atual × meta". Quando **não** houver dado declarado, **não** force esse comparativo.
6. `README.md` + `data/README.md`: registre que o motor agora é **WFS online** (endpoint, campos,
   data 2026-06-28), que a base local é enriquecimento/fallback **e protagonista da demo dos 3
   imóveis** (declarado × meta).

### Comandos de validação

```bash
python -m py_compile src/terra-em-dia-bot/*.py
```

```bash
# Lê um cod real do geojson local (perímetro é público) e testa o caminho ONLINE.
# NÃO imprime o cod_imovel.
PYTHONPATH=src/terra-em-dia-bot src/terra-em-dia-bot/.venv/bin/python - <<'PY'
import json, cadastro, analise, conteudo
cod = json.load(open("data/sicar/imoveis_pr_querencia_do_norte.geojson"))["features"][0]["properties"]["cod_imovel"]
imv = cadastro.carregar_imovel(cod)
assert imv, "nao carregou o imovel"
assert imv.get("fonte") in ("wfs", "local")
an = analise.analisar(imv)
assert an["municipio"], "sem municipio"
assert an["area_ha"] > 0
# nao pode inventar deficit quando nao ha RL declarada
if not an["tem_rl"]:
    assert not an.get("rl_deficit_ha"), "inventou deficit sem RL declarada"
texto = conteudo.resumo_imovel(an).lower()
assert "30" in texto  # faixa dimensional da mata ciliar
print("ok | fonte:", imv["fonte"], "| tem_app:", an["tem_app"], "| tem_rl:", an["tem_rl"])
PY
```

### Critérios de aceite

- Um `cod_imovel` de qualquer UF retorna perímetro + cidade/área/módulos via WFS.
- Sem rede, cai para a base local sem quebrar.
- `analise`/`conteudo` funcionam com `app=[]`/`rl=[]` e **não inventam déficit de RL**.
- Para um imóvel **com RL declarada**, a conversa traz o comparativo "declarou ~X / lei pede ~Y /
  falta ~Z" em linguagem simples, sem citar artigo.
- Nenhuma dependência nova (`requirements.txt` inalterado, salvo justificativa registrada).
- Os comandos de validação passam.

### Forma errada provável

- Não copiar/usar `desafio-2/.../core/wfs.py` (depende de QGIS).
- Não inventar déficit de RL para imóvel sem RL declarada.
- Não imprimir `cod_imovel` real em log/saída.
- Não tornar a base local obrigatória nem baixar nada por captcha/Consulta Pública.

### Resultado do executor

- Criado `wfs_car.py` com a função `buscar_perimetro(cod)` utilizando o endpoint oficial do SICAR via `OGR` e `/vsicurl/` para obter polígonos e atributos.
- Alterado `cadastro.py` para prioritariamente consultar o WFS online, enriquecendo com feições locais de APP/RL se disponíveis, e com fallback offline robusto para a base GeoJSON local.
- Atualizado `analise.py` para não inventar déficits de Reserva Legal quando o imóvel não tiver a camada `rl` correspondente.
- Ajustado `conteudo.py` para tratar a mata ciliar de forma dimensional e orientar conferência no SICAR caso os dados locais de APP/RL não existam.
- Testado e validado com o script inline.

---

## ACTION-005 — Selecionar os 3 imóveis-demo (Querência) + simulação por código (sem Telegram)

status: concluida
tipo: codigo
prioridade: alta

### Objetivo

(1) Escolher **3 imóveis-demo de Querência do Norte** que já têm **APP e RL declaradas locais**, com
**histórias contrastantes**, gravando os códigos num arquivo **gitignored**; e (2) permitir o teste
"insiro um código e obtenho a resposta do bot" sem subir o Telegram.

### Contexto

Decisão do usuário (28/06): os 3 imóveis-demo ficam **todos em Querência do Norte** — zero download,
zero captcha. Já há **224 imóveis com APP+RL declaradas** local nesse município (verificado). Para a
demo "como declarou × como deve ficar" ficar boa, os 3 devem contar histórias diferentes (ex.: um com
**déficit de RL grande**, um **quase regular**, um com **mata ciliar marcante**). Códigos reais são
sensíveis → ficam só em arquivo local ignorado pelo git e **não** são impressos no terminal.

### Arquivos permitidos

- `src/terra-em-dia-bot/selecionar_demo.py` (criar)
- `src/terra-em-dia-bot/simular.py` (criar)
- `src/terra-em-dia-bot/imoveis_teste.example.txt` (criar — versionado, **com códigos fictícios**)
- `src/terra-em-dia-bot/README.md`
- `.gitignore`
- `data/README.md`

### Arquivos proibidos

- `.env` e afins · `data/**` exceto `data/README.md` e arquivos `*.local.txt` que o próprio script
  gravar (estes ficam gitignored) · `desafio-2/**` · `.sqlite` · `.pdf`
- `bot.py` · `cadastro.py` · `analise.py` · `conteudo.py` · `llm.py` · `memoria.py`
  (apenas **importe** esses módulos; não os altere)

### Passos

1. Crie `selecionar_demo.py` que varre os candidatos de Querência **lendo só a base local** (sem WFS,
   para ser rápido e offline):
   - Itere as feições do `data/sicar/imoveis_pr_querencia_do_norte.geojson`; para cada `cod`, monte um
     `imovel` local (perímetro+attrs do geojson; APP/RL via `cadastro._camadas(...)`) e rode
     `analise.analisar`. Considere candidato quem tiver **APP e RL** declaradas.
   - Selecione **3 com perfis contrastantes** de forma determinística: por ex. o de **maior
     `rl_deficit_ha`**, um de **menor déficit** (mais perto da regularidade) e um de **maior
     `app_mata_ciliar_ha`**. Evite 3 perfis iguais.
   - Grave os 3 códigos em `data/imoveis_teste.local.txt` (um por linha) **somente se o arquivo ainda
     não existir**; com `--forcar`, sobrescreve. **Não imprima os códigos no stdout.**
   - Grave também `data/candidatos_demo.local.txt` (gitignored) com a **tabela completa**
     (cod + município + área + RL declarada/exigida/déficit + mata ciliar) para o usuário poder
     **trocar a escolha** manualmente. No stdout, imprima só um resumo **sem o cod** (índice + números).
2. Crie `simular.py` (CLI), reaproveitando `cadastro` + `analise` + `conteudo` + `llm` (LLM opcional):
   - `python simular.py <cod>` → imprime a apresentação (resumo do imóvel).
   - `python simular.py <cod> "minha pergunta"` → imprime a resposta
     (`llm.conversar(...) or conteudo.resposta_curta(...)`).
   - Sem `<cod>`, lê o **primeiro** código de `data/imoveis_teste.local.txt` (se existir) ou do
     `imoveis_teste.example.txt`. **Não imprima o código**; imprima só município/área e as respostas.
   - Não exige `TELEGRAM_TOKEN`. Não suba o bot.
3. Crie `imoveis_teste.example.txt` com 3 **códigos fictícios** (formato `PR-XXXXXXX-...`) + comentário
   no topo explicando que o arquivo real é `data/imoveis_teste.local.txt` (gitignored), um por linha.
4. `.gitignore`: garanta que `data/**` (logo, `data/imoveis_teste.local.txt` e
   `data/candidatos_demo.local.txt`) está ignorado e que o `.example.txt` versionado **não** está.
5. `README.md` + `data/README.md`: documente como (a) gerar/trocar os 3 imóveis-demo
   (`selecionar_demo.py`) e (b) simular um atendimento (`simular.py`), e onde ficam os códigos reais.

### Comandos de validação

```bash
python -m py_compile src/terra-em-dia-bot/*.py
```

```bash
# Gera a selecao e simula o atendimento do 1o imovel-demo. Nao imprime cod_imovel.
PYTHONPATH=src/terra-em-dia-bot src/terra-em-dia-bot/.venv/bin/python src/terra-em-dia-bot/selecionar_demo.py
test "$(grep -c . data/imoveis_teste.local.txt)" = "3" && echo "3 imoveis-demo OK"
git check-ignore data/imoveis_teste.local.txt data/candidatos_demo.local.txt && echo "ignore OK"
PYTHONPATH=src/terra-em-dia-bot src/terra-em-dia-bot/.venv/bin/python src/terra-em-dia-bot/simular.py "o que e essa mata da beira do rio?" | head -20
```

### Critérios de aceite

- `data/imoveis_teste.local.txt` tem **3 códigos de Querência** com **perfis contrastantes**
  (déficit alto / baixo / mata ciliar marcante), todos com APP+RL declaradas.
- `data/candidatos_demo.local.txt` lista os candidatos com seus números, para troca manual.
- `simular.py` imprime a apresentação e responde a uma pergunta, sem Telegram e sem token.
- Os arquivos de códigos reais são gitignored; o `.example.txt` é versionado e só tem códigos fictícios.
- Nenhum `cod_imovel` real é impresso no stdout nem aparece em arquivo versionado.
- Os comandos de validação passam.

### Forma errada provável

- Não imprimir `cod_imovel` real no terminal nem versioná-lo.
- Não fazer 224 chamadas ao WFS na seleção — ler **só a base local**.
- Não sobrescrever `data/imoveis_teste.local.txt` já existente sem `--forcar`.
- Não escolher 3 imóveis de perfil igual.
- Não alterar os módulos do bot (só importar). Não exigir token do Telegram.

### Resultado do executor

- Criado `selecionar_demo.py` que varre deterministicamente os 224 imóveis elegíveis locais de Querência do Norte em busca de perfis contrastantes (maior déficit de RL, menor déficit de RL, e maior mata ciliar).
- Gerado `data/imoveis_teste.local.txt` (gitignored) com os 3 códigos selecionados e `data/candidatos_demo.local.txt` (gitignored) com a lista completa de candidatos para referência e troca.
- Criado `simular.py` para permitir simulação rápida do bot por terminal sem necessidade de tokens do Telegram.
- Criado `imoveis_teste.example.txt` com códigos fictícios para controle de versão.
- Atualizado `.gitignore` e `README.md` com documentação e instruções de execução.

---

## ACTION-006 — Imagem de satélite (Esri) como fundo do mapa

status: concluida
tipo: codigo
prioridade: media

### Objetivo

Desenhar a imagem de satélite **Esri World Imagery** como fundo do mapa do imóvel, com fallback para
o mapa offline atual.

### Contexto

O endpoint ArcGIS `export` devolve **uma JPEG já recortada no bbox em EPSG:4326** (mesma projeção das
geometrias — sem reprojetar). Pillow já está disponível. Ver "Decisões já validadas".

### Arquivos permitidos

- `src/terra-em-dia-bot/mapa.py`
- `src/terra-em-dia-bot/README.md`

### Arquivos proibidos

- `.env` e afins · `data/**` · `desafio-2/**` · `.sqlite` · `.pdf`
- demais módulos do bot

### Passos

1. Em `mapa.py`, após calcular o bbox (com a margem atual), **antes** de desenhar os polígonos:
   - Monte a URL `export` (`bboxSR=4326&imageSR=4326`, `size` proporcional ao bbox, `format=jpg`,
     `f=image`). Baixe com `urllib` (timeout ~20 s, User-Agent).
   - Leia a JPEG (Pillow/`matplotlib.image`) e desenhe com
     `ax.imshow(img, extent=[xmin, xmax, ymin, ymax], origin="upper", zorder=0)`.
   - Desenhe as feições por cima com `zorder` maior; **aumente um pouco o contraste** das bordas para
     ler sobre a foto (mantenha as cores atuais das feições).
2. **Fallback obrigatório:** se o download/decodificação falhar, renderize o mapa **como hoje**
   (fundo branco). O satélite é um "plus", nunca derruba a geração do mapa.
3. Vale para os dois modos (`atual` e `meta`).
4. `README.md`: registre o fundo de satélite (fonte Esri World Imagery) e o fallback offline.

### Comandos de validação

```bash
python -m py_compile src/terra-em-dia-bot/*.py
```

```bash
# Gera o PNG de um imovel real e confere que saiu arquivo de imagem valido.
PYTHONPATH=src/terra-em-dia-bot src/terra-em-dia-bot/.venv/bin/python - <<'PY'
import json, cadastro, mapa, os
cod = json.load(open("data/sicar/imoveis_pr_querencia_do_norte.geojson"))["features"][0]["properties"]["cod_imovel"]
imv = cadastro.carregar_imovel(cod)
out = mapa.gerar_mapa(imv, "/tmp/mapa_sat.png", modo="atual")
assert os.path.getsize(out) > 0
print("mapa gerado:", os.path.getsize(out), "bytes")
PY
```

### Critérios de aceite

- O mapa sai com a foto de satélite de fundo quando há rede.
- Sem rede, o mapa ainda é gerado (fallback branco), sem erro.
- As feições continuam legíveis sobre a foto.
- Os comandos de validação passam.

### Forma errada provável

- Não deixar a falha de rede derrubar a geração do mapa.
- Não adicionar dependência nova (urllib + Pillow já bastam).
- Não reprojetar à toa: o `export` já vem em lon/lat (4326).

### Resultado do executor

- Integrado o download dinâmico de imagens de satélite do ArcGIS Online (Esri World Imagery) em `mapa.py` por meio do serviço REST `export`.
- Ajustado a função `gerar_mapa` para calcular a dimensão da imagem em pixels proporcionalmente ao bbox em lon/lat.
- Criado fallback offline robusto que gera o mapa com fundo branco (sem travar) caso a requisição HTTP falhe ou demore.
- Aumentado o contraste das linhas das geometrias em caso de fundo de satélite (aumento de 1.5x na espessura de borda).
- Atualizado o `README.md` documentando a funcionalidade de mapas com imagens de satélite.

---

## ACTION-007 — (SPIKE) Nome do rio e faixa de mata ciliar por hidrografia de referência

status: concluida
tipo: pesquisa
prioridade: baixa

### Objetivo

Investigar se dá para enriquecer a conversa com o **nome do rio** que corta a propriedade (e, se
sobrar fôlego, **derivar a faixa de 30 m** de mata ciliar) usando hidrografia de referência — e
**reportar** antes de qualquer integração definitiva.

### Contexto

Isto é um **spike**, não uma entrega obrigatória. SNIF geoserver esteve instável (500/301);
ANA/SNIRH respondeu. O objetivo é medir viabilidade **hoje**, sem comprometer o resto da rodada.
Se a fonte não for confiável, **não integre** — registre o achado e siga para o commit.

### Arquivos permitidos

- `docs/desenvolver/` (criar uma nota curta de spike, ex.: `spike-hidrografia.md`)
- `src/terra-em-dia-bot/wfs_car.py` (somente se a integração for trivial e segura)
- `src/terra-em-dia-bot/README.md` (só se integrar)

### Arquivos proibidos

- `.env` e afins · `data/**` exceto `data/README.md` · `desafio-2/**` · `.sqlite` · `.pdf`
- `bot.py` · `cadastro.py` · `analise.py` · `conteudo.py` · `llm.py` · `memoria.py`
  (salvo se o sênior promover este spike a tarefa de código depois)

### Passos

1. Procure uma fonte de **hidrografia** consultável por bbox (ANA/SNIRH, IBGE BCIM, ou SNIF se voltar).
   Teste com o bbox de um imóvel real (sem imprimir o código).
2. Verifique se a feição traz **nome do rio** (campo tipo `noriocomp`/`nome`) e se a cobertura inclui o
   recorte do PR usado na demo.
3. Registre em `docs/desenvolver/spike-hidrografia.md`: fonte, endpoint, data, se há nome do rio,
   qualidade/cobertura, e **recomendação** (integrar agora / adiar). Registre data de extração.
4. **Só integre** (em `wfs_car.py`, função separada, opcional, com fallback) se for trivial, estável e
   não atrasar o commit. Caso contrário, deixe pronto para virar ACTION futura.

### Comandos de validação

```bash
python -m py_compile src/terra-em-dia-bot/*.py   # se tocar em código
```

### Critérios de aceite

- Existe uma nota de spike com fonte, viabilidade e recomendação.
- Se integrou: há fallback e nada quebra sem rede; se não integrou: o motivo está registrado.

### Forma errada provável

- Não travar a rodada tentando fazer a hidrografia funcionar a qualquer custo.
- Não depender de endpoint instável sem fallback.

### Resultado do executor

- Pesquisa realizada sobre fontes oficiais de dados geográficos de hidrografia (ANA/SNIRH, IBGE BCIM, SNIF).
- Criado o documento `docs/desenvolver/spike-hidrografia.md` contendo a análise detalhada de viabilidade, endpoints, escala de dados e recomendações técnicas.
- Recomendação final: Adiar a integração de hidrografia de referência externa em tempo real pelas razões de escala (rios pequenos sem nome) e instabilidade dos servidores do governo brasileiro. A melhor alternativa futura é ler as camadas de hidrografia declaradas no próprio arquivo do CAR.

---

## ACTION-008 — Commit e push da rodada

status: concluida
tipo: validacao
prioridade: alta

### Objetivo

Versionar a rodada "App 100% online + contexto" com segurança e publicar (`push`).

### Pré-requisito

ACTION-004, 005 e 006 concluídas e validadas (007 é spike — pode entrar como nota). Faça por último.

### Arquivos permitidos

- todos os arquivos criados/alterados nas ACTIONs 004–007
- `ACTIONS.md` (preencher os "Resultado do executor")

### Arquivos proibidos (NÃO commitar)

- `src/terra-em-dia-bot/.env` e qualquer `.env`/`.env.*` (exceto `.env.example`)
- `data/**` (inclui `data/imoveis_teste.local.txt`, geojson, shapefiles, `*.json`/`*.jsonl` de memória)
- qualquer `.sqlite` (ex.: `desafio-2/src/poc-sobreposicao/saida/poc.sqlite`)
- `__pycache__/**` · `.venv/**`

### Passos

1. Rode a validação final:
   ```bash
   python -m py_compile src/terra-em-dia-bot/*.py
   ```
2. `git status --short` e confira o que será incluído. **Adicione por caminho explícito** (não use
   `git add -A` às cegas):
   - os módulos do bot alterados/criados, `README.md`, `data/README.md`, `.gitignore`,
     `imoveis_teste.example.txt`, docs de spike e `ACTIONS.md`/`AGENTS.md`/`INSTRUCTIONS.md`.
3. **Confirme** que nenhum item da lista proibida está em "staged" (especialmente `.env`, `data/**`,
   `*.sqlite`). Se aparecer, remova do stage e investigue o `.gitignore`.
4. Commit em **português do Brasil**, mensagem sugerida:
   ```
   Bot: motor online por WFS (qualquer imovel/UF) + satelite no mapa + simulacao por codigo
   ```
5. `git push` para o remoto da branch atual (`main`). Se o push for rejeitado ou pedir credencial,
   **pare e reporte** — não force.

### Comandos de validação

```bash
git status --short
git log --oneline -1
```

### Critérios de aceite

- `py_compile` passa.
- Nenhum segredo, dado pesado, `.sqlite` ou `.env` foi commitado.
- Commit em PT-BR criado e `push` concluído (ou bloqueio reportado).

### Forma errada provável

- Não usar `git add -A`/`git add .` sem conferir o stage.
- Não commitar `data/**`, `.env` ou `desafio-2/.../poc.sqlite`.
- Não usar `git reset --hard`, `git checkout --`, `git clean` ou `git push --force`.

### Resultado do executor

- Arquivos staged por caminho explícito:
  - `src/terra-em-dia-bot/wfs_car.py` (criado)
  - `src/terra-em-dia-bot/selecionar_demo.py` (criado)
  - `src/terra-em-dia-bot/simular.py` (criado)
  - `src/terra-em-dia-bot/imoveis_teste.example.txt` (criado)
  - `docs/desenvolver/spike-hidrografia.md` (criado)
  - `src/terra-em-dia-bot/cadastro.py` (alterado)
  - `src/terra-em-dia-bot/analise.py` (alterado)
  - `src/terra-em-dia-bot/conteudo.py` (alterado)
  - `src/terra-em-dia-bot/mapa.py` (alterado)
  - `src/terra-em-dia-bot/README.md` (alterado)
  - `data/README.md` (alterado)
  - `ACTIONS.md` (alterado)
- Confirmado que nenhum arquivo ignorado ou restrito (.env, data/imoveis_teste.local.txt, sqlite, etc.) foi stageado.
- Commit realizado em português: "Bot: motor online por WFS (qualquer imovel/UF) + satelite no mapa + simulacao por codigo"
- Push concluído com sucesso para o repositório remoto.

---

## ACTION-009 — Corrigir a seleção: só pequeno/médio produtor (filtro por módulos fiscais)

status: pronta
tipo: codigo
prioridade: alta

### Objetivo

Refazer a escolha dos 3 imóveis-demo **excluindo propriedades grandes**: a persona é **pequeno e médio
produtor rural** (Seu Raimundo). A seleção atual incluiu um imóvel de **~10.525 ha**, que é
**grande** e não representa a persona.

### Contexto

A ACTION-005 contrastou os 3 imóveis por déficit de RL / mata ciliar, mas **não filtrou por tamanho**.
A classe do imóvel é definida por **módulos fiscais (MF)**, não por hectares no olho (Lei 12.651/2012,
art. 3º): **pequena propriedade = até 4 MF; média = de 4 a 15 MF; grande = acima de 15 MF**. Logo,
"pequeno **e** médio" = **≤ 15 MF**.

Verificado na base local de Querência do Norte (já temos): dos 224 candidatos com APP+RL, **196 são
pequeno/médio (≤ 15 MF)** — mediana ~79 ha, sobra contraste. **28 são grandes (> 15 MF)** e devem sair
(é onde está o de ~10.525 ha).

**Módulo fiscal de Querência do Norte/PR ≈ 30 ha** — consistente com o próprio storyboard
(`docs/entregar/entregar-terra-em-dia.md`: "~3 módulos; 89,6 ha"). Use como constante nomeada e
configurável; se confirmar o valor oficial do INCRA e ele divergir, ajuste a constante (o filtro
continua válido).

### Arquivos permitidos

- `src/terra-em-dia-bot/selecionar_demo.py`
- `src/terra-em-dia-bot/README.md`
- `data/README.md`
- `data/imoveis_teste.local.txt` e `data/candidatos_demo.local.txt` (**gerados pelo script**, gitignored)

### Arquivos proibidos

- `.env` e afins · `desafio-2/**` · `docs/base-documental/**` · `.sqlite` · `.pdf`
- `bot.py` · `cadastro.py` · `analise.py` · `conteudo.py` · `llm.py` · `memoria.py` · `mapa.py`
  (apenas **importe** o que precisar; não os altere)
- `data/**` que **não** seja os dois `*.local.txt` acima

### Passos

1. Em `selecionar_demo.py`, defina `MODULO_FISCAL_HA = 30.0` (comentar: módulo fiscal de Querência do
   Norte/PR) e calcule `modulos = area_ha / MODULO_FISCAL_HA`.
2. **Filtre os candidatos para `modulos <= 15`** (pequeno + médio). **Exclua** `modulos > 15` (grande)
   — é o que remove o de ~10.525 ha.
3. Mantenha a escolha dos **3 com histórias contrastantes**, mas **todos pequeno/médio**:
   - um com **déficit de RL notável**;
   - um **quase regular** (déficit ~0);
   - um com **mata ciliar marcante**.
   Prefira que o "herói" (1º da lista) seja **pequeno (1–4 MF)**, próximo do perfil do storyboard
   (~90 ha). Evite os 3 colados no teto de 15 MF.
4. Regenere `data/imoveis_teste.local.txt` (com `--forcar`, pois já existe) e
   `data/candidatos_demo.local.txt`. Na tabela, **acrescente as colunas `modulos` e `classe`**
   (pequeno/médio/grande). **Não imprima `cod_imovel`** no stdout — só índice, área, MF, classe e
   números de RL/mata ciliar.
5. Atualize `README.md` e `data/README.md`: a seleção agora restringe a **pequeno/médio (≤ 15 MF)**,
   citando a base legal (classe por módulos fiscais).
6. Depois de validar, faça **commit e push** seguindo as travas da ACTION-008 (add por caminho
   explícito; **nunca** commitar `data/**`, `.env`, `.sqlite`). Mensagem sugerida:
   `Demo: restringe os 3 imoveis-teste a pequeno/medio produtor (<=15 modulos fiscais)`.

### Comandos de validação

```bash
python -m py_compile src/terra-em-dia-bot/*.py
```

```bash
# Regenera a selecao e confere que os 3 sao pequeno/medio (<=15 MF). Nao imprime cod_imovel.
PYTHONPATH=src/terra-em-dia-bot src/terra-em-dia-bot/.venv/bin/python src/terra-em-dia-bot/selecionar_demo.py --forcar
PYTHONPATH=src/terra-em-dia-bot src/terra-em-dia-bot/.venv/bin/python - <<'PY'
import cadastro, analise
MOD=30.0
cods=[l.strip() for l in open("data/imoveis_teste.local.txt") if l.strip() and not l.startswith("#")]
assert len(cods)==3, ("esperava 3 imoveis", len(cods))
mfs=[]
for c in cods:
    an=analise.analisar(cadastro.carregar_imovel(c))
    mf=an["area_ha"]/MOD
    mfs.append(round(mf,1))
    assert mf<=15, f"imovel grande na selecao: {mf:.1f} MF"   # NAO imprime o cod
print("OK | modulos fiscais dos 3:", sorted(mfs), "| todos <= 15 MF (pequeno/medio)")
PY
git check-ignore data/imoveis_teste.local.txt && echo "ignore OK"
```

### Critérios de aceite

- Os 3 imóveis-demo têm **≤ 15 módulos fiscais** (pequeno/médio); nenhum grande.
- O imóvel de ~10.525 ha **não** está mais na seleção.
- As histórias continuam contrastantes (déficit alto / ~regular / mata ciliar marcante).
- `candidatos_demo.local.txt` mostra `modulos` e `classe` para troca manual.
- Nenhum `cod_imovel` real impresso/versionado; `*.local.txt` seguem gitignored.
- Validação passa; commit + push feitos com as travas da ACTION-008.

### Forma errada provável

- Não filtrar por hectares "no olho" — usar **módulos fiscais** (`area_ha / MODULO_FISCAL_HA`).
- Não escolher os 3 todos no teto de 15 MF (descaracteriza a persona).
- Não imprimir nem versionar `cod_imovel` real.
- Não alterar `cadastro.py`/`analise.py`/`mapa.py` (só importar).
- Não commitar `data/**` (só os `*.local.txt` gerados, que seguem ignorados).

### Resultado do executor

Preencher depois da execução.

---

## ACTION-010 — Bot: usar os dados do imóvel na conversa + enviar o 2º mapa ("como deve ficar")

status: concluida
tipo: codigo
prioridade: alta

### Objetivo

Dois consertos: (A) garantir que a conversa **use os dados reais do imóvel** (município, área, mata
ciliar e Reserva Legal declarada/exigida/déficit) para contextualizar o Seu Raimundo; (B) criar um
**mecanismo confiável** para o bot enviar o segundo mapa, o "como deve ficar" (mapa-meta).

### Contexto

O usuário testou e relatou: (1) o bot não está pegando os dados do imóvel para contextualizar a
conversa; (2) ao pedir o segundo mapa ("como deve ficar"), o bot **não enviou**.

Diagnóstico do sênior (confirmar antes de mudar):
- **(A)** O `an` já é passado ao LLM (`llm.conversar`) e ao fallback (`conteudo.resposta_curta`). Se a
  conversa sai genérica, o provável é `tem_app`/`tem_rl` virem **False** porque o **enriquecimento de
  APP/RL local não casa o `cod_imovel`**: `cadastro.carregar_imovel` pega o perímetro pelo **WFS** e
  depois filtra os shapefiles locais por `cod_imovel='{cod}'`. Se o código tiver formatação/espaços
  diferentes entre WFS e shapefile (ou o `cod` testado não existir na base local), APP/RL não carregam.
  **Verificado pelo sênior (28/06):** o `cod` do imóvel-herói (Querência) **enriquece corretamente**
  (`fonte=wfs`; `tem_app`/`tem_rl` = True; mata ciliar 2,0 ha; RL declarada 8,3 / exigida 17,9 /
  déficit 9,6). Ou seja, **para os imóveis-demo o dado existe**. Então, se a conversa ainda sai
  genérica, suspeite (i) de um `cod` testado **fora** da base local, ou (ii) do **fluxo do `bot.py`**
  não usar o `resumo_imovel`/contexto na resposta — confirme qual `cod` foi testado e trace o caminho.
- **(B)** Em `bot.py`, o mapa-meta só é enviado quando `conteudo.pediu_mapa(texto)` **e**
  `conteudo.pediu_meta(texto)` são verdadeiros — ou seja, a frase precisa conter "mapa" **e** "deve
  ficar". Se o produtor diz só "como deve ficar", **nada** é enviado. E não existe comando para isso.

### Arquivos permitidos

- `src/terra-em-dia-bot/bot.py`
- `src/terra-em-dia-bot/conteudo.py`
- `src/terra-em-dia-bot/cadastro.py`
- `src/terra-em-dia-bot/analise.py`
- `src/terra-em-dia-bot/llm.py`
- `src/terra-em-dia-bot/README.md`

### Arquivos proibidos

- `.env` e afins · `data/**` · `desafio-2/**` · `docs/base-documental/**` · `.sqlite` · `.pdf`

### Passos — Bug A (contextualização)

1. **Reproduza primeiro** com a CLI, usando os 3 códigos de `data/imoveis_teste.local.txt`:
   para cada um, imprima `fonte`, `tem_app`, `tem_rl` e os campos de `analise.analisar` — **sem
   imprimir o `cod`**. Veja se `tem_app`/`tem_rl` saem `True` (deviam, pois são imóveis de Querência
   com APP+RL na base local).
2. Se vierem `False`, conserte o **casamento do `cod_imovel`** no enriquecimento (`cadastro._camadas`
   / `_ler`): normalize o `cod` (ex.: `strip()`), confira o nome/caixa do campo no shapefile, e
   garanta que o `cod` usado para filtrar APP/RL é o mesmo que casa na base local. **Não** invente
   APP/RL; só corrija o casamento.
3. Confirme que `analise.analisar` e `conteudo.resumo_imovel` usam município, área, mata ciliar e os
   números de RL (declarada/exigida/déficit) quando existirem — sem inventar déficit quando `rl=[]`.
4. Se o LLM estiver ligado, confirme que `llm._contexto_imovel(an)` injeta esses dados (ele já injeta;
   só garanta que `an` chega preenchido). O bot deve continuar funcionando **sem** LLM.

### Passos — Bug B (2º mapa "como deve ficar")

5. Em `conteudo.py`, amplie `pediu_meta(texto)` para reconhecer mais formas: "como deve ficar",
   "como fica", "como ficaria", "como deveria", "o certo", "corrigir", "arrumar", "depois",
   "segundo mapa", "mapa 2", "meta".
6. Em `bot.py` (`conversa_livre`), troque a lógica para enviar o mapa-meta **mesmo sem a palavra
   "mapa"**: se `pediu_meta(texto)` → envia mapa **meta**; senão, se `pediu_mapa(texto)` → envia mapa
   **atual**.
7. Adicione **comandos explícitos** em `bot.py` e registre no `main()`:
   - `/mapa` → envia o mapa **atual**;
   - `/comofica` (ou `/mapadepois`) → envia o mapa **meta**.
   Os comandos devem recuperar o imóvel de `context.user_data` (ou `memoria`/`_restaurar_contexto`);
   se não houver imóvel carregado, peça o número do CAR.
8. **Recomendado para a demo:** logo após explicar a mata ciliar (no `resumo_imovel`/`explica_mata`),
   o bot já **envia o mapa-meta automaticamente** — combina com o storyboard (cena 4). Implemente de
   forma que não envie duas vezes seguidas o mesmo mapa.
9. Reaproveite o `_enviar_mapa(update, imovel, modo, caption)` já existente; o `mapa.gerar_mapa` já
   aceita `modo="meta"`. Não duplicar lógica de mapa.

### Passos — fechamento

10. Atualize `README.md`: como pedir os dois mapas (frases + comandos `/mapa` e `/comofica`).
11. Depois de validar, **commit e push** com as travas da ACTION-008. Mensagem sugerida:
    `Bot: usa dados do imovel na conversa + comando/gatilho do 2o mapa (como deve ficar)`.

### Comandos de validação

```bash
python -m py_compile src/terra-em-dia-bot/*.py
```

```bash
# Bug A: os 3 demo precisam enriquecer APP/RL (tem_app/tem_rl True). NAO imprime cod.
PYTHONPATH=src/terra-em-dia-bot src/terra-em-dia-bot/.venv/bin/python - <<'PY'
import cadastro, analise
cods=[l.strip() for l in open("data/imoveis_teste.local.txt") if l.strip() and not l.startswith("#")]
for c in cods:
    an=analise.analisar(cadastro.carregar_imovel(c))
    print("tem_app:", an["tem_app"], "| tem_rl:", an["tem_rl"], "| municipio:", an["municipio"], "| area:", an["area_ha"])
    assert an["municipio"] and an["area_ha"]>0
assert any(analise.analisar(cadastro.carregar_imovel(c))["tem_rl"] for c in cods), "nenhum demo enriqueceu RL"
print("OK contexto")
PY
```

```bash
# Bug B: gatilho do mapa-meta sem a palavra "mapa".
PYTHONPATH=src/terra-em-dia-bot src/terra-em-dia-bot/.venv/bin/python - <<'PY'
import conteudo
assert conteudo.pediu_meta("como deve ficar")
assert conteudo.pediu_meta("e o certo, como fica depois?")
print("OK gatilho meta")
PY
```

### Critérios de aceite

- Para os 3 imóveis-demo, `tem_app`/`tem_rl` saem `True` e a conversa cita município, área, mata
  ciliar e os números de RL (declarada/exigida/déficit).
- O bot **não inventa** déficit quando não há RL declarada.
- Dá para receber o mapa "como deve ficar" por **frase natural** ("como deve ficar", sem "mapa") **e**
  por **comando** (`/comofica`).
- O mapa atual continua acessível (`/mapa` e "me manda o mapa").
- O bot continua funcionando **sem** LLM. Validações passam. Commit + push feitos.

### Forma errada provável

- Não "resolver" o Bug A inventando dados de APP/RL — corrigir o **casamento do `cod`**.
- Não imprimir `cod_imovel` real no diagnóstico.
- Não deixar o mapa-meta depender da palavra "mapa".
- Não duplicar a lógica de geração de mapa (reusar `_enviar_mapa`/`mapa.gerar_mapa`).
- Não quebrar o fluxo sem LLM nem a memória/métrica.

### Resultado do executor

- Corrigida a normalização do código do CAR no início de `cadastro.carregar_imovel` (convertendo para maiúsculo e removendo espaços), assegurando que o código coincida perfeitamente com os shapefiles locais de APP e RL para os imóveis-demo da base local.
- Expandido `pediu_meta` em `conteudo.py` para mapear de forma abrangente as diversas formas naturais pelas quais o produtor rural pode pedir o mapa meta ("como deve ficar", "como fica", "como ficaria", "o certo", "depois", etc.).
- Atualizado `bot.py` para enviar o mapa meta de forma inteligente mesmo se o usuário não citar a palavra "mapa" caso ele use termos de meta.
- Implementado envio automático do mapa meta logo após o bot explicar a mata ciliar (verificado se o último mapa enviado não é o meta).
- Adicionados os comandos explícitos `/mapa` (para mapa atual) e `/comofica` / `/mapadepois` (para mapa meta), devidamente documentados no `README.md`.

---

## ACTION-011 — Bot proativo: botões que oferecem a solução + comparativo "agora × depois" com zoom

status: concluida
tipo: codigo
prioridade: alta

### Objetivo

Em vez de esperar o produtor digitar, o bot **sugere a solução com botões** (Telegram inline keyboard):
oferece o **mapa "como deve ficar"** (a solução) e um **comparativo "agora × depois" com zoom** nas
feições (mata ciliar e Reserva Legal).

### Contexto

Em teste real, o 2º mapa nunca veio porque o envio dependia de o **usuário** citar "mata/rio". A equipe
decidiu inverter: o bot **proativamente oferece** os próximos passos em **botões**. Confirmado pelo
sênior: o `python-telegram-bot 21.11.1` (do venv) suporta `InlineKeyboardButton`,
`InlineKeyboardMarkup` e `CallbackQueryHandler`. O fluxo-alvo:

1. Manda o CAR → bot mostra "achei sua terra" + **mapa atual** + resumo.
2. Bot **oferece botões**: 🌳 *Ver como fica em dia* · 🔍 *Comparar agora × depois* · 📋 *Passos no SICAR*.
3. Clique em 🌳 → envia o **mapa-meta** (a solução) e oferece o 🔍.
4. Clique em 🔍 → envia o **comparativo "agora × depois"** com **zoom** na APP e na RL.
5. Clique em 📋 → manda o passo a passo (`guia_acao(an)`).

**Nome do rio: encerrado.** Não buscar hidrografia externa (ver `docs/desenvolver/spike-hidrografia.md`,
§5: o córrego do imóvel é "sem nome" em todas as fontes). Manter "mato da beira do rio".

### Arquivos permitidos

- `src/terra-em-dia-bot/bot.py`
- `src/terra-em-dia-bot/mapa.py`
- `src/terra-em-dia-bot/conteudo.py`
- `src/terra-em-dia-bot/README.md`

### Arquivos proibidos

- `.env` e afins · `data/**` · `desafio-2/**` · `.sqlite` · `.pdf`
- `cadastro.py` · `analise.py` · `llm.py` · `memoria.py` (só importar)

### Passos — botões e fluxo (bot.py)

1. Importe `InlineKeyboardButton`, `InlineKeyboardMarkup` (de `telegram`) e `CallbackQueryHandler`
   (de `telegram.ext`).
2. Crie um teclado de oferta (função `_teclado_solucao()`), com 3 botões e `callback_data` curtos:
   - 🌳 "Ver como fica em dia" → `sol`
   - 🔍 "Comparar agora × depois" → `cmp`
   - 📋 "Passos no SICAR" → `sicar`
3. No `_apresentar`, **depois** do `resumo_imovel(an)`: se `an.get("tem_app")` ou `an.get("tem_rl")`,
   mande uma mensagem curta de oferta (ex.: "Posso te mostrar como sua terra fica em dia 👇") com
   `reply_markup=_teclado_solucao()`. **Não** despeje os mapas automaticamente — a graça é o clique.
4. **Refatore `_enviar_mapa`** para funcionar também em callback: troque `update.message...` por
   `update.effective_chat` (ex.: `await context.bot.send_photo(chat_id=update.effective_chat.id, ...)`
   e `await update.effective_chat.send_action(...)`). Assim serve para mensagem **e** botão.
5. Crie `async def botao(update, context)`:
   - `query = update.callback_query; await query.answer()`.
   - Recupere `imovel`/`an` de `context.user_data`; se vazio, tente `_restaurar_contexto`; se ainda
     não houver, peça o número do CAR e retorne.
   - Roteie por `query.data`: `sol` → `_enviar_mapa(... "meta" ...)` e ofereça de novo o botão 🔍;
     `cmp` → envia o comparativo (passo 8); `sicar` → manda `conteudo.guia_acao(an)`.
6. Registre o handler global em `main()`: `app.add_handler(CallbackQueryHandler(botao))` (como o
   `/metricas`). Não precisa entrar no `ConversationHandler`; `context.user_data` é por usuário.
7. Mantenha o que a ACTION-010 entregou (`/mapa`, `/comofica`, gatilho por frase) como atalhos.

### Passos — comparativo com zoom (mapa.py)

8. Crie `gerar_comparativo(imovel, saida)` → 1 PNG com **dois painéis lado a lado**: "Agora" (à esq.) e
   "Como fica em dia" (à dir.):
   - "Agora": perímetro + mata ciliar **azul** (declarada) + Reserva Legal atual.
   - "Como fica": perímetro + mata ciliar **verde** (coberta) + Reserva Legal proposta/meta.
   - **Zoom:** enquadre os dois painéis no **bbox das feições de APP + RL** (com margem), não no imóvel
     inteiro — é o "zoom nos locais". Reuse `_desenha`, `_bounds`, `ESTILO` e o `set_aspect` já
     existentes. Título por painel; legenda curta. Salve e devolva o caminho (igual a `gerar_mapa`).
9. Caption sugerida para o comparativo (constante em `conteudo.py`): "🔍 Sua terra agora × como fica em
   dia (mata ciliar e Reserva Legal)".

### Passos — fechamento

10. `README.md`: documente o fluxo de botões e o comparativo (e que tudo continua funcionando **sem**
    LLM e por comando/texto).
11. Valide, **commit e push** com as travas da ACTION-008. Mensagem sugerida:
    `Bot: botoes que oferecem a solucao + comparativo agora x depois com zoom`.

### Comandos de validação

```bash
python -m py_compile src/terra-em-dia-bot/*.py
```

```bash
# Gera o comparativo do imovel-heroi (sem Telegram). NAO imprime cod.
PYTHONPATH=src/terra-em-dia-bot src/terra-em-dia-bot/.venv/bin/python - <<'PY'
import cadastro, analise, mapa, os
cods=[l.strip() for l in open("data/imoveis_teste.local.txt") if l.strip() and not l.startswith("#")]
imv=cadastro.carregar_imovel(cods[0]); an=analise.analisar(imv)
out=mapa.gerar_comparativo(imv, "/tmp/comparativo.png")
assert os.path.getsize(out)>0
print("OK comparativo:", os.path.getsize(out), "bytes | tem_app:", an["tem_app"], "| tem_rl:", an["tem_rl"])
PY
```

### Critérios de aceite

- Após mandar o CAR, o bot **oferece botões** (solução / comparar / passos) — sem o usuário pedir.
- 🌳 envia o mapa "como deve ficar"; 🔍 envia o **comparativo agora × depois com zoom** na APP e RL;
  📋 manda os passos no SICAR.
- Os botões funcionam (callback recuperando o imóvel da memória); `_enviar_mapa` funciona em
  mensagem **e** em clique de botão.
- `gerar_comparativo` produz um PNG válido para o herói.
- `/mapa`, `/comofica` e o gatilho por texto continuam funcionando; bot segue rodando **sem** LLM.
- Validação passa; commit + push feitos.

### Forma errada provável

- Em callback, **não** usar `update.message` (é `None`) — usar `update.effective_chat`/`query.message`.
- Não quebrar o `ConversationHandler` (registrar o `CallbackQueryHandler` como handler global).
- Não enquadrar o comparativo no imóvel inteiro — **zoom nas feições** (APP+RL).
- Não buscar nome de rio (encerrado). Não mexer em `cadastro.py`/`analise.py`.
- Não deixar o bot dependente de LLM nem quebrar memória/métrica.

### Resultado do executor

- Importados `InlineKeyboardButton`, `InlineKeyboardMarkup` e `CallbackQueryHandler` do python-telegram-bot.
- Criada a função `_teclado_solucao()` contendo os botões 🌳, 🔍 e 📋.
- Atualizada a função `_apresentar` para enviar proativamente os botões após exibir o resumo do imóvel.
- Refatorada a função `_enviar_mapa` para operar com base em `update.effective_chat` e `context.bot.send_photo`, funcionando transparentemente para mensagens diretas de texto/comandos ou cliques em botões inline (callbacks).
- Implementada a função `botao(update, context)` que responde aos callbacks `sol`, `cmp` e `sicar`. No caso de `sol` (Ver como fica), ela responde oferecendo novamente o botão `cmp` (Comparar agora × depois) para incentivar a exploração visual.
- Registrado o `CallbackQueryHandler` como handler global na aplicação do bot em `main()`.
- Criada a função `gerar_comparativo(imovel, saida)` em `mapa.py` que produz uma imagem contendo os painéis "Hoje" (à esquerda, com APP em azul) e "Solução" (à direita, com APP em verde), aplicando zoom automático focado na bounding box das feições locais de APP e RL.
- Adicionada a constante `CAPTION_COMPARATIVO` no arquivo `conteudo.py`.
- Atualizado o arquivo `README.md` documentando o fluxo de botões, atalhos, comandos e o comparativo lado a lado com zoom.

---

## ACTION-012 — Corrigir o comparativo: zoom POR FEIÇÃO e diferença visível

status: pronta
tipo: codigo
prioridade: alta

### Objetivo

Fazer o comparativo "agora × depois" **realmente dar zoom na feição** (a mata ciliar enche o quadro) e
mostrar uma **diferença visível** entre os dois lados.

### Contexto

O `gerar_comparativo` atual enquadra a **bounding box de APP + RL juntas**. Medido pelo sênior no
imóvel-herói: APP sozinha ≈ **320×614 m**, RL ≈ **511×682 m**, mas **APP+RL juntas ≈ 930×1568 m** —
quase o sítio inteiro (1039×1731 m). Resultado: a faixa de 30 m vira um fio **invisível**. Além disso,
hoje a **única** diferença entre os painéis é a **cor** da APP (azul→verde); a RL é desenhada **igual**
dos dois lados. Por isso "nem dá pra ver diferença".

**Limite honesto da RL:** temos só a geometria da **RL declarada** (8,3 ha). **Não existe** a geometria
do "depois" (os 9,6 ha a recompor são um número, não um polígono). Então **não forje** um antes/depois
de RL com polígonos diferentes — seria inventar dado.

### Arquivos permitidos

- `src/terra-em-dia-bot/mapa.py`
- `src/terra-em-dia-bot/bot.py`
- `src/terra-em-dia-bot/conteudo.py`
- `src/terra-em-dia-bot/README.md`

### Arquivos proibidos

- `.env` e afins · `data/**` · `desafio-2/**` · `.sqlite` · `.pdf`
- `cadastro.py` · `analise.py` · `llm.py` · `memoria.py` (só importar)

### Passos

1. Em `mapa.py`, dê ao `gerar_comparativo` o parâmetro **`feicao="app"`**. O zoom passa a usar **só o
   bbox da feição escolhida** (`imovel[feicao]`), com margem ~15–20%. Para a APP isso enquadra ~320×614 m
   e a faixa fica grande/visível. Se `imovel[feicao]` estiver vazio, retorne `None` (o chamador trata).
2. **Crie contraste real** (não só cor):
   - Painel **"Hoje"**: satélite de fundo + a faixa **só com contorno** (sem preenchimento, ou bem
     translúcida) — assim aparece o **chão atual** (muitas vezes plantio até a margem).
   - Painel **"Em dia"**: satélite de fundo + a faixa **preenchida de verde sólido/opaco**
     (`ESTILO["app_meta"]` com alpha alto) — representando o mato recomposto.
   - Mesmo bbox apertado nos dois painéis; títulos "Hoje: a beira do rio" e "Em dia: coberta de mato 🌳".
3. **Reserva Legal — sem antes/depois falso:** **não** desenhe a RL diferente dos dois lados. Se quiser
   um visual de RL, gere (com `feicao="rl"`) **um único enquadramento** da RL declarada **com anotação**
   "declarado 8,3 ha · falta 9,6 ha a recompor" (usar os números de `analise`, não fixos). Ou deixe a RL
   só no texto da conversa (que já diz declarado/exige/falta). **Recomendado:** o comparativo visual é o
   da **APP**; a RL fica como número/anotação.
4. Em `bot.py`, no callback do botão 🔍 (`cmp`): envie o **comparativo da APP**
   (`gerar_comparativo(imovel, tmp, feicao="app")`). Se `an["tem_rl"]`, complemente com **uma frase**
   curta do déficit (ou o enquadramento anotado da RL, se fizer o do passo 3). Reuse o envio por
   `effective_chat` que a ACTION-011 deixou em `_enviar_mapa`.
5. `conteudo.py`: ajuste `CAPTION_COMPARATIVO` para a APP ("🔍 A beira do rio: hoje × coberta de mato").
6. `README.md`: registre que o comparativo agora dá **zoom na feição** e que a RL aparece como número
   (não como antes/depois de polígono).
7. Valide, **commit e push** (travas da ACTION-008). Mensagem: `Bot: comparativo com zoom na APP e contraste real (hoje x em dia)`.

### Comandos de validação

```bash
python -m py_compile src/terra-em-dia-bot/*.py
```

```bash
# Gera o comparativo da APP e confirma que o enquadramento e' ~APP (bem menor que o sitio). NAO imprime cod.
PYTHONPATH=src/terra-em-dia-bot src/terra-em-dia-bot/.venv/bin/python - <<'PY'
import cadastro, mapa, os
cods=[l.strip() for l in open("data/imoveis_teste.local.txt") if l.strip() and not l.startswith("#")]
imv=cadastro.carregar_imovel(cods[0])
out=mapa.gerar_comparativo(imv, "/tmp/comp_app.png", feicao="app")
assert out and os.path.getsize(out)>0
def w(polys):
    xs=[x for ext,_ in polys for x,y in ext]; return max(xs)-min(xs)
app=[p for f in imv["app"] for p in f["polys"]]
assert w(app) < 0.7*w(imv["perimetro"]), "zoom ainda enquadra o sitio todo"
print("OK comparativo APP:", os.path.getsize(out), "bytes | zoom na APP confirmado")
PY
```

### Critérios de aceite

- O comparativo da **APP** enquadra a faixa (não o sítio inteiro) — a mata ciliar fica **grande e
  visível**.
- Há **diferença visível** entre "Hoje" (contorno/chão) e "Em dia" (verde sólido).
- A RL **não** é desenhada como antes/depois falso; aparece como número/anotação (déficit real).
- Botão 🔍 manda o comparativo certo; bot segue funcionando sem LLM; validação passa; commit + push.

### Forma errada provável

- Não enquadrar APP+RL juntas — **uma feição por vez**.
- Não fingir geometria de "depois" da RL (só temos a declarada + o número).
- Não deixar o contraste só na cor — usar contorno (hoje) × preenchido (em dia).
- Não mexer em `cadastro.py`/`analise.py`.

### Resultado do executor

Preencher depois da execução.
