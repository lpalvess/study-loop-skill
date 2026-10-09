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
        self.assertEqual(json.loads(r.stdout), {"topics": [], "problems": [], "folder": str(self.base)})
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
        self.assertEqual(json.loads(r.stdout), {"topic": "dns", "added": ["c1", "c2"], "folder": str(self.base)})
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


class FolderField(CliBase):
    def test_topics_reports_folder_and_creates_nothing(self):
        out = json.loads(run(["topics"], self.base).stdout)
        self.assertEqual(out["folder"], str(self.base))
        self.assertFalse(self.base.exists())

    def test_add_reports_folder(self):
        out = json.loads(run(["add", "--topic", "dns"], self.base, CARDS).stdout)
        self.assertEqual(out["folder"], str(self.base))

    def test_due_and_grade_outputs_have_no_folder(self):
        run(["add", "--topic", "dns"], self.base, CARDS)
        self.assertNotIn("folder", json.loads(run(["due"], self.base, today="2026-10-10").stdout))
        g = run(["grade", "--topic", "dns", "--id", "c1", "--result", "right"], self.base)
        self.assertNotIn("folder", json.loads(g.stdout))


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


class AddFromFile(CliBase):
    def cards_file(self, text=CARDS, name="cards.json"):
        path = self.root / name
        path.write_bytes(text.encode("utf-8"))
        return path

    def test_add_from_file(self):
        path = self.cards_file()
        r = run(["add", "--topic", "dns", "--file", str(path)], self.base)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), {"topic": "dns", "added": ["c1", "c2"], "folder": str(self.base)})
        out = json.loads(run(["due"], self.base, today="2026-10-10").stdout)
        self.assertEqual([c["id"] for c in out["cards"]], ["c1", "c2"])

    def test_dash_reads_stdin(self):
        r = run(["add", "--topic", "dns", "--file", "-"], self.base, CARDS)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), {"topic": "dns", "added": ["c1", "c2"], "folder": str(self.base)})

    def test_missing_file_exits_2_and_creates_nothing(self):
        path = self.root / "nope.json"
        r = run(["add", "--topic", "dns", "--file", str(path)], self.base, CARDS)
        self.assertEqual(r.returncode, 2)
        self.assertIn("error: cannot read cards file nope.json (No such file or directory)", r.stderr)
        self.assertNotIn("Traceback", r.stderr)
        self.assertFalse(self.base.exists())

    def test_stderr_does_not_show_the_full_path(self):
        path = self.root / "nope.json"
        r = run(["add", "--topic", "dns", "--file", str(path)], self.base, CARDS)
        self.assertIn("nope.json", r.stderr)
        self.assertNotIn(str(self.root), r.stderr)

    def test_directory_as_file_exits_2(self):
        folder = self.root / "somedir"
        folder.mkdir()
        r = run(["add", "--topic", "dns", "--file", str(folder)], self.base, CARDS)
        self.assertEqual(r.returncode, 2)
        self.assertIn("error: cannot read cards file somedir (Is a directory)", r.stderr)
        self.assertNotIn("Traceback", r.stderr)
        self.assertNotIn(str(self.root), r.stderr)
        self.assertFalse(self.base.exists())

    @unittest.skipIf(not hasattr(os, "geteuid") or os.geteuid() == 0, "needs a non-root POSIX user")
    def test_unreadable_file_exits_2_with_the_reason(self):
        path = self.cards_file()
        path.chmod(0)
        self.addCleanup(path.chmod, 0o600)
        r = run(["add", "--topic", "dns", "--file", str(path)], self.base, CARDS)
        self.assertEqual(r.returncode, 2)
        self.assertIn("error: cannot read cards file cards.json (Permission denied)", r.stderr)
        self.assertNotIn(str(self.root), r.stderr)
        self.assertFalse(self.base.exists())

    def test_invalid_json_in_file_exits_2_and_writes_nothing(self):
        path = self.cards_file("not json")
        r = run(["add", "--topic", "dns", "--file", str(path)], self.base, CARDS)
        self.assertEqual(r.returncode, 2)
        self.assertIn("cards file cards.json must be JSON", r.stderr)
        self.assertFalse(self.base.exists())

    def test_invalid_utf8_in_file_exits_2(self):
        path = self.root / "bad.json"
        path.write_bytes(b"[\xff\xfe]")
        r = run(["add", "--topic", "dns", "--file", str(path)], self.base, CARDS)
        self.assertEqual(r.returncode, 2)
        self.assertIn("cards file bad.json must be UTF-8 text", r.stderr)
        self.assertFalse(self.base.exists())

    def test_card_without_answer_in_file_exits_2(self):
        path = self.cards_file(json.dumps([{"question": "q"}]))
        r = run(["add", "--topic", "dns", "--file", str(path)], self.base, CARDS)
        self.assertEqual(r.returncode, 2)
        self.assertIn("each card needs", r.stderr)
        self.assertFalse(self.base.exists())

    def test_file_wins_over_stdin(self):
        path = self.cards_file(json.dumps([{"question": "from file", "answer": "a"}]))
        r = run(["add", "--topic", "dns", "--file", str(path)], self.base, CARDS)
        self.assertEqual(json.loads(r.stdout)["added"], ["c1"])
        out = json.loads(run(["due", "--topic", "dns"], self.base, today="2026-10-10").stdout)
        self.assertEqual([c["question"] for c in out["cards"]], ["from file"])

    def test_bom_in_file_is_accepted(self):
        path = self.root / "bom.json"
        path.write_bytes(b"\xef\xbb\xbf" + CARDS.encode("utf-8"))
        r = run(["add", "--topic", "dns", "--file", str(path)], self.base)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["added"], ["c1", "c2"])

    def test_non_latin_and_emoji_round_trip_through_a_file(self):
        text = json.dumps([{"question": "なぜ空は青い？ 🌤", "answer": "Dispersão de Rayleigh, ação"}],
                          ensure_ascii=False)
        path = self.cards_file(text)
        r = run(["add", "--topic", "dns", "--file", str(path)], self.base, CARDS)
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(run(["due", "--topic", "dns"], self.base, today="2026-10-10").stdout)
        self.assertEqual(out["cards"][0]["question"], "なぜ空は青い？ 🌤")
        self.assertEqual(out["cards"][0]["answer"], "Dispersão de Rayleigh, ação")

    def test_cards_file_is_left_unchanged(self):
        path = self.cards_file()
        before = path.read_bytes()
        r = run(["add", "--topic", "dns", "--file", str(path)], self.base)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(len(json.loads((self.base / "dns.json").read_text(encoding="utf-8"))["cards"]), 2)
        self.assertTrue(path.is_file())
        self.assertEqual(path.read_bytes(), before)


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
