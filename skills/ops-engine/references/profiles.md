# Profiles and provenance

## Select by evidence, not by product label

- Legacy Nuvolaris/OpenServerless 0.1.0 can use namespace `nuvolaris`, legacy
  `OPS_OLARIS` tasks and different service implementations. Use its own manifests
  and the CLI skill's legacy index. No all-version migration compatibility is
  implied by this engine skill.
- OPS 0.9.0 commonly uses namespace `openserverless`, versioned tasks and Whisk/
  WhiskUser operator resources. Builds and forks may differ materially.
- **ADV 1.0.0** in the inspected work is a private personal laboratory candidate,
  not an independently established Apache release or a production qualification.
  The original ADV installation and the later full Kafka KRaft laboratory are
  different targets. Windows Trustant/WSL is another independently versioned host.

The CLI's `ops -info` identifies the selected command/task profile, not the
cluster's complete image inventory. Source catalog values, CR fields, rendered
workloads and running digests may differ. Capture that difference explicitly.

## Source anchors used to author this skill

Inspected 2026-11-09. These are reference revisions, not required versions or
assertions of current deployment. Resolve the selected checkout independently.

| Source | Repository / reference revision |
|---|---|
| Operator composition, reconciliation, tenancy and service manifests | `miki3421/openserverless-operator`, `51bf939e1d0227b768428b4f5f96dea94f68fac1` |
| Matching task surface/catalog | `miki3421/openserverless-task-custom`, `98f6a66e5c86f352f3d15319099fa83dc0369e4e` |
| Runtime/proxy and native-library sources | `miki3421/openserverless-runtimes`, `7f7d672a869d8702787764725e3fa8fcc7e684c2` |
| Authenticated Streamer source | `miki3421/openserverless-streamer`, `7424070f20482154ffb1248a2546e46df70e9a6a` |
| Controller/Invoker build integration | `miki3421/openserverless-build`, `914b30b70fb77c150e5090a0f82e0c5092489219` |
| OpenWhisk source layout | Reviewed source revision `5b49c060ad42e02e170bc43edc14cb5d33aaaf3e`; match applied patches/build provenance before inferring a running binary |

No hostnames, SSH identities, kubeconfigs, API keys, user records or operational
payloads belong in this skill. Locate access through the user's current approved
context. The examples are architectural lessons, not permission to connect to a
remembered machine.

## Historical evidence worth preserving, not universal guarantees

The November 9 ADV laboratory had native backports and OpenSSH removal qualified
on selected AMD64 images. The exact inventory scan covered 32 unique running
images and retained 48 raw Critical occurrences. Static follow-up classified
1 confirmed, 13 needing review and 34 not actionable on the examined surfaces.
Those numbers are a dated checkpoint, not a fresh scan or a permanent allowlist.
They do not establish ARM64, HA, production readiness or full fresh-install
acceptance. PostgreSQL libxml2 remained a proposed fix at that checkpoint.

The authoritative retained comparison/triage collection for that work is keyed
by the original operator target and uses `artifacts/adv-comparison/` and
`artifacts/critical-triage-20261109/`. When continuing that same workspace, follow
its AGENTS.md artifact read/save and graphic-maintenance instructions. Do not
create a new source of truth by copying mutable reports into this skill.

Update these references when new source or qualification evidence changes the
decision criteria. Preserve dates on historical results and keep deployment
claims outside reusable instructions unless bound to an explicit snapshot.
