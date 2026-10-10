# study-loop

Uma skill de estudo para assistentes de código com IA. Você explica um tema com suas próprias palavras. A skill encontra o ponto fraco, um por vez, transforma pontos fracos em flashcards e agenda revisões para você rever cada cartão antes de esquecê-lo.

Ela responde no idioma em que você escrever.

> **Idioma / Language:** Português primeiro, [English abaixo](#english) — a documentação completa em inglês está no fim deste arquivo.

## Instalação

Claude Code: a partir da pasta que contém o diretório `study-loop`, copie-o para o seu diretório de skills.

```bash
cp -r study-loop ~/.claude/skills/
```

Salvar e agendar precisam de Python 3.8 ou mais novo (`python3`, ou `python`/`py` se for o nome no seu sistema). O código foi escrito para 3.8 e testado no Python 3.12.3 no Linux. Windows e macOS não foram testados. Sem Python, a parte da conversa continua funcionando, mas nada é salvo.

Apenas o Claude Code foi testado. Outras ferramentas que leem o formato Agent Skills podem funcionar.

## Context7 (recomendado)

Context7 é um servidor MCP que fornece documentação atualizada de bibliotecas. Para temas de biblioteca ou API, o study-loop usa o Context7 para conferir a resposta de cada cartão contra a documentação antes de pedir para salvar: uma consulta por conceito, no máximo 3 chamadas, e um cartão que discorde da documentação é corrigido (você é avisado do que mudou).

É recomendado, mas não obrigatório. A skill foi feita para continuar funcionando sem ele, mas esse caminho não foi registrado; para temas de biblioteca ou API, o modelo é instruído a dizer uma vez que os cartões não foram conferidos.

Para adicionar no Claude Code:

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

Veja https://github.com/upstash/context7 para instruções e opções atualizadas.

Privacidade: as consultas vão para o serviço do Context7. A skill é instruída a enviar apenas perguntas genéricas de biblioteca, nunca o seu próprio texto.

## Uso

- "Use study-loop: quero estudar como o DNS funciona."
- "Use study-loop: estude este texto: <cole o texto aqui>"
- "Use study-loop: revise meus cartões vencidos."

Depois, explique o tema com suas próprias palavras quando a skill pedir.

Nomes de tópico são comparados ignorando maiúsculas e pontuação (`C++` e `C#` viram ambos `c`). Use uma sessão por vez por tópico: duas sessões salvando o mesmo tópico ao mesmo tempo podem perder uma atualização.

## Como funciona

1. Você explica o tema sem consultar nada.
2. A skill cita você e faz uma pergunta sobre uma lacuna. Ela não dá a resposta.
3. Quando a explicação se sustenta, ela propõe de 3 a 6 cartões. Você edita ou descarta qualquer um.
4. Você decide se salva. Depois de um sim, o modelo escreve os cartões em um arquivo JSON temporário e roda `study.py add --topic <nome> --file <arquivo>` em um único comando (`--file -` ou sem `--file` lê da entrada padrão).
5. Nas revisões você responde primeiro, depois vê a resposta, e diz certo, quase ou errado.

As revisões usam cinco caixas com intervalos de 1, 3, 7, 16 e 35 dias. Certo move o cartão uma caixa para cima. Quase mantém na caixa. Errado devolve para a caixa 1.

## Seus dados

Os cartões ficam em `~/.study-loop/`, um arquivo JSON por tópico. Defina `STUDY_DIR` para usar outra pasta. Nada é salvo antes de você dizer sim. O `study.py` não faz chamadas de rede e não há contas. Sua conversa ainda vai para o seu provedor de IA, e a conferência opcional pelo Context7 consulta esse serviço (veja [Context7](#context7-recomendado)).

## Custo de tokens

| O quê | Tokens aprox. |
|---|---|
| Listagem (descrição, a cada turno) | 59 |
| Invocação (SKILL.md) | 966 |
| references/cards.md (só quando necessário) | 187 |
| references/gaps.md (só quando necessário) | 201 |

Contado como palavras x 1.35. Os guias carregam apenas quando a skill precisa deles.

## Registros de execuções

Execuções reais em `examples/`, cada uma com a ferramenta e o modelo usados. As sessões 1 a 5 foram gravadas quando a skill se chamava teach-back, então seus prompts e caminhos dizem teach-back; são mantidos verbatim.

- `examples/session-1-topic.md`: um tópico nomeado em uma frase, em inglês; seguiu as regras só em parte, porque a resposta pendeu para o lado da resposta e a pergunta mirou numa lacuna diferente da do aprendiz.
- `examples/session-2-pasted-text.md`: um texto colado, em português; pediu ao aprendiz para explicar de memória primeiro e respondeu em português, com uma leve inclinação para a estrutura do texto.
- `examples/session-3-review.md`: uma revisão de um cartão vencido; mostrou só a pergunta e esperou a resposta do aprendiz.
- `examples/session-4-multi-turn.md`: uma conversa que ensina (inglês) e uma segunda que revisa três cartões. A revisão funcionou: o modelo mostrou cada pergunta antes da resposta, rodou `grade` três vezes, e os três cartões foram para a caixa 2 no disco. O salvamento não funcionou nesse ambiente: o modelo tentou `add` com um heredoc entre aspas, a regra de permissão headless recusou, e os cartões foram adicionados à mão antes da revisão. O modelo avisou o aprendiz que os cartões não foram salvos. Uma das perguntas de lacuna pendeu para o lado da resposta.

- `examples/session-5-save-through-file.md`: uma conversa, só o dia 1, no SKILL.md de 848fb89 (depois de `add --file`, dc03ea8). O modelo rodou três rodadas de lacuna, não uma. O salvamento funcionou: após o sim do aprendiz, o modelo escreveu os cartões num arquivo com a ferramenta Write, rodou `add --file` em uma linha, e cinco cartões chegaram ao disco, sem nada adicionado à mão. Não repetiu a nota de que nomes de tópico ignoram maiúsculas e pontuação, e disse que os cartões foram para a pasta padrão de dados (citou a pasta padrão antiga `~/.teach-back/`) embora os dados estivessem em `$STUDY_DIR`. Essa execução foi feita antes de o campo `folder` existir na saída de `topics` e `add`, adicionado depois para que o modelo possa informar a pasta real; não foi regravado. A revisão desses cartões não foi refeita (a sessão 4 cobre revisão). A execução usou regras allow (`Bash(python3 *)` e `Edit(//tmp/**)`); uma sessão interativa mostraria pedidos de aprovação, o que não foi testado.
- `examples/session-6-two-days.md`: dois dias no SKILL.md final (46e1bd4), com o nome study-loop, tópico: como uma tabela hash trata colisões. O dia 1 salvou cinco cartões por um arquivo de cartões com `add --file` em uma linha, e o modelo citou a pasta real de dados. O dia 2 revisou os cinco: o modelo mostrou cada pergunta primeiro, rodou `grade` cinco vezes com os resultados que o aprendiz deu (quatro certos, um quase) e terminou com `due --limit 1` e contagem real de 0. Defeitos: o modelo fez uma pergunta de lacuna e o aprendiz a respondeu por completo, então a lacuna planejada (função de hash e load factor) nunca surgiu; o modelo escreveu o arquivo de cartões direto em /tmp; e avisou o aprendiz que os cartões novos venciam agora quando venciam no dia seguinte. Nada foi recusado. Regras allow iguais às da sessão 5.
- `examples/session-7-library-topic.md`: uma conversa, só o dia 1, tópico: o módulo pathlib do Python, no SKILL.md de 2613e97 (o commit que adicionou a regra do Context7). As ferramentas do Context7 estavam disponíveis e o modelo fez três chamadas (`resolve-library-id` uma vez, `query-docs` duas) antes de pedir para salvar. O aprendiz disse algo errado de propósito (que `Path.mkdir()` cria pastas pai por padrão); o modelo corrigiu, citando `parents=False` e `FileNotFoundError`, e os cartões salvos trazem a resposta corrigida. Defeitos: a pergunta de lacuna do modelo já apontava para a frase errada, então a execução não mostra a conferência da documentação pegando algo que a etapa de lacuna não pegou; um cartão (o operador `/`) não foi coberto por nenhuma consulta, então não foi conferido; a primeira consulta quebrou a regra de um conceito por consulta; o arquivo de cartões foi para /tmp de novo. Nada foi recusado. A allow list era as duas regras da sessão 5 mais as duas ferramentas do Context7. O caso sem Context7 não foi gravado.

Limites conhecidos:

- Escopo
  - As execuções foram feitas com Claude Code e um modelo, `claude-sonnet-5-5`.
  - A skill foi usada nas sete execuções, e todo prompt a nomeou explicitamente. As execuções mostram como ela se comporta quando invocada pelo nome; não mostram que ela começa por conta própria a partir da descrição.
- Qual SKILL.md cada execução usou (cada gravação rodou numa versão diferente)
  - Sessões 1 a 3: 35c047b (editado depois: comando python, contagem final de vencidos, tratamento de falha de salvamento, nomes de tópico).
  - Sessão 4: 96dc307 (a instrução de salvamento dela, um heredoc entre aspas, foi substituída depois pelo arquivo de cartões, então a falha de salvamento que registra não descreve mais o SKILL.md atual).
  - Sessão 5: 848fb89 (editado depois: o campo `folder` e o nome da pasta na pergunta de salvamento).
  - Sessão 6: 46e1bd4 (antes da regra do Context7 ser reescrita).
  - Sessão 7: 2613e97, a atual.
  - Sessões 1 a 5 foram gravadas quando a skill se chamava teach-back, então seus prompts e caminhos dizem teach-back.
- Método
  - Os turnos de aprendiz das sessões 4 a 7 foram escritos por um piloto de testes de IA, não por um humano.
  - As execuções usaram regras allow headless, então os pedidos de aprovação interativos não foram testados.
  - As gravações usaram um perfil limpo (`examples/clean-profile.json`); as skills e plugins pessoais do autor continuaram instalados.
- Confiabilidade
  - A sessão 1 seguiu a regra de uma pergunta só na sua terceira gravação, e a resposta ainda pendeu para o lado da resposta, então ela não é típica de uma tentativa única.
  - Uma gravação anterior no ambiente do próprio autor respondeu em português a um pedido em inglês, e a causa não foi isolada.

## Testes

```bash
python3 -m unittest discover -s tests -v
python3 tools/check_budget.py .
```

## Licença

MIT

---

# English

A study skill for AI coding assistants. You explain a topic back in your own words. The skill finds the weak spot, one at a time, turns weak spots into flashcards, and schedules reviews so you see each card again before you forget it.

It answers in the language you write in.

## Install

Claude Code: from the folder that contains the `study-loop` folder, copy it into your skills directory.

```bash
cp -r study-loop ~/.claude/skills/
```

Saving and scheduling need Python 3.8 or newer (`python3`, or `python`/`py` if that is the name on your system). The code was written for 3.8 and tested on Python 3.12.3 on Linux. Windows and macOS have not been tested. Without Python the conversation part still works, but nothing is saved.

Only Claude Code has been tested. Other tools that read the Agent Skills format may work.

## Context7 (recommended)

Context7 is an MCP server that serves current documentation for libraries. For library or API topics, study-loop uses it to check each card's answer against the docs before you are asked to save: one query per concept, at most 3 calls, and a card that disagrees with the docs is corrected (you are told what changed).

It is recommended but not required. The skill is meant to keep working without it, but that path was not recorded; for library or API topics the model is told to say once that the cards were not checked.

To add it in Claude Code:

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

See https://github.com/upstash/context7 for current instructions and options.

Privacy: the queries go to the Context7 service. The skill is told to send only generic library questions, never your own text.

## Use

- "Use study-loop: I want to study how DNS works."
- `Use study-loop: study this text: <paste it here>`
- "Use study-loop: review my due cards."

Then explain the topic in your own words when the skill asks.

Topic names are matched ignoring case and punctuation (`C++` and `C#` both become `c`). Use one session at a time per topic: two sessions saving the same topic at once can lose an update.

## How it works

1. You explain the topic without looking anything up.
2. The skill quotes you and asks one question about one gap. It does not give the answer.
3. When the explanation holds up, it proposes 3 to 6 cards. You edit or drop any.
4. You decide whether to save them. After a yes, the model writes the cards to a temporary JSON file and runs `study.py add --topic <name> --file <that file>` as one single-line command (`--file -` or no `--file` reads stdin).
5. In reviews you answer first, then see the answer, then say right, almost or wrong.

Reviews use five boxes with gaps of 1, 3, 7, 16 and 35 days. Right moves a card up one box. Almost keeps it in its box. Wrong sends it back to box 1.

## Your data

Cards live in `~/.study-loop/`, one JSON file per topic. Set `STUDY_DIR` to use another folder. Nothing is saved before you say yes. `study.py` makes no network calls and there are no accounts. Your conversation still goes to your AI provider, and the optional Context7 check queries that service (see [Context7](#context7-recommended)).

## Token cost

| What | Approx. tokens |
|---|---|
| Listing (description, every turn) | 59 |
| Invocation (SKILL.md) | 966 |
| references/cards.md (only when needed) | 187 |
| references/gaps.md (only when needed) | 201 |

Counted as words x 1.35. The guides load only when the skill needs them.

## Recorded runs

Real runs in `examples/`, each with the tool and model used. Sessions 1 to 5 were recorded when the skill was named teach-back, so their prompts and paths say teach-back; they are kept verbatim.

- `examples/session-1-topic.md`: a topic named in one sentence, in English; it followed the rules only partly, because the reply leaned toward the answer and its question targeted a different gap than the learner's.
- `examples/session-2-pasted-text.md`: a pasted text, in Portuguese; it asked the learner to explain from memory first and replied in Portuguese, with a mild lean toward the text's structure.
- `examples/session-3-review.md`: a review of one due card; it showed the question only and waited for the learner's answer.
- `examples/session-4-multi-turn.md`: one conversation that teaches back (English) and a second that reviews three cards. The review worked: the model showed each question before its answer, ran `grade` three times, and all three cards moved to box 2 on disk. The save did not work in that setup: the model tried `add` with a quoted heredoc, the headless permission rule refused it, and the cards were added by hand before the review. The model told the learner the cards were not saved. One of its gap questions leaned toward the answer.

- `examples/session-5-save-through-file.md`: one conversation, day 1 only, on the SKILL.md of 848fb89 (after `add --file`, dc03ea8). The model ran three gap rounds, not one. The save worked: after the learner's yes the model wrote the cards to a file with its Write tool, ran `add --file` as a single line, and five cards landed on disk, with nothing added by hand. It did not repeat the note that topic names ignore case and punctuation, and it said the cards went to the default data folder (it named the old default folder `~/.teach-back/`) although the data was in `$STUDY_DIR`. This run was made before the `folder` field existed in the output of `topics` and `add`, which was added afterwards so the model can state the real folder; it was not re-recorded. The review of those cards was not re-run (session 4 covers review). The run used allow rules (`Bash(python3 *)` and `Edit(//tmp/**)`); an interactive session would show approval prompts instead, which were not tested.
- `examples/session-6-two-days.md`: two days on the final SKILL.md (46e1bd4), under the name study-loop, topic: how a hash table handles collisions. Day 1 saved five cards through a cards file with `add --file` as one line, and the model named the real data folder. Day 2 reviewed all five: the model showed each question first, ran `grade` five times with the results the learner gave (four right, one almost) and ended with `due --limit 1` and a true count of 0. Flaws: the model asked one gap question and the learner answered it fully, so the planned gap (hash function and load factor) never came up; the model wrote the cards file directly in /tmp; and it told the learner the new cards were due now when they were due the next day. Nothing was refused. Allow rules were the same two as in session 5.
- `examples/session-7-library-topic.md`: one conversation, day 1 only, topic: Python's pathlib module, on the SKILL.md of 2613e97 (the commit that added the Context7 rule). The Context7 tools were available and the model made three calls (`resolve-library-id` once, `query-docs` twice) before asking to save. The learner stated one wrong thing on purpose (that `Path.mkdir()` creates parent folders by default); the model corrected it, citing `parents=False` and `FileNotFoundError`, and the saved cards carry the corrected answer. Flaws: the model's gap question already pointed at the wrong sentence, so the run does not show the docs check catching something the gap step missed; one card (the `/` operator) was not covered by any query, so it was not checked; the first query broke the one-concept-per-query rule; the cards file went to /tmp itself. Nothing was refused. The allow list was the two rules of session 5 plus the two Context7 tools. The case without Context7 was not recorded.

Known limits:

- Scope
  - The runs were made with Claude Code and one model, `claude-sonnet-5-5`.
  - The skill was used in all seven runs, and every prompt named it explicitly. The runs show how it behaves when invoked by name; they do not show that it starts on its own from its description.
- Which SKILL.md each run used (each recording ran on a different one)
  - Sessions 1 to 3: 35c047b (edited afterwards: python command, final due count, failed-save handling, topic names).
  - Session 4: 96dc307 (its save instruction, a quoted heredoc, was replaced afterwards by the cards file, so the save failure it records no longer describes the current SKILL.md).
  - Session 5: 848fb89 (edited afterwards: the `folder` field and the name of the folder in the save question).
  - Session 6: 46e1bd4 (before the Context7 rule was reworded).
  - Session 7: 2613e97, the current one.
  - Sessions 1 to 5 were recorded when the skill was named teach-back, so their prompts and paths say teach-back.
- Method
  - Learner turns in sessions 4 to 7 were written by an AI test driver, not a human.
  - The runs used headless allow rules, so interactive approval prompts were not tested.
  - The recordings used a clean profile (`examples/clean-profile.json`); the author's personal skills and plugins stayed installed.
- Reliability
  - Session 1 followed the one-question rule only on its third recording and its reply still leaned toward the answer, so it is not typical of a single attempt.
  - An earlier recording in the author's own environment replied in Portuguese to an English request, and the cause was not isolated.

## Tests

```bash
python3 -m unittest discover -s tests -v
python3 tools/check_budget.py .
```

## License

MIT
