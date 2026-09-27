import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from codex_session_day import scan


def message(time, text, role="user", message_id=None):
    return {"type": "response_item", "timestamp": time,
            "payload": {"type": "message", "role": role, "id": message_id,
                        "content": [{"type": "input_text", "text": text}]}}


class DayReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def log(self, name, records, source="cli", **meta):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        header = {"type": "session_meta", "payload":
                  {"id": name, "source": source, **meta}}
        path.write_text("\n".join(json.dumps(r) for r in [header, *records]) + "\n",
                        encoding="utf-8")
        return path

    def run_scan(self, **kwargs):
        output = []
        summary = scan(self.root, "2026-09-12", output.append, **kwargs)
        return output, summary

    def test_half_open_day_and_explicit_offsets(self):
        self.log("rollout-old.jsonl", [
            message("2026-09-11T15:59:59.999Z", "before"),
            message("2026-09-11T16:00:00Z", "start"),
            message("2026-09-12T23:59:59.999+08:00", "last"),
            message("2026-09-12T16:00:00Z", "next")])
        out, summary = self.run_scan()
        self.assertEqual([r["text"] for r in out], ["start", "last"])
        self.assertEqual(summary["matched_messages"], 2)
        self.assertTrue(summary["coverage_complete"])

    def test_old_directory_and_mtime_do_not_exclude_current_messages(self):
        path = self.log("2020/01/01/rollout-old.jsonl",
                        [message("2026-09-12T02:00:00Z", "long-lived")])
        os.utime(path, (100, 100))
        out, _ = self.run_scan()
        self.assertEqual(out[0]["text"], "long-lived")

    def test_only_explicit_spawn_is_deferred_and_forks_are_kept(self):
        row = message("2026-09-12T02:00:00Z", "result")
        self.log("rollout-main.jsonl", [row])
        self.log("rollout-fork.jsonl", [row], forked_from_id="main")
        self.log("rollout-sub.jsonl", [row],
                 source={"subagent": {"thread_spawn": {"parent_thread_id": "main"}}})
        self.log("rollout-unknown.jsonl", [row], source={"subagent": "other"})
        out, summary = self.run_scan()
        self.assertEqual({r["session_kind"] for r in out},
                         {"main_candidate", "fork_or_continuation", "unknown"})
        self.assertEqual(summary["deferred_subagent_messages"], 1)
        self.assertEqual(summary["matched_messages"], 4)
        self.assertEqual(len(summary["deferred_subagent_files"]), 1)
        all_out, _ = self.run_scan(include_subagents=True)
        self.assertEqual(len(all_out), 4)

    def test_event_mirrors_and_internal_reasoning_are_not_exported(self):
        self.log("rollout-types.jsonl", [
            message("2026-09-12T02:00:00Z", "visible"),
            message("2026-09-12T02:00:00Z", "system secret", role="system"),
            {"type": "event_msg", "timestamp": "2026-09-12T02:00:00Z",
             "payload": {"message": "mirror"}},
            {"type": "response_item", "timestamp": "2026-09-12T02:00:00Z",
             "payload": {"type": "reasoning", "text": "private"}}])
        out, _ = self.run_scan()
        self.assertEqual([r["text"] for r in out], ["visible"])

    def test_missing_ids_are_preserved_not_deduplicated_as_none(self):
        row = message("2026-09-12T02:00:00Z", "same words")
        self.log("rollout-ids.jsonl", [row, row])
        out, summary = self.run_scan()
        self.assertEqual(len(out), 2)
        self.assertEqual(summary["messages_without_id"], 2)
        self.assertNotEqual(out[0]["line"], out[1]["line"])

    def test_bad_json_and_unzoned_time_keep_valid_progress_but_report_gap(self):
        path = self.log("rollout-bad.jsonl", [
            message("2026-09-12T02:00:00", "ambiguous"),
            message("2026-09-12T02:00:00Z", "valid")])
        with path.open("ab") as f:
            f.write(b'{"unfinished":')
        out, summary = self.run_scan()
        self.assertEqual([r["text"] for r in out], ["valid"])
        self.assertFalse(summary["coverage_complete"])
        self.assertEqual({e["kind"] for e in summary["errors"]},
                         {"message_time", "json"})

    def test_missing_root_is_not_reported_as_empty_success(self):
        summary = scan(self.root / "missing", "2026-09-12", lambda _: None)
        self.assertFalse(summary["coverage_complete"])
        self.assertEqual(summary["errors"][0]["kind"], "root")

    def test_snapshot_does_not_chase_appended_content(self):
        path = self.log("rollout-live.jsonl",
                        [message("2026-09-12T02:00:00Z", "initial")])
        out = []
        def collect(row):
            out.append(row)
            with path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(message("2026-09-12T03:00:00Z", "late")) + "\n")
        summary = scan(self.root, "2026-09-12", collect)
        self.assertEqual([r["text"] for r in out], ["initial"])
        self.assertEqual(len(summary["changed_files"]), 1)
        self.assertTrue(summary["coverage_complete"])  # Initial byte range, not subsequent appends.

    def test_missing_content_is_reported_not_emitted_as_empty(self):
        row = message("2026-09-12T02:00:00Z", "lost")
        del row["payload"]["content"]
        self.log("rollout-missing-content.jsonl", [row])
        out, summary = self.run_scan()
        self.assertEqual(out, [])
        self.assertFalse(summary["coverage_complete"])
        self.assertEqual(summary["errors"][0]["kind"], "message_content")

    def test_unknown_session_is_distinct_from_known_session_with_no_messages(self):
        self.log("rollout-quiet.jsonl", [], session_id="quiet")
        _, known = self.run_scan(session="quiet")
        self.assertTrue(known["coverage_complete"])
        _, unknown = self.run_scan(session="missing")
        self.assertFalse(unknown["coverage_complete"])
        self.assertEqual(unknown["errors"][0]["kind"], "session_not_found")

    def test_session_filter_keeps_only_selected_source_and_reports_scope(self):
        row = message("2026-09-12T02:00:00Z", "content")
        self.log("rollout-one.jsonl", [row], session_id="one")
        self.log("rollout-two.jsonl", [row], session_id="two")
        out, summary = self.run_scan(session="two")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["session_id"], "two")
        self.assertEqual(summary["session_filter"], "two")

    def test_cli_summary_has_no_body_and_creates_no_files(self):
        self.log("rollout-cli.jsonl", [message("2026-09-12T02:00:00Z", "PRIVATE")])
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve().parents[1]
                                / "codex_session_day.py"), "--root", str(self.root),
                                "--date", "2026-09-12", "--summary-only"],
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("PRIVATE", result.stdout)
        self.assertEqual(json.loads(result.stdout)["matched_messages"], 1)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})


if __name__ == "__main__":
    unittest.main()
