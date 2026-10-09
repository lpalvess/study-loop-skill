import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import study  # noqa: E402


class SlugTests(unittest.TestCase):
    def test_simple_name(self):
        self.assertEqual(study.slugify("Redes / DNS"), "redes-dns")

    def test_path_traversal_collapses(self):
        self.assertEqual(study.slugify("../../etc/passwd"), "etc-passwd")

    def test_non_latin_letters_are_kept(self):
        self.assertEqual(study.slugify("日本語 DNS"), "日本語-dns")

    def test_nothing_usable_raises(self):
        for bad in ("", "../", "   ", "--__--"):
            with self.assertRaises(ValueError):
                study.slugify(bad)

    def test_long_names_are_cut_to_60(self):
        self.assertEqual(len(study.slugify("a" * 200)), 60)

    def test_decomposed_and_precomposed_accents_match(self):
        self.assertEqual(study.slugify("cafe\u0301"), "caf\u00e9")
        self.assertEqual(study.slugify("caf\u00e9"), "caf\u00e9")

    def test_accent_is_not_dropped(self):
        self.assertNotEqual(study.slugify("cafe"), study.slugify("caf\u00e9"))

    def test_devanagari_vowel_signs_are_kept(self):
        self.assertEqual(study.slugify("हिन्दी DNS"), "हिन्दी-dns")

    def test_arabic_diacritics_are_kept(self):
        self.assertEqual(study.slugify("مَرْحَبًا"), "مَرْحَبًا")


class StorageTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name) / "data"

    def write_raw(self, name, text):
        self.base.mkdir(exist_ok=True)
        path = self.base / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_save_creates_dir_and_round_trips_unicode(self):
        path = study.topic_path(self.base, "dns")
        data = {"topic": "dns", "cards": [
            study.new_card("c1", "pergunta ação", "日本語 🌤", date(2026, 10, 9))]}
        study.save_topic(path, data)
        self.assertEqual(study.load_topic(path), data)

    def test_save_leaves_no_temp_file(self):
        study.save_topic(study.topic_path(self.base, "dns"), {"topic": "dns", "cards": []})
        self.assertEqual([p.name for p in self.base.iterdir()], ["dns.json"])

    def test_invalid_json_keeps_original_and_makes_backup(self):
        path = self.write_raw("x.json", "{oops")
        with self.assertRaises(study.CorruptTopic):
            study.load_topic(path)
        self.assertEqual(path.read_text(encoding="utf-8"), "{oops")
        self.assertEqual((self.base / "x.json.bak").read_text(encoding="utf-8"), "{oops")

    def test_invalid_cards_are_corrupt(self):
        good = study.new_card("c1", "q", "a", date(2026, 10, 9))
        variants = {
            "missing field": [{"id": "c1"}],
            "box out of range": [dict(good, box=9)],
            "unhashable box": [dict(good, box=[1])],
            "bad due date": [dict(good, due="tomorrow")],
            "cards not a list": "nope",
        }
        for index, (label, cards) in enumerate(variants.items()):
            with self.subTest(label):
                text = json.dumps({"topic": "v", "cards": cards})
                path = self.write_raw(f"v{index}.json", text)
                with self.assertRaises(study.CorruptTopic):
                    study.load_topic(path)
                self.assertEqual(path.read_text(encoding="utf-8"), text)
                self.assertTrue((self.base / f"v{index}.json.bak").exists())

    def test_next_card_id_never_reuses(self):
        self.assertEqual(study.next_card_id([]), "c1")
        self.assertEqual(study.next_card_id([{"id": "c1"}, {"id": "c7"}, {"id": "custom"}]), "c8")

    def test_iter_topics_handles_missing_dir_and_skips_backups(self):
        self.assertEqual(study.iter_topics(self.base), [])
        study.save_topic(study.topic_path(self.base, "b"), {"topic": "b", "cards": []})
        study.save_topic(study.topic_path(self.base, "a"), {"topic": "a", "cards": []})
        self.write_raw("a.json.bak", "x")
        self.assertEqual([slug for slug, _ in study.iter_topics(self.base)], ["a", "b"])


if __name__ == "__main__":
    unittest.main()
