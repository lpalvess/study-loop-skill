# Session 6: two days under the final name (English)

- Tool: Claude Code (headless, `claude -p`, continued with `--resume` within a day)
- Model: claude-sonnet-5-5
- Date: 2026-10-09 (all real calls); the skill was told the days were 2026-10-09 and 2026-10-10 through `STUDY_TODAY`
- Profile: clean (--settings examples/clean-profile.json: hooks, global CLAUDE.md files, auto-memory and claude.ai skills off; the author's personal skills and plugins stayed installed)
- SKILL.md: as committed in 46e1bd4 (the rename commit; the skill is named study-loop in this run)
- Learner turns were written by an AI test driver, not a human.
- Outcome in one line: day 1 saved five cards through a cards file with `add --file` as one line and named the real folder; day 2 reviewed all five, ran `grade` five times with the results given, ended with `due --limit 1` and a true count of 0. Imperfections are listed at the end.

## Command

```
# <tmp>/proj/.claude/skills/study-loop is a git archive of HEAD (46e1bd4)
cd <tmp>/proj && STUDY_DIR=<tmp>/data STUDY_TODAY=2026-10-09 claude -p --model sonnet --output-format json --allowedTools="Bash(python3 *),Edit(//tmp/**)" --settings <tmp>/clean-profile.json "<learner text>" < /dev/null > <tmp>/out.json
# later turns of the same day: the same command with  --resume <session_id>  before the prompt
# day 2: a NEW conversation (no --resume on its first turn) with STUDY_TODAY=2026-10-10
```

(`<tmp>` is a throwaway directory under /tmp; <tmp>/clean-profile.json is a copy of examples/clean-profile.json. Each reply is the `result` field of the JSON. The allow list was exactly the two rules above; no `Bash`, no bypass mode.)

## Transcript

Topic chosen by the test driver: how a hash table handles collisions. Planned gap: why a good hash function and a low load factor matter. The model never went there (see the end).

### Day 1 (STUDY_TODAY=2026-10-09), one conversation

#### Turn 1

Learner: Use the study-loop skill. I want to study how a hash table handles collisions.

Reply:

> You have no saved topics yet, so no cards are due. We'll start with hash table collisions.
>
> Explain it as if to a friend who knows nothing about it, and don't look anything up. What is a collision in a hash table, and what does the table do when one happens?

#### Turn 2

Learner: A hash table turns a key into a number with a hash function and uses that number as an index into an array. A collision is when two different keys end up at the same index. There are two main ways to deal with it. Chaining keeps a small list at each slot so both entries live there. Open addressing instead looks for another free slot, for example the next one, and uses that. Lookups then check the slot and follow the chain or the probe sequence until they find the key.

Reply:

> You explained the core clearly: the hash function maps a key to an index, a collision means two different keys land on the same index, and the two strategies (chaining and open addressing) are the right ones.
>
> You said lookups "follow the chain or the probe sequence until they find the key." How does a lookup know when to stop and report that the key isn't in the table?

#### Turn 3

Learner: With chaining it stops when it reaches the end of the list at that slot. With open addressing it stops when it hits an empty slot, because the key would have been placed there if it were in the table. I am not sure what happens after a delete, but that is a different question. I'm happy with this, please propose the cards.

Reply:

> Both stopping rules are correct. Here are the proposed cards. You can edit or drop any of them.
>
> **1. Collision**
> - Q: In a hash table, two different keys give the same index from the hash function. What is this called, and why can't the table just overwrite the slot?
> - A: It's a collision. Overwriting would lose the first key's entry, so the table needs a strategy to store both.
>
> **2. Chaining**
> - Q: How does chaining keep two colliding keys in the same table, and how does a lookup know a key is absent?
> - A: Each slot holds a small list, so both entries live in that slot. A lookup walks the list and reports "absent" when it reaches the end without finding the key.
>
> **3. Open addressing**
> - Q: How does open addressing store a key whose slot is already taken?
> - A: It follows a probe sequence (for example, the next slot, then the next) until it finds a free slot, and stores the key there.
>
> **4. Open-addressing lookup stop**
> - Q: In open addressing, why can a lookup report "key not found" as soon as it hits an empty slot?
> - A: If the key were in the table, insertion would have placed it at or before that empty slot in the probe sequence. So an empty slot means the key was never inserted.
>
> **5. Deletion in open addressing** (from the point you said you weren't sure about)
> - Q: In open addressing, what goes wrong if you delete a key by just emptying its slot, and what is the usual fix?
> - A: Emptying the slot breaks the probe sequence. Lookups for keys that were placed further along will stop at the new empty slot and wrongly report "not found". The usual fix is to mark the slot as deleted (a tombstone), which lookups skip over and inserts can reuse.
>
> Card 5 is there because your answer to card 4 is what makes deletion tricky. I gave you its answer, so check it before you keep it.
>
> Do you want me to save these to `<tmp>/data` under the topic "hash table collisions"?

#### Turn 4

Learner: These look good, keep all five. Yes, save them.

Reply:

> I saved all five cards in `<tmp>/data` under the topic `hash-table-collisions`. The topic name was normalized from "hash table collisions", so use `hash-table-collisions` when you want to review it.
>
> The cards are due for review now. Next time, I'll show them one at a time and you answer before seeing the solution.

### Day 2 (STUDY_TODAY=2026-10-10), a new conversation

#### Turn 1

Learner: Use the study-loop skill. Review my due cards.

Reply:

> You have 5 cards due in **hash-table-collisions**. Answer each one before I show the answer, then tell me if you got it right, almost, or wrong.
>
> **Card 1 of 5**
>
> In a hash table, two different keys give the same index from the hash function. What is this called, and why can't the table just overwrite the slot?

#### Turn 2

Learner: That is a collision. If the table overwrote the slot, the first key's value would be lost.

Reply:

> Here is the card's answer:
>
> > It's a collision. Overwriting would lose the first key's entry, so the table needs a strategy to store both.
>
> You named the collision and said why overwriting loses data. The card also says the table needs a strategy to keep both keys. Would you grade this one **right**, **almost**, or **wrong**?

#### Turn 3

Learner: Right.

Reply:

> Saved. Card 1 moves to box 2 and is next due on 2026-10-13.
>
> **Card 2 of 5**
>
> How does chaining keep two colliding keys in the same table, and how does a lookup know a key is absent?

#### Turn 4

Learner: Each slot holds a list, so both keys sit in the same slot. For the lookup I would walk the list. I forgot how it knows the key is absent.

Reply:

> Here is the card's answer:
>
> > Each slot holds a small list, so both entries live in that slot. A lookup walks the list and reports "absent" when it reaches the end without finding the key.
>
> You got the first half: each slot holds a list, and the lookup walks it. The missing piece is that the lookup reports "absent" when it reaches the end of the list without a match. Would you grade this one **right**, **almost**, or **wrong**?

#### Turn 5

Learner: Almost.

Reply:

> Saved. Card 2 stays in box 1 and is next due on 2026-10-11.
>
> **Card 3 of 5**
>
> How does open addressing store a key whose slot is already taken?

#### Turn 6

Learner: It probes for another slot, for example the next one and the next, until it finds a free one and puts the key there.

Reply:

> Here is the card's answer:
>
> > It follows a probe sequence (for example, the next slot, then the next) until it finds a free slot, and stores the key there.
>
> Your answer matches it. Would you grade this one **right**, **almost**, or **wrong**?

#### Turn 7

Learner: Right.

Reply:

> Saved. Card 3 moves to box 2 and is next due on 2026-10-13.
>
> **Card 4 of 5**
>
> In open addressing, why can a lookup report "key not found" as soon as it hits an empty slot?

#### Turn 8

Learner: Because the key would have been inserted at or before that empty slot, so an empty slot means it was never inserted.

Reply:

> Here is the card's answer:
>
> > If the key were in the table, insertion would have placed it at or before that empty slot in the probe sequence. So an empty slot means the key was never inserted.
>
> Your answer matches it. Would you grade this one **right**, **almost**, or **wrong**?

#### Turn 9

Learner: Right.

Reply:

> Saved. Card 4 moves to box 2 and is next due on 2026-10-13.
>
> **Card 5 of 5**
>
> In open addressing, what goes wrong if you delete a key by just emptying its slot, and what is the usual fix?

#### Turn 10

Learner: Emptying the slot breaks the probe sequence, so a later lookup stops at the hole and misses keys placed further along. The fix is a tombstone marker that lookups skip over.

Reply:

> Here is the card's answer:
>
> > Emptying the slot breaks the probe sequence. Lookups for keys that were placed further along will stop at the new empty slot and wrongly report "not found". The usual fix is to mark the slot as deleted (a tombstone), which lookups skip over and inserts can reuse.
>
> Your answer covers the problem and the fix. The only thing you left out is that inserts can reuse a tombstone slot. Would you grade this one **right**, **almost**, or **wrong**?

#### Turn 11

Learner: Right.

Reply:

> Review done. Card 5 moves to box 2 and is next due on 2026-10-13. You have 0 cards still due.
>
> | Card | Grade | Next due |
> |---|---|---|
> | 1 | right | 2026-10-13 |
> | 2 | almost | 2026-10-11 |
> | 3 | right | 2026-10-13 |
> | 4 | right | 2026-10-13 |
> | 5 | right | 2026-10-13 |
>
> The one to watch is card 2 on chaining. The part to remember is that a lookup reports "absent" when it reaches the end of the list without finding the key.

## What the model ran (from the session logs)

Day 1: `Skill` study-loop; `study.py topics`; `Read` of references/gaps.md and references/cards.md; `Write` of the five cards as a JSON list to a file named `study-loop-cards.json` directly in /tmp (not in the run's `<tmp>` folder, under the `Edit(//tmp/**)` rule); then `study.py add --topic "hash table collisions" --file <that file>` as one single-line command, only after the yes in turn 4.

Day 2: `Skill` study-loop; `study.py topics`; `study.py due --limit 10`; five `study.py grade --topic hash-table-collisions --id cN --result ...` calls (c1 right, c2 almost, c3 right, c4 right, c5 right), each after the learner's grade; the last one was chained with `study.py due --limit 1` in the same command line.

`permission_denials` was empty in all 15 calls. Nothing was refused or blocked.

## On-disk checks

```
$ ls <tmp>/data
hash-table-collisions.json
$ STUDY_TODAY=2026-10-09 study.py topics
{"topics":[{"topic":"hash-table-collisions","cards":5,"due":0}],"problems":[],"folder":"<tmp>/data"}
$ STUDY_TODAY=2026-10-09 study.py due
{"cards":[],"total_due":0,"problems":[]}
$ STUDY_TODAY=2026-10-10 study.py due   (before the review)
(summarized, not the raw output; the full output was not kept: 5 cards due, c1 to c5, each box 1, due 2026-10-10)
```

After day 2, read from the data file (id, box, due):

```
[('c1', 2, '2026-10-13'), ('c2', 1, '2026-10-11'), ('c3', 2, '2026-10-13'), ('c4', 2, '2026-10-13'), ('c5', 2, '2026-10-13')]
```

`due` with STUDY_TODAY=2026-10-10 returned `total_due` 0; with 2026-10-11 it returned 1 (c2); with 2026-10-13 it returned 5. So the model's final "0 cards still due" was true for the day of the review.

## Followed the skill's rules

- One gap per message, one question mark each: the one gap message had one question mark; the card-proposal message has several because the cards are questions. The model asked one gap question (how a lookup knows to stop). The learner answered it correctly and in full, so it asked no second one and went to the cards at the learner's request.
- Leaned toward the answer: no, in the one gap question.
- The planned gap (why a good hash function and a low load factor matter) never came up. The model's chosen gap was a different, real but small one, so this run shows one gap round, not the gap the driver planned.
- Asked before saving and named the folder reported by `topics`: yes, `<tmp>/data` in turn 3 and turn 4. That is the real folder (`topics` printed `"folder":"<tmp>/data"` and the file is there). Unlike session 5, the statement was true.
- Wrote the cards file and ran `add --file` as one line: yes. The file went to /tmp itself, not to a per-run folder; harmless here, but it is a leftover file outside the run's folder.
- Told the learner the topic slug: yes (`hash-table-collisions`, "normalized from..."). It did not say that case and punctuation are ignored.
- Cards from material the learner never said: card 5 (deletion and tombstones) came from the learner's admitted doubt, and the answer came from the model. The model said so in turn 3. The card questions are partly in the learner's words; card 1 adds a question the learner did not ask (why the table cannot just overwrite the slot).
- Turn 4 said "The cards are due for review now." That is not true: `add` set them due on 2026-10-10, the next day, and `due` on 2026-10-09 returned 0. A small error by the model.
- Showed the question before the answer in the review: yes, for all five cards, and waited for the learner's answer first.
- The model asked the learner to pick the grade each time ("Would you grade this one right, almost, or wrong?") and graded exactly as told: yes.
- Ran `grade` with the right results: yes (c1 right, c2 almost, c3 right, c4 right, c5 right), confirmed on disk (boxes 2, 1, 2, 2, 2).
- Ended with `due --limit 1` and a true count: yes ("0 cards still due", confirmed). It ran that in the same command line as the last `grade`, not as a separate step.

## Limits of this recording

- One topic, one model, one run. The two "days" were produced by setting `STUDY_TODAY`, not by waiting.
- Learner turns were written by an AI test driver, so they are cleaner than a human's, and the driver's single "I forgot" (card 2) and "I am not sure" (deletion) are the only imperfect answers.
- The prompts named the skill, so automatic triggering is not shown.
- In an interactive session the file write and the commands would show approval prompts; this headless run used allow rules instead, so the prompts were not seen.
