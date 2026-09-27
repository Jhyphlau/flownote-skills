import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'kimi_session_day.py'


def user(t, text='hello'):
    return dict(type='context.append_message', time=t,
                message=dict(role='user', content=[dict(type='text', text=text)], origin={'kind': 'user'}))


def part(t, kind='text', text='answer'):
    return dict(type='context.append_loop_event', time=t,
                event=dict(type='content.part', uuid='p1', turnId='t1', stepUuid='s1',
                           part={'type': kind, kind: text}))


class KimiTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.exists(), 'Kimi reader is not implemented')
        spec = importlib.util.spec_from_file_location('kimi_reader', SCRIPT)
        self.reader = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.reader)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def log(self, rows, agent='main', parent=None):
        base = self.root / 'old-workspace' / 'session_old'
        path = base / 'agents' / agent / 'wire.jsonl'
        path.parent.mkdir(parents=True, exist_ok=True)
        state = base / 'state.json'
        data = json.loads(state.read_text()) if state.exists() else {'agents': {}}
        data['agents'][agent] = {'parentAgentId': parent}
        state.write_text(json.dumps(data), encoding='utf-8')
        path.write_text(''.join(json.dumps(r)+'\n' for r in rows), encoding='utf-8')
        return path

    def scan(self, **kwargs):
        out = []
        report = self.reader.scan(self.root, '2026-09-12', out.append, **kwargs)
        return out, report

    def test_date_boundary_uses_epoch_milliseconds_not_mtime(self):
        # 2026-09-12 00:00 UTC+8 == 2026-09-11 16:00 UTC.
        from datetime import datetime
        start = int(datetime.fromisoformat('2026-09-11T16:00:00+00:00').timestamp()*1000)
        path = self.log([user(start-1), user(start, 'start'), part(start+86399999), user(start+86400000)])
        os.utime(path, (100, 100))
        out, report = self.scan()
        self.assertEqual([r['text'] for r in out], ['start', 'answer'])
        self.assertTrue(report['coverage_complete'])

    def test_excludes_reasoning_prompt_mirror_and_compaction(self):
        t = 1789185600000  # 2026-09-12, UTC+8
        self.log([user(t), part(t), part(t, 'think', 'PRIVATE'),
                  {'type': 'turn.prompt', 'time': t, 'input': 'hello'},
                  {'type': 'context.apply_compaction', 'time': t, 'summary': 'old text'}])
        out, _ = self.scan()
        self.assertEqual([r['text'] for r in out], ['hello', 'answer'])

    def test_only_parent_marked_agents_are_deferred(self):
        self.log([user(1789185600000)])
        self.log([part(1789185600000)], 'agent-0', 'main')
        self.log([part(1789185600000)], 'other')
        out, report = self.scan()
        self.assertEqual(len(out), 2)
        self.assertEqual(report['deferred_subagent_records'], 1)
        all_out, _ = self.scan(include_subagents=True)
        self.assertEqual(len(all_out), 3)

    def test_unverified_assistant_message_is_not_duplicate_visible_part(self):
        row = user(1789185600000, 'answer')
        row['message']['role'] = 'assistant'
        self.log([row, part(1789185600000)])
        out, report = self.scan()
        self.assertEqual([r['text'] for r in out], ['answer'])
        self.assertFalse(report['coverage_complete'])
        self.assertEqual(report['errors'][0]['kind'], 'unverified_assistant_message')

    def test_missing_time_bad_json_and_content_are_gaps(self):
        bad = user(1789185600000)
        del bad['message']['content']
        path = self.log([user(None), bad, user(1789185600000)])
        with path.open('ab') as f:
            f.write(b'{')
        out, report = self.scan()
        self.assertEqual(len(out), 1)
        self.assertEqual({e['kind'] for e in report['errors']}, {'time', 'content', 'json'})

    def test_known_empty_session_not_confused_with_missing(self):
        self.log([])
        _, known = self.scan(session='old')
        _, missing = self.scan(session='absent')
        self.assertTrue(known['coverage_complete'])
        self.assertFalse(missing['coverage_complete'])
        self.assertEqual(missing['errors'][0]['kind'], 'session_not_found')

    def test_append_is_not_chased_and_missing_root_fails(self):
        path = self.log([user(1789185600000)])
        def emit(_):
            with path.open('a') as f:
                f.write(json.dumps(user(1789185600000))+'\n')
        report = self.reader.scan(self.root, '2026-09-12', emit)
        self.assertEqual(report['emitted_records'], 1)
        self.assertEqual(len(report['changed_files']), 1)
        self.assertTrue(report['coverage_complete'])
        report = self.reader.scan(self.root/'absent', '2026-09-12', emit)
        self.assertFalse(report['coverage_complete'])

    def test_cli_summary_is_read_only(self):
        self.log([user(1789185600000, 'PRIVATE')])
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--root', str(self.root),
                                 '--date', '2026-09-12', '--summary-only'], capture_output=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('PRIVATE', result.stdout)
        self.assertEqual(json.loads(result.stdout)['emitted_records'], 1)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_desktop_shared_session_layout_and_prefixed_id(self):
        # Desktop-linked logs use the same wire format. A newer state may omit
        # parentAgentId for main; neither state version nor cwd is a client tag.
        path = self.log([user(1789185600000), part(1789185600000),
                         part(1789185600000, 'think', 'PRIVATE')])
        state = path.parents[2] / 'state.json'
        state.write_text(json.dumps({'id': 'old', 'version': 2, 'cwd': '/example',
                                     'agents': {'main': {'type': 'main', 'homedir': str(path.parent)}},
                                     'custom': {}}), encoding='utf-8')
        out, report = self.scan(session='session_old')
        self.assertTrue(report['coverage_complete'])
        self.assertEqual([(r['role'], r['text'], r['session_kind']) for r in out],
                         [('user', 'hello', 'main'), ('assistant', 'answer', 'main')])
        self.assertEqual({r['session_id'] for r in out}, {'old'})

    def test_shared_session_scan_does_not_duplicate_explicit_session_read(self):
        self.log([user(1789185600000), part(1789185600000)])
        all_out, all_report = self.scan()
        selected, selected_report = self.scan(session='session_old')
        self.assertTrue(all_report['coverage_complete'])
        self.assertTrue(selected_report['coverage_complete'])
        self.assertEqual(len(all_out), 2)
        self.assertEqual(all_out, selected)
