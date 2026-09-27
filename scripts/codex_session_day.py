"""Read one UTC+8 day from local Codex logs; emit JSONL without writing files."""
import argparse
from datetime import date, datetime, time, timedelta, timezone
import json
import os
from pathlib import Path
import sys

LOCAL = timezone(timedelta(hours=8))


def session_kind(meta):
    source = meta.get("source")
    sub = source.get("subagent") if isinstance(source, dict) else None
    if isinstance(sub, dict) and "thread_spawn" in sub:
        return "spawned_subagent"
    if meta.get("forked_from_id") or meta.get("parent_thread_id"):
        return "fork_or_continuation"
    return "main_candidate" if isinstance(source, str) else "unknown"


def scan(root, day, emit, include_subagents=False, session=None):
    root = Path(root)
    start = datetime.combine(date.fromisoformat(day), time(), LOCAL)
    end = start + timedelta(days=1)
    report = dict(kind="summary", root=str(root), start=start.isoformat(),
                  end_exclusive=end.isoformat(), session_filter=session,
                  read_started_at=datetime.now(LOCAL).isoformat(),
                  files=0, snapshot_bytes=0, bytes_read=0, matched_messages=0,
                  emitted_messages=0, messages_without_id=0,
                  deferred_subagent_messages=0, deferred_subagent_files=[],
                  matched_files=[], changed_files=[], errors=[])

    def error(kind, path, line=None):
        report["errors"].append(dict(kind=kind, file=str(path), line=line))

    snapshot = []
    session_found = False
    if not root.is_dir():
        error("root", root)
    else:
        for folder, _, names in os.walk(root, onerror=lambda e: error("directory", e.filename)):
            for name in sorted(names):
                if name.startswith("rollout-") and name.endswith(".jsonl"):
                    path = Path(folder) / name
                    try:
                        stat = path.stat()
                        snapshot.append((path, stat.st_size, stat.st_mtime_ns))
                    except OSError:
                        error("stat", path)
    report["files"] = len(snapshot)
    report["snapshot_bytes"] = sum(size for _, size, _ in snapshot)
    for path, size, mtime in snapshot:
        meta, matched, deferred, consumed = {}, 0, 0, 0
        try:
            with path.open("rb") as stream:
                line = 0
                while consumed < size:
                    raw = stream.readline(size - consumed)
                    if not raw:
                        error("short_read", path, line + 1)
                        break
                    consumed += len(raw)
                    report["bytes_read"] += len(raw)
                    line += 1
                    if not raw.strip():
                        continue
                    try:
                        record = json.loads(raw)
                        if not isinstance(record, dict):
                            raise ValueError()
                    except (ValueError, UnicodeError):
                        error("json", path, line)
                        continue
                    payload = record.get("payload")
                    if not isinstance(payload, dict):
                        error("record_shape", path, line)
                        continue
                    if record.get("type") == "session_meta":
                        meta = payload
                        if session and session in (meta.get("session_id"), meta.get("id")):
                            session_found = True
                        continue
                    if record.get("type") != "response_item" or payload.get("type") != "message":
                        continue
                    if payload.get("role") not in ("user", "assistant"):
                        continue
                    if session and session not in (meta.get("session_id"), meta.get("id")):
                        continue
                    try:
                        stamp = datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00"))
                        if stamp.utcoffset() is None:
                            raise ValueError()
                    except (KeyError, AttributeError, TypeError, ValueError):
                        error("message_time", path, line)
                        continue
                    if not start <= stamp < end:
                        continue
                    matched += 1
                    report["matched_messages"] += 1
                    kind = session_kind(meta)
                    if kind == "spawned_subagent" and not include_subagents:
                        deferred += 1
                        report["deferred_subagent_messages"] += 1
                        continue
                    content = payload.get("content")
                    if not isinstance(content, list):
                        error("message_content", path, line)
                        continue
                    texts, non_text = [], []
                    for block in content:
                        if not isinstance(block, dict):
                            error("message_content", path, line)
                        elif block.get("type") in ("input_text", "output_text"):
                            if isinstance(block.get("text"), str):
                                texts.append(block["text"])
                            else:
                                error("message_content", path, line)
                        else:
                            non_text.append(block.get("type", "unknown"))
                    if not payload.get("id"):
                        report["messages_without_id"] += 1
                    emit(dict(kind="message", file=str(path), line=line,
                              session_id=meta.get("session_id") or meta.get("id"),
                              session_kind=kind, forked_from_id=meta.get("forked_from_id"),
                              parent_thread_id=meta.get("parent_thread_id"),
                              timestamp=stamp.astimezone(LOCAL).isoformat(),
                              message_id=payload.get("id"), role=payload["role"],
                              phase=payload.get("phase"), text="\n".join(texts),
                              non_text_types=non_text))
                    report["emitted_messages"] += 1
        except OSError:
            error("read", path)
        if matched:
            report["matched_files"].append(dict(file=str(path), messages=matched,
                                               session_id=meta.get("session_id") or meta.get("id"),
                                               session_kind=session_kind(meta)))
        if deferred:
            report["deferred_subagent_files"].append(str(path))
        try:
            after = path.stat()
            if (after.st_size, after.st_mtime_ns) != (size, mtime):
                report["changed_files"].append(str(path))
                if after.st_size <= size:
                    error("changed_in_place_or_shrunk", path)
        except OSError:
            error("post_read_stat", path)
    if session and not session_found:
        error("session_not_found", root)
    report["coverage_complete"] = not report["errors"]
    report["scope"] = ("Accessible rollout files at enumeration, bounded to initial file sizes; "
                       "visible text only, not tool results or attachment bodies. "
                       "Append-only logs assumed; no guarantee for unknown roots or concurrent replacement.")
    report["read_finished_at"] = datetime.now(LOCAL).isoformat()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD, UTC+8")
    parser.add_argument("--session", help="Optional session ID restriction")
    parser.add_argument("--include-subagents", action="store_true")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()
    try:
        date.fromisoformat(args.date)
    except ValueError:
        parser.error("--date must be YYYY-MM-DD")
    sys.stdout.reconfigure(encoding="utf-8")
    def output(row):
        print(json.dumps(row, ensure_ascii=False))
    report = scan(args.root, args.date, lambda row: None if args.summary_only else output(row),
                  include_subagents=args.include_subagents, session=args.session)
    output(report)
    return 0 if report["coverage_complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
