from __future__ import annotations

import contextlib
import io
import os
import secrets
import string
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_docs
import check_secrets


SECTIONS = ("Purpose", "Inputs", "Flow", "Boundaries", "Outputs", "Adaptation", "Verification")


def _git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), *args],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )


def _recipe(title: str = "Sample") -> str:
    return "# " + title + "\n\n" + "\n\n".join(f"## {section}\n\nSample content." for section in SECTIONS) + "\n"


def _fixture(root: Path) -> Path:
    (root / "blueprints" / "skills").mkdir(parents=True)
    (root / "blueprints" / "automations").mkdir()
    (root / "README.md").write_text(
        "# Sample repository\n\n[Catalog](blueprints/README.md) and [license](LICENSE).\n",
        encoding="ascii",
    )
    (root / "LICENSE").write_text("Sample license text.\n", encoding="ascii")
    (root / "blueprints" / "README.md").write_text(
        "# Sample catalog\n\n## Recipes\n\n"
        "- [Sample skill](skills/sample-skill.md)\n"
        "- [Sample automation](automations/sample-automation.md)\n\n"
        "## Authoring contract\n\nRecipe files are plain Markdown.\n",
        encoding="ascii",
    )
    (root / "blueprints" / "skills" / "sample-skill.md").write_text(_recipe(), encoding="ascii")
    (root / "blueprints" / "automations" / "sample-automation.md").write_text(
        _recipe("Sample automation"), encoding="ascii"
    )
    _git(root, "init", "--quiet")
    _git(root, "add", "README.md", "LICENSE", "blueprints")
    return root


def _temp_root() -> tempfile.TemporaryDirectory[str]:
    return tempfile.TemporaryDirectory(prefix="docs-ci-tests-", dir=os.environ.get("TMPDIR"))


class DocumentationChecks(unittest.TestCase):
    def test_published_corpus_passes(self) -> None:
        self.assertTrue(check_docs.validate_repository(ROOT))

    def test_valid_synthetic_corpus_passes(self) -> None:
        with _temp_root() as directory:
            self.assertTrue(check_docs.validate_repository(_fixture(Path(directory))))

    def test_broken_local_link_fails(self) -> None:
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            with (root / "README.md").open("a", encoding="ascii") as stream:
                stream.write("\n[missing](missing.md)\n")
            self.assertFalse(check_docs.validate_repository(root))

    def test_recipe_section_order_fails(self) -> None:
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            recipe = root / "blueprints" / "skills" / "sample-skill.md"
            recipe.write_text(recipe.read_text(encoding="ascii").replace("## Inputs", "## Outputs", 1), encoding="ascii")
            self.assertFalse(check_docs.validate_repository(root))

    def test_catalog_must_cover_every_recipe(self) -> None:
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            catalog = root / "blueprints" / "README.md"
            catalog.write_text(catalog.read_text(encoding="ascii").replace("- [Sample automation]", "- Sample automation"), encoding="ascii")
            self.assertFalse(check_docs.validate_repository(root))

    def test_reference_links_cover_catalog_and_extra_local_links_are_allowed(self) -> None:
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            catalog = root / "blueprints" / "README.md"
            text = catalog.read_text(encoding="ascii").replace(
                "[Sample skill](skills/sample-skill.md)", "[Sample skill][skill]"
            )
            catalog.write_text(text + "\n[skill]: skills/sample-skill.md\n[Catalog](README.md)\n", encoding="ascii")
            self.assertTrue(check_docs.validate_repository(root))

    def test_ascii_frontmatter_and_exact_layout_are_enforced(self) -> None:
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            readme = root / "blueprints" / "skills" / "sample-skill.md"
            readme.write_bytes(readme.read_bytes() + b"\xc3\xa9")
            self.assertFalse(check_docs.validate_repository(root))
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            readme = root / "blueprints" / "skills" / "sample-skill.md"
            readme.write_text("---\ntitle: hidden metadata\n---\n" + _recipe(), encoding="ascii")
            self.assertFalse(check_docs.validate_repository(root))
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            (root / "blueprints" / "extra").mkdir()
            self.assertFalse(check_docs.validate_repository(root))
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            (root / "blueprints" / "skills" / "extra.txt").write_text("not a recipe\n", encoding="ascii")
            self.assertFalse(check_docs.validate_repository(root))

    def test_escape_and_tracked_symlink_fail(self) -> None:
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            recipe = root / "blueprints" / "skills" / "sample-skill.md"
            recipe.write_text(recipe.read_text(encoding="ascii") + "\n[escape](../../README.md)\n", encoding="ascii")
            self.assertFalse(check_docs.validate_repository(root))
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            (root / "outside-link").symlink_to("LICENSE")
            _git(root, "add", "outside-link")
            self.assertFalse(check_docs.validate_repository(root))

    def test_document_and_target_symlinks_fail(self) -> None:
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            (root / "blueprints" / "skills" / "linked.md").symlink_to("sample-skill.md")
            self.assertFalse(check_docs.validate_repository(root))
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            (root / "linked-license").symlink_to("LICENSE")
            with (root / "README.md").open("a", encoding="ascii") as stream:
                stream.write("\n[linked license](linked-license)\n")
            self.assertFalse(check_docs.validate_repository(root))

    def test_unsupported_markup_links_and_non_https_targets_fail(self) -> None:
        invalid = (
            "\n[anchor](#missing-anchor)\n",
            "\n[anchor](sample-skill.md#missing-anchor)\n",
            "\n<script>unsafe</script>\n",
            "\n&amp;\n",
            "\n[shortcut]\n",
            "\n[web](http://example.org/path)\n",
            "\n<https://localhost/path>\n",
        )
        for addition in invalid:
            with self.subTest(addition=addition), _temp_root() as directory:
                root = _fixture(Path(directory))
                recipe = root / "blueprints" / "skills" / "sample-skill.md"
                recipe.write_text(recipe.read_text(encoding="ascii") + addition, encoding="ascii")
                self.assertFalse(check_docs.validate_repository(root))

    def test_public_https_link_is_syntax_checked_without_fetching(self) -> None:
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            catalog = root / "blueprints" / "README.md"
            catalog.write_text(catalog.read_text(encoding="ascii") + "\n[Public](https://github.com/example/project)\n", encoding="ascii")
            self.assertTrue(check_docs.validate_repository(root))

    def test_code_markup_is_masked_but_unclosed_fence_fails(self) -> None:
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            recipe = root / "blueprints" / "skills" / "sample-skill.md"
            recipe.write_text(
                recipe.read_text(encoding="ascii")
                + "\n```text\n<script> &copy; [shortcut]\n```\n"
                + "\nInline: `<script> &copy; [shortcut]`\n",
                encoding="ascii",
            )
            self.assertTrue(check_docs.validate_repository(root))
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            recipe = root / "blueprints" / "skills" / "sample-skill.md"
            recipe.write_text(recipe.read_text(encoding="ascii") + "\n```text\nunfinished\n", encoding="ascii")
            self.assertFalse(check_docs.validate_repository(root))


class SecretCheckDiagnostics(unittest.TestCase):
    def test_scan_input_collision_and_nested_temp_fail_closed(self) -> None:
        with _temp_root() as directory:
            root = _fixture(Path(directory) / "repo")
            (root / ".gitleaksignore").write_text("ignored controls\n", encoding="ascii")
            existing = root / ".gitleaksignore.scan-input"
            existing.write_text("existing input must not be overwritten\n", encoding="ascii")
            self.assertFalse(check_secrets._copy_working_tree(root, Path(directory) / "copy"))
            self.assertEqual(existing.read_text(encoding="ascii"), "existing input must not be overwritten\n")
            with mock.patch.dict(os.environ, {"TMPDIR": str(root)}):
                self.assertEqual(check_secrets.scan(root, "working-tree", "/missing/scanner"), "error")

    def _fake_scanner(self, directory: str) -> Path:
        binary = Path(directory) / "fake-gitleaks"
        binary.write_text(
            "#!/bin/sh\n"
            "if [ \"$1\" = version ]; then printf '8.30.1\\n'; exit 0; fi\n"
            "printf 'SCANNER_OUTPUT_SENTINEL\\n'\n"
            "exit 9\n",
            encoding="ascii",
        )
        binary.chmod(0o755)
        return binary

    def test_missing_scanner_is_nonzero_and_safe(self) -> None:
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            output = io.StringIO()
            with mock.patch.object(check_secrets, "REPO_ROOT", root), mock.patch.dict(os.environ, {}, clear=True):
                with contextlib.redirect_stdout(output):
                    status = check_secrets.main(["--working-tree"])
            self.assertNotEqual(status, 0)
            self.assertIn("ERROR", output.getvalue())
            self.assertNotIn("SCANNER_OUTPUT_SENTINEL", output.getvalue())

    def test_scanner_error_output_is_suppressed(self) -> None:
        with _temp_root() as directory:
            root = _fixture(Path(directory))
            binary = self._fake_scanner(directory)
            output = io.StringIO()
            with mock.patch.object(check_secrets, "REPO_ROOT", root), mock.patch.dict(
                os.environ, {"GITLEAKS_BINARY": str(binary)}
            ):
                with contextlib.redirect_stdout(output):
                    status = check_secrets.main(["--working-tree"])
            self.assertNotEqual(status, 0)
            self.assertIn("scanner unavailable or failed", output.getvalue())
            self.assertNotIn("SCANNER_OUTPUT_SENTINEL", output.getvalue())


@unittest.skipUnless(os.environ.get("GITLEAKS_BINARY"), "set GITLEAKS_BINARY to run native Gitleaks canaries")
class NativeGitleaksCanaries(unittest.TestCase):
    @staticmethod
    def _synthetic_token() -> str:
        alphabet = string.ascii_letters + string.digits
        return "ghp_" + "".join(secrets.choice(alphabet) for _ in range(36))

    @staticmethod
    def _poison_repository_config(root: Path) -> None:
        (root / ".gitleaks.toml").write_text(
            'title = "test-only empty rule set"\n[extend]\nuseDefault = false\n', encoding="ascii"
        )
        (root / ".gitleaksignore").write_text("repository ignore file must not weaken the scan\n", encoding="ascii")

    def test_working_tree_finding_ignores_local_disablers_and_inline_allow(self) -> None:
        with _temp_root() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            self._poison_repository_config(root)
            (root / "canary.txt").write_text(
                "GITHUB_TOKEN=" + self._synthetic_token() + " # gitleaks:allow\n", encoding="ascii"
            )
            self.assertEqual(check_secrets.scan(root, "working-tree"), "finding")

    def test_repository_ignore_file_content_is_scanned(self) -> None:
        with _temp_root() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            (root / ".gitleaksignore").write_text("GITHUB_TOKEN=" + self._synthetic_token() + "\n", encoding="ascii")
            self.assertEqual(check_secrets.scan(root, "working-tree"), "finding")

    def test_deleted_diff_disabled_finding_remains_in_history(self) -> None:
        with _temp_root() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            _git(root, "init", "--quiet")
            _git(root, "config", "user.name", "Canary Test")
            _git(root, "config", "user.email", "canary@example.invalid")
            (root / ".gitattributes").write_text("* -diff\n", encoding="ascii")
            self._poison_repository_config(root)
            _git(root, "add", ".gitattributes", ".gitleaks.toml", ".gitleaksignore")
            _git(root, "commit", "--quiet", "-m", "attributes and scanner controls")
            self.assertEqual(check_secrets.scan(root, "working-tree"), "pass")
            self.assertEqual(check_secrets.scan(root, "history"), "pass")
            (root / "removed.txt").write_text(
                "GITHUB_TOKEN=" + self._synthetic_token() + " # gitleaks:allow\n", encoding="ascii"
            )
            _git(root, "add", "removed.txt")
            _git(root, "commit", "--quiet", "-m", "add synthetic canary")
            (root / "removed.txt").unlink()
            _git(root, "add", "-u")
            _git(root, "commit", "--quiet", "-m", "remove synthetic canary")
            self.assertEqual(check_secrets.scan(root, "working-tree"), "pass")
            self.assertEqual(check_secrets.scan(root, "history"), "finding")


if __name__ == "__main__":
    unittest.main()
