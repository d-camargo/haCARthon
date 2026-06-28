# INSTRUCTIONS.md - Como o executor junior deve trabalhar

Este arquivo e para o agente ou desenvolvedor junior que vai executar tarefas no
projeto Terra em Dia.

Voce nao e o planejador. Voce e o executor.

Sua responsabilidade e implementar exatamente a tarefa recebida, com o menor
escopo possivel, validando o resultado e reportando o que foi feito. Se a tarefa
estiver ambigua, pare e peca esclarecimento antes de inventar uma solucao.

## Regra principal

Siga a tarefa registrada pelo planejador senior em `ACTIONS.md`.

Nao adicione funcionalidades extras.
Nao reestruture arquivos sem pedido.
Nao mude documentacao fora do escopo.
Nao "melhore" textos, fluxos ou arquitetura por conta propria.
Nao corrija problemas que voce encontrou se eles nao bloqueiam a tarefa.

Se achar um problema fora do escopo, registre no final como observacao.

## Ordem obrigatoria de execucao

Execute sempre nesta ordem:

1. Leia a tarefa inteira antes de mexer em qualquer arquivo.
2. Leia `ACTIONS.md` e identifique a tarefa marcada como `status: pronta`.
3. Leia `INSTRUCTIONS.md`.
4. Leia `AGENTS.md` apenas para contexto e regras do projeto.
5. Confira o estado do git.
6. Leia apenas os arquivos permitidos pela tarefa.
7. Confirme mentalmente quais arquivos sao proibidos.
8. Faca a menor alteracao possivel.
9. Rode os comandos de validacao indicados.
10. Confira `git status --short`.
11. Preencha o resultado da tarefa em `ACTIONS.md`, se a tarefa pedir isso.
12. Responda com resumo objetivo.

Nao execute tarefas que nao estejam em `ACTIONS.md`.
Nao execute tarefas com `status: rascunho`, `status: bloqueada` ou
`status: concluida`.

Comando inicial obrigatorio:

```bash
git status --short
```

## Arquivos que voce nunca deve abrir ou exibir

Nunca abra, copie, imprima ou resuma:

- `src/terra-em-dia-bot/.env`
- qualquer arquivo `.env`
- qualquer arquivo `.env.*`, exceto `.env.example`
- arquivos locais com CPF, codigo SNCR, token, chave de API ou codigo CAR real

Se precisar saber se uma variavel existe, olhe somente `.env.example`.

## Arquivos e diretorios protegidos

Nao altere estes caminhos, a menos que a tarefa permita explicitamente:

- `desafio-2/**`
- `data/**`, exceto `data/README.md`
- `docs/base-documental/**`
- arquivos `.pdf`
- arquivos `.sqlite`
- `__pycache__/**`
- `.venv/**`

O diretorio `desafio-2/` e legado. Pode ser lido se o planejador mandar, mas nao
deve ser reestruturado nem atualizado.

## Como editar

Faca edicoes pequenas.

Preferencias:

- preserve o estilo do arquivo existente;
- mantenha portugues do Brasil;
- nao misture refatoracao com funcionalidade;
- nao renomeie funcoes ou arquivos sem necessidade;
- nao apague codigo que ainda pode ser usado, salvo instrucao explicita;
- nao altere comportamento de metrica, memoria ou LLM sem validar.

Quando alterar texto do chatbot:

- respostas curtas;
- linguagem de atendimento;
- sem aula juridica;
- sem paragrafo grande;
- sem repetir apresentacao;
- sem terminar toda resposta com "qualquer duvida estou aqui";
- sem promessa de credito;
- sem dizer que o bot executa algo no SICAR.

## Como trabalhar no chatbot

Arquivos principais:

- `src/terra-em-dia-bot/bot.py`: fluxo do Telegram;
- `src/terra-em-dia-bot/conteudo.py`: textos e fallback sem LLM;
- `src/terra-em-dia-bot/llm.py`: prompt e chamada de LLM;
- `src/terra-em-dia-bot/memoria.py`: memoria persistente local;
- `src/terra-em-dia-bot/metricas.py`: metricas de entendimento;
- `src/terra-em-dia-bot/README.md`: instrucoes do bot.

Regras obrigatorias:

- o bot deve funcionar sem LLM;
- o LLM deve ser opcional;
- a memoria deve evitar repetir contexto;
- `/cancel` deve apagar a memoria do chat;
- o bot deve pedir numero do CAR ou foto quando nao houver contexto;
- o bot deve responder ao que o Seu Raimundo perguntou;
- o bot nao deve conduzir quiz automaticamente;
- o bot nao deve despejar legislacao.

## Validacao obrigatoria para codigo Python

Depois de mexer em qualquer `.py` do bot, rode:

```bash
python -m py_compile src/terra-em-dia-bot/*.py
```

Se mexer em conversa, fallback ou memoria, rode tambem:

```bash
PYTHONPATH=src/terra-em-dia-bot python - <<'PY'
import conteudo, memoria
an = {
    "municipio": "QUERENCIA DO NORTE", "uf": "PR", "area_ha": 89.6,
    "faixa_app_m": 30, "tem_rl": True, "rl_deficit_ha": 1.2,
    "rl_proposta_ha": 8.0, "rl_exigida_ha": 9.2,
}
assert "mata ciliar" in conteudo.resposta_curta("o que e essa mata do rio?", an)
assert conteudo.pediu_mapa("me manda o mapa")
memoria.atualizar(-1, cod="TESTE", historico=[])
memoria.adicionar_mensagem(-1, "user", "teste")
assert memoria.carregar(-1)["cod"] == "TESTE"
memoria.limpar(-1)
print("ok")
PY
```

Nao rode `python bot.py` se voce nao tiver instrucao explicita para iniciar o
bot. Esse comando depende de token local no `.env`.

## Como lidar com erro

Se um comando falhar:

1. Leia a mensagem de erro.
2. Corrija apenas o necessario.
3. Rode o mesmo comando de novo.
4. Se falhar de novo pelo mesmo motivo, pare e reporte o bloqueio.

Nao instale dependencias sem autorizacao.
Nao use rede sem autorizacao.
Nao apague arquivos gerados sem autorizacao.
Nao rode comandos destrutivos.

Comandos proibidos sem autorizacao explicita:

```bash
git reset --hard
git checkout --
rm -rf
git clean
```

## Como responder ao planejador

No final, responda sempre neste formato:

```md
Feito.

Arquivos alterados:
- caminho/arquivo.py: o que mudou

Validacao:
- `comando`: passou

Nao testado:
- item que nao foi testado, com motivo

Observacoes:
- arquivo nao versionado ou risco fora do escopo, se houver
```

Se nada foi alterado, diga:

```md
Nao alterei arquivos.

Motivo:
- explique o bloqueio ou a decisao
```

## Criterios de qualidade

Antes de dizer "feito", confira:

- a tarefa pedida foi atendida;
- nao houve mudanca fora dos arquivos permitidos;
- os comandos de validacao passaram;
- nenhum segredo foi aberto ou exibido;
- nenhum dado pesado foi adicionado;
- o bot continua com tom de atendimento;
- o resumo final e curto e verificavel.

## Quando pedir ajuda

Peca ajuda antes de executar se:

- a tarefa nao diz quais arquivos podem ser alterados;
- voce precisa abrir `.env` ou dado sensivel;
- a solucao exige mudar `desafio-2/`;
- a validacao exige token, rede ou dependencia ausente;
- duas instrucoes entram em conflito;
- voce percebe que a tarefa planejada pode quebrar memoria, metricas ou fluxo do bot.
