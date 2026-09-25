#!/usr/bin/env python3
"""
VMark Tab Cleaner (vmark-tab-cleaner)
High-speed, zero-data-loss window/tab manager for VMark via official MCP server.
"""

import argparse
import json
import os
import select
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Set

VMARK_MCP_BIN = "/Applications/VMark.app/Contents/MacOS/vmark-mcp-server"
MIN_PACING_INTERVAL = 0.08


class VMarkMCPClient:
    def __init__(self, binary_path: str = VMARK_MCP_BIN, timeout: float = 10.0):
        if not os.path.exists(binary_path):
            raise FileNotFoundError(f"VMark MCP server binary not found at: {binary_path}")
        self.binary_path = binary_path
        self.timeout = timeout
        self.proc: Optional[subprocess.Popen] = None
        self.req_id = 0

    def start(self):
        # Use DEVNULL for stderr to prevent pipe buffer deadlock
        self.proc = subprocess.Popen(
            [self.binary_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1
        )
        # 1. initialize
        init_res = self._send("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "vmark-tab-cleaner", "version": "1.0.0"}
        })
        if not init_res or "result" not in init_res or init_res.get("error"):
            raise RuntimeError(f"MCP initialize failed: {init_res}")

        # 2. notifications/initialized
        self._notify("notifications/initialized", {})
        # Pacing delay to let MCP server establish local IPC socket connection to VMark GUI
        time.sleep(0.3)
        return init_res

    def _read_line_with_timeout(self, remaining_timeout: float) -> Optional[str]:
        if not self.proc or not self.proc.stdout or remaining_timeout <= 0:
            return None
        rlist, _, _ = select.select([self.proc.stdout], [], [], remaining_timeout)
        if not rlist:
            raise TimeoutError(f"VMark MCP read timed out after {remaining_timeout}s")
        return self.proc.stdout.readline()

    def _send(self, method: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        if not self.proc or not self.proc.stdin:
            raise RuntimeError("VMark MCP process is not running")
        self.req_id += 1
        current_id = self.req_id
        payload = {
            "jsonrpc": "2.0",
            "id": current_id,
            "method": method
        }
        if params is not None:
            payload["params"] = params
        self.proc.stdin.write(json.dumps(payload) + "\n")
        self.proc.stdin.flush()

        # Read lines until matching response ID is found within deadline
        deadline = time.time() + self.timeout
        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                raise TimeoutError(f"VMark MCP request {current_id} timed out waiting for response")
            line = self._read_line_with_timeout(remaining)
            if not line:
                break
            try:
                data = json.loads(line)
            except Exception:
                continue
            if data.get("id") == current_id:
                return data
        return None

    def _notify(self, method: str, params: Optional[Dict[str, Any]] = None):
        if not self.proc or not self.proc.stdin:
            return
        payload = {
            "jsonrpc": "2.0",
            "method": method
        }
        if params is not None:
            payload["params"] = params
        self.proc.stdin.write(json.dumps(payload) + "\n")
        self.proc.stdin.flush()

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        res = self._send("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
        if not res:
            return {"error": "No response or timeout from MCP server"}
        if "error" in res:
            return {"error": res["error"]}
        result = res.get("result", {})
        if result.get("isError"):
            err_msg = ""
            for item in result.get("content", []):
                if item.get("type") == "text":
                    err_msg += item.get("text", "")
            return {"error": err_msg or "Tool execution error"}

        if "structuredContent" in result:
            return result["structuredContent"]
        content = result.get("content", [])
        if content and content[0].get("type") == "text":
            try:
                return json.loads(content[0]["text"])
            except Exception:
                return {"text": content[0]["text"]}
        return result

    def get_state(self) -> Dict[str, Any]:
        return self.call_tool("session", {"action": "get_state"})

    def save_tab(self, tab_id: str) -> Dict[str, Any]:
        return self.call_tool("workspace", {"action": "save", "tabId": tab_id})

    def close_tab(self, tab_id: str, force: bool = True) -> Dict[str, Any]:
        return self.call_tool("workspace", {"action": "close", "tabId": tab_id, "force": force})

    def switch_tab(self, tab_id: str) -> Dict[str, Any]:
        return self.call_tool("workspace", {"action": "switch_tab", "tabId": tab_id})

    def stop(self):
        if self.proc:
            try:
                self.proc.terminate()
                self.proc.wait(timeout=1.0)
            except Exception:
                self.proc.kill()
            self.proc = None


def run_cleaner(keep_count: int = 5, dry_run: bool = False, interval: float = MIN_PACING_INTERVAL) -> Dict[str, Any]:
    safe_keep = max(0, keep_count)
    if interval < MIN_PACING_INTERVAL:
        return {
            "status": "ERROR",
            "message": f"Interval {interval}s is below minimum safe threshold {MIN_PACING_INTERVAL}s (rate-limit invariant)."
        }

    client = VMarkMCPClient()
    t_start = time.time()
    try:
        client.start()
        state = client.get_state()
        if "error" in state:
            return {"status": "ERROR", "message": state["error"]}

        windows = state.get("windows", [])
        if not isinstance(windows, list):
            return {"status": "ERROR", "message": f"Invalid windows schema: {windows}"}

        all_tabs: List[Dict[str, Any]] = []
        for win in windows:
            if not isinstance(win, dict):
                continue
            tabs = win.get("tabs", [])
            if not isinstance(tabs, list):
                continue
            for tab in tabs:
                if not isinstance(tab, dict):
                    return {"status": "ERROR", "message": f"Malformed tab object: {tab}"}
                tab_id = tab.get("id")
                if not isinstance(tab_id, str) or not tab_id.strip():
                    return {"status": "ERROR", "message": f"Invalid tab ID: {tab_id}"}
                all_tabs.append(tab)

        total_initial = len(all_tabs)
        if total_initial == 0:
            return {
                "status": "PASS",
                "initial_count": 0,
                "kept_count": 0,
                "closed_count": 0,
                "saved_dirty_count": 0,
                "final_count": 0,
                "kept_tabs": [],
                "elapsed_seconds": round(time.time() - t_start, 3),
                "message": "No open tabs in VMark."
            }

        # Inspect and evaluate recency mtime for each tab
        processed_tabs = []
        now = time.time()
        for tab in all_tabs:
            fpath = tab.get("filePath")
            is_dirty = bool(tab.get("dirty", False))
            title = str(tab.get("title", "Untitled"))
            tab_id = tab["id"]

            mtime = 0.0
            if is_dirty:
                mtime = now + 1000.0
            elif fpath and isinstance(fpath, str) and os.path.exists(fpath):
                try:
                    mtime = os.path.getmtime(fpath)
                except OSError:
                    mtime = 0.0

            processed_tabs.append({
                "tabId": tab_id,
                "title": title,
                "filePath": fpath,
                "dirty": is_dirty,
                "mtime": mtime
            })

        # Sort descending by mtime: newest modifications first
        processed_tabs.sort(key=lambda t: t["mtime"], reverse=True)

        target_keep = min(safe_keep, total_initial)
        keep_list = processed_tabs[:target_keep]
        candidate_close_list = processed_tabs[target_keep:]

        saved_dirty_count = 0
        closed_count = 0
        close_errors = []

        # Partition with Zero Data Loss Invariant (applied identically to dry-run and real-run)
        verified_close_list = []
        for tab_info in candidate_close_list:
            if tab_info["dirty"]:
                fpath = tab_info.get("filePath")
                if not fpath or not isinstance(fpath, str):
                    # Untitled dirty document: refuse to close to preserve work
                    keep_list.append(tab_info)
                    continue
                if not dry_run:
                    # Persist via MCP save and strictly verify response
                    save_res = client.save_tab(tab_info["tabId"])
                    if not isinstance(save_res, dict) or "error" in save_res:
                        keep_list.append(tab_info)
                        continue
                    is_saved = save_res.get("saved") is True or bool(save_res.get("revision"))
                    if not is_saved:
                        keep_list.append(tab_info)
                        continue
                    saved_dirty_count += 1
                    time.sleep(interval)
            verified_close_list.append(tab_info)

        if not dry_run:
            # Paced Sequential Closure
            for tab_info in verified_close_list:
                close_res = client.close_tab(tab_info["tabId"], force=True)
                if isinstance(close_res, dict) and close_res.get("closed") is True:
                    closed_count += 1
                else:
                    close_errors.append({"tabId": tab_info["tabId"], "response": close_res})
                    return {
                        "status": "FAIL",
                        "message": f"Tab closure unverified for tab {tab_info['tabId']}: {close_res}",
                        "initial_count": total_initial,
                        "kept_count": len(keep_list),
                        "closed_count": closed_count,
                        "close_errors": close_errors,
                        "elapsed_seconds": round(time.time() - t_start, 3)
                    }
                time.sleep(interval)

            # Focus top kept tab if tabs remain
            if keep_list:
                top_tab_id = keep_list[0]["tabId"]
                client.switch_tab(top_tab_id)

            # Strict post-state verification: validate both count AND tab ID set
            time.sleep(0.1)
            final_state = client.get_state()
            if "error" in final_state:
                return {
                    "status": "FAIL",
                    "message": f"Post-verification get_state failed: {final_state['error']}",
                    "initial_count": total_initial,
                    "closed_count": closed_count
                }

            final_windows = final_state.get("windows")
            if not isinstance(final_windows, list):
                return {"status": "FAIL", "message": f"Malformed final windows schema: {final_windows}"}

            final_tabs = []
            final_tab_ids = []
            for win in final_windows:
                if not isinstance(win, dict):
                    continue
                tabs = win.get("tabs")
                if not isinstance(tabs, list):
                    continue
                for tab in tabs:
                    if not isinstance(tab, dict):
                        return {"status": "FAIL", "message": f"Malformed final tab: {tab}"}
                    tid = tab.get("id")
                    if not isinstance(tid, str) or not tid.strip():
                        return {"status": "FAIL", "message": f"Invalid final tab ID: {tid}"}
                    final_tabs.append(tab)
                    final_tab_ids.append(tid)

            if len(final_tab_ids) != len(set(final_tab_ids)):
                return {"status": "FAIL", "message": "Duplicate tab IDs detected in final state"}

            expected_ids = sorted([t["tabId"] for t in keep_list])
            actual_ids = sorted(final_tab_ids)

            if actual_ids != expected_ids:
                return {
                    "status": "FAIL",
                    "message": f"Tab verification mismatch: expected IDs {expected_ids}, actual IDs {actual_ids}",
                    "initial_count": total_initial,
                    "kept_count": len(keep_list),
                    "closed_count": closed_count,
                    "final_count": len(final_tabs),
                    "close_errors": close_errors,
                    "elapsed_seconds": round(time.time() - t_start, 3)
                }
        else:
            final_count = len(keep_list)
            closed_count = len(verified_close_list)

        t_elapsed = round(time.time() - t_start, 3)

        return {
            "status": "PASS",
            "initial_count": total_initial,
            "kept_count": len(keep_list),
            "closed_count": closed_count,
            "saved_dirty_count": saved_dirty_count,
            "final_count": final_count,
            "kept_tabs": [{"title": t["title"], "filePath": t["filePath"]} for t in keep_list],
            "close_errors": close_errors,
            "elapsed_seconds": t_elapsed,
            "dry_run": dry_run
        }
    finally:
        client.stop()


def validate_interval(val: str) -> float:
    f = float(val)
    if f < MIN_PACING_INTERVAL:
        raise argparse.ArgumentTypeError(
            f"Interval {f}s is below minimum safe threshold {MIN_PACING_INTERVAL}s (rate-limit invariant)."
        )
    return f


def main():
    parser = argparse.ArgumentParser(description="High-speed, zero-data-loss VMark tab cleaner.")
    parser.add_argument("--keep", "-k", type=int, default=5, help="Number of most recently modified tabs to keep (default: 5). Use 0 to close all.")
    parser.add_argument("--all", "-a", action="store_true", help="Close all open tabs (equivalent to --keep 0).")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without closing tabs.")
    parser.add_argument("--interval", type=validate_interval, default=MIN_PACING_INTERVAL, help=f"Delay between closures in seconds (min: {MIN_PACING_INTERVAL}).")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format.")

    args = parser.parse_args()
    keep_n = 0 if args.all else max(0, args.keep)

    result = run_cleaner(keep_count=keep_n, dry_run=args.dry_run, interval=args.interval)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if result.get("status") != "PASS":
        print(f"Error: {result.get('message', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)

    mode_str = " (DRY RUN)" if args.dry_run else ""
    print(f"=== VMark Tab Cleaner{mode_str} ===")
    print(f"Initial open tabs:    {result['initial_count']}")
    print(f"Kept tabs:            {result['kept_count']}")
    print(f"Closed tabs:          {result['closed_count']}")
    print(f"Auto-saved dirty tabs:{result['saved_dirty_count']}")
    print(f"Final open tabs:      {result['final_count']}")
    print(f"Elapsed time:         {result['elapsed_seconds']}s")

    if result["kept_tabs"]:
        print("\nPreserved Tabs:")
        for idx, tab in enumerate(result["kept_tabs"], 1):
            print(f"  {idx}. {tab['title']}")


if __name__ == "__main__":
    main()
