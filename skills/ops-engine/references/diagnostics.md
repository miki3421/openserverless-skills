# Engine diagnosis

Choose the smallest path that explains the reported symptom. Gather exact
timestamps/timezones, component identities and the first relevant failure.
Bound log/time ranges and redact credentials, headers and application payloads.
An inventory of every log is rarely necessary.

## Establish the failing boundary

For a known target, useful read-only observations include Kubernetes context,
workload status, selected container imageIDs, events, service endpoints, ingress
routes and the affected controller/operator logs. Project JSON instead of dumping
all manifests: CRs, annotations, environment and command arguments can contain
secrets. Do not retrieve a kubeconfig if diagnosis can run through the approved
remote host's existing access. Unknown SSH host keys require verification.

| Symptom | Next discriminating evidence |
|---|---|
| Operator resume/create failed but pods look healthy | The exact failing handler/API, dependency listener timeline and subsequent retry; inspect readiness probes and error handling |
| Invocation unauthorized/not found | Origin, namespace/package/action, caller identity class and actual HTTP status; distinguish ingress, Controller, web action and downstream-provider denial |
| Request accepted but no result | Controller dispatch/ack, broker health, Invoker allocation/init/run, runtime failure and limits; correlate the same action/time/activation |
| Missing action logs/history | Actual configured activation store, logging/retention policy and full action identity; inspect bounded existing container logs if retained |
| Blank stream with HTTP 200 | Callback acceptance and payload bytes, action exception handling, upstream result; a caught exception may return an empty successful result |
| No callback / timeout | Producer-reachable callback host/port, server/action handshake compatibility, preamble deadline and first-byte timing |
| Scheduled action missing | CronJob/Job result, schedule window, owner credential lookup, dispatch status and action side-effect heartbeat |
| Services ready but tenant app fails | The app's actual generated binding, scope and first service operation; direct operator/admin access is a different principal |
| Works on Linux but not Windows | Browser-facing origin, launcher listener/proxy, Host routing, WSL address/mode and then the in-cluster path |

## Streaming and HTTP layers

Trace the actual browser request, including iframe/dev-server origin; the page
in the address bar may not be the host sending `/stream/web/...`. A GET health
response from Streamer proves only its HTTP listener, not an invocation or stream.

Distinguish a caller HTTP cancellation, an action closing its producer TCP
connection and a reverse proxy canceling its upstream. A log string such as
`Client closed connection` is not sufficient to identify which peer it means;
read the owning handler. Never conclude a token/preamble failure solely from
an empty response.

For the inspected ADV Streamer, search the source for `streamStartTimeout`,
`handshakeTimeout`, `callbackIdleTimeout` and `maxStreamLifetime`. Historical
values were 20 s callback start, 1 s preamble, 30 s inactivity and 5 min total.
Treat these as version-bound observations, not settings to apply universally.
Per-process/per-namespace admission is not a cluster-wide tenant quota.

When a downstream AI/provider call fails, compare the configured action values
with the user-designated configuration source without printing the values.
Use the relevant API operation to test authorization when authorized: `/models`
returning 200 does not prove `/chat/completions` accepts the same key. A minimal
inference can consume quota and create an activation; it is a distinct operation
from reading logs. Report request origin and result, not just connectivity.

## Scheduling and history

Correlate scheduler jobs with dispatch records and a controlled tenant-owned
side effect. The executor queries subjects/actions and invokes under the owning
identity; an administrator's manual invocation does not exercise that lookup.
Check bounds, pagination, owner resolution and interval selection in the actual
`actionexecutor.py`. Do not infer catch-up semantics, exact-once execution or
replay of an interrupted Job from a later successful heartbeat.

Activation history can be unavailable while action execution works. Conversely,
a successful activation can contain a caught application error or an empty
payload. Use an existing activation result/log and correlate it with output.
If history is absent, say what direct evidence remains available; do not create
or reset a database merely to obtain logs.

## WSL/desktop topology

Identify the launcher actually owning the listener, its source/build identity,
the already-running distribution and its networking mode. Do not assume the
Windows process name contains `launcher` or that `netsh portproxy` is involved;
the executable may implement its own reverse proxy. Preserve Host routing when
comparing Windows loopback, WSL and service responses. Check current backend IP,
localhost forwarding and effective listener state before firewall speculation.

Compare equivalent requests from equivalent layers before attributing a failure
to the OS. Do not launch a stopped WSL distribution, restart the launcher or
change networking as part of an implicitly read-only check.
