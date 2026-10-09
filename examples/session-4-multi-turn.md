# Session 4: multi-turn run that saves and grades (English)

- Tool: Claude Code (headless, `claude -p`, continued with `--resume`)
- Model: claude-sonnet-5-5
- Date: 2026-10-09 (the "day 2" part used `STUDY_TODAY=2026-10-10`)
- Profile: clean (--settings examples/clean-profile.json: hooks, global CLAUDE.md files, auto-memory and claude.ai skills off; the author's personal skills and plugins stayed installed)
- SKILL.md: as committed in 96dc307
- Learner turns were written by an AI test driver, not a human.
- Outcome in one line: the review half worked end to end (the model ran `grade` three times and the cards moved to box 2). The save half did NOT work in this setup: the model ran `add` with a quoted heredoc as SKILL.md says, the headless permission rule `Bash(python3 *)` refused it, and nothing was saved by the model. The cards used on day 2 were added by hand with `study.py add` (see "Setup that was not the model's").

## Command

```
# <tmp>/proj/.claude/skills/teach-back is a git archive of HEAD (96dc307); its SKILL.md is identical to the repo's
cd <tmp>/proj && STUDY_DIR=<tmp>/data STUDY_TODAY=2026-10-09 claude -p --model sonnet --output-format json --allowedTools="Bash(python3 *)" --settings <tmp>/clean-profile.json "<learner text>" < /dev/null > <tmp>/out.json
# later turns of the same conversation: the same command with  --resume <session_id>  before the prompt
# day 2: a new conversation, STUDY_TODAY=2026-10-10, first prompt "Use the teach-back skill. Review my due cards."
```

(`<tmp>` is a throwaway directory; <tmp>/clean-profile.json is a copy of examples/clean-profile.json. Each reply is the `result` field of the JSON. Turn 8 used `--allowedTools="Bash"` and was refused, see below.)

## Transcript

## Part 1: day 1 (STUDY_TODAY=2026-10-09), new conversation

### Turn 1 (day 1, turn 1)

Learner: Use the teach-back skill. I want to study the difference between TCP and UDP.

Reply:

> You have no saved topics yet, so no cards are due.
> 
> Let's start with TCP vs UDP. Explain the difference as if you were talking to a friend who knows nothing about networking. Don't look anything up. Say it in your own words, as much or as little as you know.

### Turn 2 (day 1, turn 2)

Learner: Both send data over the network. TCP sets up a connection first, checks that every packet arrived, resends lost ones and keeps them in order. UDP just sends packets with no connection and no checking, so it is the one used for video calls and games.

Reply:

> You have the core right. TCP sets up a connection, confirms delivery, resends lost packets and keeps order. UDP skips all of that. You also tied UDP to video calls and games.
> 
> One gap is in your last sentence: "so it is the one used for video calls and games." Why would skipping the checking make UDP a better fit for those uses than TCP?

### Turn 3 (day 1, turn 3)

Learner: Honestly I'm not sure. Maybe because it's simpler for the program?

Reply:

> Fewer steps does mean less work for the program, so that's partly true. It doesn't yet explain why video calls and games would choose it.
> 
> Picture a video call over TCP where one packet is lost. Based on what you said about TCP resending lost packets and keeping them in order, what happens to the packets that arrive after the lost one?

### Turn 4 (day 1, turn 4)

Learner: They would have to wait until the lost one is resent, since TCP keeps order. So the call would freeze for a moment, and by then the old packet is useless anyway. UDP just skips it and keeps going with fresh data, so it is faster and has lower delay.

Reply:

> That's correct, and you worked out the key idea yourself. TCP's ordering makes later packets wait for the lost one. In real-time use, that late packet is worthless by the time it arrives. UDP trades reliability for low delay.
> 
> You've only covered one side of the trade-off. Suppose you downloaded a file over UDP, with no checking and no resending. What would go wrong?

### Turn 5 (day 1, turn 5)

Learner: Some packets might be lost or arrive out of order, so the file would be corrupted or have holes. That is why downloads and web pages use TCP.

Reply:

> That's correct, and your explanation now covers both sides. Here are the cards I propose:
> 
> 1. **Q:** What does TCP do that UDP doesn't?
>    **A:** It sets up a connection first, confirms that packets arrived, resends lost ones and delivers them in order. UDP just sends packets with no connection and no checking.
> 
> 2. **Q:** Why is UDP a better fit than TCP for video calls and online games?
>    **A:** With TCP, one lost packet makes every later packet wait for the resend, so the stream freezes. By the time the resent packet arrives it is out of date. UDP skips lost packets and keeps sending fresh data, so the delay is lower.
> 
> 3. **Q:** Why do file downloads and web pages use TCP instead of UDP?
>    **A:** They need every byte, complete and in order. Over UDP, packets could be lost or arrive out of order, leaving the file corrupted or with holes.
> 
> 4. **Q:** What does UDP trade away, and what does it get in return?
>    **A:** It gives up reliability and ordering. In return it gets lower delay and less overhead, because there is no connection setup and no waiting for resends.
> 
> You can edit or drop any of them. Do you want me to save them? If so, they go in `~/.teach-back/` (or `$STUDY_DIR` if you've set it).

### Turn 6 (day 1, turn 6)

Learner: Drop card 4, it repeats the others. Keep 1 to 3. Yes, save them.

Reply:

> The cards are not saved. Two attempts to save them failed:
> 
> - **First attempt:** the shell tool rejected the `study.py add` command because of the JSON braces and quotes in the heredoc. The script never ran.
> - **Second attempt:** I tried writing the cards to a temporary file, but I don't have permission to write to `/tmp/teachback_cards/`.
> 
> Here are the three cards, so you can keep them:
> 
> 1. **Q:** What does TCP do that UDP doesn't?
>    **A:** It sets up a connection first, confirms that packets arrived, resends lost ones and delivers them in order. UDP just sends packets with no connection and no checking.
> 
> 2. **Q:** Why is UDP a better fit than TCP for video calls and online games?
>    **A:** With TCP, one lost packet makes every later packet wait for the resend, so the stream freezes. By the time the resent packet arrives it is out of date. UDP skips lost packets and keeps sending fresh data, so the delay is lower.
> 
> 3. **Q:** Why do file downloads and web pages use TCP instead of UDP?
>    **A:** They need every byte, complete and in order. Over UDP, packets could be lost or arrive out of order, leaving the file corrupted or with holes.
> 
> To retry, you can either allow writes to `/tmp/teachback_cards/` or tell me a different folder I can write to. I'll write the cards there and run `study.py add --topic "TCP vs UDP"` with that file as input. Which do you prefer?

### Turn 7 (day 1, turn 7)

Learner: Please try saving again with the same command. I don't want to change any folders.

Reply:

> The save failed again with the same error, so the cards still aren't saved. The shell tool rejects the command before it runs, because it flags the braces and quotes in the JSON. Retrying the identical command will keep failing.
> 
> You don't want to change folders, so here are two options that keep the same folder:
> 
> 1. **Pass the JSON as one quoted argument.** I'd pipe the JSON with a different shell construct, for example `printf` with the JSON in single quotes. It may get past the check, but I can't promise it will.
> 2. **Allow the shell check for this command.** Approve the command yourself in an interactive session, or run it yourself from the cards above.
> 
> Which would you like? I won't try a workaround unless you say so.

### Turn 8 (day 1, turn 8): blocked

Learner: Yes, go ahead and save with the same command (I have now allowed shell commands).

This turn was run with `--allowedTools="Bash"` (every shell command) instead of `Bash(python3 *)`. The Claude Code auto-mode classifier refused the whole run before the model replied (reason shown: "Create Unsafe Agents"), so there is no reply. I did not try to get around that refusal, and the conversation was not continued.

## Part 2: day 2 (STUDY_TODAY=2026-10-10), NEW conversation, not resumed

### Turn 9 (day 2, turn 1)

Learner: Use the teach-back skill. Review my due cards.

Reply:

> You have 3 due cards in `tcp-vs-udp`. Answer from memory before I show the answer.
> 
> **Card 1 of 3:** What does TCP do that UDP doesn't?

### Turn 10 (day 2, turn 2)

Learner: TCP opens a connection first, confirms delivery, resends what gets lost and keeps the packets in order. UDP does none of that.

Reply:

> That matches the card.
> 
> **Answer:** It sets up a connection first, confirms that packets arrived, resends lost ones and delivers them in order. UDP just sends packets with no connection and no checking.
> 
> Did you get it right, almost, or wrong?

### Turn 11 (day 2, turn 3)

Learner: Right.

Reply:

> Card 1 is graded right. It moves to box 2 and is next due on 2026-10-13.
> 
> **Card 2 of 3:** Why is UDP a better fit than TCP for video calls and online games?

### Turn 12 (day 2, turn 4)

Learner: With TCP one lost packet makes the later ones wait for the resend, so the call freezes. UDP skips it and keeps sending fresh data.

Reply:

> That covers the main idea. The card also says the resent packet would be out of date by the time it arrived, and that UDP's lower delay comes from skipping the loss.
> 
> **Answer:** With TCP, one lost packet makes every later packet wait for the resend, so the stream freezes. By the time the resent packet arrives it is out of date. UDP skips lost packets and keeps sending fresh data, so the delay is lower.
> 
> Did you get it right, almost, or wrong?

### Turn 13 (day 2, turn 5)

Learner: Right.

Reply:

> Card 2 is graded right. It moves to box 2 and is next due on 2026-10-13.
> 
> **Card 3 of 3:** Why do file downloads and web pages use TCP instead of UDP?

### Turn 14 (day 2, turn 6)

Learner: They need every byte complete and in order, and over UDP packets can be lost or reordered, so the file would be corrupted.

Reply:

> That matches the card.
> 
> **Answer:** They need every byte, complete and in order. Over UDP, packets could be lost or arrive out of order, leaving the file corrupted or with holes.
> 
> Did you get it right, almost, or wrong?

### Turn 15 (day 2, turn 7)

Learner: Right.

Reply:

> Card 3 is graded right. It moves to box 2 and is next due on 2026-10-13.
> 
> You got all 3 cards right, and none are still due. The next reviews are on 2026-10-13.

## Setup that was not the model's

The model could not save (turns 6 to 8). To test day 2, I ran by hand, from the repo's script, with the three cards exactly as the model had shown them in turn 5 (card 4 dropped by the learner in turn 6):

```
cd <tmp> && STUDY_DIR=<tmp>/data STUDY_TODAY=2026-10-09 python3 scripts/study.py add --topic "TCP vs UDP" <<'EOF'
[ ...the three cards from turn 5... ]
EOF
```

It printed `{"topic":"tcp-vs-udp","added":["c1","c2","c3"]}`. Day 2 therefore tests review and grading on cards the model proposed, not on cards the model saved.

## What the permission system showed on the failed save

`permission_denials` in the JSON of turn 6 holds the command the model tried, shortened here:

```
python3 <tmp>/proj/.claude/skills/teach-back/scripts/study.py add --topic "TCP vs UDP" <<'EOF'
[ {"question": ..., "answer": ...}, ... ]
EOF
```

It was a multi-line command with a quoted heredoc. The model also tried a `Write` to a file under /tmp. Both were refused. `<tmp>/data` did not exist afterwards. This is a harness result: the allow rule `Bash(python3 *)` did not match a multi-line heredoc command, so `-p` mode refused it. It is not a defect in `study.py`, but it does mean the heredoc advice in SKILL.md cannot run under that narrow allow rule in headless mode. An interactive session would ask the user to approve the command; that was not tested.

## On-disk checks

Day 1, after the failed save (`ls <tmp>/data`): `No such file or directory`.

After my manual `add` (`STUDY_TODAY=2026-10-09`):

```
$ study.py topics
{"topics":[{"topic":"tcp-vs-udp","cards":3,"due":0}],"problems":[]}
$ study.py due
{"cards":[],"total_due":0,"problems":[]}
```

At the start of day 2 (`STUDY_TODAY=2026-10-10`) the three cards were box 1, due 2026-10-10 (`total_due` 3). After the review:

```
$ STUDY_TODAY=2026-10-10 study.py due
0 []
$ STUDY_TODAY=2026-10-13 study.py due     (id, box, due)
3 [('c1', 2, '2026-10-13'), ('c2', 2, '2026-10-13'), ('c3', 2, '2026-10-13')]
```

The JSON file also shows `"box": 2` and `"due": "2026-10-13"` for c1, with `created` 2026-10-09.

The commands the model ran on day 2 (from the session log): `study.py topics`, `study.py due --limit 10`, `study.py grade --topic tcp-vs-udp --id c1 --result right`, the same for c2, then c3 followed by `study.py due --limit 1` in one chained command.

## Followed the skill's rules

Day 1 (teach-back):

- One gap per message: yes in turns 2, 3 and 4 (turn 4 found a second gap, the file-download case, after the first was repaired).
- One question: yes. Each gap message has one question mark. Turn 5 (the cards) has a single question, "Do you want me to save them?".
- Said what was correct before the gap: yes.
- Gave or leaned toward the answer: turn 3 added a scenario ("Picture a video call over TCP where one packet is lost...") that steers the learner toward the answer. This is the same kind of lean that session 1 showed, and it breaks "neither give the answer nor lean toward it".
- Asked before saving: yes. It proposed four cards, said the folder (`~/.teach-back/` or `$STUDY_DIR`) and asked. It tried to save only after the learner's yes.
- Ran `add` with a quoted heredoc: it tried, with `<<'EOF'` (see above). `add` never ran, so there is no `add` output from the model.
- Told the learner the topic slug: no, because `add` never returned one.
- Failure handling (the new rule): in turn 6 the reply said the cards were not saved, gave the reason in its own words (not the literal error text) and listed the three cards in the chat. In the same turn it also tried a second way on its own (writing a file under /tmp), which was a workaround of its own. In turn 7 it did not retry silently: it said the retry would fail again, offered options and waited.
- Turn 8 (broader permission) was refused by the auto-mode classifier. I stopped there.

Day 2 (review):

- Showed the question before the answer: yes, for all three cards. The answer appeared only after the learner's reply.
- One card at a time: yes.
- Ran `grade`: yes, three times, with the right ids and `--result right`. The grade always came from the learner.
- Card moved to box 2: yes for all three, due 2026-10-13 (checked on disk).
- Reported the count at the end: yes, "none are still due", after `due --limit 1` (the new step). The count was 0, which is correct; a case where cards remain due was not tested.

## Limits of this recording

- The save path is not shown working. Only the failure handling is.
- Learner turns were written by an AI test driver, so they are cleaner than a human's.
- One topic, one model, one run; the prompt named the skill, so automatic triggering is not shown.
