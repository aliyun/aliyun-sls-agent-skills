# Logstore Operations Examples

Complete examples for managing SLS Logstores using aliyun-cli.

## List Logstores

### List all logstores in a project

```bash
aliyun sls list-log-stores --project my-project
```

### List with pagination

```bash
aliyun sls list-log-stores \
  --project my-project \
  --offset 0 \
  --size 100
```

Default: `--size 200`, max: `500`

### Filter list results

Optional filters (can be combined). If a filter is omitted, it is not applied (all / no filter):

- **`--logstore-name "name"`** – Fuzzy match; returns logstores whose names contain the string (e.g. `"app-log"`).
- **`--mode`** – `standard` (full analytics only) or `query` (high-performance query only, no SQL analytics).
- **`--telemetry-type`** – `None` (log types only) or `Metrics` (time-series metrics only).

```bash
# List all logstores, including both log types and time-series metrics, both standard and query logstores
aliyun sls list-log-stores --project my-project --offset 0 --size 200

# By name (fuzzy), by mode, and by telemetry type
# e.g. standard metric stores whose name contains "app-metrics"
aliyun sls list-log-stores --project my-project --logstore-name "app-metrics" --mode standard --telemetry-type Metrics --offset 0 --size 200
```

## Create Logstore

### Basic creation

```bash
aliyun sls create-log-store \
  --project my-project \
  --logstore-name my-logstore \
  --ttl 30 \
  --shard-count 2
```

### Create with auto-split enabled

```bash
aliyun sls create-log-store \
  --project my-project \
  --logstore-name my-logstore \
  --ttl 30 \
  --shard-count 2 \
  --auto-split true \
  --max-split-shard 256
```

### Create with encryption

```bash
aliyun sls create-log-store \
  --project my-project \
  --logstore-name encrypted-logs \
  --ttl 30 \
  --shard-count 2 \
  --encrypt-conf '{"enable":true,"encrypt_type":"default"}'
```

## Update Logstore

**Important**: First run **get-log-store** to fetch the current config, then call **update-log-store** with all relevant parameters (including unchanged ones) so nothing is reset. Only change the parameter(s) you intend to update.

### Get-then-update example (e.g. set appendMeta to true)

**Step 1 – Get current config:**

```bash
aliyun sls get-log-store --project my-project --logstore test
```

Example response:

```json
{
  "appendMeta": false,
  "archiveSeconds": 0,
  "autoSplit": true,
  "createTime": 1763106279,
  "enable_tracking": true,
  "hot_ttl": 60,
  "infrequentAccessTTL": 0,
  "lastModifyTime": 1770804113,
  "logstoreName": "test",
  "maxSplitShard": 256,
  "mode": "standard",
  "shardCount": 8,
  "telemetryType": "",
  "ttl": 60
}
```

**Step 2 – Update with all parameters, only changing the one you need (e.g. `appendMeta` → true):**

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

If you omit other parameters, they may be reset to defaults. Always pass through values from the get result for any field you are not intentionally changing.

## Logstore Naming Requirements

- Unique within the same project
- Lowercase letters, numbers, hyphens (`-`), and underscores (`_`)
- Must start and end with lowercase letter or number
- Length: 2-63 characters

**Valid examples**:

- `app-logs`
- `server_log_2024`
- `nginx-access`

**Invalid examples**:

- `AppLogs` (uppercase not allowed)
- `log-` (cannot end with hyphen)
- `-log` (cannot start with hyphen)
- `a` (too short, minimum 2 characters)
