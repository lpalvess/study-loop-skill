#!/usr/bin/env python3
"""study-loop: review agenda (box method) and flashcard storage.

Exit codes: 0 ok, 1 not found, 2 bad input, 3 unreadable data file.
"""
import argparse
import json
import os
import re
import shutil
import sys
import unicodedata
from datetime import date, timedelta
from pathlib import Path

INTERVALS = {1: 1, 2: 3, 3: 7, 4: 16, 5: 35}
RESULTS = ("right", "almost", "wrong")
DEFAULT_LIMIT = 10


def today():
    forced = os.environ.get("STUDY_TODAY")
    return date.fromisoformat(forced) if forced else date.today()


def data_dir():
    return Path(os.environ.get("STUDY_DIR") or Path.home() / ".study-loop")


def new_card(card_id, question, answer, on):
    return {
        "id": card_id,
        "question": question,
        "answer": answer,
        "box": 1,
        "due": (on + timedelta(days=INTERVALS[1])).isoformat(),
        "created": on.isoformat(),
    }


def apply_grade(card, result, on):
    if result not in RESULTS:
        raise ValueError(f"result must be one of {RESULTS}")
    box = card["box"]
    if result == "right":
        box = min(box + 1, 5)
    elif result == "wrong":
        box = 1
    updated = dict(card)
    updated["box"] = box
    updated["due"] = (on + timedelta(days=INTERVALS[box])).isoformat()
    return updated


def is_due(card, on):
    return date.fromisoformat(card["due"]) <= on


REQUIRED_FIELDS = ("id", "question", "answer", "box", "due", "created")


class CorruptTopic(Exception):
    """A topic file could not be read; the message is its file name."""


def slugify(name):
    text = unicodedata.normalize("NFC", name.casefold())
    slug = "".join(
        ch if ch.isalnum() or unicodedata.category(ch).startswith("M") else "-"
        for ch in text
    )
    slug = re.sub(r"-+", "-", slug).strip("-")
    if not slug:
        raise ValueError("topic name has no usable characters")
    return slug[:60].rstrip("-")


def topic_path(base, topic):
    return base / f"{slugify(topic)}.json"


def _validate(data):
    if not isinstance(data, dict) or not isinstance(data.get("cards"), list):
        raise ValueError("missing cards list")
    for card in data["cards"]:
        if not isinstance(card, dict) or any(k not in card for k in REQUIRED_FIELDS):
            raise ValueError("card missing fields")
        if card["box"] not in INTERVALS:
            raise ValueError("box out of range")
        date.fromisoformat(card["due"])
        date.fromisoformat(card["created"])


def load_topic(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        _validate(data)
    except (ValueError, TypeError) as exc:
        backup = path.with_name(path.name + ".bak")
        if not backup.exists():
            shutil.copy2(path, backup)
        raise CorruptTopic(path.name) from exc
    return data


def save_topic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def next_card_id(cards):
    used = set()
    for card in cards:
        match = re.fullmatch(r"c(\d+)", str(card.get("id", "")))
        if match:
            used.add(int(match.group(1)))
    return f"c{max(used, default=0) + 1}"


def iter_topics(base):
    if not base.is_dir():
        return []
    return sorted((p.stem, p) for p in base.glob("*.json"))


def collect_due(base, on, topic=None, limit=DEFAULT_LIMIT):
    if topic is not None:
        path = topic_path(base, topic)
        paths = [(slugify(topic), path)] if path.is_file() else []
    else:
        paths = iter_topics(base)
    found, problems = [], []
    for slug, path in paths:
        try:
            data = load_topic(path)
        except (CorruptTopic, OSError):
            problems.append(path.name)
            continue
        for card in data["cards"]:
            if is_due(card, on):
                found.append({"topic": slug, "id": card["id"], "question": card["question"],
                              "answer": card["answer"], "box": card["box"], "due": card["due"]})
    found.sort(key=lambda c: (c["due"], c["topic"], c["id"]))
    return found[:limit], len(found), problems


def summarize_topics(base, on):
    topics, problems = [], []
    for slug, path in iter_topics(base):
        try:
            data = load_topic(path)
        except (CorruptTopic, OSError):
            problems.append(path.name)
            continue
        topics.append({"topic": slug, "cards": len(data["cards"]),
                       "due": sum(1 for c in data["cards"] if is_due(c, on))})
    return topics, problems


def emit(obj):
    print(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))


def fail(message, code=2):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(code)


def positive_int(text):
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a whole number")
    if value < 1:
        raise argparse.ArgumentTypeError("must be 1 or more")
    return value


def cmd_topics(args, on):
    topics, problems = summarize_topics(data_dir(), on)
    emit({"topics": topics, "problems": problems, "folder": os.path.abspath(data_dir())})


def cmd_due(args, on):
    cards, total, problems = collect_due(data_dir(), on, args.topic, args.limit)
    emit({"cards": cards, "total_due": total, "problems": problems})


def cmd_add(args, on):
    path = topic_path(data_dir(), args.topic)
    source = "stdin"
    try:
        if args.file is None or args.file == "-":
            text = sys.stdin.read()
        else:
            source = f"cards file {Path(args.file).name}"
            with open(args.file, encoding="utf-8-sig") as handle:
                text = handle.read()
        incoming = json.loads(text)
    except UnicodeDecodeError:
        fail(f"{source} must be UTF-8 text")
    except ValueError:
        fail(f"{source} must be JSON: a list of {{question, answer}}")
    except OSError as exc:
        reason = exc.strerror or type(exc).__name__
        fail(f"cannot read {source} ({reason})")
    if not isinstance(incoming, list) or not incoming:
        fail(f"{source} must be a non-empty JSON list")
    for item in incoming:
        ok = (isinstance(item, dict)
              and isinstance(item.get("question"), str) and item["question"].strip()
              and isinstance(item.get("answer"), str) and item["answer"].strip())
        if not ok:
            fail("each card needs non-empty text fields question and answer")
    data = load_topic(path) if path.is_file() else {"topic": args.topic, "cards": []}
    added = []
    for item in incoming:
        card_id = next_card_id(data["cards"])
        data["cards"].append(new_card(card_id, item["question"].strip(), item["answer"].strip(), on))
        added.append(card_id)
    save_topic(path, data)
    emit({"topic": slugify(args.topic), "added": added, "folder": os.path.abspath(data_dir())})


def cmd_grade(args, on):
    path = topic_path(data_dir(), args.topic)
    if not path.is_file():
        fail("unknown topic", 1)
    data = load_topic(path)
    for index, card in enumerate(data["cards"]):
        if card["id"] == args.id:
            data["cards"][index] = apply_grade(card, args.result, on)
            save_topic(path, data)
            emit({"id": args.id, "box": data["cards"][index]["box"],
                  "due": data["cards"][index]["due"]})
            return
    fail("unknown card id", 1)


COMMANDS = {"topics": cmd_topics, "due": cmd_due, "add": cmd_add, "grade": cmd_grade}


def build_parser():
    parser = argparse.ArgumentParser(prog="study.py")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("topics")
    due = sub.add_parser("due")
    due.add_argument("--topic")
    due.add_argument("--limit", type=positive_int, default=DEFAULT_LIMIT)
    add = sub.add_parser("add")
    add.add_argument("--topic", required=True)
    add.add_argument("--file")
    grade = sub.add_parser("grade")
    grade.add_argument("--topic", required=True)
    grade.add_argument("--id", required=True)
    grade.add_argument("--result", required=True, choices=RESULTS)
    return parser


def main(argv=None):
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = build_parser().parse_args(argv)
    try:
        on = today()
    except ValueError:
        fail("STUDY_TODAY must be YYYY-MM-DD")
    try:
        COMMANDS[args.command](args, on)
    except CorruptTopic as exc:
        fail(f"cannot read {exc}; a copy was kept next to it as .bak", 3)
    except OSError as exc:
        fail(f"cannot read or write a data file ({type(exc).__name__})", 3)
    except ValueError as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
