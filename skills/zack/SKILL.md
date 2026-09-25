---
name: zack
description: "Trigger when user says 'Zack', 'map:', 'Zack, I want to understand', 'Zack，我想了解', or asks to orient, deconstruct, and build a mental/world/decision model for a new tool, discipline, book, technology, or concept. Generates a deep AI-era learning map in English and saves it as a standalone Markdown note."
---

# Zack: Mental Model & Concept Orienteer

## Invocation Matrix

| Trigger | Mode | Input Arguments | Deterministic Action |
| :--- | :--- | :--- | :--- |
| `zack:` / `map:` / `Zack` | Domain Orienteering | Concept, technology, discipline, or book | Build full-stack mental model map, prerequisite graph, and decision heuristics |

---

## 4-Stage Orienteering Map

1. **Stage 1: First Principles & Core Definition**: What problem does this concept solve that could not be solved before?
2. **Stage 2: Topology & Prerequisite Graph**: Visual Mermaid tree of core components, dependencies, and adjacent disciplines.
3. **Stage 3: Common Pitfalls & High-Leverage Heuristics**: 80/20 leverage points, costly beginner mistakes, and counter-intuitive insights.
4. **Stage 4: 30-Day Execution Roadmap**: Step-by-step progression from novice to practitioner.

---

## Invariants & Operational Boundaries

1. **First-Principles Rigor**: Define concepts through fundamental causality, not descriptive buzzwords.
2. **Actionable Heuristics**: Formulate rules as testable `IF [condition] THEN [action]` decision trees.
3. **Storage Archival**: Save generated learning maps to `${VAULT_DIR:-$HOME/Documents/AI_Workspace}/Learning Maps/`.

---

## Runnable Input/Output Contract

### Input
```text
map: Vector Databases and Embedding Models
```

### Output Payload
```markdown
# Vector Databases & Embeddings — Orienteering Map

### 1. First Principles
Embeddings convert high-dimensional semantic meaning into spatial coordinates; vector databases perform geometric nearest-neighbor searches (HNSW/Cosine) to retrieve semantically related concepts in constant time.

### 2. High-Leverage Heuristics
- `IF` retrieval accuracy degrades on domain jargon `THEN` apply hybrid search (BM25 sparse + dense embedding) before fine-tuning.
- `IF` dataset < 100k vectors `THEN` use in-memory SQLite/pgvector rather than standing up a standalone Pinecone/Milvus cluster.
```

---

## Acceptance Criteria

1. **Clarity**: Output establishes a complete conceptual foundation for a new subject in under 5 minutes of reading time.
2. **Visual Mapping**: Includes at least one valid, error-free Mermaid architecture diagram.
