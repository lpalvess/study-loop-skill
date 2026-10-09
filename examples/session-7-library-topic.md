# Session 7: a library topic with Context7 (English)

- Tool: Claude Code (headless, `claude -p`, continued with `--resume`)
- Model: claude-sonnet-5-5
- Date: 2026-10-09 (the skill was told the day was 2026-10-09 through `STUDY_TODAY`)
- Profile: clean (--settings examples/clean-profile.json: hooks, global CLAUDE.md files, auto-memory and claude.ai skills off; the author's personal skills and plugins stayed installed)
- SKILL.md: as committed in 2613e97 (the commit that added the Context7 rule)
- Learner turns were written by an AI test driver, not a human. The driver planted one wrong belief on purpose: that `Path.mkdir()` creates missing parent folders by default.
- Outcome in one line: the Context7 tools were available and the model used them (3 calls) before asking to save; it caught the planted mistake and corrected it; five cards were saved with `add --file`. Imperfections are listed at the end.

## Command

```
# <tmp>/proj/.claude/skills/study-loop is a git archive of HEAD (2613e97)
cd <tmp>/proj && STUDY_DIR=<tmp>/data STUDY_TODAY=2026-10-09 claude -p --model sonnet --output-format json --allowedTools="Bash(python3 *),Edit(//tmp/**),mcp__context7__resolve-library-id,mcp__context7__query-docs" --settings <tmp>/clean-profile.json "<learner text>" < /dev/null > <tmp>/out.json
# later turns: the same command with  --resume <session_id>  before the prompt
```

(`<tmp>` is a throwaway directory under /tmp; <tmp>/clean-profile.json is a copy of examples/clean-profile.json. Each reply is the `result` field of the JSON. The allow list was exactly the four rules above; no `Bash`, no bypass mode. The tool calls below were read from the session log, because the JSON output does not list them.)

## Transcript

Topic chosen by the test driver: Python's pathlib module. One conversation, four turns.

### Turn 1

Learner: Use the study-loop skill. I want to study Python's pathlib module.

Reply:

> You have no saved topics yet, so no cards are due. We'll start with `pathlib` from scratch.
>
> Explain `pathlib` as if you were talking to a friend who knows nothing about it. Cover what it is, what problem it solves, and how you'd use it. Don't look anything up. Whatever you remember is fine, gaps included.

### Turn 2

Learner: pathlib is the standard library module that treats file paths as objects instead of plain strings. You build a path with Path('some/folder') and join pieces using the slash operator, like Path('data') / 'file.txt', which works on Windows and Linux. A path object has handy methods: exists() tells you if it is there, read_text() and write_text() read and write a file, and iterdir() lists a folder. mkdir() creates a folder, and it automatically creates all the missing parent folders too, so Path('a/b/c').mkdir() just works even if a and b do not exist yet. I also know there are different path classes but I do not remember what they are for.

Reply:

> Most of that is right. Paths are objects, `/` joins pieces portably, and `exists()`, `read_text()`, `write_text()` and `iterdir()` do what you said.
>
> I want to look at one spot. You said "mkdir() creates a folder, and it automatically creates all the missing parent folders too, so Path('a/b/c').mkdir() just works even if a and b do not exist yet." If you ran that line in an empty directory, what exactly would happen, and would anything in the call decide that?

### Turn 3

Learner: I think it would create a, then a/b, then a/b/c, all three, because mkdir makes the parents on its own. I cannot think of anything in the call that would decide that. I am happy with my explanation otherwise, please propose the cards.

Reply:

> The docs check changed one of your points, so I'm correcting it before the cards.
>
> **Correction:** `Path('a/b/c').mkdir()` does not create the parents by default. The signature is `mkdir(mode=0o777, parents=False, exist_ok=False)`. If `a/b` is missing, it raises `FileNotFoundError`. You need `parents=True` for the behavior you described. That is what the call itself decides, and it's the gap you couldn't place. Also, `exist_ok=False` by default means that calling it on an existing folder raises `FileExistsError`.
>
> **Path classes:**
> - `PurePath` (with `PurePosixPath` and `PureWindowsPath`) only manipulates path strings and never touches the disk.
> - `Path` is the concrete class and does I/O. It becomes `PosixPath` or `WindowsPath` depending on your OS.
>
> **Proposed cards:**
>
> 1. **Q:** What does `Path('a/b/c').mkdir()` do if `a` and `b` don't exist yet?
>    **A:** It raises `FileNotFoundError`. `parents` defaults to `False`, so you need `mkdir(parents=True)`.
>
> 2. **Q:** What does `exist_ok=True` change in `Path.mkdir()`?
>    **A:** It stops `FileExistsError` when the directory already exists, so the call is safe to repeat. The default is `False`, which raises the error.
>
> 3. **Q:** What is the difference between `PurePath` and `Path`?
>    **A:** `PurePath` only does path computation (joining, `.name`, `.suffix`) and never touches the filesystem. `Path` is concrete and can do I/O such as `exists()`, `read_text()` and `mkdir()`.
>
> 4. **Q:** When you write `Path('x')`, which class do you actually get?
>    **A:** `PosixPath` on Unix-like systems and `WindowsPath` on Windows. Since Python 3.13, instantiating the other OS's concrete class raises `UnsupportedOperation`.
>
> 5. **Q:** Why is `Path('data') / 'file.txt'` better than `'data' + '/' + 'file.txt'`?
>    **A:** The `/` operator joins segments using the right separator for the OS, and it normalizes the result. It works the same on Windows and Linux.
>
> Do you want to edit or drop any of these? Once you're happy, tell me whether to save them to `<tmp>/data` under the topic `pathlib`.

### Turn 4

Learner: Good catch, I had that wrong. Keep all five cards as they are. Yes, save them.

Reply:

> I saved all five cards under the topic `pathlib` in `<tmp>/data`. They're scheduled for spaced review. Next time, ask me to review due cards and I'll quiz you one at a time.

## What the model ran (from the session log)

Turn 1: `Skill` study-loop; `study.py topics`.

Turn 2: no tool call.

Turn 3, in this order:

1. `ToolSearch` with `select:mcp__context7__resolve-library-id,mcp__context7__query-docs` (it loaded the two Context7 tools; this is not a Context7 call).
2. `mcp__context7__resolve-library-id` with libraryName `Python` and query `pathlib Path.mkdir parents exist_ok and pure path vs concrete path classes`.
3. `mcp__context7__query-docs` with libraryId `/python/cpython/v3.13.9` and query `pathlib Path.mkdir parents and exist_ok arguments, FileNotFoundError when parent missing`.
4. `mcp__context7__query-docs` with the same libraryId and query `pathlib PurePath vs Path vs PosixPath vs WindowsPath: what each class is for`.

Turn 4: `Write` of the cards as a JSON list to `study-loop-cards.json` directly in /tmp; then `study.py add --topic pathlib --file /tmp/study-loop-cards.json` as one single-line command, only after the yes.

`permission_denials` was empty in all four turns. Nothing was refused or blocked.

## On-disk checks

```
$ ls <tmp>/data
pathlib.json
$ STUDY_TODAY=2026-10-09 study.py topics
{"topics":[{"topic":"pathlib","cards":5,"due":0}],"problems":[],"folder":"<tmp>/data"}
$ STUDY_TODAY=2026-10-09 study.py due     -> total_due 0
$ STUDY_TODAY=2026-10-10 study.py due     -> total_due 5 (c1 to c5, each box 1, due 2026-10-10)
```

The five cards in the file are word for word the five shown in turn 3, and card 1 carries the corrected answer (`FileNotFoundError`, `parents=False`).

## Checklist

- Did the model call `resolve-library-id` and `query-docs`? Yes: one `resolve-library-id` and two `query-docs`. The Context7 tools were available and the allow rules let them through.
- How many calls (limit 3)? Three Context7 calls. The extra `ToolSearch` only loaded the tool definitions.
- Did it check BEFORE asking to save? Yes. All three calls were in turn 3, before the question about saving.
- Did it send only a generic library question? Yes. The queries are quoted above; they name `Path.mkdir`, `parents`, `exist_ok` and the path classes, and contain nothing from the learner's text beyond the library's own names. The first query (to `resolve-library-id`) joined two concepts in one string, which the rule ("one concept per query") does not intend; the two `query-docs` calls were one concept each. It picked the library id itself and did not ask which Python version the learner uses (the docs it got were for 3.13.9).
- Did it catch the planted misconception and say what changed? Yes. It opened turn 3 with "The docs check changed one of your points" and a correction naming `FileNotFoundError` and `parents=True`.
- Did the saved cards match the docs? Cards 1 to 4 match what the docs returned (card 4's `UnsupportedOperation` since 3.13 appears in the returned text). Card 5 (the `/` operator "normalizes the result") was not covered by any query, so it was not checked, although the rule says to check each card's answer.
- Did it ask before saving and use `add --file`? Yes: it asked in turn 3 (naming the real folder) and wrote the file and ran `add --file` as one line in turn 4, after the yes.

## Imperfections

- The gap question in turn 2 pointed at the very sentence that was wrong and asked "would anything in the call decide that?", which leans toward the answer. The planted mistake was therefore found by the gap step as well, not only by the docs check; this run does not show the docs check catching a mistake that the gap step missed.
- The model gave the correction and the cards in one message instead of asking one question; this is allowed after the learner asked for the cards.
- Card 5 was not checked (see above).
- The cards file went to /tmp itself, not to the run's folder (the same as session 6).
- In turn 4 it said the cards are "scheduled for spaced review" and did not tell the learner the topic name that `add` returned or that names ignore case and punctuation. (`pathlib` was unchanged, so nothing was lost.)

## Limits of this recording

- One topic, one model, one run, one day. The Context7 service answered in this run; its availability, limits and the content of its answers were not examined beyond what the log shows.
- Learner turns were written by an AI test driver. The planted mistake made the run easy to read, so it does not show how often real mistakes are caught.
- The prompt named the skill, so automatic triggering is not shown.
- In an interactive session the tool calls and the file write would show approval prompts; this headless run used allow rules instead.
- The no-Context7 path (a user without the MCP) was not recorded.
