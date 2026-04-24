# Automated Ingestion Pipeline Deployment Report

## 1. System Architecture
This repository ('Project-Helios-US-Archive') serves as a structured digital archive for US historical, legal, and crisis data. The architecture comprises several distinct directories (`Federal_Law`, `Historical_Eras`, `Full_Law_Books`, `Legal_Repositories`, `Web_Archives`, `Major_Events_Crises`) that house specific data types. The automated pipeline is designed to fetch live data from public sources like Project Gutenberg and the Wikidata SPARQL endpoint, format this data into Markdown files, and place them into the appropriate folders.

## 2. Automated Cross-Linking Workflow
The pipeline incorporates a cross-linking mechanism to enrich the archival context. When historical events are fetched and converted into Markdown, the script parses the event titles and descriptions. If specific keywords (e.g., 'civil war', 'revolution') are detected, the script automatically generates relative Markdown links to relevant foundational documents (like the Emancipation Proclamation or the Declaration of Independence). These links are appended under a `Related Foundational Documents` section in the event's Markdown file.

## 3. Checkpointing Mechanism
To prevent redundant data fetching and to seamlessly resume interrupted processes, the pipeline uses an `archive_state.json` file. This state file tracks:
- `downloaded_urls`: A list of URLs (from Gutenberg, Wikidata, etc.) that have already been processed.
- `api_cursors`: Placeholders for pagination states (essential for future integrations with APIs like CourtListener).
- `cloned_repositories`: A record of GitHub repositories that have already been cloned into the archive.

Before fetching any new data, the script verifies the target URL against the `downloaded_urls` list. If the URL is found, the script skips the ingestion for that specific item.

## 4. Batch Size Configurations
The current implementation executes batch processing to manage rate limits and API constraints. For instance:
- The Wikidata SPARQL query is configured with `LIMIT 3` and an `OFFSET 30` to retrieve a small, manageable batch of new historical events per execution.
- Books and other large text files are processed individually (e.g., fetching one book at a time) to ensure stable downloading and file writing.
