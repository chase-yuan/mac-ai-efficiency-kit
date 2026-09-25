---
name: nlpm
description: "Natural-Language Programming Manager (NLPM) based on Li Xiaolai's xiaolai/nlpm repository. Trigger when user says 'nlpm:', '/nlpm:score', '/nlpm:check', '/nlpm:fix', '/nlpm:test', 'nlpm', '自然语言编程', '提示词质检', '给提示词打分', '优化Prompt', or asks to lint, score, validate, or refactor natural-language artifacts (Skills, Agents, Prompts, AGENTS.md, CLAUDE.md)."
---

# NLPM: Natural-Language Programming Manager

## Invocation Matrix

| Command | Mode | Target Artifact | Deterministic Action |
| :--- | :--- | :--- | :--- |
| `nlpm:score` / `/nlpm:score` | 100-Point Quality Scoring | Markdown prompts, skills, agents | Score against 50 NLPM rules; output penalty breakdown and score card |
| `nlpm:check` / `/nlpm:check` | Static Consistency Check | Plugin manifests, file paths | Execute `~/.local/bin/nlpm-check`; verify disk-vs-manifest consistency |
| `nlpm:fix` / `/nlpm:fix` | Industrial Auto-Refactor | Failing NL artifacts (<90 score) | Strip fluff, eliminate vague quantifiers, enforce positive invariants, refactor to 95+ |
| `nlpm:test` / `/nlpm:test` | NL-TDD Boundary Testing | Specification files | Execute edge-case verification matrices against prompt contracts |

---

## 100-Point Scoring Rubric

```text
Base Score = 100
Final Score = max(0, min(100, 100 - SUM(Penalties)))
```

### Core Penalty Matrix (50 Rules of NL Programming)

| Rule ID | Quality Dimension | Violation Condition | Penalty |
| :--- | :--- | :--- | :---: |
| **R01** | **Quantifier Precision** | Vague quantifiers without criteria (e.g. uncalibrated terms without explicit criteria) | -2 each (cap -20) |
| **R02 / R05** | **Token Justification & Density** | Decorative emojis, conversational pleasantries, empty marketing narrative | -5 to -15 |
| **R03** | **Imperative Framing** | Negative prohibitions without explicit positive operational invariants | -5 |
| **R04** | **Trigger Specificity** | Description missing specific action phrases matching user queries (<3 triggers) | -15 to -25 |
| **R06** | **Contract Grounding** | Missing concrete runnable Input/Output contract payloads | -10 |
| **R07** | **Operational Boundaries** | Missing invariant boundaries, rate limits, or error fallbacks | -10 |
| **R08** | **Testable Acceptance** | Missing quantifiable, testable completion criteria | -15 |
| **R12** | **Logical Consistency** | Conflicting rules, broken file paths, or self-contradictory metrics | -20 |

---

## Execution Standards

When invoked:
1. **Output Structured Score Card**:
   - `Final Score`: `[X / 100]` (Production: >=90, Good: 80-89, Refactor: <80).
   - `Rule Violations`: List `Rule ID`, offending line/phrase, and exact penalty.
   - `Actionable Fixes`: Provide precise replacement text.
2. **On Refactoring (`nlpm:fix`)**: Emit 100% complete, drop-in replacement Markdown code blocks without partial omissions.

---

## Acceptance Criteria

1. **Deterministic Scoring**: Same input artifact produces identical penalty calculations across runs.
2. **Validation Tooling**: Seamless integration with standalone `~/.local/bin/nlpm-check` binary.
