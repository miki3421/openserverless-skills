# Engine changes, recovery and qualification

## Choose the owner of the change

Classify the defect as source logic, generated manifest, catalog/pin, rendered
configuration, running workload or persisted state. Repair its durable owner:
an ad hoc workload patch may be reverted on operator reconciliation. An image
build alone does not update the operator/task catalogs or an existing CR.

Inspect `main.py` create/update/resume and component reconciliation before
changing startup behavior. Missing versus explicit configuration values can
have migration semantics. Reconciliation should preserve identity/credentials,
be idempotent and expose real failures without logging secret-bearing payloads.

For dependency startup, prefer bounded checks of the required private API and
appropriate startup/readiness probes. Prove the ordering from timestamps. Waiting
only for a dependency's Pod Ready flag can retain the original race; changing
an authorization verifier to fail open does not fix an availability race.

An engine patch should identify source revision → build recipe → immutable image
identity → selected catalog/template → rendered workload → running digest.
Pin and check the relevant chain; registry tags and a preloaded image cache are
not proof that the Invoker chooses that image. Distinguish a compiler/source
version from the image manifest and its platform-specific config/CRI identity.

## Compatibility and acceptance

Select checks proportional to the affected contract:

| Change | Evidence that matters |
|---|---|
| Runtime/proxy/library | Init/run, source and old archive formats, representative prebuilt native ABI, compiler/launcher, config/env/limits, actual selected runtime |
| Controller/Invoker/broker | Invocation/result/ack, runtime selection, both tenants, relevant asynchronous and scheduled paths, recovery and failed-request record |
| Tenant provisioning | Owner create/read/write, peer-denied operations, scoped bindings, idempotency and persistence |
| Streamer | Actual payload delivery/framing, wrong-token rejection, cancellation/timeouts, upstream error propagation and relevant admission isolation |
| Operator/startup | New install and existing-resource reconcile where affected; dependency unavailability, repeat/resume and preservation of credentials/PVCs |
| Database/image | Application operations, extensions/ABI, authentication/isolation, preserved mount/data identity, restart and backup/restore contract |

A distribution/major-version upgrade can remove vulnerable packages while
breaking native ABI or stored-data compatibility. A narrow source backport can
be preferable when its provenance, license, ABI and regression evidence are
bound to the exact image. A developer library, data-only package and runtime
library can have different applicability despite sharing a source-package CVE.

Use synthetic scoped tenant fixtures where authorized. Existing business data
and production services are not implicit test targets. Keep failed controls and
qualification failures; do not change the target or disable a component just
to turn a failed rehearsal green.

Trustant's live app watcher owns generated wrappers/archives and action deploys
when its contract says so. Use its declared redeploy/status interface; do not
start a second watcher or apply engine-level procedures to bypass app ownership.

## Backup, migration and recovery

Classify the path before choosing commands: same-cluster update, fresh install,
same-host replacement, cross-host restore and destructive reinitialization are
different workflows. Consult the selected task implementation and its existing
checkpoint/manifest contract through the CLI skill; do not synthesize an
all-version upgrade recipe.

Record the consistency unit: metadata, credentials/signing keys, application
data, object/vector dependencies and target versions. Restore data and identity
together where required. Preserve original encrypted custody and independent
recovery sources; uncertainty is not authorization to delete plaintext or keys.

Rollback of an image is different from rollback of a data/schema migration.
Identify irreversible steps and the restore point before an authorized mutation.
After recovery, verify original data through the owning application/tenant,
cross-tenant denial, selected image identities and repeat/restart behavior.

Deletion/recreation of workloads, CRs, PVCs or namespaces may invoke finalizers,
owner-reference garbage collection and storage reclaim policies. Resolve those
effects before using deletion to recover a partial installation. Retention jobs
are intentional data deletion: in the inspected candidate, new-task defaults
and old CRs missing the field have different activation-retention behavior.
Read `activation_retention.py` and `activation_cleanup.py` before modifying it.

Finish with what was implemented versus deployed versus newly qualified, known
failed requests/jobs, persistent object identity, rollback evidence and remaining
gaps. Successful post-recovery checks do not establish HA or no downtime.
