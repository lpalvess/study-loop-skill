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
