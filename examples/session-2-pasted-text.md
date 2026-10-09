# Session 2: pasted text (Portuguese)

- Tool: Claude Code (headless, `claude -p`)
- Model: claude-sonnet-5-5
- Date: 2026-10-09
- Profile: clean (--settings examples/clean-profile.json: hooks, global CLAUDE.md files, auto-memory and claude.ai skills off; the author's personal skills and plugins stayed installed)
- Followed the skill's rules: yes. One request, no question about the text yet; it asked the learner to explain from memory first, in Portuguese (the learner's language), and did not summarize or teach. Minor: the request lists what to cover ("o que é um índice, para que ele serve e qual é o preço de usá-lo"), which mirrors the text's structure slightly. This run used the SKILL.md after the first tightening; the second tightening (question rule only) came after and does not touch this flow.
- Note: a harmless stderr warning (`no stdin data received in 3s`) appeared because stdin was not redirected; it is not part of the reply.

## Prompt

Use a skill teach-back. Quero estudar este texto: 'Um índice de banco de dados é uma estrutura separada que guarda os valores de uma coluna ordenados, com a posição de cada linha. Assim, para achar uma linha, o banco busca no índice em vez de ler a tabela inteira. Em troca, cada escrita precisa atualizar também o índice.'

## Reply

Você ainda não tem tópicos salvos, então não há cards para revisar. Vamos direto ao texto.

Explique com suas palavras, como se fosse para um amigo que não sabe nada de banco de dados, o que é um índice, para que ele serve e qual é o preço de usá-lo. Não olhe o texto enquanto escreve.
