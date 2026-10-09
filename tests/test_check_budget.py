import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import check_budget  # noqa: E402


def make_skill(root, description="Short description.", body="one line", refs=None):
    skill = Path(root) / "skill"
    (skill / "references").mkdir(parents=True)
    text = f"---\nname: x\ndescription: {description}\n---\n{body}\n"
    (skill / "SKILL.md").write_text(text, encoding="utf-8")
    for name, content in (refs or {}).items():
        (skill / "references" / name).write_text(content, encoding="utf-8")
    return skill


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = self._tmp.name

    def test_small_skill_passes(self):
        errors, warnings, costs = check_budget.check(make_skill(self.root))
        self.assertEqual((errors, warnings), ([], []))
        self.assertIn("listing", costs)
        self.assertIn("invocation", costs)

    def test_tokens_are_words_times_1_35(self):
        self.assertEqual(check_budget.tokens("one two three four"), 5)

    def test_long_description_is_an_error(self):
        errors, _, _ = check_budget.check(make_skill(self.root, description="x" * 301))
        self.assertTrue(any("description" in e for e in errors))

    def test_missing_description_is_an_error(self):
        skill = make_skill(self.root)
        (skill / "SKILL.md").write_text("---\nname: x\n---\nbody\n", encoding="utf-8")
        errors, _, _ = check_budget.check(skill)
        self.assertTrue(any("description" in e for e in errors))

    def test_over_500_lines_is_an_error(self):
        errors, _, _ = check_budget.check(make_skill(self.root, body="\n".join(["l"] * 600)))
        self.assertTrue(any("lines" in e for e in errors))

    def test_over_5000_tokens_is_an_error(self):
        errors, _, _ = check_budget.check(make_skill(self.root, body="word " * 4000))
        self.assertTrue(any("tokens" in e for e in errors))

    def test_over_150_lines_is_only_a_warning(self):
        errors, warnings, _ = check_budget.check(make_skill(self.root, body="\n".join(["l"] * 200)))
        self.assertEqual(errors, [])
        self.assertTrue(any("lines" in w for w in warnings))

    def test_references_are_costed_and_tabulated(self):
        skill = make_skill(self.root, refs={"gaps.md": "a b c d"})
        _, _, costs = check_budget.check(skill)
        self.assertEqual(costs["references/gaps.md"], 5)
        table = check_budget.markdown_table(costs)
        self.assertIn("references/gaps.md", table)
        self.assertTrue(table.startswith("| What |"))


if __name__ == "__main__":
    unittest.main()
