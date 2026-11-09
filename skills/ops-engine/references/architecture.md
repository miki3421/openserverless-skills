# Architecture and source map

Paths are relative to the matching component repository. Map them to the user's
selected checkout; an old local checkout does not establish running behavior.

## Planes and ownership

| Component | Responsibility | Focused source anchors |
|---|---|---|
| OPS tasks | Render configuration and orchestrate install/update/app workflows | Task repo `docopts.md`, `opsfile.yml`, `runtimes.json`; resolve active profile first |
| Operator | Reconcile Whisk/WhiskUser resources, components, identities, endpoints and tenant services | Operator `openserverless/main.py`, `operator_util.py`, `patcher.py`, `user_handlers.py`, `user_patcher.py`, `config.py`, `deploy/`, `openserverless/templates/` |
| OpenWhisk Controller | Authenticate invocation/control requests, resolve action metadata, enforce limits and dispatch | OpenWhisk `core/controller/.../Controller.scala`, `AuthenticatedRoute.scala`, `AuthorizedRouteDispatcher.scala`, load-balancer implementations |
| Invoker and runtime | Allocate execution containers, initialize/run actions, handle results and logs | OpenWhisk `core/invoker/.../InvokerReactive.scala`, `containerpool/`; runtimes `proxy.go`, `openwhisk/`, `runtime/<language>/` |
| Messaging | Controller/Invoker transport and broker coordination, according to mode | Operator `openwhisk.py`, `openwhisk_enterprise.py`, `openwhisk_standalone.py`, `kafka.py`, `kafka_profile.py`, `messaging_security.py`, `zookeeper.py` |
| Platform metadata/history | Subjects, action/package records and activation records in configured stores | Operator `couchdb*.py`, `userdb_util.py`, `files/*design_document*`; OpenWhisk `common/scala/.../database/ArtifactStore*` and selected provider |
| Streamer | Invoke an action and relay a separate producer TCP callback to an HTTP consumer | Streamer `src/handlers/stream.go`, `action_handler.go`, `web_action_handler.go`, `admission.go`, `src/tcp/tcpserver.go` |
| Scheduler | Discover due actions/annotations and invoke as the owning identity | Operator `cronjob.py`, `actionexecutor.py`, `deploy/scheduler/`, scheduler templates |
| Tenant services | Provision scoped SQL, Redis, Mongo, vector and object-store capabilities | Operator `postgres_operator.py`, `postgres_credentials.py`, `redis*.py`, `mongodb_native.py`, `ferretdb.py`, `milvus*.py`, `seaweedfs*.py` |
| Static/ingress/Admin API | Route public assets, platform administration and application HTTP paths | Operator `endpoint.py`, `ingress_data.py`, `route_data.py`, `storage_static.py`, `deploy/nginx-static/`; inspect the separate Admin API checkout for its handlers |

`components.invoker` selects standalone versus separate enterprise deployment
in the inspected operator. Check that branch before assuming a separate Kafka
or Invoker exists. A KRaft candidate and a ZooKeeper-era installation require
different broker/recovery reasoning. The OPS cron executor is distinct from
OpenWhisk's optional scheduler/container-pool-v2 implementation.

## Request paths

Ordinary invocation usually follows ingress/API authentication → Controller
metadata/limits → mode-specific dispatch → Invoker/container pool → runtime
initialization/execution → result/acknowledgment and configured history/log
storage. Verify the selected store providers and mode rather than assuming all
steps are separate processes or that CouchDB is the only possible provider.

An action identity is namespace/package/action, with a default-package form
where supported. Do not confuse a UI app name, an action's displayed name and
the fully qualified endpoint. Admission/dispatch success does not prove action
success; action success does not prove its downstream API returned useful data.

Streaming adds two distinct legs: client HTTP → Streamer → action invocation,
then action → producer TCP callback → Streamer → client HTTP body. A gateway or
desktop proxy adds another hop; test it separately from the callback leg.
For the inspected authenticated Streamer, `STREAM_HOST`, `STREAM_PORT` and a
per-invocation `STREAM_TOKEN` are injected. The producer sends the ASCII
`OPS-STREAM <token>\n` preamble before output. The server consumes the preamble;
the payload is byte-preserving, so NDJSON framing belongs to the producer and
incremental consumer. This contract must be matched to both server and action
versions; do not restore an unauthenticated fallback on a patched server.

The shared ActionLoop proxy is also a separate versioned artifact: compiler,
launcher, source/archive packaging and runtime libraries all matter. A successful
plain-language action does not qualify an old native addon or compiled archive.

## Storage distinctions

- Platform action/identity metadata and activation history are not application
  PostgreSQL/Mongo documents. Redis used by an app is not necessarily the store
  governing Controller/Invoker dispatch.
- Milvus metadata in etcd and its object storage must be considered together;
  copying one volume does not establish a coherent vector-data restore.
- SeaweedFS S3, Filer and Master are different interfaces with different trust
  boundaries. An object served publicly is not permission to list or mutate its
  private data bucket, nor to access Filer administration.
- PostgreSQL tenant database/schema/role, Redis key/channel prefix, Mongo
  user/database, Milvus database and S3 bucket identities are separate scopes.
  Read their actual generated contracts rather than deriving secrets or resource
  names by analogy.
- Kubernetes PVC names, UIDs, backing volumes and mount paths are persistence
  evidence. Workload Ready, source tags and a successful empty-database query
  do not establish that the original data survived.
