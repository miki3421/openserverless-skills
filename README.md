# OpenServerless skills

Codex skills for using the OPS CLI, maintaining its service engine and authoring
OpenServerless/Nuvolaris tasks.
This is a personal collection, not an official Apache release.

- [ops-cli-usage](skills/ops-cli-usage/SKILL.md): select commands using the active
  CLI, task revision and project plugins; follow versioned operational procedures.
- [ops-engine](skills/ops-engine/SKILL.md): explain and diagnose the service engine,
  trace invocation/streaming/scheduling paths, and maintain tenant-service,
  persistence, security and recovery contracts using version-bound evidence.
- [ops-task-authoring](skills/ops-task-authoring/SKILL.md): author thin task YAML
  and use companion Bun/TypeScript runners for substantial logic.

## Install

With Codex's bundled skill installer:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo miki3421/openserverless-skills \
  --path skills/ops-cli-usage skills/ops-engine skills/ops-task-authoring
```

The installer refuses existing skill directories. Review existing installations
before replacing them. Restart Codex to pick up newly installed skills. Invoke
`$ops-cli-usage`, `$ops-engine` or `$ops-task-authoring`; normal automatic discovery
is enabled.
The catalogue helper requires Python3.12+ and Git.

## Versioned references

The usage skill includes 41 static task namespaces for the pinned0.1.0 profile
and44 for the personal migration candidate based on0.9.0. Each catalogue records
repository, full commit, working-tree state and definition hashes. These are
command indices, not proof of runtime compatibility or a universal updater.
The0.9.0 CLI reference additionally indexes main/embedded tools and flag aliases;
its source checkout is not claimed to match every installed CLI binary.

Published indices omit machine-specific checkout paths. Map repository/commit
identifiers to the actual active checkout. Project plugins need their own scan.
The [profiles](skills/ops-cli-usage/references/profiles.md) and
[procedures](skills/ops-cli-usage/references/procedures.md) distinguish inspected
code, user-reported outcomes and pending acceptance checks.

The engine skill includes a focused component/source map and references for
diagnosis, lifecycle qualification, security boundaries and profile provenance.
Its ADV notes are explicitly dated private-laboratory evidence, not current
vendor status, deployment authority or production acceptance. Engine references
do not replace the CLI command catalogues or imply that every OPS installation
has the same topology, image versions or enabled services.

## Refresh and verify

```bash
python3 skills/ops-cli-usage/scripts/catalog.py build \
  --root /path/to/selected/tasks --label selected-profile --revision FULL_COMMIT \
  --source-repository https://github.com/OWNER/REPOSITORY \
  --output /path/to/new-catalog.json
python3 skills/ops-cli-usage/scripts/catalog.py find \
  --catalog skills/ops-cli-usage/references/catalog-0.1.0.json 'cloud k3s'
python3 -m unittest discover -s tests -v
```

Build uses a fresh output file and reads static definitions/Git metadata. It
never executes OPS, task commands or Kubernetes. Add `--cli /path/to/cli` and
`--cli-repository https://github.com/OWNER/CLI_REPOSITORY` for a portable CLI index.
Review an updated catalogue before replacing its predecessor. Do not commit
credentials, actual configurations, private keys, customer data or raw lab logs.

License: [Apache License2.0](LICENSE); source attribution: [NOTICE](NOTICE).
