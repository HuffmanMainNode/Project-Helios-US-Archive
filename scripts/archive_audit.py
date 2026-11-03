#!/usr/bin/env python3
"""Audit archive files for provenance gaps, placeholders, LFS pointers, and duplicates."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

SPECIAL_FILES = ("archive_state.json", "knowledge_graph.json")
ARCHIVE_ROOTS = (
    "Federal_Law",
    "Historical_Eras",
    "Major_Events_Crises",
    "Cyber_Law",
    "State_Local_Law",
    "Full_Law_Books",
    "Summaries",
    "Web_Archives",
    "Phase_4_Analysis_Synthesis",
)
CITATION_REQUIRED_ROOTS = {
    "Federal_Law",
    "Historical_Eras",
    "Major_Events_Crises",
    "Cyber_Law",
    "State_Local_Law",
}
LFS_POINTER = re.compile(
    rb"^version https://git-lfs\.github.com/spec/v1\n"
    rb"oid sha256:[0-9a-f]{64}\n"
    rb"size [0-9]+\n?$"
)
PLACEHOLDER = re.compile(
    r"\[[^\]]*(?:placeholder|mocked|mock|full proclamation text)[^\]]*\]"
    r"|\bcaselaw access project\s*\(mock\)",
    re.IGNORECASE,
)
SOURCE_REFERENCE = re.compile(
    r"\*\*Source(?: Citation)?:\*\*|https?://|www\.gutenberg\.org",
    re.IGNORECASE,
)
TEXT_SUFFIXES = {".md", ".txt", ".html", ".htm", ".json", ".py"}


def audit_archive(root: str | Path) -> dict:
    root = Path(root).resolve()
    entries = []
    errors = []
    hashes: dict[str, list[str]] = defaultdict(list)

    candidate_paths = [root / name for name in SPECIAL_FILES if (root / name).is_file()]
    for directory in ARCHIVE_ROOTS:
        base = root / directory
        if base.is_dir():
            candidate_paths.extend(path for path in base.rglob("*") if path.is_file())

    for path in sorted(candidate_paths):
            relative = path.relative_to(root).as_posix()
            try:
                raw = path.read_bytes()
            except OSError as error:
                errors.append({"path": relative, "error": type(error).__name__})
                continue

            digest = hashlib.sha256(raw).hexdigest()
            hashes[digest].append(relative)
            statuses = []
            is_lfs = bool(LFS_POINTER.fullmatch(raw))
            if is_lfs:
                statuses.append("lfs_payload_not_inspected")
            elif path.suffix.lower() in TEXT_SUFFIXES:
                text = raw.decode("utf-8", errors="replace")
                if PLACEHOLDER.search(text):
                    statuses.append("placeholder_or_mock_content")
                if (
                    any(
                        part in CITATION_REQUIRED_ROOTS
                        for part in path.relative_to(root).parts[:-1]
                    )
                    and not SOURCE_REFERENCE.search(text)
                ):
                    statuses.append("source_reference_missing")
                if path.suffix.lower() == ".md" and len(raw) < 300:
                    statuses.append("short_record_review")
            entries.append({
                "path": relative,
                "bytes": len(raw),
                "sha256": digest,
                "format": path.suffix.lower().lstrip(".") or "unknown",
                "statuses": statuses,
            })

    duplicates = [
        {"sha256": digest, "paths": sorted(paths)}
        for digest, paths in sorted(hashes.items())
        if len(paths) > 1
    ]
    duplicate_paths = {
        path for group in duplicates for path in group["paths"]
    }
    for entry in entries:
        if entry["path"] in duplicate_paths:
            entry["statuses"].append("duplicate_content_review")

    status_counts = defaultdict(int)
    for entry in entries:
        for status in entry["statuses"]:
            status_counts[status] += 1

    return {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files_scanned": len(entries),
        "errors": errors,
        "status_counts": dict(sorted(status_counts.items())),
        "duplicate_content_groups": duplicates,
        "entries": entries,
        "interpretation": {
            "sha256": "Local content fingerprint only; it does not authenticate a source or prove historical accuracy.",
            "lfs_payload_not_inspected": "The Git LFS pointer was found, but the referenced payload was not inspected.",
            "placeholder_or_mock_content": "The file contains an explicit mock or placeholder marker and must not be treated as a complete primary source.",
            "source_reference_missing": "No recognizable source citation or URL was found in a folder where provenance is expected.",
            "short_record_review": "A short Markdown record may be an index or an incomplete record; human review is required.",
            "duplicate_content_review": "Identical file content occurs at multiple paths. This may be intentional duplication across archive indexes.",
        },
        "limitations": [
            "This is a local structural and provenance screen, not a legal review or source-authenticity certification.",
            "A source URL does not establish that the file matches the source or that reuse is authorized.",
            "Text heuristics can miss placeholders and can produce false positives.",
            "Git LFS pointer metadata does not verify the availability or correctness of the referenced payload.",
            "The audit does not make network requests or modify archive content.",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Archive repository root")
    parser.add_argument("--output", help="Optional JSON report path; defaults to stdout")
    args = parser.parse_args(argv)
    try:
        report = audit_archive(args.root)
    except OSError as error:
        print(f"Archive audit failed: {error}", file=sys.stderr)
        return 2

    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
