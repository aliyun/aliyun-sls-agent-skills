# Log Query Operations (get-logs-v2)

Use **get-logs-v2** to query logs. Two modes: **query (search)** and **SQL analytics**. Both require `--project`, `--logstore`, `--from`, `--to` (Unix timestamp, left-closed right-open `[from, to)`), and **get-logs-v2** requires `--accept-encoding lz4`.

---

## 1. Query (search) mode

**Use when**: Return logs that match the specified filter conditions.

### Query syntax

```
* and "someWord" and key1: "value1" and (key2: "value2" or key3: "value3") not key4: "value4"
```

- `*`: match all.
- `someWord`: Use full-text index to filter logs that contain this text.
- `key: "value"`: Use field index to filter logs where field key contains value (contains relationship; use quotes for value).
- `and` / `or` / `not`: logic operators; use parentheses for grouping.

**Example**:

Search all logs.

```bash
aliyun sls get-logs-v2 --project my-project --logstore my-logstore \
  --accept-encoding lz4 --from 1740000000 --to 1740003600 --line 100
```

Filters logs where the field `season` contains `winter` and the log content contains `flowers`.

```bash
aliyun sls get-logs-v2 --project my-project --logstore my-logstore \
  --accept-encoding lz4 --from 1740000000 --to 1740003600 --line 100 --query '* and "flowers" and season: "winter"'
```

### Pagination

- **--offset**: start row (default 0).
- **--line**: max lines per request (required for query). Acts as page size.

**Example**:

```bash
aliyun sls get-logs-v2 --project my-project --logstore my-logstore \
  --accept-encoding lz4 --from 1740000000 --to 1740003600 \
  --query 'error' --offset 50 --line 50
```

#### Total count

If the number of logs returned is less than the requested `--line` (size), you can use **get-histograms** to get the total count for pagination.

Call **get-histograms** with the same `--project`, `--logstore`, `--from`, `--to`, and `--query`. The result gives log distribution/count in the time range (sum the counts for total if needed).

**Example**:

```bash
aliyun sls get-histograms --project my-project --logstore my-logstore \
  --from 1740000000 --to 1740003600 --query 'error'
```

### Sort order (query mode only)

- **--reverse false** (default): ascending by log time.
- **--reverse true**: descending by log time.

---

## 2. SQL analytics mode

**Use when**: You need aggregation, filtering, or sorting with SQL. Format: **query part | SQL part**. Table is fixed as `log` (`FROM log`).

### Syntax

```

<query_syntax> | select ... from log where ... order by ... limit ...

```

- Left of `|`: query syntax (e.g. `*` or `status: "500"`).
- Right of `|`: SQL; **from log** is fixed. Add `where`, `order by`, `limit` as needed.

### Pagination

- Use **LIMIT offset, count** in SQL (e.g. `limit 0, 100`). If **LIMIT** is omitted, default is **limit 100**.
- Use **LIMIT all** to return all matching logs; only recommended when the result set is small.

### Total count

Run a separate query with **select count(\*)** in the SQL part (same query left of `|`), e.g.  
`* | select count(*) as total from log`.

### Sort

Use **order by** in SQL: `order by <column> asc` or `order by <column> desc`.  
In SQL mode, **--reverse** is ignored; order is controlled only by SQL.

### Examples

```bash
# Simple SQL: count (no limit; returns one row)
aliyun sls get-logs-v2 --project my-project --logstore my-logstore \
  --accept-encoding lz4 --from 1740000000 --to 1740003600 \
  --query '* | select count(*) as total from log'

# Filter + sort + pagination: first 100 rows, newest first
aliyun sls get-logs-v2 --project my-project --logstore my-logstore \
  --accept-encoding lz4 --from 1740000000 --to 1740003600 \
  --query '* | select * from log where status = 500 order by __time__ desc limit 0, 100'

# Next page: offset 100, size 100
aliyun sls get-logs-v2 --project my-project --logstore my-logstore \
  --accept-encoding lz4 --from 1740000000 --to 1740003600 \
  --query '* | select * from log order by __time__ desc limit 100, 100'

# Aggregation: group by and count
aliyun sls get-logs-v2 --project my-project --logstore my-logstore \
  --accept-encoding lz4 --from 1740000000 --to 1740003600 \
  --query 'status: "500" | select request_uri, count(*) as cnt from log group by request_uri order by cnt desc limit 20'
```

---

## Result structure

The response has two main parts:

- **data**: Array of log entries (the logs returned).
- **meta**: Metadata.
  - **meta.progress** indicates whether the result is precise: **Complete** = precise; otherwise the result may be incomplete (e.g. when the query or analysis scans a very large amount of data). Retry if you need precise results.
  - **meta.isAccurate** does **not** mean whether the query result is precise. It indicates second-level accuracy of timestamp ordering only, and is unrelated to result precision.

---

## Quick reference

| Need              | Query mode              | SQL mode                          |
|-------------------|-------------------------|-----------------------------------|
| Pagination        | `--offset`, `--line`    | `limit offset, count` in SQL (default 100) |
| Total count       | **get-histograms**      | `select count(*) from log`        |
| Sort by time      | `--reverse true/false`  | `order by __time__ asc/desc`      |
| Filter syntax     | Query syntax only       | Query left of `\|`; SQL right, `from log` fixed |
