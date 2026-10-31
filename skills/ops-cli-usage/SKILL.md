---
name: ops-cli-usage
description: Use and troubleshoot the OpenServerless/Nuvolaris ops CLI, select commands for the active CLI/task/plugin versions, and guide configuration, installation, users, actions, services, SSO, backup or update workflows. For implementing task definitions use ops-task-authoring instead.
---

# OPS CLI usage

Select the command from the user's active CLI and task profile. OPS is a binary,
embedded tools, versioned tasks and optional project plugins; its version alone
does not determine the available commands. This skill supplies routing and
versioned operational knowledge, not authority to change a cluster.

## Resolve the profile once

Use an existing recent `ops -info` result when available. Otherwise request or
run it within the authorized environment. Record `OPS_VERSION`, `OPS_BRANCH`,
`OPS_ROOT`, `OPS_REPO`, `OPS_TASKS` or legacy `OPS_OLARIS`, and `OPS_ROOT_PLUGIN`.
Distinguish the machine running OPS from the cluster it targets. Configuration,
SSH identity and kubeconfig belong to that selected profile.

Do not repeat repository-wide discovery on every turn. Keep the resolved profile
and successful steps in context. Re-resolve when the user changes environment,
branch, plugin, binary or task checkout.

## Locate the command cheaply

1. Read [profiles](references/profiles.md) to select the matching index.
2. Query the relevant namespace; do not load both complete JSON catalogues:
   `python3 scripts/catalog.py find --catalog references/catalog-0.1.0.json 'cloud k3s'`
   (resolve paths relative to this skill's directory).
3. `publicUsage` is the documented interface. `taskHelpers` are implementation
   names, not proof that docopts accepts them as user commands. For example a
   helper present in YAML may require a parent task rather than direct invocation.
4. Use the relevant [procedure](references/procedures.md) when its profile and
   prerequisites match. For new/ambiguous behavior inspect only the definition
   returned by the index and its referenced script, resolving files under the
   selected source root. Published indices use repository/commit identifiers; map
   those to the active checkout rather than assuming a path on another machine. Prefer `docopts.md` over `docopts.txt` when both exist,
   consistent with the inspected CLI.
5. For `ops -<tool>`, embedded tools or `ops action`-style wrappers, use the
   CLI reference in the index and [CLI ownership](references/cli-ownership.md).
   Do not infer installed-binary support from a different CLI source checkout.

`ops -config` and `ops config`, or `ops -update` and `ops update`, are separate
surfaces. Never replace one with the other based on name similarity.

## Operate within the requested mode

For user-led testing give one OPS command at a time, specify where to run it,
explain its expected result and wait for the output before dependent steps.
When the user delegates execution, perform authorized steps without repetitive
confirmation. Keep source/target, user and namespace explicit. Do not invent a
manual-testing restriction for unrelated future tasks.

Before a mutation check the actual task or matching verified procedure for
prerequisites and effects. A command called `status`, `help` or `--plan` is not
sufficient evidence by itself. Record unexpected failures, stop when the user
requested stopping, and do not silently change tasks, images or config to turn a
failed clean rehearsal into a success. Distinguish prerequisite preparation from
source-code fixes. Do not ask for or publish password/token dumps from config.

Treat observed success, user-reported success and static code inspection as
separate evidence. Cluster installation is not proof that applications, data,
authentication, isolation, restart persistence or migration work.

## Refresh only the relevant index

Use `scripts/catalog.py build --root <selected-task-checkout> --label <profile>
--revision <full-commit> --output <new-json>`; optionally provide `--cli <checkout>`. For portable publication add
`--source-repository <url>` and, with CLI sources, `--cli-repository <url>` to
omit machine-specific root paths.
The helper requires Python3.12+ and Git. This reads static definitions and Git metadata; it never runs OPS, task commands,
Kubernetes or installers. Supply a new output path, review it and replace the
matching catalogue deliberately. Git pins, working-tree status and definition hashes expose changes;
for a directory without Git the supplied revision is only an assertion.

Scan additional project/plugin roots separately. The bundled catalogues are
pinned references, not universal/current command inventories. They do not grant
production compatibility or certify a complete automatic legacy upgrade.
