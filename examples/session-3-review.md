# Session 3: review of a due card

- Tool: Claude Code (headless, `claude -p`)
- Model: claude-sonnet-5-5
- Date: 2026-10-09 (the run used `STUDY_TODAY=2026-10-10` so the card, added on 2026-10-09, was due)
- Profile: clean (--settings examples/clean-profile.json: hooks, global CLAUDE.md files, auto-memory and claude.ai skills off; the author's personal skills and plugins stayed installed)
- SKILL.md: as committed in 35c047b
- Followed the skill's rules: yes. It found the one due card, showed the question only (not the answer), asked for an answer in the learner's own words, and waited. One question; the answer was not given or hinted at. The reply is in English, the language of the prompt and the card.
- Language history: the first recording of this session (author's personal environment, earlier wording) replied in Portuguese to an English prompt and card. The recordings in the clean profile (an intermediate wording, then this one on the final wording) replied in English. The profile and the wording changed together, so the cause of the earlier Portuguese reply is not isolated.
- Setup: one card was added with `study.py add --topic dns` (question: "Why does a DNS lookup usually not walk the whole hierarchy every time?") before the run.

## Command

```
cd <tmp>/proj && STUDY_DIR=<tmp>/data STUDY_TODAY=2026-10-10 claude -p --model sonnet --output-format json --settings <tmp>/clean-profile.json --allowedTools="Bash(python3 *)" "Use the teach-back skill. Review my due cards." < /dev/null > <tmp>/out.json
```

(`<tmp>` is a throwaway directory; <tmp>/clean-profile.json is a copy of examples/clean-profile.json. The reply is the `result` field of the JSON.)

## Prompt

Use the teach-back skill. Review my due cards.

## Reply

You have 1 card due, in the topic "dns".

**Question:** Why does a DNS lookup usually not walk the whole hierarchy every time?

Answer in your own words before I show the answer.
