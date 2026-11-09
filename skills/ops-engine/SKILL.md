---
name: ops-engine
description: >-
  Explain, diagnose and maintain the OpenServerless/Nuvolaris OPS engine as a
  service: operator reconciliation, Controller/Invoker, action runtimes,
  streaming, scheduling, tenant services, persistence and recovery. Use for
  platform behavior and engine changes; CLI command selection belongs to
  ops-cli-usage and task definitions to ops-task-authoring.
---

# OPS engine

Work from the selected installation's actual topology and component identities.
OPS is a composition of independently versioned services, not one executable
whose CLI version identifies every server component. This skill supplies engine
knowledge; the user's request determines whether the work is explanation,
diagnosis, implementation, qualification or an authorized rollout.

## Establish the installation once

Reuse recent relevant evidence. Otherwise establish only the facts needed:

- Execution host, Kubernetes context/namespace and installation identity. A
  Windows launcher, WSL distribution, VM and cluster are distinct boundaries.
- Operator/task source revisions, rendered desired configuration, and actual
  running image digests. Record uncommitted changes affecting the path.
- Standalone versus separate Controller/Invoker mode, broker topology, enabled
  tenant services, action kinds, endpoint/TLS configuration and storage layout.
- Current tenant, action endpoint and failing operation when diagnosing a request.

Use [profiles and provenance](references/profiles.md) to distinguish legacy,
0.9.0 and private ADV evidence. Do not transfer a fix, setting, image identity or
qualification between installations because they share a version label.

## Follow the affected path

Read only the reference needed for the task:

| Task | Reference |
|---|---|
| Understand components, invocation, tenants, storage or source ownership | [Architecture and source map](references/architecture.md) |
| Diagnose startup, invocation, streaming, schedules, history or a desktop proxy | [Diagnosis](references/diagnostics.md) |
| Change engine code, images, catalogs, install/update or recover data | [Lifecycle and qualification](references/lifecycle.md) |
| Assess tenant boundaries, authentication, runtime packages or CVEs | [Security boundaries](references/security.md) |

Locate a command through `ops-cli-usage` when available; inspect matching task
definitions when it is not. Use `ops-task-authoring` for task implementation.
Do not guess CLI syntax from Python helper names or a different task checkout.

Find source through the map, then inspect the selected revision rather than
loading an entire workspace. Component filenames below are search anchors,
not a claim that every release has those implementations.

## Evidence that changes the conclusion

- A Pod becoming Ready does not prove its private API or reconciliation is ready.
- HTTP success, action completion, activation-history availability, delivered
  stream bytes and an external provider accepting a request are separate facts.
- A catalog pin is desired state; a running digest is observed state. A new
  build has its own identity even when the source version is unchanged.
- Recovery after a failed request is not uninterrupted availability. A scheduler
  heartbeat is not evidence of missed-job replay or exactly-once execution.
- A raw package/CVE match is not an established attacker-to-sink path. A source
  backport needs evidence bound to the scanned/deployed image.

When implementing, preserve the platform contracts touched by the change and
verify the actual affected path. Distinguish static inspection, prior retained
tests, newly executed checks and user-reported behavior. Finish with the result,
its installation/component identity, material limitations and remaining work.

## Operational boundaries

Use existing approved access and keep credentials out of output, arguments and
retained public artifacts. Diagnose through the operator, manifests and bounded
read-only observations before considering changes. Do not use a restart as a
substitute for a causal explanation.

Proceed with actions already authorized by the user; the skill adds no blanket
permission for deployments, data deletion, credential rotation, downloads or
external publication. Preserve unrelated edits, persistent-object identities
and failure evidence. Follow the target repository's instructions, including
managed app watcher ownership when working inside Trustant.

This is an engine reference, not a replacement security audit or an exhaustive
vulnerability assessment. Use the relevant dedicated security workflow when
the user requests one; ordinary engine diagnosis does not start a new scan.
