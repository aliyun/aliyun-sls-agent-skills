# Put Logs

Write logs to a logstore using `put-json-logs`. Each `--logs` flag takes a JSON object representing one log entry.

## Key parameters

| Parameter | Description |
|-----------|-------------|
| `--project` | Target project name (required) |
| `--logstore` | Target logstore name (required) |
| `--logs` | JSON object for one log entry; repeat the flag to send multiple logs in one call |
| `--topic` | Log topic tag (optional, used to classify logs) |
| `--source` | Log source tag, e.g. server IP (optional) |

## Rules

1. `__time__` is a reserved field — its value must be a **string** of Unix timestamp in seconds (e.g. `"1715769600"`, not `1715769600`). If omitted, the server uses the receive time.
2. The target logstore must already exist. If you need to query or analyze these logs, an index must also be configured (see [index.md](index.md)).

## Examples

### Single log

```bash
aliyun sls put-json-logs --project my-project --logstore my-logstore \
  --logs '{"__time__":"1715769600", "region":"cn-hangzhou", "content":"hello aliyun cli"}'
```

### Multiple logs in one call

Repeat `--logs` for each log entry:

```bash
aliyun sls put-json-logs --project my-project --logstore my-logstore \
  --logs '{"__time__":"1715769600", "region":"cn-hangzhou", "content":"log entry 1"}' \
  --logs '{"__time__":"1715769601", "region":"cn-hangzhou", "content":"log entry 2"}'
```

### With topic and source

```bash
aliyun sls put-json-logs --project my-project --logstore my-logstore \
  --logs '{"level":"info","msg":"started"}' \
  --topic "app-server" \
  --source "192.168.1.10"
```
