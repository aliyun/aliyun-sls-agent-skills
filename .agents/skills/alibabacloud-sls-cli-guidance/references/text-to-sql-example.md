# Text-to-SQL (call-ai-tools)

Use **call-ai-tools** with tool **text_to_sql** to generate SQL from natural language on the server. Use it when:

- You need to run **complex SQL** and want the service to produce a high-quality statement from a natural-language question.
- A **SQL query has failed** (syntax error, wrong schema, or poor results); retry by asking in natural language and using the generated SQL.

Then pass the returned SQL into **get-logs-v2** as `--query` (e.g. `* | <returned_sql>`). See [query-logs-example.md](query-logs-example.md) for get-logs-v2 usage.

---

## Command

```bash
aliyun sls call-ai-tools --tool-name text_to_sql --region cn-shanghai --biz-region-id <bizRegionId> --params '{
  "project": "<projectName>",
  "logstore": "<logstoreName>",
  "sys.query": "当前时间: <current_time>,问题:<question_text>"
}'
```

**Command options**

| Option | Value / note |
|--------|----------------|
| `--tool-name` | `text_to_sql` |
| `--region` | Must be `cn-shanghai` |
| `--biz-region-id` | Region of the project; if unset, use the region from `aliyun configure get \| grep region_id` |

**Params (JSON body)**

- **project** / **logstore** — Replace `<projectName>` and `<logstoreName>` with your project and logstore names.
- **sys.query** — Format: `当前时间: <current_time>,问题:<question_text>`
  - **`<current_time>`**: Human-readable time + space + Unix timestamp, e.g. `2026-03-18 14:04:11 1773813851` (strftime `"%Y-%m-%d %H:%M:%S"` then append `<unix_ts>`).
  - **`<question_text>`**: The user's question in natural language.

**Next step**: Pass the returned SQL into **get-logs-v2** as `--query` (e.g. `* | <returned_sql>`).
