# teach-back

A study skill for AI coding assistants. You explain a topic back in your own words. The skill finds the weak spot, one at a time, turns weak spots into flashcards, and schedules reviews so you see each card again before you forget it.

It answers in the language you write in.

## Install

Claude Code: from the folder that contains the `teach-back` folder, copy it into your skills directory.

```bash
cp -r teach-back ~/.claude/skills/
```

Saving and scheduling need Python 3.8 or newer. Without Python the conversation part still works, but nothing is saved.

Only Claude Code has been tested. Other tools that read the Agent Skills format may work.

## Use

- "Use teach-back: I want to study how DNS works."
- Paste a text and say you want to study it.
- "Use teach-back: review my due cards."

Then explain the topic in your own words when the skill asks.

## How it works

1. You explain the topic without looking anything up.
2. The skill quotes you and asks one question about one gap. It does not give the answer.
3. When the explanation holds up, it proposes 3 to 6 cards. You edit or drop any.
4. You decide whether to save them.
5. In reviews you answer first, then see the answer, then say right, almost or wrong.

Reviews use five boxes with gaps of 1, 3, 7, 16 and 35 days. Right moves a card up one box. Almost keeps it in its box. Wrong sends it back to box 1.

## Your data

Cards live in `~/.teach-back/`, one JSON file per topic. Set `STUDY_DIR` to use another folder. Nothing is saved before you say yes. Nothing leaves your computer: no network calls and no accounts.

## Token cost

| What | Approx. tokens |
|---|---|
| Listing (description, every turn) | 59 |
| Invocation (SKILL.md) | 734 |
| references/cards.md (only when needed) | 187 |
| references/gaps.md (only when needed) | 201 |

Counted as words x 1.35. The guides load only when the skill needs them.

## Recorded runs

Real runs in `examples/`, each with the tool and model used.

- `examples/session-1-topic.md`: a topic named in one sentence, in English; it followed the rules only partly, because the reply leaned toward the answer and its question targeted a different gap than the learner's.
- `examples/session-2-pasted-text.md`: a pasted text, in Portuguese; it asked the learner to explain from memory first and replied in Portuguese, with a mild lean toward the text's structure.
- `examples/session-3-review.md`: a review of one due card; it showed the question only and waited for the learner's answer.

Known limits: the runs were made with Claude Code and one model, `claude-sonnet-5-5`, and the skill was used in all three. Every prompt named the skill explicitly, so the runs show how it behaves when invoked by name; they do not show that it starts on its own from its description. Session 1 followed the one-question rule only on its third recording and its reply still leaned toward the answer, so it is not typical of a single attempt. An earlier recording in the author's own environment replied in Portuguese to an English request, and the cause was not isolated. The recordings used a clean profile (`examples/clean-profile.json`; the author's personal skills and plugins stayed installed) and the SKILL.md as committed in 35c047b.

## Tests

```bash
python3 -m unittest discover -s tests -v
python3 tools/check_budget.py .
```

## License

MIT
