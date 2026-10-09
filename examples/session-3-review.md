# Session 3: review of a due card

- Tool: Claude Code (headless, `claude -p`)
- Model: claude-sonnet-5-5
- Date: 2026-10-09 (the run used `STUDY_TODAY=2026-10-10` so the card, added on 2026-10-09, was due)
- Followed the skill's rules: mostly yes. The skill triggered, found the one due card, showed the question only (not the answer), and waited for the learner. Oddity: the learner's prompt and the card were in English, but the reply was in Portuguese, so "replies in the learner's language" was not followed here. Likely cause: not investigated.
- Setup: one card was added with `study.py add --topic dns` (question: "Why does a DNS lookup usually not walk the whole hierarchy every time?"). The CLI also printed a harmless stderr warning, `Warning: no stdin data received in 3s, proceeding without it`, which is not part of the reply.

## Prompt

Use the teach-back skill. Review my due cards.

## Reply

Você tem 1 card vencido, do tópico **dns**.

**Pergunta:** Por que uma consulta DNS normalmente não percorre toda a hierarquia a cada vez?

Responda com suas próprias palavras antes de eu mostrar a resposta.
