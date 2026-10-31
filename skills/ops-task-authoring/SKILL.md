---
name: ops-task-authoring
description: Use this skill when creating or refactoring OpenServerless/Nuvolaris `ops` tasks, Taskfile-style `opsfile.yml` files, `docopts.md` command surfaces, or companion Bun/TypeScript task runners. Prefer it when complex task logic should move out of YAML into `.ts` scripts executed by the Bun binary bundled with `ops`.
---

# Ops Task Authoring

## Core Pattern

Use the `olaris/debug` plugin as the reference style:

- keep `opsfile.yml` small and declarative;
- put command discovery and help text in `docopts.md`;
- use `tasks.<name>.desc` for human-facing summaries;
- use `silent: true` for normal machine-like output and let `ops debug verbose`
  toggle it while debugging;
- move non-trivial branching, parsing, file edits, Kubernetes object mapping,
  retries, and cleanup into a colocated `.ts` script;
- run TypeScript with `bun script.ts ...`; Bun is included in the `ops`
  runtime under `~/.ops/<os>-<arch>/bin/bun`.

Avoid growing an `opsfile.yml` into a large shell program embedded in YAML.

## Opsfile Shapes

Minimal command:

```yaml
version: "3"

tasks:
  status:
    desc: show status
    silent: true
    cmds:
      - kubectl -n nuvolaris get po
```

Subcommand prefix:

```yaml
tasks:
  kube:
    desc: kubernetes support subcommand prefix
```

Delegating complex work to Bun:

```yaml
tasks:
  restore:
    desc: restore system backup
    silent: true
    cmds:
      - bun restore.ts {{.__dry_run}} {{._backup_}}
```

Task dependency with computed vars:

```yaml
tasks:
  sub:
    cmds:
      - task: main
        vars:
          OBJECT:
            sh: echo "pod/$(cat _pod)"
```

## Argument Conventions

Common `ops` template variables:

- `{{._name_}}`: positional argument named by docopts.
- `{{.__flag}}`: boolean flag from docopts.
- `{{._cmds_}}`: array-like capture for trailing command parts.
- `{{.VAR}}`: task variable from `vars:`.
- `{{OS}}`, `{{ARCH}}`: platform values exposed by ops/task.

For pass-through arrays, follow `debug verbose`:

```yaml
cmds:
  - CMDS={{._cmds_}} ; bun verbose.ts {{.__no}} {{.__reset}} ${CMDS[@]}
```

Use shell only for thin argument plumbing. Put validation and real behavior in
the Bun script when it grows beyond a few lines.

## Environment

Use `env:` for values that tasks and scripts need consistently:

```yaml
env:
  KUBECONFIG:
    sh: |-
      if test -e "$OPS_TMP/kubeconfig"
      then echo "$OPS_TMP/kubeconfig"
      else echo ~/.kube/config
      fi
```

Useful runtime variables:

- `$OPS_ROOT`: main `olaris` plugin root.
- `$OPS_ROOT_PLUGIN`: parent of `olaris-*` plugin directories.
- `$OPS_PWD`: caller working directory.
- `$OPS_TMP`: temp/runtime directory used by ops.
- `$OPS`: current ops executable.

## Devcontainer Commands

For OpenServerless/Nuvolaris task workflows that must run inside the project
devcontainer, prefer the OPS-provided wrapper over hand-written Docker
commands in `Taskfile.yml` or `opsfile.yml`.

Run commands from the directory that contains the `.devcontainer` folder:

```yaml
cmds:
  - printf '%s\n' 'task build-all:local' | ops ide devcontainer
```

This lets OPS resolve the devcontainer, workspace path, mounted Docker socket,
user, and environment consistently across machines. Avoid duplicating that
behavior with custom `docker build` / `docker run` wrappers in task files. Keep
Docker commands in task files only when Docker itself is the actual build
operation, such as `docker build` for an application image or `docker buildx`
for a multi-arch image.

## Bun Script Rules

Prefer dependency-free TypeScript:

```ts
import { $ } from "bun";

function die(message: string): never {
  console.error(`ERROR: ${message}`);
  process.exit(1);
}
```

Use Bun shell for external commands, `quiet()` for captured output, and
`nothrow()` when non-zero exits are part of control flow. Use Node standard
modules (`fs`, `path`) for file traversal and structured operations.

When a script edits files:

- resolve the target file explicitly;
- validate inputs before mutation;
- preserve subrepo boundaries by using `git -C <targetDir> rev-parse
  --show-toplevel`;
- prefer structured tools (`yq`, JSON parsers, Kubernetes JSON output) over
  fragile string edits.

## Documentation And Validation

When adding a command:

1. Add or update `docopts.md` usage and command descriptions.
2. Keep the `opsfile.yml` command path stable.
3. If the task uses a script, check it with the bundled Bun:
   `~/.ops/$(uname -s | tr A-Z a-z)-$(uname -m)/bin/bun script.ts --help`
   when the script supports help, or run a harmless dry-run/status path.
4. Parse YAML with an available local parser.
5. Run the narrow `ops <plugin> <command>` smoke test when safe.

Do not modify existing `olaris` task files just to learn their structure.
