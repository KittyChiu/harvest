import ast
import json
import re
import tempfile
import unittest
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
MARKETPLACE_PATH = REPOSITORY_ROOT / ".github" / "plugin" / "marketplace.json"
PLUGINS_ROOT = REPOSITORY_ROOT / "plugins"
AGENT_PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
KEBAB_CASE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLUGIN_NAME = re.compile(
    r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$"
)
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
PLUGIN_FIELDS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}
SKILL_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
EVAL_FIELDS = {"id", "prompt", "expected_output", "files", "assertions"}
RESOURCE_LINK = re.compile(r"\[[^\]]+\]\(((?:assets|references)/[^)#\s]+)\)")
SCRIPT_REFERENCE = re.compile(r"(scripts/[A-Za-z0-9_.-]+\.py)")
ATOMIC_ACTOR = re.compile(r"\bcreate-atomic-note/\d+\.\d+\.\d+\b")


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

    try:
        fields = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as error:
        raise AssertionError(f"{path} contains invalid YAML frontmatter") from error
    if not isinstance(fields, dict) or not all(
        isinstance(key, str) for key in fields
    ):
        raise AssertionError(f"{path} frontmatter must be a YAML mapping")
    return fields, "\n".join(lines[end + 1 :]).strip(), len(lines)


def validate_manifest(manifest):
    errors = []
    if not isinstance(manifest, dict):
        return ["manifest must be a JSON object"]

    unknown = set(manifest) - PLUGIN_FIELDS
    if unknown:
        errors.append(f"unknown Agent Plugins fields: {sorted(unknown)}")
    if manifest.get("$schema") != AGENT_PLUGIN_SCHEMA:
        errors.append("manifest must declare the Agent Plugins 1.0 schema")

    name = manifest.get("name")
    if not isinstance(name, str) or not PLUGIN_NAME.fullmatch(name):
        errors.append("manifest name is invalid")
    elif len(name) > 64:
        errors.append("manifest name exceeds 64 characters")

    version = manifest.get("version")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        errors.append("manifest version must be semantic")

    if not isinstance(manifest.get("description"), str) or not manifest[
        "description"
    ].strip():
        errors.append("manifest description is required")

    author = manifest.get("author")
    author_name = author.get("name") if isinstance(author, dict) else None
    if not isinstance(author_name, str) or not author_name.strip():
        errors.append("manifest author name is required")
    elif set(author) - {"name", "email", "url"}:
        errors.append("manifest author contains unknown fields")

    keywords = manifest.get("keywords")
    if not isinstance(keywords, list) or not keywords:
        errors.append("manifest keywords must be a non-empty list")
    elif not all(isinstance(keyword, str) and keyword.strip() for keyword in keywords):
        errors.append("manifest keywords must be non-empty strings")
    elif len(keywords) != len(set(keywords)):
        errors.append("manifest keywords must be unique")

    return errors


def validate_skill(skill_file, manifest):
    errors = []
    try:
        frontmatter, body, line_count = load_skill_frontmatter(skill_file)
    except AssertionError as error:
        return [str(error)]

    unknown = set(frontmatter) - SKILL_FIELDS
    if unknown:
        errors.append(f"unknown Agent Skills fields: {sorted(unknown)}")

    name = frontmatter.get("name")
    if not isinstance(name, str) or not KEBAB_CASE.fullmatch(name):
        errors.append("skill name must be lowercase kebab-case")
    elif len(name) > 64:
        errors.append("skill name exceeds 64 characters")
    if name != skill_file.parent.name:
        errors.append("skill name must match its parent directory")

    description = frontmatter.get("description")
    if (
        not isinstance(description, str)
        or not description
        or len(description) > 1024
    ):
        errors.append("skill description must contain 1-1024 characters")

    compatibility = frontmatter.get("compatibility")
    if compatibility is not None and (
        not isinstance(compatibility, str)
        or not 1 <= len(compatibility) <= 500
    ):
        errors.append("skill compatibility must contain 1-500 characters")

    metadata = frontmatter.get("metadata")
    if metadata is not None and (
        not isinstance(metadata, dict)
        or not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in metadata.items()
        )
    ):
        errors.append("skill metadata must map strings to strings")

    allowed_tools = frontmatter.get("allowed-tools")
    if allowed_tools is not None and (
        not isinstance(allowed_tools, str) or not allowed_tools.strip()
    ):
        errors.append("skill allowed-tools must be a non-empty string")

    if frontmatter.get("license") != manifest.get("license"):
        errors.append("skill and plugin licenses must match")
    if not body:
        errors.append("skill body must not be empty")
    if line_count > 500:
        errors.append("SKILL.md must stay within the 500-line disclosure budget")

    for directory in ("assets", "references"):
        resource_root = skill_file.parent / directory
        if not resource_root.exists():
            continue
        for resource in sorted(path for path in resource_root.rglob("*") if path.is_file()):
            relative = resource.relative_to(skill_file.parent).as_posix()
            if relative not in body:
                errors.append(f"unreferenced skill resource: {relative}")

    referenced_resources = set(RESOURCE_LINK.findall(body))
    referenced_scripts = set(SCRIPT_REFERENCE.findall(body))
    for relative in sorted(referenced_resources | referenced_scripts):
        if not (skill_file.parent / relative).is_file():
            errors.append(f"missing referenced skill file: {relative}")

    scripts_root = skill_file.parent / "scripts"
    if scripts_root.exists():
        if "Resolve `<skill-directory>` from this `SKILL.md`." not in body:
            errors.append("skill must explain how to resolve <skill-directory>")
        validators = sorted(scripts_root.glob("validate_*.py"))
        if not validators:
            errors.append("scripts directory must contain a validator")
        for validator in validators:
            relative = validator.relative_to(skill_file.parent).as_posix()
            if relative not in referenced_scripts:
                errors.append(f"unreferenced validator: {relative}")
            test_path = validator.with_name(f"test_{validator.name}")
            if not test_path.is_file():
                errors.append(f"validator has no owning test: {test_path.name}")

    return errors


def validate_eval_suite(path, expected_skill_name):
    errors = []
    try:
        suite = load_json(path)
    except (OSError, json.JSONDecodeError) as error:
        return [f"eval suite is not valid JSON: {error}"]

    if not isinstance(suite, dict):
        return ["eval suite must be a JSON object"]
    if set(suite) != {"skill_name", "evals"}:
        errors.append("eval suite must contain only skill_name and evals")
    if suite.get("skill_name") != expected_skill_name:
        errors.append("eval skill_name must match the skill")

    evals = suite.get("evals")
    if not isinstance(evals, list) or len(evals) < 2:
        errors.append("eval suite must contain at least two scenarios")
        return errors

    skill_root = path.parent.parent.resolve()
    identifiers = []
    for index, evaluation in enumerate(evals, start=1):
        label = f"eval {index}"
        if not isinstance(evaluation, dict):
            errors.append(f"{label} must be an object")
            continue

        unknown = set(evaluation) - EVAL_FIELDS
        if unknown:
            errors.append(f"{label} has unknown fields: {sorted(unknown)}")

        identifier = evaluation.get("id")
        if not isinstance(identifier, (int, str)) or identifier == "":
            errors.append(f"{label} must have a non-empty id")
        else:
            identifiers.append(identifier)

        for field in ("prompt", "expected_output"):
            value = evaluation.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{label} {field} must be a non-empty string")

        assertions = evaluation.get("assertions")
        if not isinstance(assertions, list) or len(assertions) < 3:
            errors.append(f"{label} must have at least three assertions")
        elif not all(
            isinstance(assertion, str) and assertion.strip()
            for assertion in assertions
        ):
            errors.append(f"{label} assertions must be non-empty strings")

        files = evaluation.get("files", [])
        if not isinstance(files, list):
            errors.append(f"{label} files must be a list")
            continue
        for relative in files:
            if not isinstance(relative, str) or not relative:
                errors.append(f"{label} file paths must be non-empty strings")
                continue
            candidate = (skill_root / relative).resolve()
            try:
                candidate.relative_to(skill_root)
            except ValueError:
                errors.append(f"{label} file escapes the skill directory: {relative}")
                continue
            if not candidate.is_file():
                errors.append(f"{label} file does not exist: {relative}")

    if len(identifiers) != len(set(identifiers)):
        errors.append("eval ids must be unique")

    return errors


class MarketplaceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.marketplace = load_json(MARKETPLACE_PATH)
        cls.entries = cls.marketplace["plugins"]

    def test_marketplace_metadata(self):
        self.assertRegex(self.marketplace["name"], KEBAB_CASE)
        self.assertTrue(self.marketplace["owner"]["name"].strip())
        self.assertEqual(len(self.entries), len({entry["name"] for entry in self.entries}))
        self.assertTrue((REPOSITORY_ROOT / "LICENSE").is_file())

    def test_catalog_matches_plugin_directories(self):
        catalog_names = {entry["name"] for entry in self.entries}
        directory_names = {
            path.name
            for path in PLUGINS_ROOT.iterdir()
            if path.is_dir() and (path / "plugin.json").is_file()
        }
        self.assertEqual(catalog_names, directory_names)

    def test_entries_match_portable_manifests_skills_and_evals(self):
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
                self.assertEqual(validate_manifest(manifest), [])
                for field in ("name", "description", "version", "license"):
                    self.assertEqual(entry[field], manifest[field])

                skills_root = plugin_root / "skills"
                self.assertTrue(skills_root.is_dir())
                skill_directories = sorted(
                    path for path in skills_root.iterdir() if path.is_dir()
                )
                self.assertTrue(skill_directories)

                for skill_root in skill_directories:
                    skill_file = skill_root / "SKILL.md"
                    self.assertTrue(skill_file.is_file())
                    frontmatter, _, _ = load_skill_frontmatter(skill_file)
                    skill_name = frontmatter.get("name", "")
                    self.assertNotIn(skill_name, skill_names)
                    skill_names.add(skill_name)
                    self.assertEqual(validate_skill(skill_file, manifest), [])
                    self.assertEqual(
                        validate_eval_suite(
                            skill_root / "evals" / "evals.json", skill_name
                        ),
                        [],
                    )

    def test_atomic_note_actor_matches_plugin_version(self):
        plugin_root = PLUGINS_ROOT / "create-atomic-note"
        manifest = load_json(plugin_root / "plugin.json")
        actor = f"{manifest['name']}/{manifest['version']}"
        for relative in (
            "skills/create-atomic-note/SKILL.md",
            "skills/create-atomic-note/assets/atomic-note-template.md",
            "skills/create-atomic-note/evals/evals.json",
            "skills/create-atomic-note/scripts/test_validate_atomic_note.py",
        ):
            self.assertIn(
                actor, (plugin_root / relative).read_text(encoding="utf-8")
            )

        legacy_fixture = (
            plugin_root
            / "skills"
            / "create-atomic-note"
            / "evals"
            / "files"
            / "revise"
            / "delivery-small-batches.md"
        )
        stale = []
        for root in (
            REPOSITORY_ROOT / ".github",
            plugin_root,
        ):
            for path in root.rglob("*"):
                if not path.is_file() or path.suffix not in {".json", ".md", ".py"}:
                    continue
                for found in ATOMIC_ACTOR.findall(path.read_text(encoding="utf-8")):
                    if found != actor and path != legacy_fixture:
                        stale.append(f"{path.relative_to(REPOSITORY_ROOT)}: {found}")
        self.assertEqual(stale, [])

    def test_skill_packages_exclude_demonstration_validator(self):
        offenders = []
        guarded_roots = (
            PLUGINS_ROOT,
            REPOSITORY_ROOT / ".github" / "plugin" / "scripts",
            REPOSITORY_ROOT / ".github" / "workflows",
        )
        allowed = {Path(__file__).resolve()}
        for root in guarded_roots:
            for path in root.rglob("*"):
                if (
                    path.resolve() in allowed
                    or not path.is_file()
                    or path.suffix
                    not in {".json", ".md", ".py", ".sh", ".toml", ".yaml", ".yml"}
                ):
                    continue
                text = path.read_text(encoding="utf-8").lower()
                if "skills-ref" in text or "skills_ref" in text:
                    offenders.append(str(path.relative_to(REPOSITORY_ROOT)))
        self.assertEqual(offenders, [])

    def test_rejects_legacy_manifest_component_paths(self):
        manifest = {
            "$schema": AGENT_PLUGIN_SCHEMA,
            "name": "example",
            "version": "1.0.0",
            "description": "Example plugin",
            "author": {"name": "Example"},
            "keywords": ["example"],
            "skills": "skills/",
        }
        self.assertIn("unknown Agent Plugins fields", "\n".join(validate_manifest(manifest)))

    def test_rejects_invalid_manifest_contracts(self):
        valid = {
            "$schema": AGENT_PLUGIN_SCHEMA,
            "name": "example",
            "version": "1.0.0",
            "description": "Example plugin",
            "author": {"name": "Example"},
            "keywords": ["example"],
        }
        cases = (
            ({"$schema": "invalid"}, "Agent Plugins 1.0 schema"),
            ({"name": "Invalid--Name"}, "manifest name is invalid"),
            ({"version": "latest"}, "manifest version must be semantic"),
            ({"description": ""}, "manifest description is required"),
            ({"author": {"url": "https://example.com"}}, "author name is required"),
            ({"author": {"name": "Example", "extra": "value"}}, "unknown fields"),
            ({"keywords": []}, "keywords must be a non-empty list"),
            ({"keywords": ["example", "example"]}, "keywords must be unique"),
        )
        for replacement, expected in cases:
            with self.subTest(replacement=replacement):
                manifest = valid | replacement
                self.assertIn(expected, "\n".join(validate_manifest(manifest)))

    def test_parses_valid_yaml_frontmatter(self):
        with tempfile.TemporaryDirectory() as directory:
            skill_root = Path(directory) / "example"
            skill_root.mkdir()
            skill = skill_root / "SKILL.md"
            skill.write_text(
                "---\n"
                "# YAML comments are valid\n"
                "name: example\n"
                "description: >-\n"
                "  Create an example when one is requested.\n"
                "license: MIT\n"
                "metadata:\n"
                '  version: "1.0"\n'
                "allowed-tools: Read\n"
                "---\n\n"
                "# Example\n\nCreate one example.\n",
                encoding="utf-8",
            )
            frontmatter, _, _ = load_skill_frontmatter(skill)
            self.assertEqual(
                frontmatter["description"],
                "Create an example when one is requested.",
            )
            self.assertEqual(validate_skill(skill, {"license": "MIT"}), [])

    def test_rejects_invalid_skill_contracts(self):
        valid = {
            "name": "example",
            "description": "Create an example when one is requested.",
            "license": "MIT",
        }
        cases = (
            ({"name": "Invalid"}, "lowercase kebab-case"),
            ({"name": "different"}, "match its parent directory"),
            ({"description": ""}, "description must contain"),
            ({"description": 123}, "description must contain"),
            ({"compatibility": "x" * 501}, "compatibility must contain"),
            ({"metadata": {"version": 1}}, "metadata must map strings to strings"),
            ({"allowed-tools": 123}, "allowed-tools must be a non-empty string"),
            ({"license": "Apache-2.0"}, "skill and plugin licenses must match"),
            ({"unknown": "value"}, "unknown Agent Skills fields"),
        )
        with tempfile.TemporaryDirectory() as directory:
            skill_root = Path(directory) / "example"
            skill_root.mkdir()
            skill = skill_root / "SKILL.md"
            for replacement, expected in cases:
                with self.subTest(replacement=replacement):
                    frontmatter = valid | replacement
                    skill.write_text(
                        "---\n"
                        + yaml.safe_dump(frontmatter, sort_keys=False)
                        + "---\n\n# Example\n\nCreate one example.\n",
                        encoding="utf-8",
                    )
                    self.assertIn(
                        expected,
                        "\n".join(validate_skill(skill, {"license": "MIT"})),
                    )

    def test_rejects_invalid_skill_files(self):
        frontmatter = (
            "---\n"
            "name: example\n"
            "description: Create an example when one is requested.\n"
            "license: MIT\n"
            "---\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            skill_root = Path(directory) / "example"
            skill_root.mkdir()
            skill = skill_root / "SKILL.md"

            cases = (
                ("", "skill body must not be empty"),
                (
                    "\n# Example\n" + "\n".join("content" for _ in range(500)),
                    "500-line disclosure budget",
                ),
                (
                    "\n# Example\n\nRead [the missing asset](assets/missing.md).\n",
                    "missing referenced skill file",
                ),
            )
            for body, expected in cases:
                with self.subTest(expected=expected):
                    skill.write_text(frontmatter + body, encoding="utf-8")
                    self.assertIn(
                        expected,
                        "\n".join(validate_skill(skill, {"license": "MIT"})),
                    )

            scripts = skill_root / "scripts"
            scripts.mkdir()
            skill.write_text(
                frontmatter
                + "\n# Example\n\n"
                "Resolve `<skill-directory>` from this `SKILL.md`.\n"
                "Run scripts/validate_example.py.\n",
                encoding="utf-8",
            )
            (scripts / "validate_example.py").write_text("", encoding="utf-8")
            self.assertIn(
                "validator has no owning test",
                "\n".join(validate_skill(skill, {"license": "MIT"})),
            )

    def test_rejects_invalid_eval_contracts(self):
        valid_eval = {
            "id": 1,
            "prompt": "Create an example.",
            "expected_output": "One example.",
            "assertions": ["One", "Two", "Three"],
        }
        valid = {
            "skill_name": "example",
            "evals": [valid_eval, valid_eval | {"id": 2}],
        }
        cases = (
            (valid | {"extra": True}, "only skill_name and evals"),
            (valid | {"skill_name": "different"}, "must match the skill"),
            (valid | {"evals": []}, "at least two scenarios"),
            (valid | {"evals": ["invalid", valid_eval]}, "eval 1 must be an object"),
            (
                valid
                | {"evals": [valid_eval | {"extra": True}, valid_eval | {"id": 2}]},
                "eval 1 has unknown fields",
            ),
            (
                valid | {"evals": [valid_eval | {"id": ""}, valid_eval | {"id": 2}]},
                "eval 1 must have a non-empty id",
            ),
            (
                valid
                | {"evals": [valid_eval | {"prompt": ""}, valid_eval | {"id": 2}]},
                "eval 1 prompt must be a non-empty string",
            ),
            (
                valid
                | {
                    "evals": [
                        valid_eval | {"assertions": ["One", "Two"]},
                        valid_eval | {"id": 2},
                    ]
                },
                "eval 1 must have at least three assertions",
            ),
            (
                valid
                | {"evals": [valid_eval | {"files": "bad"}, valid_eval | {"id": 2}]},
                "eval 1 files must be a list",
            ),
            (
                valid
                | {
                    "evals": [
                        valid_eval | {"files": ["../outside.md"]},
                        valid_eval | {"id": 2},
                    ]
                },
                "file escapes the skill directory",
            ),
            (
                valid | {"evals": [valid_eval, valid_eval]},
                "eval ids must be unique",
            ),
        )
        with tempfile.TemporaryDirectory() as directory:
            evals = Path(directory) / "evals"
            evals.mkdir()
            path = evals / "evals.json"
            for suite, expected in cases:
                with self.subTest(expected=expected):
                    path.write_text(json.dumps(suite), encoding="utf-8")
                    self.assertIn(
                        expected,
                        "\n".join(validate_eval_suite(path, "example")),
                    )

    def test_relationship_taxonomy_is_synchronized(self):
        validator_paths = (
            PLUGINS_ROOT
            / "create-domain-moc"
            / "skills"
            / "create-domain-moc"
            / "scripts"
            / "validate_moc.py",
            PLUGINS_ROOT
            / "create-atomic-note"
            / "skills"
            / "create-atomic-note"
            / "scripts"
            / "validate_atomic_note.py",
            PLUGINS_ROOT
            / "create-obsidian-marp-slides"
            / "skills"
            / "create-obsidian-marp-slides"
            / "scripts"
            / "validate_marp_slides.py",
        )
        taxonomies = []
        for path in validator_paths:
            module = ast.parse(path.read_text(encoding="utf-8"))
            assignment = next(
                node
                for node in module.body
                if isinstance(node, ast.Assign)
                and any(
                    isinstance(target, ast.Name)
                    and target.id == "SUPPORTED_RELATIONSHIPS"
                    for target in node.targets
                )
            )
            taxonomies.append(ast.literal_eval(assignment.value))
        self.assertTrue(
            all(taxonomy == taxonomies[0] for taxonomy in taxonomies[1:])
        )

        for relative in (
            "create-domain-moc/skills/create-domain-moc/references/domain-design.md",
            "create-obsidian-marp-slides/skills/create-obsidian-marp-slides/references/slides-design.md",
        ):
            text = (PLUGINS_ROOT / relative).read_text(encoding="utf-8")
            normalized = text.lower()
            for relationship in sorted(taxonomies[0]):
                self.assertIn(relationship, normalized)
            self.assertIn("`Example`", text)
            self.assertIn("No pattern-to-pattern edge", text)

    def test_rejects_eval_with_missing_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evals = root / "evals"
            evals.mkdir()
            path = evals / "evals.json"
            path.write_text(
                json.dumps(
                    {
                        "skill_name": "example",
                        "evals": [
                            {
                                "id": 1,
                                "prompt": "Create an example from the supplied file.",
                                "expected_output": "One example output.",
                                "files": ["evals/files/missing.md"],
                                "assertions": ["One", "Two", "Three"],
                            },
                            {
                                "id": 2,
                                "prompt": "Reject an invalid example.",
                                "expected_output": "No output file.",
                                "assertions": ["One", "Two", "Three"],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            self.assertIn(
                "file does not exist", "\n".join(validate_eval_suite(path, "example"))
            )

    def test_rejects_unreferenced_skill_resource(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "assets").mkdir(parents=True)
            (root / "assets" / "orphan.md").write_text("orphan", encoding="utf-8")
            skill = root / "SKILL.md"
            skill.write_text(
                "---\n"
                "name: example\n"
                "description: Create an example. Use when an example is requested.\n"
                "license: MIT\n"
                "---\n\n"
                "# Example\n\nCreate one example.\n",
                encoding="utf-8",
            )
            errors = validate_skill(skill, {"license": "MIT"})
            self.assertIn("unreferenced skill resource", "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
