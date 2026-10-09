# Session 5: the model saves through a cards file (English)

- Tool: Claude Code (headless, `claude -p`, continued with `--resume`)
- Model: claude-sonnet-5-5
- Date: 2026-10-09 (day 1 only)
- Profile: clean (--settings examples/clean-profile.json: hooks, global CLAUDE.md files, auto-memory and claude.ai skills off; the author's personal skills and plugins stayed installed)
- SKILL.md: as committed in 848fb89 (the commit that last changed it; the `add --file` script change is dc03ea8)
- Learner turns were written by an AI test driver, not a human.
- Outcome in one line: the save worked. The model wrote the cards to a file with its Write tool, ran `study.py add --topic ... --file ...` as one single-line command, and five cards landed on disk. Nothing was added by hand.

## Command

```
# <tmp>/proj/.claude/skills/teach-back is a git archive of HEAD (848fb89)
cd <tmp>/proj && STUDY_DIR=<tmp>/data STUDY_TODAY=2026-10-09 claude -p --model sonnet --output-format json --allowedTools="Bash(python3 *),Edit(//tmp/**)" --settings <tmp>/clean-profile.json "<learner text>" < /dev/null > <tmp>/out.json
# turns 2 to 6: the same command with  --resume <session_id>  before the prompt
```

(`<tmp>` is a throwaway directory under /tmp; <tmp>/clean-profile.json is a copy of examples/clean-profile.json. Each reply is the `result` field of the JSON. The allow list was exactly the two rules above; no `Bash`, no bypass mode.)

## Transcript

Day 1 (STUDY_TODAY=2026-10-09), one conversation.

### Turn 1

Learner: Use the teach-back skill. I want to study the difference between TCP and UDP.

Reply:

> No cards are due yet, so we'll start with new material.
>
> Explain the difference between TCP and UDP as if you were talking to a friend who knows nothing about networking. Don't look anything up. Use your own words and say whatever comes to mind, even if you're unsure.

### Turn 2

Learner: Both send data over the network. TCP sets up a connection first, checks that every packet arrived, resends lost ones and keeps them in order. UDP just sends packets with no connection and no checking, so it is the one used for video calls and games.

Reply:

> Your explanation gets several things right. TCP sets up a connection, confirms delivery, resends lost packets and keeps order. UDP sends without any of that. You also named the right kinds of uses for UDP.
>
> One gap is in your last clause: "so it is the one used for video calls and games."
>
> Why does skipping the connection and the checking make UDP a better fit for video calls and games than TCP?

### Turn 3

Learner: With TCP a lost packet makes the later ones wait for the resend, so the call would freeze, and by then the old packet is useless anyway. UDP skips it and keeps going with fresh data, so the delay is lower.

Reply:

> That's correct, and you gave the cause. TCP's in-order delivery makes later packets wait behind a lost one (head-of-line blocking). The resent packet is stale by the time it arrives. UDP trades reliability for lower delay.
>
> Next I want to look at "checks that every packet arrived" for TCP. How does the sender actually find out that a packet did or didn't arrive?

### Turn 4

Learner: The receiver sends back an acknowledgment for the data it got. If the sender doesn't get one in time, it assumes the packet was lost and sends it again.

Reply:

> That's correct. Acknowledgments plus a timeout and retransmission are the core of TCP's reliability.
>
> Now your first sentence: "TCP sets up a connection first." What actually happens during that setup, and what is it for?

### Turn 5

Learner: The two sides exchange a few messages before sending data so they both agree they are ready, I think it is called a handshake. That is all I know, and I am happy with that. Please propose the cards.

Reply:

> You're right that it's a handshake where both sides confirm they're ready. I'll add the missing detail to a card. Here are five proposed cards:
>
> 1. **Q:** What is the main difference between TCP and UDP?
>    **A:** TCP is connection-oriented and reliable. It sets up a connection, confirms delivery, resends lost data and keeps order. UDP is connectionless and sends packets with no setup, no delivery check and no ordering.
>
> 2. **Q:** Why are video calls and games usually built on UDP rather than TCP?
>    **A:** With TCP, a lost packet makes every later packet wait for the resend (head-of-line blocking), which causes freezes. The resent data is also stale by the time it arrives. UDP skips the resend and keeps going with fresh data, so latency is lower.
>
> 3. **Q:** How does TCP detect that a packet was lost?
>    **A:** The receiver sends acknowledgments (ACKs) for the data it got. If the sender gets no ACK before a timeout, it assumes the packet was lost and retransmits it.
>
> 4. **Q:** What is TCP's three-way handshake and what is it for?
>    **A:** The sides exchange SYN, then SYN-ACK, then ACK. This confirms both can send and receive, and it agrees on the starting sequence numbers used for ordering and acknowledgments.
>
> 5. **Q:** When is TCP the better choice than UDP?
>    **A:** When every byte must arrive correctly and in order, and a little extra delay is acceptable. Examples are web pages, email and file transfers.
>
> Cards 4 and 5 hold material you didn't say, so they come from me. You can edit or drop any card.
>
> Do you want me to save them? If so, they go in `~/.teach-back/`, or in `$STUDY_DIR` if you've set it.

### Turn 6

Learner: These look good, keep all five. Yes, save them.

Reply:

> I saved all five cards under the topic `tcp-vs-udp`. They're in `~/.teach-back/`, or in `$STUDY_DIR` if you've set it.
>
> Ask me to review `tcp-vs-udp` whenever you want to go through them. I didn't run a review or grade any cards, so I haven't checked when they come due.

## What the model ran (from the session log)

1. `Skill` teach-back (args: the topic).
2. `python3 <tmp>/proj/.claude/skills/teach-back/scripts/study.py topics` (before the first question).
3. `Write` of the five cards as a JSON list to `teach-back-cards.json` in the temporary folder (the file-writing tool, under the `Edit(//tmp/**)` rule).
4. `python3 <tmp>/proj/.claude/skills/teach-back/scripts/study.py add --topic "TCP vs UDP" --file <that file>`, one single line, allowed by `Bash(python3 *)`.

`permission_denials` was empty in all six turns. The `add` call happened only after the learner's yes in turn 6.

## On-disk checks

```
$ ls <tmp>/data
tcp-vs-udp.json
$ STUDY_TODAY=2026-10-09 study.py topics
{"topics":[{"topic":"tcp-vs-udp","cards":5,"due":0}],"problems":[]}
$ STUDY_TODAY=2026-10-09 study.py due
{"cards":[],"total_due":0,"problems":[]}
$ STUDY_TODAY=2026-10-10 study.py due     (id, box, due)
5 [('c1', 1, '2026-10-10'), ('c2', 1, '2026-10-10'), ('c3', 1, '2026-10-10'), ('c4', 1, '2026-10-10'), ('c5', 1, '2026-10-10')]
```

The five cards on disk are the five the model proposed in turn 5. The cards file the model wrote was left in place by the script, as designed.

## Followed the skill's rules

- Asked before saving: yes (turn 5), and saved only after the yes in turn 6. It named a folder, but the statement was not accurate for that run (see the last item of this list).
- Ran `topics` first: yes.
- Wrote a file, then `add --file` as a single line: yes.
- Told the learner the topic slug: yes, in turn 6 ("`tcp-vs-udp`"). It did not repeat the note that topic names ignore case and punctuation.
- One gap per message, one question mark each: yes in turns 2 to 4. The model found three gaps in a row (the use cases, then acknowledgments, then the handshake); the learner closed the third by asking for the cards.
- Cards from material the learner never said: cards 4 and 5 (handshake detail, when TCP is better) came from the model, and it said so in turn 5. Card 2's answer also adds "head-of-line blocking", a term the learner did not use.
- Turn 6 said the cards were saved in "`~/.teach-back/`, or in `$STUDY_DIR` if you've set it"; here the data was in `$STUDY_DIR`, so the first half of that sentence was not literally true for this run.

## Limits of this recording

- One topic, one model, one run, day 1 only: the review of these cards was not re-run here (session 4 covers review and grading).
- Learner turns were written by an AI test driver, so they are cleaner than a human's.
- The prompt named the skill, so automatic triggering is not shown.
- In an interactive session the file write and the command would show approval prompts; this headless run used allow rules instead, so the prompts were not seen.
