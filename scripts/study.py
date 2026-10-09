#!/usr/bin/env python3
"""teach-back: review agenda (box method) and flashcard storage.

Exit codes: 0 ok, 1 not found, 2 bad input, 3 unreadable data file.
"""
import argparse
import json
import os
import re
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

INTERVALS = {1: 1, 2: 3, 3: 7, 4: 16, 5: 35}
RESULTS = ("right", "almost", "wrong")
DEFAULT_LIMIT = 10


def today():
    forced = os.environ.get("STUDY_TODAY")
    return date.fromisoformat(forced) if forced else date.today()


def data_dir():
    return Path(os.environ.get("STUDY_DIR") or Path.home() / ".teach-back")


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
    slug = re.sub(r"[\W_]+", "-", name.casefold(), flags=re.UNICODE).strip("-")
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
