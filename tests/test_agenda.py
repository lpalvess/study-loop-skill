import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import study  # noqa: E402


def card(box, due="2026-01-01"):
    return {"id": "c1", "question": "q", "answer": "a", "box": box,
            "due": due, "created": "2026-01-01"}


class AgendaTests(unittest.TestCase):
    def test_new_card_starts_in_box_1_due_next_day(self):
        c = study.new_card("c1", "q", "a", date(2026, 10, 9))
        self.assertEqual((c["box"], c["due"], c["created"]), (1, "2026-10-10", "2026-10-09"))

    def test_right_moves_up_one_box_with_that_boxs_interval(self):
        c = study.apply_grade(card(1), "right", date(2026, 10, 10))
        self.assertEqual((c["box"], c["due"]), (2, "2026-10-13"))

    def test_interval_for_each_box_on_almost(self):
        base = date(2026, 1, 1)
        for box, days in {1: 1, 2: 3, 3: 7, 4: 16, 5: 35}.items():
            got = study.apply_grade(card(box), "almost", base)
            self.assertEqual(got["box"], box)
            self.assertEqual(got["due"], (base + timedelta(days=days)).isoformat())

    def test_right_in_box_5_stays_in_box_5(self):
        got = study.apply_grade(card(5), "right", date(2026, 1, 1))
        self.assertEqual((got["box"], got["due"]), (5, "2026-02-05"))

    def test_wrong_returns_to_box_1_due_tomorrow(self):
        got = study.apply_grade(card(4), "wrong", date(2026, 1, 1))
        self.assertEqual((got["box"], got["due"]), (1, "2026-01-02"))

    def test_grade_does_not_change_its_input(self):
        original = card(2)
        study.apply_grade(original, "right", date(2026, 1, 1))
        self.assertEqual(original, card(2))

    def test_invalid_result_raises(self):
        with self.assertRaises(ValueError):
            study.apply_grade(card(1), "meh", date(2026, 1, 1))

    def test_is_due_today_and_past_but_not_future(self):
        on = date(2026, 10, 10)
        self.assertTrue(study.is_due(card(1, "2026-10-10"), on))
        self.assertTrue(study.is_due(card(1, "2026-10-01"), on))
        self.assertFalse(study.is_due(card(1, "2026-10-11"), on))

    def test_leap_day_and_year_boundaries(self):
        self.assertEqual(study.new_card("c1", "q", "a", date(2028, 2, 28))["due"], "2028-02-29")
        self.assertEqual(study.new_card("c1", "q", "a", date(2026, 12, 31))["due"], "2027-01-01")


if __name__ == "__main__":
    unittest.main()
