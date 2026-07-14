<div align="center">
  <h3>🏛️ Official Borrell & Huffman LLC Enterprise Portfolio</h3>
  <p><i>This repository is a verified public asset of the Borrell & Huffman Intellectual Property Ecosystem.</i></p>
  <p>
    <img src="https://img.shields.io/badge/Enterprise-Borrell_%26_Huffman-blue.svg?style=for-the-badge" alt="Enterprise ID">
    <img src="https://img.shields.io/badge/Status-Public_Showcase-success.svg?style=for-the-badge" alt="Status">
    <img src="https://img.shields.io/badge/Clearance-Unclassified-yellow.svg?style=for-the-badge" alt="Clearance">
  </p>
</div>

---

# SB26-189 Compliance Boilerplate

## Pre-Decision Notice
**[Insert this notice prominently before a user engages with the system]**

> **NOTICE OF AUTOMATED DECISION-MAKING TECHNOLOGY (ADMT)**
> Please be aware that this system uses an Automated Decision-Making Technology (ADMT) to materially influence a consequential decision affecting you. For more information on how this ADMT works and how your data is used, please see our [Link to full documentation/privacy policy].

---

## Post-Adverse Decision Explanation
**[Provide this explanation within 30 days of an adverse outcome]**

> **EXPLANATION OF ADVERSE DECISION**
>
> **The Decision:** You have received an adverse outcome regarding [State the specific decision, e.g., your application, eligibility, etc.].
>
> **Role of ADMT:** This decision was materially influenced by our Automated Decision-Making Technology (ADMT), known as [Insert Name of ADMT], version [Insert Version Number], developed by [Insert Developer Name]. The ADMT processed the following types of personal data from these sources: [List types and sources of data].
>
> **How to Request More Information or Exercise Your Rights:** You have the right to request additional information regarding this decision and the ADMT used. You may also exercise your consumer rights under Colorado law, including the right to correct data or opt-out. To do so, please follow this process: [Insert simple-to-follow instructions, e.g., click here, email us at X, or fill out this form].


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