import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "study.py"
CARDS = json.dumps([{"question": "q1", "answer": "a1"}, {"question": "q2", "answer": "a2"}])


def run(args, base, stdin="", today="2026-10-09"):
    env = dict(os.environ, STUDY_DIR=str(base), STUDY_TODAY=today)
    return subprocess.run([sys.executable, str(SCRIPT), *args], input=stdin,
                          capture_output=True, text=True, encoding="utf-8", env=env)


class CliBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.base = self.root / "data"  # does not exist until something is saved


class ReadOnlyCommands(CliBase):
    def test_topics_on_missing_dir_is_empty_and_creates_nothing(self):
        r = run(["topics"], self.base)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(json.loads(r.stdout), {"topics": [], "problems": []})
        self.assertFalse(self.base.exists())

    def test_due_on_missing_dir_is_empty_and_creates_nothing(self):
        r = run(["due"], self.base)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(json.loads(r.stdout), {"cards": [], "total_due": 0, "problems": []})
        self.assertFalse(self.base.exists())

    def test_script_has_no_network_imports(self):
        source = SCRIPT.read_text(encoding="utf-8")
        for word in ("urllib", "socket", "http", "requests", "ftplib", "smtplib"):
            self.assertIsNone(re.search(rf"^\s*(import|from)\s+{word}", source, re.M), word)


class AddAndDue(CliBase):
    def test_add_then_due_next_day(self):
        r = run(["add", "--topic", "dns"], self.base, CARDS)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(json.loads(r.stdout), {"topic": "dns", "added": ["c1", "c2"]})
        today_out = json.loads(run(["due"], self.base, today="2026-10-09").stdout)
        self.assertEqual(today_out["total_due"], 0)
        out = json.loads(run(["due"], self.base, today="2026-10-10").stdout)
        self.assertEqual(out["total_due"], 2)
        self.assertEqual([c["id"] for c in out["cards"]], ["c1", "c2"])

    def test_second_add_never_reuses_ids(self):
        run(["add", "--topic", "dns"], self.base, CARDS)
        r = run(["add", "--topic", "DNS"], self.base, CARDS)
        self.assertEqual(json.loads(r.stdout)["added"], ["c3", "c4"])

    def test_limit_caps_cards_but_not_total(self):
        run(["add", "--topic", "dns"], self.base, CARDS)
        out = json.loads(run(["due", "--limit", "1"], self.base, today="2026-10-10").stdout)
        self.assertEqual((len(out["cards"]), out["total_due"]), (1, 2))

    def test_limit_zero_is_rejected(self):
        self.assertEqual(run(["due", "--limit", "0"], self.base).returncode, 2)

    def test_topic_filter(self):
        run(["add", "--topic", "dns"], self.base, CARDS)
        run(["add", "--topic", "tcp"], self.base, CARDS)
        out = json.loads(run(["due", "--topic", "tcp"], self.base, today="2026-10-10").stdout)
        self.assertEqual({c["topic"] for c in out["cards"]}, {"tcp"})

    def test_topics_counts_cards_and_due(self):
        run(["add", "--topic", "dns"], self.base, CARDS)
        out = json.loads(run(["topics"], self.base, today="2026-10-10").stdout)
        self.assertEqual(out["topics"], [{"topic": "dns", "cards": 2, "due": 2}])


class Grade(CliBase):
    def setUp(self):
        super().setUp()
        run(["add", "--topic", "dns"], self.base, CARDS)

    def test_right_moves_to_box_2(self):
        r = run(["grade", "--topic", "dns", "--id", "c1", "--result", "right"],
                self.base, today="2026-10-10")
        self.assertEqual(json.loads(r.stdout), {"id": "c1", "box": 2, "due": "2026-10-13"})

    def test_unknown_id_exits_1_and_changes_nothing(self):
        before = (self.base / "dns.json").read_bytes()
        r = run(["grade", "--topic", "dns", "--id", "zz", "--result", "right"], self.base)
        self.assertEqual(r.returncode, 1)
        self.assertEqual((self.base / "dns.json").read_bytes(), before)

    def test_unknown_topic_exits_1(self):
        r = run(["grade", "--topic", "nope", "--id", "c1", "--result", "right"], self.base)
        self.assertEqual(r.returncode, 1)

    def test_invalid_result_exits_2(self):
        r = run(["grade", "--topic", "dns", "--id", "c1", "--result", "meh"], self.base)
        self.assertEqual(r.returncode, 2)


class TopicNames(CliBase):
    def test_path_traversal_stays_inside_data_dir(self):
        r = run(["add", "--topic", "../../teachback-escape-probe"], self.base, CARDS)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(json.loads(r.stdout)["topic"], "teachback-escape-probe")
        self.assertTrue((self.base / "teachback-escape-probe.json").is_file())
        self.assertFalse((self.root.parent / "teachback-escape-probe.json").exists())

    def test_name_with_no_usable_characters_is_rejected(self):
        r = run(["add", "--topic", "../"], self.base, CARDS)
        self.assertEqual(r.returncode, 2)
        self.assertFalse(self.base.exists())

    def test_non_latin_names_and_text_round_trip(self):
        cards = json.dumps([{"question": "なぜ空は青い？ 🌤", "answer": "Dispersão de Rayleigh, ação"}],
                           ensure_ascii=False)
        r = run(["add", "--topic", "日本語 DNS"], self.base, cards)
        self.assertEqual(r.returncode, 0)
        out = json.loads(run(["due", "--topic", "日本語 DNS"], self.base, today="2026-10-10").stdout)
        self.assertEqual(out["cards"][0]["question"], "なぜ空は青い？ 🌤")
        self.assertEqual(out["cards"][0]["answer"], "Dispersão de Rayleigh, ação")


class BadInput(CliBase):
    def test_malformed_stdin_exits_2_and_writes_nothing(self):
        r = run(["add", "--topic", "dns"], self.base, "not json")
        self.assertEqual(r.returncode, 2)
        self.assertFalse(self.base.exists())

    def test_card_without_answer_exits_2(self):
        r = run(["add", "--topic", "dns"], self.base, json.dumps([{"question": "q"}]))
        self.assertEqual(r.returncode, 2)
        self.assertFalse(self.base.exists())

    def test_empty_list_exits_2(self):
        self.assertEqual(run(["add", "--topic", "dns"], self.base, "[]").returncode, 2)

    def test_bad_study_today_exits_2(self):
        self.assertEqual(run(["topics"], self.base, today="yesterday").returncode, 2)


class CorruptFiles(CliBase):
    def setUp(self):
        super().setUp()
        run(["add", "--topic", "good"], self.base, CARDS)
        (self.base / "broken.json").write_text("{not json", encoding="utf-8")

    def test_due_skips_corrupt_file_and_reports_it(self):
        r = run(["due"], self.base, today="2026-10-10")
        self.assertEqual(r.returncode, 0)
        out = json.loads(r.stdout)
        self.assertEqual(out["total_due"], 2)
        self.assertEqual(out["problems"], ["broken.json"])
        self.assertEqual((self.base / "broken.json").read_text(encoding="utf-8"), "{not json")
        self.assertTrue((self.base / "broken.json.bak").is_file())

    def test_grade_on_corrupt_file_exits_3(self):
        r = run(["grade", "--topic", "broken", "--id", "c1", "--result", "right"], self.base)
        self.assertEqual(r.returncode, 3)

    def test_add_to_corrupt_topic_exits_3_and_leaves_file(self):
        r = run(["add", "--topic", "broken"], self.base, CARDS)
        self.assertEqual(r.returncode, 3)
        self.assertEqual((self.base / "broken.json").read_text(encoding="utf-8"), "{not json")

    def test_unreadable_entry_is_reported_not_fatal(self):
        (self.base / "weird.json").mkdir()
        r = run(["due"], self.base, today="2026-10-10")
        self.assertEqual(r.returncode, 0)
        out = json.loads(r.stdout)
        self.assertEqual(out["total_due"], 2)
        self.assertEqual(sorted(out["problems"]), ["broken.json", "weird.json"])

    def test_add_over_unreadable_entry_exits_3(self):
        (self.base / "weird.json").mkdir()
        r = run(["add", "--topic", "weird"], self.base, CARDS)
        self.assertEqual(r.returncode, 3)


if __name__ == "__main__":
    unittest.main()
