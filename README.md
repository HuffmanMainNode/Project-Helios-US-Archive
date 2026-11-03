# Project Helios: US Archive

Project Helios is an experimental, static research archive containing selected U.S. historical, legal, and civic reference materials. Its purpose is to preserve navigable source texts and research notes, not to provide legal advice or a verified, comprehensive legal database.

## What is currently present

- Public-domain and historical texts, including selected Project Gutenberg editions of foundational U.S. documents and political works.
- Local HTML/text captures of selected public legal-reference pages.
- Short historical-event and legal-topic records, summaries, and excerpts.
- An optional CourtListener API wrapper in `courtlistener_integration.py`. It requires a CourtListener API token and is not a complete ingestion pipeline.
- Git LFS-tracked files for archive state and knowledge-graph artifacts. Their pointer files are present in the repository, but the referenced payloads have not been verified in this review.

## Important accuracy and completeness warning

Some files are incomplete examples, short excerpts, mock citations, or explicit placeholders rather than full primary-source texts. For example, several Supreme Court case files contain only short excerpts and placeholder notes; the Articles of Confederation and Emancipation Proclamation records are not complete texts. Do not cite these files as complete opinions, statutes, or official editions.

Every legal or historical record should identify its source, edition, date retrieved, and whether it is a full text, excerpt, summary, or research note. A title or quotation alone is not a reliable citation.

## What is not currently implemented

The repository does not currently contain a reproducible automated Gutenberg/Wikidata ingestion pipeline, a completed CourtListener crawler, a spaCy NER pipeline, a generated and inspectable knowledge graph, a semantic/vector search engine, or a deployed static site. The historical `Actions_Report.md`, `Deployment_Report.md`, and roadmap describe ambitions and earlier claims; they are not proof that those capabilities are present in the current checkout.

## Audit the archive

The repository includes a local, dependency-free structural and provenance screen:

```bash
python scripts/archive_audit.py --root .
python -m unittest discover -s tests -p 'test_*.py' -v
```

It reports Git LFS pointers, explicit placeholder/mock content, missing source references in legal/history folders, short records, and identical files at multiple paths. See [Archive Audit](docs/ARCHIVE_AUDIT.md) for interpretation and limitations.

The audit does not authenticate sources, prove historical accuracy, determine copyright status, or validate legal conclusions.

## Using the CourtListener wrapper

The optional CourtListener client requires a valid `COURTLISTENER_API_KEY`. It is separate from the local archive audit and is not required to browse the existing files. See [CourtListener integration](docs/COURTLISTENER.md) for its scope and safety limits.


## Repository structure caveat

Two historical Git submodule entries exist under `Legal_Repositories/`, but the repository has no `.gitmodules` file. One pinned commit corresponds to `18F/open-source-policy`; the other pinned commit could not be matched to the similarly named CFPB repository. Their URLs and checkout availability are therefore unresolved. They are not counted as verified archive content, and this update does not invent submodule URLs or rewrite the gitlinks.

## Source and licensing

The repository-level MIT license applies to the repository's own code and documentation to the extent the maintainer has rights to license them. It does not automatically relicense third-party texts, archived web pages, images, or other source material. Review each source's own terms and applicable public-domain/copyright status before redistribution or commercial use.

## Responsible use

- Preserve attribution and source context.
- Distinguish primary sources, excerpts, summaries, and analysis.
- Do not treat historical summaries or automated extraction as legal advice.
- Verify current law and controlling authority from official sources before relying on a legal proposition.
- Do not infer completeness or authenticity from a file name, folder, or checksum.
