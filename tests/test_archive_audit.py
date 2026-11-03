import tempfile
import unittest
from pathlib import Path

from scripts.archive_audit import audit_archive


LFS_POINTER = (
    "version https://git-lfs.github.com/spec/v1\n"
    "oid sha256:" + "a" * 64 + "\n"
    "size 1234\n"
)


class ArchiveAuditTests(unittest.TestCase):
    def test_detects_lfs_placeholders_missing_sources_and_duplicate_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            federal = root / "Federal_Law"
            historical = root / "Historical_Eras" / "Founding_Era"
            phase = root / "Phase_4_Analysis_Synthesis"
            federal.mkdir(parents=True)
            historical.mkdir(parents=True)
            phase.mkdir(parents=True)

            (federal / "case.md").write_text(
                "Opinion excerpt. [Unabridged Opinion Content placeholder]",
                encoding="utf-8",
            )
            (federal / "no-source.md").write_text(
                "A short legal record without a citation.",
                encoding="utf-8",
            )
            (federal / "constitution.md").write_text(
                "Primary text. Source: https://example.org/constitution",
                encoding="utf-8",
            )
            (historical / "constitution-copy.md").write_text(
                "Primary text. Source: https://example.org/constitution",
                encoding="utf-8",
            )
            (phase / "graph.json").write_text(LFS_POINTER, encoding="utf-8")

            report = audit_archive(root)
            by_path = {entry["path"]: entry["statuses"] for entry in report["entries"]}

            self.assertIn("placeholder_or_mock_content", by_path["Federal_Law/case.md"])
            self.assertIn("source_reference_missing", by_path["Federal_Law/no-source.md"])
            self.assertIn("lfs_payload_not_inspected", by_path["Phase_4_Analysis_Synthesis/graph.json"])
            self.assertIn("duplicate_content_review", by_path["Federal_Law/constitution.md"])
            self.assertEqual(len(report["duplicate_content_groups"]), 1)

    def test_does_not_claim_source_authenticity_from_a_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Full_Law_Books").mkdir()
            (root / "Full_Law_Books" / "book.txt").write_text("text", encoding="utf-8")
            report = audit_archive(root)
            self.assertIn("does not authenticate", report["interpretation"]["sha256"])


if __name__ == "__main__":
    unittest.main()
