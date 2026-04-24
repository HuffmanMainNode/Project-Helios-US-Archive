# Project Helios: US Digital Archive & Research Hub

## ⚖️ Mission Statement
Project Helios is a specialized initiative dedicated to the systematic archival, auditing, and analysis of United States historical, legal, and governmental datasets. By applying Zero Trust principles and advanced Natural Language Processing, we aim to transform static archives into dynamic, interlinked knowledge ecosystems for cybersecurity research and legal transparency.

---

## 📁 Project Hub Overview
This repository serves as the central node for the **US Archive** and the **Protocol Helios** initiatives. It bridges the gap between raw historical data and actionable intelligence through phased development.

### 🚀 Project Phases

1.  **Phase 1: Foundational Ingestion**
    *   Primary sources: National Archives, GovInfo, and Project Gutenberg.
    *   Core assets: Declaration of Independence, US Constitution, and Federalist Papers.

2.  **Phase 2: Legal & Crisis Archiving**
    *   Mapping major US historical events and crises via Wikidata SPARQL.
    *   Initial scaffolding for authenticated case law ingestion via CourtListener.

3.  **Phase 3: NLP & Knowledge Graphing**
    *   Named Entity Recognition (NER) using `spaCy` to extract Persons, Organizations, and Geopolitical Entities.
    *   Generation of a structured `knowledge_graph.json` mapping relationships across 60+ foundational documents.

4.  **Phase 4: Semantic Search & Analysis (Upcoming)**
    *   Implementation of vector embeddings and semantic conceptual search.

---

## 🗺️ Hierarchical Navigation

> Use the links below to navigate the core indices of the archive.

*   **[Historical Eras](./Historical_Eras/)**: Documents organized by Founding, Civil War, and Modern eras.
*   **[Federal Law](./Federal_Law/)**: Central repository for foundational acts and Supreme Court cases.
*   **[Major Events & Crises](./Major_Events_Crises/)**: A chronological index of US history linked to legal shifts.
*   **[Full Law Books](./Full_Law_Books/)**: Complete digital library of foundational legal treatises.
*   **[Web Archives](./Web_Archives/)**: Offline HTML/Text captures of key public legal resources.
*   **[Audit Reports](./Audit_Reports/)**: Security and integrity reports for the archive datasets.

---

## 🛠️ Technical Methodology
*   **Language**: Python 3.x
*   **NLP**: spaCy (en_core_web_sm)
*   **Auditing**: Lazarus Protocol Standards (Zero Trust Verification)
*   **State Management**: Automated checkpointing via `archive_state.json`