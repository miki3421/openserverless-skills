# Procedures and evidence

## Clean legacy 0.1.0 source on K3s

Evidence date: 2026-10-31. CLI/task pins are in `profiles.md`. Installation steps
below succeeded according to the user performing this clean rehearsal; these are
not independent live acceptance results or a claim about every environment.

1. Install the pinned CLI using the official versioned installer under the user's
   home. Verify its checksum and task checkout, then check `ops -info`.
2. `ops config slim`: selects the legacy slim controller with Redis, PostgreSQL,
   FerretDB, SeaweedFS, application etcd, Milvus, cron, static and registry.
3. `ops config apihost <guest-ip>.sslip.io --protocol=http`: isolated synthetic lab
   example. Select the actual intended host/protocol for another deployment.
4. Prepare sudo-capable SSH access from the CLI machine to the target. When
   running inside the target itself this still requires working SSH to itself.
   The pinned k3sup uses a default RSA key path. Verify host identity and SSH/sudo;
   do not copy prior cluster credentials or weaken host verification to proceed.
5. `ops cloud k3s create <guest-ip> ubuntu`: legacy task pins K3s
   `v1.27.7-rc1+k3s2`. Its `cloud/k3s/cert-manager.yaml` is already tracked in the
   pinned checkout. It is not a missing manual download prerequisite. A helper
   named `get-cert-manager` also exists; its presence does not establish a public
   command. Preserve the bundled file unless deliberately reviewing a change.
6. `ops cloud k3s status`: user observed node `Ready` with Kubernetes1.27.
7. `ops setup cluster`: installs the platform and performs the legacy login path.
   User reported the 0.1.0 cluster online. Next useful check: `ops setup status`.

Pending in this new rehearsal: independent workload readiness, Admin API and
Streamer presence, compatible Python/Node runtime catalog, Alpha/Beta deployment,
backend data, auth/isolation, streaming and cron checks, fresh backup and complete
migration acceptance. Do not infer those from cluster setup succeeding.

## Route other tasks through the matching index

| Intent | Namespace / source to inspect |
| --- | --- |
| Components, domains, runtime configuration | `ops config` |
| K3s / Kubernetes / platform installation | `ops cloud k3s`, `ops setup`, nested setup tasks |
| Tenant provisioning and lifecycle | `ops admin`, nested user/SSO tasks present in that version |
| App/project deployment and login | `ops ide`, then project/plugin definitions |
| Action operations | Binary wsk wrappers and embedded wsk, not a guessed task |
| Backends and credentials | `ops devel`, `ops admin`; never export secret config into chat |
| SSO configuration | `ops config sso` in matching 0.9.0 tasks; binary/login support is separate |
| Runtime deployment or updates | `ops config runtimes`, runtime setup, versioned `ops update` |
| Backup, inventory, restore and migration | Candidate `ops update` docs plus companion native adapters |
| Troubleshooting | Matching `status` and `ops debug` tasks and their implementation |

## Migration and update limits

`ops -update` is not a full platform migration. Candidate `ops update --check` and
`--plan` perform comparison; inspect each actual implementation before execution.
The legacy migration rehearsal uses separate versioned native recovery adapters.
A successful current-clone rehearsal does not establish a new clean run, an
all-version automatic updater, production cutover permission or safe uninstall.

Generic `ops-k3s-backup` ARM64 guest helpers are separate from the AMD64 migration
adapter. Their retained SQLite/standard-layout/empty-Milvus limits must not be
bypassed for a migration example. Follow the selected adapter's contract.
