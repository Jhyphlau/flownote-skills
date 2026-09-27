import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'claude_session_day.py'


def row(text='hi', stamp='2026-09-12T04:00:00Z', entry='cli', side=False):
    return dict(type='user', timestamp=stamp, entrypoint=entry, isSidechain=side,
                sessionId='s1', uuid=None, message=dict(role='user', content=text))


class ClaudeTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.exists(), 'Claude reader not implemented')
        spec=importlib.util.spec_from_file_location('claude_reader', SCRIPT)
        self.reader=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.reader)
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def log(self, rows):
        p=self.root/'old-project'/'s1.jsonl'
        p.parent.mkdir(exist_ok=True)
        p.write_text(''.join(json.dumps(r)+'\n' for r in rows), encoding='utf-8')
        return p

    def scan(self, **args):
        out=[]
        report=self.reader.scan(self.root,'2026-09-12',out.append,**args)
        return out, report

    def test_boundary_and_old_mtime(self):
        p=self.log([row('before','2026-09-11T15:59:59Z'),row('start','2026-09-11T16:00:00Z'),
                    row('end','2026-09-12T23:59:59.999+08:00'),row('next','2026-09-12T16:00:00Z')])
        os.utime(p,(100,100))
        out,report=self.scan()
        self.assertEqual([r['text'] for r in out],['start','end'])
        self.assertTrue(report['coverage_complete'])

    def test_entrypoint_filter_preserves_unknown_in_all(self):
        self.log([row(entry='cli'),row(entry='claude-desktop-3p'),row(entry='sdk-cli')])
        out,_=self.scan(client='desktop')
        self.assertEqual(len(out),1)
        out,report=self.scan()
        self.assertEqual(len(out),3)
        self.assertEqual(report['unknown_client_records'],1)

    def test_thinking_tools_and_system_are_not_exported(self):
        a=row(); a.update(type='assistant',message={'role':'assistant','content':[
            {'type':'thinking','thinking':'PRIVATE'},{'type':'text','text':'visible'},
            {'type':'tool_use','input':{'secret':'PRIVATE'}}]})
        b=row(); b['message']['content']=[{'type':'tool_result','content':'PRIVATE'}]
        self.log([a,b,{'type':'system','content':'PRIVATE'}])
        out,_=self.scan()
        self.assertEqual([r['text'] for r in out],['visible'])

    def test_subagent_deferred_without_excluding_parent_link(self):
        a=row(); a['parentUuid']='previous'
        self.log([a,row(side=True)])
        out,r=self.scan()
        self.assertEqual(len(out),1)
        self.assertEqual(r['deferred_subagent_records'],1)
        out,_=self.scan(include_subagents=True)
        self.assertEqual(len(out),2)

    def test_bad_records_and_missing_session_report_gaps(self):
        b=row(); del b['message']['content']
        p=self.log([row(stamp='2026-09-12T12:00:00'),b,row()])
        with p.open('ab') as f: f.write(b'{')
        out,r=self.scan()
        self.assertEqual(len(out),1)
        self.assertEqual({e['kind'] for e in r['errors']},{'time','content','json'})
        _,r=self.scan(session='absent')
        self.assertIn('session_not_found',{e['kind'] for e in r['errors']})

    def test_no_dedup_by_missing_uuid_or_shared_api_message_id(self):
        a=row(); a['message']['id']='shared'
        self.log([a,a])
        out,_=self.scan()
        self.assertEqual(len(out),2)
        self.assertNotEqual(out[0]['line'],out[1]['line'])

    def test_filename_is_not_proof_of_session_identity(self):
        a=row(); a['sessionId']='different'
        self.log([a])
        out,r=self.scan(session='s1')
        self.assertEqual(out,[])
        self.assertFalse(r['coverage_complete'])
        self.assertEqual(r['errors'][0]['kind'],'session_not_found')

    def test_append_bounded_and_missing_root_fails(self):
        p=self.log([row()])
        def emit(_):
            with p.open('a') as f: f.write(json.dumps(row())+'\n')
        r=self.reader.scan(self.root,'2026-09-12',emit)
        self.assertEqual(r['emitted_records'],1)
        self.assertEqual(len(r['changed_files']),1)
        self.assertTrue(r['coverage_complete'])
        r=self.reader.scan(self.root/'absent','2026-09-12',emit)
        self.assertFalse(r['coverage_complete'])

    def test_cli_summary_does_not_write_sources(self):
        p=self.log([row('PRIVATE')]); before=p.read_bytes()
        r=subprocess.run([sys.executable,'-B',str(SCRIPT),'--root',str(self.root),
                          '--date','2026-09-12','--summary-only'],capture_output=True,encoding='utf-8')
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertNotIn('PRIVATE',r.stdout)
        self.assertEqual(json.loads(r.stdout)['emitted_records'],1)
        self.assertEqual(p.read_bytes(),before)
