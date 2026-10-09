# Session 3: review of a due card

- Tool: Claude Code (headless, `claude -p`)
- Model: claude-sonnet-5-5
- Date: 2026-10-09 (the run used `STUDY_TODAY=2026-10-10` so the card, added on 2026-10-09, was due)
- Profile: clean (--settings examples/clean-profile.json: hooks, global CLAUDE.md files, auto-memory and claude.ai skills off; the author's personal skills and plugins stayed installed)
- Followed the skill's rules: yes. It found the one due card, showed the question only (not the answer), asked for an answer from memory, and waited. One question. The reply is in English, the language of the prompt and the card (in the earlier personal-profile run it was Portuguese). This run used the SKILL.md after the first tightening; the second tightening came after and does not touch the review flow.
- Setup: one card was added with `study.py add --topic dns` (question: "Why does a DNS lookup usually not walk the whole hierarchy every time?"). The call used `< /dev/null` for stdin.

## Prompt

Use the teach-back skill. Review my due cards.

## Reply

You have 1 card due, from the topic **dns**.

**Question:** Why does a DNS lookup usually not walk the whole hierarchy every time?

Answer from memory first, and then I'll show you the card's answer.
