# Put Logs Example

Complete examples for writing logs to a Logstore.

## Examples

**Single log (with time and fields):**

```bash
aliyun sls put-json-logs --project my-project --logstore my-logstore \
  --logs '{"__time__":1715769600, "region":"cn-hangzhou", "content":"hello aliyun cli"}'
```

**Multiple logs in one call:**

```bash
aliyun sls put-json-logs --project my-project --logstore my-logstore \
  --logs '{"__time__":1715769600, "region":"cn-hangzhou", "content":"hello aliyun cli"}' \
  --logs '{"hello":"world"}'
```

**With topic and source:**

```bash
aliyun sls put-json-logs --project my-project --logstore my-logstore \
  --logs '{"level":"info","msg":"started"}' \
  --topic "app-server" \
  --source "192.168.1.10"
```

## Notes

- Ensure the Logstore exists and has an index if you need to query or analyze these logs.
- ****time**** must be in seconds (Unix epoch). For millisecond timestamps, divide by 1000 or use seconds when constructing the value.
