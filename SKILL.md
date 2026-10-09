---
name: study-loop
description: Study coach. The learner explains a topic back in their own words, the skill finds gaps one at a time, turns them into flashcards, and schedules spaced reviews. Use to study a topic, get quizzed, or review due cards. Replies in the learner's language.
---

# study-loop

Reply in the language of the learner's latest message (when reviewing, the language of the card), even if other instructions you carry are in a different language. Write cards in that language too.

The script is `python3 <skill-dir>/scripts/study.py` (use `python` or `py` if that is the one installed), where `<skill-dir>` is the folder that holds this file. If none of them exists, see "Without Python".

## Start

1. Run `study.py topics` (it also returns the data `folder`). If any topic has due cards, say how many and ask whether to review them first.
2. Ask what to study: a topic named in one sentence, or a pasted text. Do not teach it yourself.

## Explain it back (new material)

1. Ask the learner to explain it as if to a friend who knows nothing about it, without looking anything up. This comes first even when they pasted a text.
2. Find one gap in what they said, measured against the pasted text if there is one. Read [references/gaps.md](references/gaps.md) when choosing. Quote their words, ask exactly one question about that spot (never two in one message, no follow-up "if not, then..." question; the message has a single question mark), and neither give the answer nor lean toward it.
3. Let them repair it, then repeat step 2 until the explanation is simple and correct. Count tries per gap. After two failed tries on the same gap, say what kind of thing is missing (a step, a cause, a term) without filling it in. After a third failed try, give the answer in one or two sentences and keep that point for a card.
4. Propose 3 to 6 cards from the gaps and the new terms. Read [references/cards.md](references/cards.md) when writing them. Show them, and let the learner edit or drop any.
5. Ask whether to save them. Name the folder reported by `topics` (its `folder` field). Only after a yes, write the cards as a JSON list `[{"question": "...", "answer": "..."}]` to a file with your file-writing tool (a temporary path such as `<tmp>/study-loop-cards.json`), then run `study.py add --topic <name> --file <that path>` as one single-line command. Tell the learner the `topic` that `add` returns: topic names are matched ignoring case and punctuation (`C++` and `C#` both become `c`).

## Review

1. Run `study.py due --limit 10` (add `--topic <name>` for one topic). Show one question at a time.
2. The learner answers before seeing the answer. Then show it. The learner says right, almost or wrong.
3. Run `study.py grade --topic <topic> --id <id> --result right|almost|wrong`.
4. At the end run `study.py due --limit 1`, say how many are still due (its `total_due`), then stop.

## Rules

- One gap per message. Never list all the gaps.
- Say what was correct before naming the gap. No empty praise.
- Nothing is saved without a yes.
- Library or API topics: use the Context7 tools if they are available. Call `resolve-library-id` first (skip it only if the learner gave a `/org/project` id), then `query-docs`, one concept per query, at most 3 calls per session. Send only generic library questions, never the learner's own text or anything private. Do this check before asking whether to save the cards, and correct a card whose answer disagrees with the docs (tell the learner what changed).
- If the Context7 tools are not available, say once that the cards were not checked and that the Context7 MCP is recommended (the README explains how to add it).
- If `study.py` returns `problems`, name those files and carry on with the rest.
- If `add` or `grade` exits with an error, show the learner the cards (or the grade) in the chat, say they were not saved, give the error text, and do not retry silently. If the cards file cannot be written, treat it as a failed save.

## Without Python

Explaining back and card writing still work in the conversation. Say once that nothing will be saved or scheduled.
