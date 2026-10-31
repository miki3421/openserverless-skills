"""Static catalogue checks; no OPS, Kubernetes, VM or cloud operations."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/ops-cli-usage'
SCRIPT=SKILL/'scripts/catalog.py'
spec=importlib.util.spec_from_file_location('catalog',SCRIPT)
catalog=importlib.util.module_from_spec(spec);spec.loader.exec_module(catalog)


class CatalogueTests(unittest.TestCase):
    def test_static_index_does_not_execute_task_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);flag=root/'SHOULD_NOT_EXIST'
            (root/'opsfile.yml').write_text('tasks:\n  hidden:\n    cmds:\n      - touch '+str(flag)+'\n')
            (root/'docopts.md').write_text('```text\nUsage:\n  public show\n```\n')
            data=catalog.build(root,'synthetic')
            self.assertFalse(flag.exists())
            self.assertEqual(data['surfaces'][0]['taskHelpers'][0]['name'],'hidden')
            self.assertNotIn('hidden',data['surfaces'][0]['publicUsage'][0]['usage'])

    def test_external_symlink_directory_is_not_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'source';source.mkdir();outside=root/'outside';outside.mkdir()
            (outside/'docopts.md').write_text('Usage: secret')
            (source/'plugin').symlink_to(outside,target_is_directory=True)
            self.assertEqual(catalog.build(source,'synthetic')['surfaces'],[])

    def test_published_indices_are_portable_and_version_specific(self):
        old=json.loads((SKILL/'references/catalog-0.1.0.json').read_text())
        new=json.loads((SKILL/'references/catalog-0.9.0.json').read_text())
        for data in [old,new]:
            self.assertIsNone(data['sourceRoot']);self.assertTrue(data['sourceRepository'].startswith('https://github.com/'))
            self.assertFalse(data['workingTreeDirty']);self.assertEqual(len(data['taskRevision']),40)
        self.assertFalse(any(x['namespace']=='ops config sso' for x in old['surfaces']))
        self.assertTrue(any(x['namespace']=='ops config sso' for x in new['surfaces']))
        self.assertIsNone(new['cliReference']['sourceRoot'])

    def test_command_line_lookup_returns_documented_legacy_syntax(self):
        p=subprocess.run([sys.executable,str(SCRIPT),'find','--catalog',str(SKILL/'references/catalog-0.1.0.json'),'ops cloud k3s'],capture_output=True,text=True,check=True)
        rows=json.loads(p.stdout)['matches']
        self.assertEqual(len(rows),1)
        self.assertIn('k3s create <server> [<user>]',rows[0]['publicUsage'][0]['usage'])


if __name__=='__main__':unittest.main()
