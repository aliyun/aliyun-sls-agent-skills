# Logstore Operations

Manage logstores within an SLS project. A logstore is the unit for log collection, storage, query, and analytics.

## Naming requirements

- Unique within the same project
- Lowercase letters, numbers, hyphens (`-`), and underscores (`_`) only
- Must start and end with a lowercase letter or number
- Length: 2–63 characters

## Key parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--ttl` | Data retention in days | — (required) |
| `--shard-count` | Number of read/write shards | — (required) |
| `--auto-split` | Auto-split shards when write throughput exceeds limit | `false` |
| `--max-split-shard` | Max shard count after auto-split | `256` |
| `--mode` | `standard` (full analytics) or `query` (high-performance query, no SQL) | `standard` |
| `--hot-ttl` | Hot storage days (0 = all hot) | `0` |
| `--append-meta` | Append server-received time and client IP to log | `false` |
| `--enable-tracking` | Enable web tracking (anonymous writes) | `false` |

## Rules

1. **Overwrite update**: `update-log-store` does not merge — omitted parameters may reset to defaults. Always call `get-log-store` first, then pass **all** parameters back (only changing what you need).

## Examples

### List logstores

```bash
aliyun sls list-log-stores --project my-project
```

Pagination: `--offset` (default 0) and `--size` (default 200, max 500).

Optional filters (can be combined):

- `--logstore-name "name"` — fuzzy match on logstore name
- `--mode standard|query` — filter by mode
- `--telemetry-type None|Metrics` — `None` for logs only, `Metrics` for time-series only

```bash
aliyun sls list-log-stores --project my-project \
  --logstore-name "app-metrics" --mode standard --telemetry-type Metrics \
  --offset 0 --size 200
```

### Create logstore

```bash
aliyun sls create-log-store \
  --project my-project \
  --logstore-name my-logstore \
  --ttl 30 \
  --shard-count 2 \
  --auto-split true \
  --max-split-shard 256
```

With encryption:

```bash
aliyun sls create-log-store \
  --project my-project \
  --logstore-name encrypted-logs \
  --ttl 30 \
  --shard-count 2 \
  --encrypt-conf '{"enable":true,"encrypt_type":"default"}'
```

### Get logstore

```bash
aliyun sls get-log-store --project my-project --logstore my-logstore
```

### Update logstore (get-then-update)

Step 1 — get current config:

```bash
aliyun sls get-log-store --project my-project --logstore test
```

Example response:

```json
{
  "appendMeta": false,
  "autoSplit": true,
  "enable_tracking": true,
  "hot_ttl": 60,
  "infrequentAccessTTL": 0,
  "logstoreName": "test",
  "maxSplitShard": 256,
  "mode": "standard",
  "shardCount": 8,
  "ttl": 60
}
```

Step 2 — update with all parameters, only changing what you need (e.g. `appendMeta` → true):

```bash
aliyun sls update-log-store \
  --project my-project \
  --logstore test \
  --logstore-name test \
  --ttl 60 \
  --append-meta true \
  --auto-split true \
  --enable-tracking true \
  --hot-ttl 60 \
  --infrequent-access-ttl 0 \
  --max-split-shard 256 \
  --mode standard
```

### Delete logstore

```bash
aliyun sls delete-log-store --project my-project --logstore my-logstore
```
