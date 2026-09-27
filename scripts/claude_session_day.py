"""Read local Claude Code CLI/Desktop JSONL by UTC+8 message date, without writes."""
import argparse
from datetime import date, datetime, time, timedelta, timezone
import json
import os
from pathlib import Path
import sys

LOCAL = timezone(timedelta(hours=8))


def scan(root, day, emit, client='all', session=None, include_subagents=False):
    root = Path(root)
    start = datetime.combine(date.fromisoformat(day), time(), LOCAL)
    end = start + timedelta(days=1)
    report = dict(kind='summary', platform='claude-code', root=str(root), client=client,
                  session_filter=session, start=start.isoformat(), end_exclusive=end.isoformat(),
                  read_started_at=datetime.now(LOCAL).isoformat(), files=0, snapshot_bytes=0,
                  bytes_read=0, matched_records=0, emitted_records=0, unknown_client_records=0,
                  deferred_subagent_records=0, matched_files=[], changed_files=[], errors=[])

    def error(kind, path, line=None):
        report['errors'].append(dict(kind=kind, file=str(path), line=line))

    snapshot = []
    if not root.is_dir():
        error('root', root)
    else:
        for folder, _, names in os.walk(root, onerror=lambda e: error('directory', e.filename)):
            for name in sorted(names):
                if not name.endswith('.jsonl'):
                    continue
                path = Path(folder)/name
                try:
                    stat = path.stat()
                    snapshot.append((path, stat.st_size, stat.st_mtime_ns))
                except OSError:
                    error('stat', path)
    report['files'] = len(snapshot)
    report['snapshot_bytes'] = sum(n for _, n, _ in snapshot)
    found = False
    for path, size, mtime in snapshot:
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
                    sid = row.get('sessionId')
                    if session and sid == session:
                        found = True
                    if row.get('type') not in ('user', 'assistant'):
                        continue
                    if session and sid != session:
                        continue
                    try:
                        stamp = datetime.fromisoformat(row['timestamp'].replace('Z','+00:00'))
                        if stamp.utcoffset() is None:
                            raise ValueError()
                    except (KeyError, AttributeError, TypeError, ValueError):
                        error('time', path, line)
                        continue
                    if not start <= stamp < end:
                        continue
                    entry = row.get('entrypoint')
                    source = {'cli':'cli', 'claude-desktop-3p':'desktop'}.get(entry, 'unknown')
                    if source == 'unknown':
                        report['unknown_client_records'] += 1
                    if client != 'all' and client != source:
                        continue
                    report['matched_records'] += 1
                    matched += 1
                    sub = row.get('isSidechain') is True
                    if sub and not include_subagents:
                        report['deferred_subagent_records'] += 1
                        continue
                    msg = row.get('message')
                    if not isinstance(msg, dict) or 'content' not in msg:
                        error('content', path, line)
                        continue
                    content = msg['content']
                    if isinstance(content, str):
                        content = [{'type':'text', 'text':content}]
                    if not isinstance(content, list):
                        error('content', path, line)
                        continue
                    texts, attachments = [], []
                    for block in content:
                        if not isinstance(block, dict):
                            error('content', path, line)
                        elif block.get('type') == 'text':
                            if isinstance(block.get('text'), str):
                                texts.append(block['text'])
                            else:
                                error('content', path, line)
                        elif block.get('type') not in ('thinking', 'redacted_thinking', 'tool_use', 'tool_result'):
                            attachments.append(block.get('type', 'unknown'))
                    if not texts and not attachments:
                        continue
                    emit(dict(kind='message', platform='claude-code', client=source, entrypoint=entry,
                              file=str(path), line=line, session_id=sid, uuid=row.get('uuid'),
                              api_message_id=msg.get('id'), parent_uuid=row.get('parentUuid'),
                              agent_id=row.get('agentId'), is_subagent=sub,
                              timestamp=stamp.astimezone(LOCAL).isoformat(), role=row['type'],
                              text='\n'.join(texts), non_text_types=attachments))
                    report['emitted_records'] += 1
        except OSError:
            error('read', path)
        if matched:
            report['matched_files'].append(dict(file=str(path), records=matched))
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
    report['scope'] = ('Enumerated project JSONL, initial byte ranges, requested client/session; '
                       'unknown_client_records are excluded from specific client filters. '
                       'Append-only assumption; visible text only, not tools, reasoning, or attachment bodies. '
                       'No guarantee for other roots, Desktop Chat/Cowork or new records.')
    report['read_finished_at'] = datetime.now(LOCAL).isoformat()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--date', required=True, help='YYYY-MM-DD, UTC+8')
    parser.add_argument('--client', choices=['all','cli','desktop'], default='all')
    parser.add_argument('--session', help='Code sessionId; Desktop UI ID must first map to cliSessionId')
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
    report = scan(args.root,args.date,lambda r: None if args.summary_only else output(r),
                  client=args.client,session=args.session,include_subagents=args.include_subagents)
    output(report)
    return 0 if report['coverage_complete'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
