#!/usr/bin/env python3
"""Index public OPS definitions without invoking OPS, shell tasks or Kubernetes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

SKIP={'.git','node_modules','.venv','private','backups'}


def revision(root):
    p=subprocess.run(['git','-C',str(root),'rev-parse','--show-toplevel'],capture_output=True,text=True)
    if p.returncode or Path(p.stdout.strip()).resolve()!=root:return None
    return subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()


def candidates(root):
    for directory, dirs, files in root.walk(follow_symlinks=False):
        dirs[:]=sorted(d for d in dirs if d not in SKIP and not (directory/d).is_symlink())
        for name in sorted(files):
            path=directory/name
            if name in {'docopts.md','docopts.txt','opsfile.yml','opsfile.yaml'} and not path.is_symlink():yield path


def usage(text):
    blocks=re.findall(r'```[^\n]*\n(.*?)```',text,re.S)
    selected=next((b for b in blocks if re.search(r'^\s*Usage:',b,re.M)),None)
    if selected is None:
        match=re.search(r'^\s*Usage:.*?(?=\n\s*\n|\Z)',text,re.S|re.M)
        selected=match.group(0) if match else ''
    return selected.strip()


def build(root, label, asserted_revision=None, cli=None):
    root=root.resolve(); detected=revision(root)
    if detected and asserted_revision and detected!=asserted_revision:raise ValueError('Task revision differs from requested pin')
    surfaces={}; fingerprints={}
    for path in candidates(root):
        relative=path.relative_to(root).as_posix(); raw=path.read_bytes();text=raw.decode('utf-8')
        fingerprints[relative]=hashlib.sha256(raw).hexdigest()
        namespace='ops'+(' '+path.parent.relative_to(root).as_posix().replace('/',' ') if path.parent!=root else '')
        entry=surfaces.setdefault(namespace,{'namespace':namespace,'definitions':[],'publicUsage':[],'taskHelpers':[]})
        entry['definitions'].append(relative)
        if path.name.startswith('docopts'):
            entry['publicUsage'].append({'file':relative,'usage':usage(text)})
        else:
            # Task names only: helper names are not assumed to be public CLI commands.
            match=re.search(r'^tasks:\s*\n(.*)',text,re.M|re.S)
            if match:
                entry['taskHelpers'].extend({'name':m.group(1),'line':text[:match.start(1)+m.start()].count('\n')+1,
                                            'file':relative} for m in re.finditer(r'^  ([A-Za-z0-9_.:-]+):\s*$',match.group(1),re.M))
    result={'schemaVersion':1,'label':label,'sourceRoot':str(root),'taskRevision':detected or asserted_revision,
            'workingTreeDirty':bool(subprocess.check_output(['git','-C',str(root),'status','--porcelain'],text=True)) if detected else None,
            'revisionEvidence':'git HEAD' if detected else 'operator-supplied snapshot label; hashes below are authoritative',
            'definitionSetSha256':hashlib.sha256(json.dumps(fingerprints,sort_keys=True).encode()).hexdigest(),
            'definitionHashes':fingerprints,'coverage':'static task namespaces, documented usage and task helper names; dynamic plugins require their own scan',
            'surfaces':sorted(surfaces.values(),key=lambda x:x['namespace'])}
    if cli:
        cli=cli.resolve(); main=(cli/'main.go').read_text(); tools=(cli/'tools/tools.go').read_text()
        group=re.search(r'var mainTools\s*=\s*\[\]string\s*\{(.*?)\}',main,re.S)
        embedded=re.search(r'var ToolList\s*=\s*\[\]Tool\s*\{(.*?)\n\}',tools,re.S)
        result['cliReference']={'sourceRoot':str(cli),'revision':revision(cli),'sameAsInstalledBinary':'not established by this index',
            'mainTools':re.findall(r'"([a-z0-9-]+)"',group.group(1)) if group else [],
            'embeddedTools':re.findall(r'\{\s*"([a-z0-9-]+)"',embedded.group(1)) if embedded else [],
            'flagAliases':sorted(set(re.findall(r'"(-[a-z][a-z-]*)"',main))),
            'implementationFiles':['main.go','tools/tools.go']}
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='action',required=True)
    create=sub.add_parser('build');create.add_argument('--root',type=Path,required=True);create.add_argument('--label',required=True)
    create.add_argument('--revision');create.add_argument('--source-repository');create.add_argument('--cli-repository');create.add_argument('--cli',type=Path);create.add_argument('--output',type=Path,required=True)
    lookup=sub.add_parser('find');lookup.add_argument('--catalog',type=Path,required=True);lookup.add_argument('query')
    args=p.parse_args()
    if args.action=='build':
        data=build(args.root,args.label,args.revision,args.cli)
        if args.source_repository:
            data['sourceRoot']=None;data['sourceRepository']=args.source_repository
        if args.cli_repository:
            if 'cliReference' not in data:p.error('--cli-repository requires --cli')
            data['cliReference']['sourceRoot']=None;data['cliReference']['sourceRepository']=args.cli_repository
        with args.output.open('x') as output:json.dump(data,output,indent=2);output.write('\n')
        print(json.dumps({'catalog':str(args.output),'namespaces':len(data['surfaces']),'revision':data['taskRevision']}))
    else:
        data=json.loads(args.catalog.read_text());query=args.query.lower()
        matches=[s for s in data['surfaces'] if query in s['namespace'].lower() or any(query in u['usage'].lower() for u in s['publicUsage'])]
        print(json.dumps({'label':data['label'],'revision':data['taskRevision'],'matches':matches},indent=2))


if __name__=='__main__':main()
