---
name: vmark-tab-cleaner
description: "Trigger when user requests cleaning or managing VMark editor tabs and windows (e.g. '清理Vmark窗口', '清理vmark', '关掉多余窗口', '保留最近修改的窗口', '保留最近5个窗口', '保留最近3个窗口', 'vmark:clean', 'vmark-clean', 'clean-vmark'). High-speed, zero-data-loss VMark tab manager that interacts directly with VMark's official MCP server, automatically saves dirty tabs to prevent data loss, sorts tabs by last modification time (mtime), retains the specified number of most recent tabs (default: 5, or 3, or custom N), and closes remaining tabs smoothly within 1-2 seconds."
---

# VMark Tab Cleaner: High-Speed Tab & Window Manager

## Invocation Matrix

| Trigger | Mode | Input Arguments | Deterministic Action |
| :--- | :--- | :--- | :--- |
| `清理Vmark窗口` / `清理vmark` | Default Keep (5) | None | Preserves top 5 most recently modified tabs; auto-saves dirty tabs; closes remaining tabs |
| `保留最近3个窗口` / `保留3个` | Targeted Keep (3) | `keep: 3` | Preserves top 3 most recently modified tabs; closes the rest |
| `保留最近 <N> 个窗口` | Custom Keep (N) | Integer $N \ge 0$ | Preserves top $N$ most recently modified tabs; closes the rest |
| `关掉全部Vmark窗口` / `全关掉` | Full Flush (0) | `keep: 0` / `--all` | Auto-saves any dirty tabs; closes 100% of open tabs (untitled dirty tabs safely preserved) |
| `vmark:clean --dry-run` | Simulation Preview | `--dry-run` | Inspects current tabs, sorts by recency, outputs keep/close plan without modifying tabs |

---

## Architecture & Execution Engine

```mermaid
flowchart TD
    Trigger["User Trigger ('清理Vmark窗口' / '保留最近N个')"] --> Step1["1. Query VMark Session (session.get_state)<br>• Enumerate and validate all open document tabs across windows"]
    Step1 --> Step2["2. Zero Data Loss Invariant Check<br>• For dirty tabs with filePath: invoke workspace.save and verify saved == true<br>• For untitled dirty tabs or failed saves: auto-preserve in keep set to prevent work loss"]
    Step2 --> Step3["3. Recency Evaluation & Sorting<br>• Query file mtime from disk / active timestamp<br>• Sort descending: newest modifications first"]
    Step3 --> Step4{"Partition Tabs"}
    Step4 -- Top N Tabs + Protected Dirty Tabs -- --> Keep["4a. Preserve Kept Tabs (workspace.switch_tab to top)"]
    Step4 -- Verified Closable Tabs -- --> Close["4b. Paced Sequential Closure (workspace.close, interval >= 0.08s)<br>• Verify closed is True per tab; avoid GUI freeze and rate limit tokens"]
    Keep & Close --> Step5["5. State Verification & Evidence Enforcement<br>• Re-query session.get_state; enforce actual final count == expected retained count"]
```

---

## Operational Boundaries & Hard Invariants

1. **Zero Data Loss Invariant (绝对零数据丢失)**:
   Any tab with `dirty == true` and a valid `filePath` MUST be persisted via `workspace.save(tabId=...)` and verified before closure. Any untitled dirty tab without a file path or any tab whose save operation cannot be confirmed MUST be preserved in the keep set to guarantee 100% user data protection.
2. **Rate-Limit & GUI Pacing Invariant (平滑流控防阻塞)**:
   VMark MCP server enforces rate limits and Webview GUI serialization. All closures MUST use sequential calls paced at `interval >= 0.08s` to eliminate `Rate limit exceeded` and `Request timeout after 20s` errors. CLI validates and rejects intervals below 0.08s.
3. **Official MCP Compliance (官方协议对齐)**:
   Exclusively use VMark's official MCP server binary (`/Applications/VMark.app/Contents/MacOS/vmark-mcp-server`) via JSON-RPC stdio. Subprocess communication implements deadline-bounded reads, response-ID matching, and `DEVNULL` stderr redirection to prevent pipe buffer deadlocks.
4. **Strict Post-State Enforcement (绝对物理状态对齐)**:
   After all closures, re-query `session.get_state`. The pipeline only emits `PASS` if the physical open tab count strictly equals the expected retained count (`len(keep_list)`) AND the final active tab-ID collection strictly matches the expected retained tab-ID set.
5. **Autonomous Parameter Extraction (自适应参数识别)**:
   Extract $N$ directly from user prompt (e.g. "保留最近3个" $\rightarrow N=3$, "保存最近5个" $\rightarrow N=5$, "全关掉" $\rightarrow N=0$). If unspecified, default to $N=5$.

---

## Execution Command

Execute the standalone script directly:

```bash
# Keep 5 most recently modified tabs (default)
${HOME}/.gemini/config/skills/vmark-tab-cleaner/scripts/clean_vmark_tabs.py --keep 5

# Keep 3 most recently modified tabs
${HOME}/.gemini/config/skills/vmark-tab-cleaner/scripts/clean_vmark_tabs.py --keep 3

# Close all tabs
${HOME}/.gemini/config/skills/vmark-tab-cleaner/scripts/clean_vmark_tabs.py --all

# Structured JSON output
${HOME}/.gemini/config/skills/vmark-tab-cleaner/scripts/clean_vmark_tabs.py --keep 5 --json
```

---

## Acceptance Criteria

1. **Execution Latency**: Tab closures complete in $\le 2.0$ seconds for up to 20 tabs ($\le 4.0$ seconds for 50 tabs).
2. **Zero Defect Operations**: 0 `Rate limit exceeded` errors; 0 `Request timeout after 20s` errors; 0 buffer deadlocks.
3. **Data Integrity Assurance**: 100% of dirty tabs with paths verified saved before closure; untitled or save-unconfirmed dirty tabs conditionally preserved.
4. **Strict State Grounding**: Physical open tab count matches the expected retained set with 0 discrepancy.
