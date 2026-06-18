# Integrated Information Retrieval System (Hybrid SOA Architecture) - 2026

An advanced, enterprise-grade Information Retrieval (IR) System built strictly on **Service-Oriented Architecture (SOA)** and **Clean Architecture** principles using Python. The system processes, indexes, and retrieves documents from large-scale datasets (>200K documents) by seamlessly combining traditional sparse retrieval mechanisms with deep learning semantic dense retrieval.

---

##  System Architecture

The project rejects monolithic paradigms and decouples components into dedicated independent services that communicate via high-performance RESTful APIs overseen by an API Gateway.

[User Interface (Streamlit UI)]
│
▼ (HTTP REST)
[API Gateway Service]
│
┌─────┴──────────────────────────────────┐
▼ (Query Routing)                        ▼ (Data Core)
[Query Refinement Service]             [Retrieval & Ranking Service]
├── Spell Correction                   ├── Traditional (BM25)
└── Synonym Expansion                  ├── Semantic (BERT Embeddings)
└── Scoring Fusion Core


* **Offline Services:** Responsible for static data preprocessing, structural inverted index compilation, and neural model serialization/storage.
* **Online Services:** Handles real-time query ingest, text normalization, dynamic rank fusion, and instantaneous evaluation execution.

---

## Key Features & Project Requirements

### 1. Data Pre-Processing Pipeline
* **Text Normalization:** Strips text of formatting irregularities, case discrepancies, and tokenizes strings cleanly.
* **Arabic/English Stemming:** Truncates structural prefixes and suffixes to distill core morphological stems.
* **Stop-Words Elimination:** Dynamically filters localized functional stop-words to optimize downstream matrix memory space.

### 2. Multi-Model Document Representation
* **VSM (TF-IDF):** Classic Vector Space Model evaluating token relevance against corpus inverse frequency.
* **BM25 Representation:** Advanced probabilistic model adjusting mathematically for non-linear frequency saturation and varying document lengths. Includes dynamic UI controls ($k_1$ and $b$ sliders).
* **BERT Semantic Embeddings:** Locally executes deep contextual embedding generation via transformer models (`all-MiniLM-L6-v2`) to capture intent beyond superficial keyword matching.

### 3. Structural Inverted Indexing
* Implements memory-efficient inverted mapping (`Term` ➔ `Posting List` with exact document frequency weights).
* Features cross-process object persistence (**Serialization**) for rapid local database lookups via an SQLite integration layer.

### 4. Query Refinement Core
* **Spell Correction:** Intercepts typographic faults locally before indexing pipelines kick in.
* **Synonym Expansion:** Extends user input through a semantic expansion layer to elevate overall **Recall** bounds.

### 5. Evaluation & Performance Analytics Framework
Calculates instantaneous performance scores against true ground-truth testing judges (`qrels` benchmarks):
* **Precision@10** & **Recall**
* **Mean Average Precision (MAP)** (Evaluates strict rank placement quality).
* **Normalized Discounted Cumulative Gain (nDCG)** (Penalizes late arrivals of top-tier matching documents).

---

##  Advanced Extra Features (Unsupervised AI Layer)

###  Documents Clustering
* Orchestrates unsupervised **K-Means Clustering** directly over dense BERT vectors offline. 
* Clusters documents into homogeneous neighborhoods, narrowing searching boundaries online to slash latency and system resource bounds.

### Topic Detection
* Employs **Latent Dirichlet Allocation (LDA)** and matrix decomposition filters to discover underlying latent themes across target clusters.
* Dynamically tags text outcomes within the interactive dashboard for streamlined analytical indexing.

---

## Project Structure

```text
├── app.py                         # Streamlit Interactive UI Main Application
├── documents.db                   # SQLite Database storing Raw Texts
├── requirements.txt               # System Dependencies
├── README.md                      # Comprehensive Architecture Documentation
└── services/
    ├── __init__.py
    ├── api_gateway/
    │   └── gateway_service.py     # Central REST Request Maestro Broker
    ├── query_processing/
    │   └── processing_service.py  # Pipeline (Normalization, Stemming, Refinement)
    ├── indexing/
    │   └── index_service.py       # Inverted Index Builder & Serializer Core
    └── retrieval_and_ranking/
        ├── retrieval_service.py   # Hybrid Engine (BM25 + BERT Embeddings)
        └── evaluation_service.py  # Metric Calculators (MAP, nDCG, Precision, Recall)