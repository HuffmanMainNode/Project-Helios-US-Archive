# Archive Integrity and Provenance Audit

Run a local, offline review:

```bash
python scripts/archive_audit.py --root .
```

Write a JSON report:

```bash
python scripts/archive_audit.py --root . --output reports/archive-audit.json
```

The audit fingerprints local files and identifies explicit placeholder/mock markers, missing recognizable source references in legal/history folders, short Markdown records, Git LFS pointer files (including root-level archive state and knowledge-graph files), and identical content at multiple paths.

## Status meanings

- `lfs_payload_not_inspected`: the checked-out file is a Git LFS pointer. The payload itself was not read or verified.
- `lfs_payload_present_unverified`: a JSON/PNG file tracked by the repository's LFS rules is present in the checkout, but this audit does not establish its source provenance or compare it to the original pointer OID.
- `placeholder_or_mock_content`: the file contains a marker that indicates incomplete or mock content.
- `source_reference_missing`: a source citation or URL was not found in a folder where provenance is expected.
- `short_record_review`: a short Markdown record needs a human decision about whether it is a summary, index, or incomplete source.
- `duplicate_content_review`: identical bytes appear at multiple paths. This may be intentional when the archive has multiple navigational indexes.

## Trust boundaries

A SHA-256 hash is a local fingerprint. It does not authenticate the source, prove the text is historically accurate, or establish legal reuse rights. A URL or citation string does not prove the local file matches that source. The audit is a screening tool, not a legal opinion or source-authenticity certification.

Git LFS pointer files are not expanded by the audit. Fetch LFS objects separately with Git LFS and rerun the audit on a complete local checkout before claiming those payloads have been inspected.

The audit makes no network requests and never modifies archive files.


## Baseline audit: 2026-11-03

The CI audit scanned **54 archive files** and reported no read errors. The baseline findings were:

| Finding | Count |
|---|---:|
| Explicit placeholder/mock content | 9 files |
| Short Markdown records requiring review | 21 files |
| Missing recognizable source reference in legal/history folders | 13 files |
| Duplicate-content groups | 7 groups (14 file paths) |
| LFS-tracked payloads present but not provenance-verified | 3 files |

These are overlapping review flags, not mutually exclusive categories. A short record is not automatically wrong, and identical content may be intentional across navigation folders. The report is a triage index, not a verdict on authenticity or legal status.
