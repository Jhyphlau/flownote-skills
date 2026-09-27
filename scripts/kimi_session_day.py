"""Read a UTC+8 day of Kimi Code wire records. No source or output files are written."""
import argparse
from datetime import date, datetime, time, timedelta, timezone
import json
import os
from pathlib import Path
import sys

LOCAL = timezone(timedelta(hours=8))


def scan(root, day, emit, include_subagents=False, session=None):
    root = Path(root)
    start = datetime.combine(date.fromisoformat(day), time(), LOCAL)
    end = start + timedelta(days=1)
    report = dict(kind='summary', platform='kimi-code', root=str(root),
                  start=start.isoformat(), end_exclusive=end.isoformat(), session_filter=session,
                  read_started_at=datetime.now(LOCAL).isoformat(), files=0, snapshot_bytes=0,
                  bytes_read=0, matched_records=0, emitted_records=0,
                  deferred_subagent_records=0, matched_files=[], changed_files=[], errors=[])

    def error(kind, path, line=None):
        report['errors'].append(dict(kind=kind, file=str(path), line=line))

    snapshot = []
    if not root.is_dir():
        error('root', root)
    else:
        for folder, _, names in os.walk(root, onerror=lambda e: error('directory', e.filename)):
            if 'wire.jsonl' in names:
                path = Path(folder) / 'wire.jsonl'
                try:
                    stat = path.stat()
                    snapshot.append((path, stat.st_size, stat.st_mtime_ns))
                except OSError:
                    error('stat', path)
    report['files'] = len(snapshot)
    report['snapshot_bytes'] = sum(n for _, n, _ in snapshot)
    found = False
    for path, size, mtime in snapshot:
        agent = path.parent.name
        base = path.parent.parent.parent
        sid = base.name.removeprefix('session_')
        if path.parent.parent.name != 'agents' or not base.name.startswith('session_'):
            error('layout', path)
            continue
        if session and sid != session.removeprefix('session_'):
            continue
        found = True
        parent = None
        identity = 'unknown'
        try:
            state = json.loads((base/'state.json').read_text(encoding='utf-8'))
            info = state['agents'][agent]
            parent = info.get('parentAgentId')
            identity = 'spawned_subagent' if parent else ('main' if agent == 'main' else 'unknown')
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            error('agent_metadata', base/'state.json')
        consumed = matched = 0
        try:
            with path.open('rb') as stream:
                line = 0
                while consumed < size:
                    raw = stream.readline(size-consumed)
                    if not raw:
                        error('short_read', path, line+1)
                        break
                    consumed += len(raw)
                    report['bytes_read'] += len(raw)
                    line += 1
                    if not raw.strip():
                        continue
                    try:
                        row = json.loads(raw)
                        if not isinstance(row, dict):
                            raise ValueError()
                    except (ValueError, UnicodeError):
                        error('json', path, line)
                        continue
                    event = row.get('event')
                    text_blocks, role, unit = None, None, None
                    message = row.get('message')
                    if row.get('type') == 'context.append_message':
                        if not isinstance(message, dict):
                            error('content', path, line)
                            continue
                        if message.get('role') not in ('user', 'assistant'):
                            continue
                        role, unit = message['role'], 'message'
                        text_blocks = message.get('content')
                    elif row.get('type') == 'context.append_loop_event' and isinstance(event, dict):
                        if event.get('type') != 'content.part':
                            continue
                        block = event.get('part')
                        if isinstance(block, dict) and block.get('type') == 'think':
                            continue
                        role, unit, text_blocks = 'assistant', 'content_part', [block]
                    else:
                        continue
                    try:
                        ms = row['time']
                        if isinstance(ms, bool) or not isinstance(ms, (int, float)):
                            raise ValueError()
                        stamp = datetime.fromtimestamp(ms/1000, LOCAL)
                    except (KeyError, ValueError, TypeError, OverflowError, OSError):
                        error('time', path, line)
                        continue
                    if not start <= stamp < end:
                        continue
                    if unit == 'message' and role == 'assistant':
                        error('unverified_assistant_message', path, line)
                        continue
                    matched += 1
                    report['matched_records'] += 1
                    if identity == 'spawned_subagent' and not include_subagents:
                        report['deferred_subagent_records'] += 1
                        continue
                    if not isinstance(text_blocks, list):
                        error('content', path, line)
                        continue
                    texts, attachments = [], []
                    for block in text_blocks:
                        if not isinstance(block, dict):
                            error('content', path, line)
                        elif block.get('type') == 'text':
                            if isinstance(block.get('text'), str):
                                texts.append(block['text'])
                            else:
                                error('content', path, line)
                        elif block.get('type') != 'think':
                            attachments.append(block.get('type', 'unknown'))
                    if not texts and not attachments:
                        continue
                    emit(dict(kind='message', platform='kimi-code', unit=unit,
                              session_id=sid, agent_id=agent, parent_agent_id=parent,
                              session_kind=identity, file=str(path), line=line,
                              timestamp=stamp.isoformat(), role=role, text=''.join(texts),
                              event_id=event.get('uuid') if isinstance(event, dict) else None,
                              step_id=event.get('stepUuid') if isinstance(event, dict) else None,
                              turn_id=event.get('turnId') if isinstance(event, dict) else None,
                              non_text_types=attachments))
                    report['emitted_records'] += 1
        except OSError:
            error('read', path)
        if matched:
            report['matched_files'].append(dict(file=str(path), session_id=sid, agent_id=agent,
                                                session_kind=identity, records=matched))
        try:
            stat = path.stat()
            if (stat.st_size, stat.st_mtime_ns) != (size, mtime):
                report['changed_files'].append(str(path))
                if stat.st_size <= size:
                    error('changed_in_place_or_shrunk', path)
        except OSError:
            error('post_read_stat', path)
    if session and not found:
        error('session_not_found', root)
    report['coverage_complete'] = not report['errors']
    report['scope'] = ('Enumerated wire files bounded to initial sizes, selected session if requested; '
                       'append-only assumption. Visible records/fragments, NOT task or full-message counts. '
                       'No tool results, attachment bodies, other roots or post-snapshot additions.')
    report['read_finished_at'] = datetime.now(LOCAL).isoformat()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--date', required=True, help='YYYY-MM-DD in UTC+8')
    parser.add_argument('--session')
    parser.add_argument('--include-subagents', action='store_true')
    parser.add_argument('--summary-only', action='store_true')
    args = parser.parse_args()
    try:
        date.fromisoformat(args.date)
    except ValueError:
        parser.error('--date must be YYYY-MM-DD')
    sys.stdout.reconfigure(encoding='utf-8')
    def output(row):
        print(json.dumps(row, ensure_ascii=False))
    report = scan(args.root, args.date, lambda r: None if args.summary_only else output(r),
                  include_subagents=args.include_subagents, session=args.session)
    output(report)
    return 0 if report['coverage_complete'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
