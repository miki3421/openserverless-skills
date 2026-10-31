# Indexed profiles

## Legacy 0.1.0

- Index: `catalog-0.1.0.json`.
- Task commit: `2de532bd1ad25766326faede6d00c364dafcc2f5`.
- Source is a clean checkout reconstructed from the legacy public task bundle.
- CLI observed in the rehearsal: `0.1.0-2409121919.dev`, installed in the user's
  `~/.local/bin/ops`; task root `~/.ops/0.1.0/olaris`.
- Legacy task revision is exposed as `OPS_OLARIS`; namespace is `nuvolaris`.
- No legacy Go source equivalence is asserted. Use the installed binary's help
  within authorized scope if an embedded flag cannot be established otherwise.

## Personal migration candidate based on 0.9.0

- Index: `catalog-0.9.0.json`.
- Tasks: `1e681b28fd54e4132be1a233f8e246fa98c2c8a2`, personal
  `miki3421/openserverless-task-custom`, branch `feature/migration-recovery-0.9.0`.
- Matching qualified operator candidate:
  `a8b3585422f26ea85a69348e40d7ff0ad4d41054`.
- CLI source reference: `b889360d27f1d8b39d9fb984e620502f0364ba19`.
  This identifies inspected code, not the installed CLI's binary provenance.
- Standard namespace: `openserverless`; task folder generally `oplugins`.
- These personal-fork capabilities are not claimed to exist in every Apache
  0.9.0 build. In particular migration/backup commands require the candidate.

For another official release, RC, ADV build or project plugin, build an index
from its actual selected root. Do not substitute one of these profiles by name.
The index lists all discovered static surfaces, not runtime compatibility tests.
