# Log Query

Use the dedicated `alibabacloud-sls-query` skill for SLS log query and analysis workflows. This file is only a quick API reference for `get-logs-v2` and `get-histograms`.

Delegate to `alibabacloud-sls-query` when the user asks to query logs, analyze logs, generate SQL/SPL, optimize a query, execute a query, or troubleshoot query results. If the skill is not installed, install it first:

```bash
# Global Codex install
npx skills add aliyun/alibabacloud-aiops-skills \
  --skill alibabacloud-sls-query \
  --agent codex \
  -g -y --full-depth
```

```bash
# Project-level Codex install
npx skills add aliyun/alibabacloud-aiops-skills \
  --skill alibabacloud-sls-query \
  --agent codex \
  -y --full-depth
```

After installation, actively locate and read the installed `alibabacloud-sls-query/SKILL.md` completely, then follow that skill's workflow.

`get-logs-v2` supports two modes: **query (search)** and **SQL analytics**.

## Key parameters

| Parameter | Description |
|-----------|-------------|
| `--project` | Project name (required) |
| `--logstore` | Logstore name (required) |
| `--from` | Start time, Unix timestamp in seconds, inclusive (required) |
| `--to` | End time, Unix timestamp in seconds, exclusive (required) |
| `--accept-encoding` | Must be `lz4` (required) |
| `--query` | Query expression; omit or `"*"` for all logs |
| `--line` | Max rows per request (query mode page size) |
| `--offset` | Start row for pagination (query mode, default 0) |
| `--reverse` | `true` = newest first, `false` = oldest first (query mode only) |

## Rules

1. Time range is **left-closed right-open** `[from, to)`.
2. The logstore must have an index configured before querying (see [index.md](index.md)).
3. **Result completeness**: check `meta.progress` in the response — `Complete` means precise; otherwise retry for accurate results.
4. **Pagination**: only paginate when the result set is large (many rows or large log entries). For small result sets, fetch all at once to avoid unnecessary round-trips.

## Query mode vs SQL mode

| | Query mode | SQL mode |
|--|------------|----------|
| **When to use** | Search and filter logs | Aggregation, complex filtering, or sorting with SQL |
| **Syntax** | `--query '<query_syntax>'` | `--query '<query_syntax> \| <SQL>'` |
| **Pagination** | `--offset` + `--line` | `LIMIT offset, count` in SQL (default `LIMIT 100`) |
| **Total count** | Use `get-histograms` | `select count(*) as total from log` |
| **Sort** | `--reverse true/false` | `ORDER BY <column> ASC/DESC` (--reverse is ignored) |

## Query syntax

```text
* and "someWord" and key1: "value1" and (key2: "value2" or key3: "value3") not key4: "value4"
```

- `*` — match all
- `"someWord"` — full-text search (requires full-text index)
- `key: "value"` — field filter, contains match (requires field index)
- `and` / `or` / `not` — logic operators; use parentheses for grouping

## SQL syntax

Format: `<query_syntax> | SELECT ... FROM log WHERE ... ORDER BY ... LIMIT ...`

- Left of `|`: query syntax (e.g. `*` or `status: "500"`) to pre-filter logs.
- Right of `|`: standard SQL; table is always `log` (can be omitted when no join log).
- `LIMIT offset, count` for pagination; `LIMIT all` to return everything (use only for small result sets).

For complex SQL, natural-language query generation, SPL, scan mode, or query failures, delegate to `alibabacloud-sls-query` and follow its `SKILL.md`.

## Examples

### Query mode: search all logs

```bash
aliyun sls get-logs-v2 --project my-project --logstore my-logstore \
  --accept-encoding lz4 --from 1740000000 --to 1740003600 --line 100
```

### Query mode: filter by field and keyword

```bash
aliyun sls get-logs-v2 --project my-project --logstore my-logstore \
  --accept-encoding lz4 --from 1740000000 --to 1740003600 --line 100 \
  --query '* and "flowers" and season: "winter"'
```

### Query mode: pagination (page 2)

```bash
aliyun sls get-logs-v2 --project my-project --logstore my-logstore \
  --accept-encoding lz4 --from 1740000000 --to 1740003600 \
  --query 'error' --offset 50 --line 50
```

### Query mode: get total count for pagination

```bash
aliyun sls get-histograms --project my-project --logstore my-logstore \
  --from 1740000000 --to 1740003600 --query 'error'
```

### SQL mode: count

```bash
aliyun sls get-logs-v2 --project my-project --logstore my-logstore \
  --accept-encoding lz4 --from 1740000000 --to 1740003600 \
  --query '* | select count(*) as total from log'
```

### SQL mode: filter + sort + pagination

```bash
# Page 1: first 100 rows, newest first
aliyun sls get-logs-v2 --project my-project --logstore my-logstore \
  --accept-encoding lz4 --from 1740000000 --to 1740003600 \
  --query '* | select * from log where status = 500 order by __time__ desc limit 0, 100'

# Page 2
aliyun sls get-logs-v2 --project my-project --logstore my-logstore \
  --accept-encoding lz4 --from 1740000000 --to 1740003600 \
  --query '* | select * from log order by __time__ desc limit 100, 100'
```

### SQL mode: aggregation

```bash
aliyun sls get-logs-v2 --project my-project --logstore my-logstore \
  --accept-encoding lz4 --from 1740000000 --to 1740003600 \
  --query 'status: "500" | select request_uri, count(*) as cnt from log group by request_uri order by cnt desc limit 20'
```
