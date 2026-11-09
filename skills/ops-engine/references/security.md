# Engine security boundaries

For ordinary diagnosis, use this map to ask the right question. A requested
security audit, supplied-finding triage or vulnerability fix has its own
dedicated workflow; do not silently replace one with the other.

## Identity and enforcement

| Boundary | What to establish |
|---|---|
| Browser/SSO → Admin API | Identity validation and exact mapped tenant; redirects/UI login are not proof of Controller or service authorization |
| API request → action | Private OpenWhisk auth versus public/custom-auth web action, namespace selection, finalized parameters and reserved metadata |
| Action → shared platform | Tenant executes code intentionally, but gains no implicit authority over operator administration, peer data, host or cluster API |
| Action → tenant service | Actual generated credential and scope; an admin client or MCP connection is not the action's runtime binding |
| Action → Streamer callback | Per-invocation capability, fixed destination contract, preamble verification and stream ownership; caller headers do not establish callback ownership |
| Tenant → credentials/state | Password/key verification, Secret handling, private versus public payloads and fail-closed reconciliation |

Redis isolation covers key patterns **and channels**, command/subcommand grants,
selectors and supported script behavior. Inspect `redis_acl.py` and the deployed
ACL: do not assume a blanket Lua ban or that a permitted `EVAL` grants cross-key
access. SQL databases/schemas/roles, Mongo roles, Milvus databases and S3 buckets
have different isolation mechanisms and require their own peer-denial checks.

SeaweedFS public web-object policy must not grant private data access, broad
listing or administrative Filer/Master access. NetworkPolicy is an additional
control only when the selected CNI enforces it; credential checks remain relevant.
Use `datastore_security.py`, `seaweedfs_ingress.py`, `s3_bucket_policy.py` and
actual rendered policy rather than labels such as "internal" or "private".

When introducing a signing or service key, distinguish first creation, retained
identity and deliberate rotation. A missing key on an existing installation
must not silently become a new identity that strands data or invalidates access.

## CVE applicability in composed images

Start from exact image digest, package/binary path, installed revision, scanner
and database identity. Preserve one record per advisory/package/image occurrence;
aggregate presentation must not silently lose repeated package rows.

For each occurrence establish vulnerable implementation → actual caller →
attacker-controlled input → configuration/privilege preconditions → boundary and
consequence. Useful counterevidence includes a qualified source patch, an absent
binary component, architecture-specific conditions or a configured parser that
is never enabled. Missing evidence is a review gap, not proof of safety.

Examples that prevent recurring mistakes:

- Debian zlib source matching can name MiniZip code not shipped in that binary.
- `linux-libc-dev` headers do not establish an executing host-kernel vulnerability.
- A Go advisory in a database image may belong to the `gosu` startup utility,
  rather than its database listener. Identify the exact Go binary and caller.
- PostgreSQL SQL is not SQLite SQL, but PostgreSQL SQL/XML can reach native
  libxml2. Trace the implementation rather than the package's apparent role.
- Presence of native Brotli does not prove an input reaches that decoder; a
  pure-Go decoder is a different implementation.
- TLS-resumption, HTTP/3/backend-auth and 32-bit-only flaws require those exact
  preconditions. A severe generic score does not establish them on ADV.
- A custom `+0ops` package may be corrected while version-based scans keep the
  raw match. Bind source patches/receipts and prior regression evidence to the
  actual image; a suffix or a test on another image is not sufficient.

Keep raw counts, applicability verdicts and demonstrated exploitation separate.
Do not claim zero risk from zero Critical results, or RCE from an established
DoS path. Do not reuse the dated ADV triage as current vendor status: verify
relevant primary advisories and current target evidence for a new assessment.
