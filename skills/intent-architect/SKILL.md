---
name: intent-architect
description: "Trigger when user says 'lucky', 'intent:', '大管家', 'spec:', or provides fast stream-of-consciousness/voice input with phonetic typos. Automatically performs silent ASR error correction, merges fragmented constraints, enforces non-destructive execution, guarantees 100% valid Markdown syntax, and outputs a concise 3-line task brief."
---

# Intent Architect

## Invocation Matrix

| Trigger | Mode | Input Arguments | Deterministic Action |
| :--- | :--- | :--- | :--- |
| `lucky` / `intent:` / `大管家` / `spec:` | Intent Synthesis | Voice/text stream of consciousness | Perform silent ASR repair; resolve constraints; emit 3-line execution brief |

---

## Execution Pipeline

1. **Silent Phonetic & ASR Correction**: Map voice recognition typos to technical reality (e.g. '批零' -> `P0`, '开复' -> `Cloudflare`, '为客' -> `VMark`).
2. **Constraint Synthesis**: Merge afterthoughts, contradictions, and fragmented sub-clauses into a single unified specification.
3. **Non-Destructive Safety Gate**: Default to backup/safe-write behaviors before modifying existing file systems.
4. **3-Line Execution Brief Output**:
   - `Core Objective`: Single unambiguous objective.
   - `Resolved Constraints`: Merged rules, flags, and paths.
   - `Immediate Action`: First physical execution step.

---

## Invariants & Operational Boundaries

1. **Zero Conversational Chatter**: Strictly limit output to the 3-line execution brief.
2. **Non-Destructive Default**: Never execute irreversible deletions or overwrites without explicit user confirmation.
3. **Syntax Integrity**: Output 100% valid Markdown without broken escape sequences.

---

## Runnable Input/Output Contract

### Input
```text
lucky: 那个帮我把批零的任务改一下就那个闲鱼的文案还有加上开复的那个域名解析
```

### Output Payload
```markdown
Intent Resolution Status:
- Core Objective: Update P0 task specification for Xianyu copy and configure Cloudflare domain DNS records.
- Resolved Constraints: Target domain `lifeaka7.com`; preserve P0 urgency; update existing Xianyu listing markdown.
- Immediate Action: Inspect `${VAULT_DIR:-$HOME/Documents/AI_Workspace}/CLI Chats/2026/2026-08/` for latest Xianyu draft.
```

---

## Acceptance Criteria

1. **Disambiguation**: 100% elimination of phonetic ASR typos.
2. **Latency**: Intent synthesis and brief generation completed in `< 500ms`.
