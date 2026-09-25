---
name: context-distiller
description: "Trigger when the user requests context compression, session handoff, or conversation resumption (e.g. 'compress:', 'handoff:', 'distill:', 'resume', 'continue', '继续', '压缩', '接力', '换窗口'). Executes (1) lossless 4-layer state distillation into a 300-600 token Context Capsule with silent macOS clipboard copy, or (2) multi-session resumption via Option 3 interactive candidate selection."
---

# Context Distiller

## Invocation Matrix

| Trigger | Execution Mode | Input Argument | Deterministic Action |
| :--- | :--- | :--- | :--- |
| `compress:` / `压缩` / `交接` | Lossless Handoff | Optional (keyword or file path) | Distill target session into 300-600 token 4-layer capsule; pipe payload to `pbcopy` |
| `handoff:` / `换窗口` | Session Handoff | None | Generate capsule; pipe to `pbcopy`; prompt user to paste in new window |
| `继续` / `resume` / `接力` | Session Resume | None | Sniff active sessions in 24h: auto-resume if single active session; render Option 3 picker if multiple |
| `继续 <index/keyword>` | Targeted Resume | Index (`1`, `2`) or keyword | Match target session and immediately resume execution without prompt |

---

## Dual-Engine Pipeline

```mermaid
flowchart TD
    subgraph Mode 1: Session Distillation (Compress / Handoff)
    A1["Input: Raw Conversation Log (>10k Tokens)"] --> B1["4-Layer State Extraction<br>1. Concept Definitions  2. Decision Trajectory<br>3. Artifact Inventory   4. Tail Breakpoint"]
    B1 --> C1["Output: Context Capsule (300-600 Tokens)<br>+ execute pbcopy silently"]
    end

    subgraph Mode 2: Session Resume (Resume / Option 3)
    A2["Input: '继续' or 'resume'"] --> B2{"Active Sessions in 24h"}
    B2 -- Single active session -- --> C2["Load state and resume work immediately"]
    B2 -- Multiple active sessions (2-3) -- --> D2["Render Option 3 Candidate Picker [1][2][3]<br>Wait for user index/keyword selection"]
    end
```

---

## 4-Layer Distillation Engine

1. **Layer 1: Concept & Config Definitions**:
   - Extract domain-specific entities, operational definitions, and static configurations (domains, models, ports, credentials).
   - Omit narrative explanations and introductory background.

2. **Layer 2: Decision Trajectory**:
   - Extract the chronological chain of user goals and architectural decisions from `## You` headings.
   - Retain only final adopted decisions; discard superseded proposals, abandoned tangents, and conversational chatter.

3. **Layer 3: Artifact Inventory**:
   - Extract all created, modified, or referenced file paths formatted as absolute `file:///` URIs.
   - Annotate current physical status on disk (`Verified Ready`, `Pending Edits`, or `Missing`).

4. **Layer 4: Tail Breakpoint & Disambiguation**:
   - Parse the final 1-2 interaction turns.
   - Disambiguate referential pronouns ("this task", "the earlier file") into explicit entity names and file paths.
   - Isolate the single unresolved P0 pending deliverable.

---

## Multi-Session Disambiguation Protocol (Option 3)

When resuming via `继续` or `resume` without arguments:
1. **Single Session Case**: If only 1 session was updated within the last 3 hours, bypass the picker and resume work immediately.
2. **Concurrent Multi-Session Case**: If 2 or more distinct sessions were updated within the last 24 hours:
   - Execute `python3 ~/.gemini/config/skills/context-distiller/scripts/resume_finder.py --list`.
   - Render a 3-option candidate card containing index, title, relative time, turn count, and last prompt snippet.
   - Await single-keystroke input (e.g. `1`) or keyword (e.g. `xianyu`).
3. **Execution on Selection**: Load the chosen session, extract its Context Capsule, output a 3-line status card, and proceed with the pending task immediately.

---

## Invariants & Operational Boundaries

1. **Strict Determinism**: Emit only factual data; omit greetings, apologies, and conversational fluff.
2. **Physical Verification**: Include only file paths verified against the local file system with `file:///` URIs.
3. **Explicit Referencing**: Bind all task descriptions to explicit file basenames and entity identifiers; omit ambiguous pronouns.
4. **Token Budget Enforcement**: Restrict Context Capsule raw payload strictly between 300 and 600 tokens. Never exceed 800 tokens.
5. **Missing File Defense**: If no chat logs exist in `${VAULT_DIR:-$HOME/Documents/AI_Workspace}/CLI Chats/`, emit `Error: No chat logs found in target directory` and abort.

---

## Runnable Input/Output Contracts

### Contract A: Handoff Mode (`compress:`)
* **Input**:
```text
compress: ${VAULT_DIR:-$HOME/Documents/AI_Workspace}/CLI Chats/2026/2026-08/2026-08-28 - 继续 --b99da70a.md
```
* **Output Payload**:
```markdown
# Context Capsule

> Source: `2026-08-28 - 继续 --b99da70a.md` (file://${VAULT_DIR:-$HOME/Documents/AI_Workspace}/CLI%20Chats/2026/2026-08/2026-08-28%20-%20%E7%BB%A7%E7%BB%AD%20--8c5fdab7.md)
> Turn Count: 30 | Artifacts: 5 | Size: ~420 tokens

---

### 1. Objectives & Decisions
- Objective: Launch interactive audiobook reader and implement customized book service on Xianyu.
- Decisions:
  1. Architecture: Cloudflare Pages static hosting + Cloudflare R2 audio streaming.
  2. Domain: Bind `lifeaka7.com`, no ICP required, global CDN acceleration.
  3. Quality System: Integrate Li Xiaolai Multi-Agent model with NLPM linting.

### 2. Artifact Inventory
- `index.html` (file://${HOME}/Vault/Audible/index.html): Verified Ready (6 audiobooks deployed).
- `course_notes` (file://${VAULT_DIR:-$HOME/Documents/AI_Workspace}/李笑来/持续学习李笑来/01笑来分享合集（更新）/): Verified Ready.

### 3. Tail Breakpoint & Next Action
- Last Focus: Xianyu listing copy and operational compliance rules.
- P0 Next Action: Record 15-second Sepia highlight demo video storyboard or configure domain DNS records.
```
*(Silent system execution: `echo "$CAPSULE_CONTENT" | pbcopy`)*

---

### Contract B: Multi-Session Resume Mode (`继续`)
* **Input**:
```text
继续
```
* **Output Payload**:
```markdown
Multiple active sessions detected. Select target session to resume:

- [1] Xianyu Audiobook Customization (3 min ago | 30 turns)
  > Focus: Listing copy and operational compliance rules...
- [2] Li Xiaolai Mental Models & Context Distiller (just now | 10 turns)
  > Focus: Building lossless context distillation agent...
- [3] Audiobook Reader Deployment (1 hour ago | 15 turns)
  > Focus: Cloudflare Pages and lifeaka7.com DNS setup...

Reply with index (e.g. 1) or keyword (e.g. Xianyu) to resume.
```

---

## Edge Cases & Verification Matrix

| Case ID | Input Trigger | Condition | Expected Behavior |
| :--- | :--- | :--- | :--- |
| **TC-01** | `compress:` | Single active session | Distill latest chat -> output 400-token capsule -> pipe to `pbcopy` |
| **TC-02** | `继续` | 2+ concurrent sessions in 24h | Trigger Option 3 -> render `[1][2][3]` picker -> wait for selection |
| **TC-03** | `继续 闲鱼` | Keyword specified | Weighted keyword match -> bypass picker -> resume target session immediately |
| **TC-04** | `继续` | Empty directory | Emit error pointing to `/CLI Chats/` -> abort cleanly without hallucination |

---

## Acceptance Criteria

1. **Latency**: Active session discovery and distillation must complete in `< 1.0s`.
2. **State Completeness**: Capsule payload must remain within 300-600 tokens while preserving 100% of active `file:///` URIs, architectural decisions, and P0 blockers.
3. **Clipboard Automation**: Generated capsule must be silently written to macOS clipboard via `pbcopy` with exit code 0.
4. **Disambiguation Accuracy**: 100% disambiguation in concurrent multi-window environments via Option 3 decision picker.
