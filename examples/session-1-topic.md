# Session 1: topic named in one sentence (English)

- Tool: Claude Code (headless, `claude -p`)
- Model: claude-sonnet-5-5
- Date: 2026-10-09
- Profile: clean (--settings examples/clean-profile.json: hooks, global CLAUDE.md files, auto-memory and claude.ai skills off; the author's personal skills and plugins stayed installed)
- SKILL.md: as committed in 35c047b
- Followed the skill's rules: partly. Yes: one question mark; the reply stayed in English; the answer was not given. No: the scenario sentence ("Picture one server holding every website's address, with millions of sites being added, moved and removed all the time.") leans toward the answer, which the rule "neither give the answer nor lean toward it" forbids; and the question (how would the server keep its information correct and up to date) targets freshness, a different gap than the learner's weak point (one server cannot know every address).

## Command

```
cd <tmp>/proj && STUDY_DIR=<tmp>/data STUDY_TODAY=2026-10-09 claude -p --model sonnet --output-format json --settings <tmp>/clean-profile.json --allowedTools="Bash(python3 *)" "Use the teach-back skill. I want to study how DNS works. My explanation: when you type a website name, your computer asks a DNS server, and the DNS server knows the address of every website, so it just sends it back." < /dev/null > <tmp>/out.json
```

(`<tmp>` is a throwaway directory; <tmp>/clean-profile.json is a copy of examples/clean-profile.json. The reply is the `result` field of the JSON.)

## History

Three recordings of this session existed: (1) the first run, in the author's personal environment, on the original wording: it asked two questions; (2) a run in the clean profile on the first tightened wording: it still asked two questions; (3) this run, in the clean profile on the final wording. The replies of runs 1 and 2 were not kept as files, so this recording is NOT typical of a single attempt: it is the third try.

## Prompt

Use the teach-back skill. I want to study how DNS works. My explanation: when you type a website name, your computer asks a DNS server, and the DNS server knows the address of every website, so it just sends it back.

## Reply

You have no saved topics yet, so nothing is due for review.

Part of your explanation is right: the computer asks a DNS server for the address that goes with a name, and the answer comes back to it.

You said "the DNS server knows the address of every website." Picture one server holding every website's address, with millions of sites being added, moved and removed all the time. How would that server keep its information correct and up to date?
