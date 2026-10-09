# Session 1: topic named in one sentence (English)

- Tool: Claude Code (headless, `claude -p`)
- Model: claude-sonnet-5-5
- Date: 2026-10-09
- Profile: clean (--settings examples/clean-profile.json: hooks, global CLAUDE.md files, auto-memory and claude.ai skills off; the author's personal skills and plugins stayed installed)
- Followed the skill's rules: yes. One question (a single question mark), asked about one gap, quoting the learner's words ("the DNS server knows the address of every website"). It did not give the answer; the scenario (millions of sites added, moved, removed) sets up the question but does not state the answer. Reply in English, the learner's language.
- History: this is the third recording of this session. Run 1 (personal profile) asked two questions. Run 2 (clean profile, first tightened wording of SKILL.md) still asked two ("Could one server really hold all of them? If not, what do you think happens...?"). SKILL.md was tightened once more (single question mark, no follow-up question) and this run 3 is the result. Run 1 and 2 replies are not kept here.
- Note: `--allowedTools` is passed as `--allowedTools="Bash(python3 *)"` because the spaced form swallows the prompt. `--settings` with a file path was accepted.

## Prompt

Use the teach-back skill. I want to study how DNS works. My explanation: when you type a website name, your computer asks a DNS server, and the DNS server knows the address of every website, so it just sends it back.

## Reply

You have no saved topics yet, so nothing is due for review.

Part of your explanation is right: the computer asks a DNS server for the address that goes with a name, and the answer comes back to it.

You said "the DNS server knows the address of every website." Picture one server holding every website's address, with millions of sites being added, moved and removed all the time. How would that server keep its information correct and up to date?
