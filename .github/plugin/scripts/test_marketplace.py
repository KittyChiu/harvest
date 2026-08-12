import json
import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
MARKETPLACE_PATH = REPOSITORY_ROOT / ".github" / "plugin" / "marketplace.json"
PLUGINS_ROOT = REPOSITORY_ROOT / "plugins"
KEBAB_CASE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def load_json(path):
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def load_skill_frontmatter(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise AssertionError(f"{path} must start with YAML frontmatter")

    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise AssertionError(f"{path} has unclosed YAML frontmatter") from error

    fields = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip().strip("\"'")
    return fields


class MarketplaceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.marketplace = load_json(MARKETPLACE_PATH)
        cls.entries = cls.marketplace["plugins"]

    def test_marketplace_metadata(self):
        self.assertRegex(self.marketplace["name"], KEBAB_CASE)
        self.assertTrue(self.marketplace["owner"]["name"].strip())
        self.assertEqual(len(self.entries), len({entry["name"] for entry in self.entries}))

    def test_catalog_matches_plugin_directories(self):
        catalog_names = {entry["name"] for entry in self.entries}
        directory_names = {
            path.name
            for path in PLUGINS_ROOT.iterdir()
            if path.is_dir() and (path / "plugin.json").is_file()
        }
        self.assertEqual(catalog_names, directory_names)

    def test_entries_match_manifests_and_skills(self):
        skill_names = set()

        for entry in self.entries:
            with self.subTest(plugin=entry["name"]):
                self.assertRegex(entry["name"], KEBAB_CASE)
                self.assertRegex(entry["version"], SEMVER)

                source = entry["source"].removeprefix("./")
                plugin_root = REPOSITORY_ROOT / source
                self.assertEqual(plugin_root.parent, PLUGINS_ROOT)
                self.assertTrue(plugin_root.is_dir())

                manifest = load_json(plugin_root / "plugin.json")
                for field in ("name", "description", "version"):
                    self.assertEqual(entry[field], manifest[field])

                skill_paths = manifest.get("skills", "skills/")
                if isinstance(skill_paths, str):
                    skill_paths = [skill_paths]
                self.assertTrue(skill_paths)

                for relative_skill_root in skill_paths:
                    skill_root = plugin_root / relative_skill_root
                    self.assertTrue(skill_root.is_dir())
                    skill_files = sorted(skill_root.glob("*/SKILL.md"))
                    self.assertTrue(skill_files)

                    for skill_file in skill_files:
                        frontmatter = load_skill_frontmatter(skill_file)
                        skill_name = frontmatter.get("name", "")
                        self.assertRegex(skill_name, KEBAB_CASE)
                        self.assertEqual(skill_name, skill_file.parent.name)
                        self.assertTrue(frontmatter.get("description", "").strip())
                        self.assertNotIn(skill_name, skill_names)
                        skill_names.add(skill_name)


if __name__ == "__main__":
    unittest.main()
