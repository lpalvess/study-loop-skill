# study-loop

A study skill for AI coding assistants. You explain a topic back in your own words. The skill finds the weak spot, one at a time, turns weak spots into flashcards, and schedules reviews so you see each card again before you forget it.

It answers in the language you write in.

## Install

Claude Code: from the folder that contains the `study-loop` folder, copy it into your skills directory.

```bash
cp -r study-loop ~/.claude/skills/
```

Saving and scheduling need Python 3.8 or newer (`python3`, or `python`/`py` if that is the name on your system). The code was written for 3.8 and tested on Python 3.12.3 on Linux. Windows and macOS have not been tested. Without Python the conversation part still works, but nothing is saved.

Only Claude Code has been tested. Other tools that read the Agent Skills format may work.

## Use

- "Use study-loop: I want to study how DNS works."
- `Use study-loop: study this text: <paste it here>`
- "Use study-loop: review my due cards."

Then explain the topic in your own words when the skill asks.

Topic names are matched ignoring case and punctuation (`C++` and `C#` both become `c`). Use one session at a time per topic: two sessions saving the same topic at once can lose an update.

## How it works

1. You explain the topic without looking anything up.
2. The skill quotes you and asks one question about one gap. It does not give the answer.
3. When the explanation holds up, it proposes 3 to 6 cards. You edit or drop any.
4. You decide whether to save them. After a yes, the model writes the cards to a temporary JSON file and runs `study.py add --topic <name> --file <that file>` as one single-line command (`--file -` or no `--file` reads stdin).
5. In reviews you answer first, then see the answer, then say right, almost or wrong.

Reviews use five boxes with gaps of 1, 3, 7, 16 and 35 days. Right moves a card up one box. Almost keeps it in its box. Wrong sends it back to box 1.

## Your data

Cards live in `~/.study-loop/`, one JSON file per topic. Set `STUDY_DIR` to use another folder. Nothing is saved before you say yes. `study.py` makes no network calls and there are no accounts. Your conversation still goes to your AI provider, and the optional Context7 check queries that service.

## Token cost

| What | Approx. tokens |
|---|---|
| Listing (description, every turn) | 59 |
| Invocation (SKILL.md) | 888 |
| references/cards.md (only when needed) | 187 |
| references/gaps.md (only when needed) | 201 |

Counted as words x 1.35. The guides load only when the skill needs them.

## Recorded runs

Real runs in `examples/`, each with the tool and model used. Sessions 1 to 5 were recorded when the skill was named teach-back, so their prompts and paths say teach-back; they are kept verbatim.

- `examples/session-1-topic.md`: a topic named in one sentence, in English; it followed the rules only partly, because the reply leaned toward the answer and its question targeted a different gap than the learner's.
- `examples/session-2-pasted-text.md`: a pasted text, in Portuguese; it asked the learner to explain from memory first and replied in Portuguese, with a mild lean toward the text's structure.
- `examples/session-3-review.md`: a review of one due card; it showed the question only and waited for the learner's answer.
- `examples/session-4-multi-turn.md`: one conversation that teaches back (English) and a second that reviews three cards. The review worked: the model showed each question before its answer, ran `grade` three times, and all three cards moved to box 2 on disk. The save did not work in that setup: the model tried `add` with a quoted heredoc, the headless permission rule refused it, and the cards were added by hand before the review. The model told the learner the cards were not saved. One of its gap questions leaned toward the answer.

- `examples/session-5-save-through-file.md`: one conversation, day 1 only, on the SKILL.md of 848fb89 (after `add --file`, dc03ea8). The model ran three gap rounds, not one. The save worked: after the learner's yes the model wrote the cards to a file with its Write tool, ran `add --file` as a single line, and five cards landed on disk, with nothing added by hand. It did not repeat the note that topic names ignore case and punctuation, and it said the cards went to the default data folder (it named the old default folder `~/.teach-back/`) although the data was in `$STUDY_DIR`. This run was made before the `folder` field existed in the output of `topics` and `add`, which was added afterwards so the model can state the real folder; it was not re-recorded. The review of those cards was not re-run (session 4 covers review). The run used allow rules (`Bash(python3 *)` and `Edit(//tmp/**)`); an interactive session would show approval prompts instead, which were not tested.
- `examples/session-6-two-days.md`: two days on the final SKILL.md (46e1bd4), under the name study-loop, topic: how a hash table handles collisions. Day 1 saved five cards through a cards file with `add --file` as one line, and the model named the real data folder. Day 2 reviewed all five: the model showed each question first, ran `grade` five times with the results the learner gave (four right, one almost) and ended with `due --limit 1` and a true count of 0. Flaws: the model asked one gap question and the learner answered it fully, so the planned gap (hash function and load factor) never came up; the model wrote the cards file directly in /tmp; and it told the learner the new cards were due now when they were due the next day. Nothing was refused. Allow rules were the same two as in session 5.

Known limits:

- Scope
  - The runs were made with Claude Code and one model, `claude-sonnet-5-5`.
  - The skill was used in all six runs, and every prompt named it explicitly. The runs show how it behaves when invoked by name; they do not show that it starts on its own from its description.
- Which SKILL.md each run used (each recording ran on a different one)
  - Sessions 1 to 3: 35c047b (edited afterwards: python command, final due count, failed-save handling, topic names).
  - Session 4: 96dc307 (its save instruction, a quoted heredoc, was replaced afterwards by the cards file, so the save failure it records no longer describes the current SKILL.md).
  - Session 5: 848fb89 (edited afterwards: the `folder` field and the name of the folder in the save question).
  - Session 6: 46e1bd4, the final one.
  - Sessions 1 to 5 were recorded when the skill was named teach-back, so their prompts and paths say teach-back.
- Method
  - Learner turns in sessions 4 to 6 were written by an AI test driver, not a human.
  - The runs used headless allow rules, so interactive approval prompts were not tested.
  - The recordings used a clean profile (`examples/clean-profile.json`); the author's personal skills and plugins stayed installed.
- Reliability
  - Session 1 followed the one-question rule only on its third recording and its reply still leaned toward the answer, so it is not typical of a single attempt.
  - An earlier recording in the author's own environment replied in Portuguese to an English request, and the cause was not isolated.

## Tests

```bash
python3 -m unittest discover -s tests -v
python3 tools/check_budget.py .
```

## License

MIT
