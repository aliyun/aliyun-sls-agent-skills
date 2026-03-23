# Text-to-SQL

Use `call-ai-tools` with tool `text_to_sql` to generate SQL from natural language via SLS Copilot. Use it when:

- You need **complex SQL** and want the service to produce a high-quality statement from a natural-language question.
- A **SQL query has failed** (syntax error, wrong schema, or poor results) — retry by describing the intent in natural language.

## Key parameters

| Parameter | Value / note |
|-----------|-------------|
| `--tool-name` | `text_to_sql` (required) |
| `--region` | Must be `cn-shanghai` |
| `--biz-region-id` | Region of the target project; if unset, defaults to the region from `aliyun configure list  \| grep default` |

**Params (JSON body)**:

| Field | Description |
|-------|-------------|
| `project` | Target project name |
| `logstore` | Target logstore name |
| `sys.query` | Format: `当前时间: <current_time>,问题:<question_text>` |

- **`<current_time>`**: human-readable time + Unix timestamp, e.g. `2026-03-18 14:04:11 1773813851`
- **`<question_text>`**: the user's question in natural language

## Example

```bash
aliyun sls call-ai-tools --tool-name text_to_sql --region cn-shanghai \
  --biz-region-id cn-hangzhou \
  --params '{
    "project": "my-project",
    "logstore": "my-logstore",
    "sys.query": "当前时间: 2026-03-18 14:04:11 1773813851,问题:最近1小时status为500的请求数量是多少"
  }'
```

## Next step

Pass the returned SQL into `get-logs-v2` as `--query` (e.g. `* | <returned_sql>`). See [query-logs.md](query-logs.md) for usage.
