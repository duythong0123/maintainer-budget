import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from maintainer_budget.cli import main
from maintainer_budget.models import ReviewComment


class CliTests(unittest.TestCase):
    def sample_comments(self):
        return [
            ReviewComment(
                "o/r", 1, "https://example.test/1", "alice",
                "Please use ConfigBuilder::default().build() for config loading.",
                path="src/a.rs", author_type="User", author_association="MEMBER",
            ),
            ReviewComment(
                "o/r", 2, "https://example.test/2", "bob",
                "Use ConfigBuilder::default().build() instead of custom config loading.",
                path="src/b.rs", author_type="User", author_association="MEMBER",
            ),
        ]

    def test_audit_prints_candidate_report(self):
        out = io.StringIO()
        with patch("maintainer_budget.cli.GitHubClient.collect", return_value=self.sample_comments()):
            with redirect_stdout(out):
                code = main(["audit", "o/r", "--similarity", "0.2"])
        self.assertEqual(code, 0)
        self.assertIn("MB-001", out.getvalue())
        self.assertIn("PR #1", out.getvalue())

    def test_audit_writes_share_card_and_codex_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            share = Path(tmp) / "share.md"
            codex = Path(tmp) / "codex.md"
            with patch("maintainer_budget.cli.GitHubClient.collect", return_value=self.sample_comments()):
                code = main([
                    "audit", "o/r", "--similarity", "0.2",
                    "--share-card", str(share),
                    "--codex-bundle", str(codex),
                ])

            self.assertEqual(code, 0)
            self.assertTrue(share.exists())
            self.assertTrue(codex.exists())
            self.assertIn("2 review comments", share.read_text(encoding="utf-8"))
            self.assertIn("MB-001", share.read_text(encoding="utf-8"))
            codex_text = codex.read_text(encoding="utf-8")
            self.assertIn("Do not invent a rule", codex_text)
            self.assertIn("https://example.test/1", codex_text)
            self.assertIn("Maintainer decision", codex_text)


if __name__ == "__main__":
    unittest.main()
