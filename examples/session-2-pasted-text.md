# Session 2: pasted text (Portuguese)

- Tool: Claude Code (headless, `claude -p`)
- Model: claude-sonnet-5-5
- Date: 2026-10-09
- Profile: clean (--settings examples/clean-profile.json: hooks, global CLAUDE.md files, auto-memory and claude.ai skills off; the author's personal skills and plugins stayed installed)
- SKILL.md: as committed in 35c047b
- Followed the skill's rules: yes. It triggered; the reply is in Portuguese (the learner's language); it asked the learner to explain from memory first, with no question about the text; it did not summarize or teach, and it gave no answer. It asks for "para que ele serve e o que se paga em troca", which mirrors the text's structure slightly (a mild lean toward the content, not an answer).
- History: one earlier recording of this session existed, on an intermediate SKILL.md wording; it was replaced by this one, recorded on the committed wording. It also followed the rules.

## Command

```
cd <tmp>/proj && STUDY_DIR=<tmp>/data STUDY_TODAY=2026-10-09 claude -p --model sonnet --output-format json --settings <tmp>/clean-profile.json --allowedTools="Bash(python3 *)" "Use a skill teach-back. Quero estudar este texto: 'Um índice de banco de dados é uma estrutura separada que guarda os valores de uma coluna ordenados, com a posição de cada linha. Assim, para achar uma linha, o banco busca no índice em vez de ler a tabela inteira. Em troca, cada escrita precisa atualizar também o índice.'" < /dev/null > <tmp>/out.json
```

(`<tmp>` is a throwaway directory; <tmp>/clean-profile.json is a copy of examples/clean-profile.json. The reply is the `result` field of the JSON.)

## Prompt

Use a skill teach-back. Quero estudar este texto: 'Um índice de banco de dados é uma estrutura separada que guarda os valores de uma coluna ordenados, com a posição de cada linha. Assim, para achar uma linha, o banco busca no índice em vez de ler a tabela inteira. Em troca, cada escrita precisa atualizar também o índice.'

## Reply

Você ainda não tem tópicos nem cartões para revisar, então vamos direto ao texto.

Sem olhar o texto e sem pesquisar, explique com suas palavras o que é um índice de banco de dados. Imagine que está falando com um amigo que não sabe nada sobre o assunto. Inclua para que ele serve e o que se paga em troca.
