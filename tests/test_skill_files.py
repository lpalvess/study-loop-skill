import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import check_budget  # noqa: E402

SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8") if (ROOT / "SKILL.md").exists() else ""


class SkillFileTests(unittest.TestCase):
    def test_skill_exists_with_the_right_name(self):
        self.assertTrue(SKILL, "SKILL.md is missing")
        self.assertRegex(SKILL, r"(?m)^name: teach-back$")

    def test_budget_is_respected(self):
        errors, _, _ = check_budget.check(ROOT)
        self.assertEqual(errors, [])

    def test_linked_references_exist(self):
        links = re.findall(r"\]\((references/[\w.-]+)\)", SKILL)
        self.assertTrue(links)
        for link in links:
            self.assertTrue((ROOT / link).is_file(), link)

    def test_only_real_commands_are_mentioned(self):
        used = set(re.findall(r"study\.py (\w+)", SKILL))
        self.assertEqual(used, {"topics", "due", "add", "grade"})

    def test_key_rules_are_present(self):
        for phrase in ("One gap per message", "Never list all the gaps", "Nothing is saved without a yes", "Without Python", "Context7"):
            self.assertIn(phrase, SKILL)

    def test_failure_and_count_rules_are_present(self):
        for phrase in ("<<'EOF'", "do not retry silently", "study.py due --limit 1"):
            self.assertIn(phrase, SKILL)

    def test_only_real_flags_are_mentioned(self):
        flags = set(re.findall(r"--[a-z][a-z-]*", SKILL))
        self.assertEqual(flags, {"--limit", "--topic", "--id", "--result"})


if __name__ == "__main__":
    unittest.main()
