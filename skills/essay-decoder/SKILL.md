---
name: essay-decoder
description: "Deconstructs dense academic, economic, technical, philosophical, or industry essays into intuitive mental models with first-principles causal mechanisms, bifurcated epistemic boundary analysis (technical ∂D vs humanistic context), and practical action takeaways. Trigger when user says 'decode:', 'demystify:', '通俗解读', '文章解读', '白话拆解', '深度省流', '看不懂这篇文章', or provides a dense article/paper. Saves structured Markdown directly to ${VAULT_DIR:-$HOME/Documents/AI_Workspace}/English/Article Deconstructions/ and silently mounts into VMark workspace."
---

# Essay Decoder & Epistemic Mental-Model Engine

Transform dense, jargon-laden essays, papers, and thought-leadership articles into crystal-clear mental models through first-principles causal deconstruction and bifurcated boundary analysis.

---

## 4-Layer Deconstruction Architecture

1. **Layer 1: The Feynman Mental Model (费曼直觉心智模型)**:
   - Eliminate academic jargon. Explain the core mechanism using a visceral, real-world physical analogy that an intelligent 12-year-old can instantly grasp.
2. **Layer 2: Causal Chain & Proposition Breakdown (因果推演与核心命题)**:
   - Extract the $N$ distinct core propositions: Premise $	o$ Causal Mechanism $	o$ Empirical Proof $	o$ Paradigm Shift.
3. **Layer 3: Bifurcated Epistemic Boundary Analysis (双轨认识论与边界旁注)**:
   - **For Technical / Architectural / Economic Claims**:
     ```markdown
     > [!NOTE] Failure Envelope & Boundary Analysis (∂D)
     > - **Invariant Preconditions**: What technical/organizational baselines must hold true?
     > - **Phase Boundary & Failure Mode (∂D)**: Under what parameter shifts does this model collapse?
     > - **Verifiable Heuristic & Acceptance Gate**: The stripped, robust operational rule and its testable assertion.
     ```
   - **For Philosophical / Humanistic / Historical Claims**:
     ```markdown
     > [!NOTE] Epistemic Context & Paradigm Boundary
     > - **Historical Precondition**: What socio-technical context produced this worldview?
     > - **Counter-Perspective**: What alternative philosophy validly challenges this premise?
     > - **Core Intellectual Value**: The non-dogmatic insight to retain.
     ```
4. **Layer 4: Actionable Playbook & Heuristic Extraction (实操行动算法)**:
   - Provide concrete, reproducible steps the reader can execute immediately.

---

## Operational Boundaries & Invariants

1. **Information-Entropy Sizing**: Output depth mathematically matches proposition density ($N$), stripping 100% of academic filler without lossy causal truncation.
2. **Language Parity**: Output body matches the source language by default.
3. **Silent Background Mount**: Silently mount newly created notes into VMark workspace without stealing OS focus.
4. **Non-Blocking Notification**: Deliver a lightweight, non-intrusive background banner upon completion: `(osascript -e 'display notification "..." with title "..."' >/dev/null 2>&1 &)`.
