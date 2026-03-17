# Index Configuration (create-index)

Index configuration enables query and SQL analytics on a Logstore. You must create an index before using query syntax or SQL on logs.

- **line**: Full-text index. Enables searching log content by keyword (e.g. `"someWord"` in query).
- **keys**: Field index. Index specific log fields for filtering (e.g. `key: "value"`) and SQL. Create indexes for fields you often filter or aggregate on.

At least one of `line` or `keys` must be specified when calling **create-index**.

**update-index** performs an **overwrite update**: the full index configuration you send replaces the existing one. It does not merge or patch. To change the index, get the current config (e.g. **get-index**), then send the complete desired config with **update-index**.

Index changes (create or update) take effect **within 1 minute**.

---

## Field index types

| Type    | Use for                |
|---------|------------------------|
| **text**  | String content; supports full-text and key-value search |
| **long**  | Integer values         |
| **double**| Floating-point values  |
| **json**  | JSON content; supports full-text and key-value search   |

**Common options for all types**:

- **alias**: Alias name for the field.
- **doc_value**: Whether to enable analytics so the field can be used in SQL (e.g. `GROUP BY`, `WHERE`). **Recommended: true.**

**Options for text and json only**:

- **caseSensitive**: Case-sensitive matching (boolean).
- **chn**: Whether the content contains Chinese (boolean). **Recommended: false** if not needed.
- **token**: List of token delimiters for full-text split (e.g. `[","," ",";","=",...]`).

---

## Example 1: Full-text index only

Only full-text search on raw log content; no field-level index.

**Config**:

```json
{
  "line": {
    "chn": false,
    "caseSensitive": false,
    "token": [",", " ", "'", "\"", ";", "=", "(", ")", "[", "]", "{", "}", "?", "@", "<", "&", "/", ":", "\n", "\t", "\r"]
  }
}
```

**CLI** (pass `--line` as JSON string; escape quotes in shell as needed):

```bash
aliyun sls create-index --project my-project --logstore my-logstore \
  --line '{"chn":false,"caseSensitive":false,"token":[","," ",";","=","(",")","[","]","{","}",":","\n","\t","\r"]}'
```

---

## Example 2: Full-text index + field index

Full-text search plus field indexes for filtering and SQL analytics.

**Config**:

```json
{
  "keys": {
    "region": {
      "doc_value": true,
      "alias": "",
      "type": "text",
      "caseSensitive": false,
      "chn": false,
      "token": [",", " ", "'", "\"", ";", "=", "(", ")", "[", "]", "{", "}", "?", "@", "<", "&", "/", ":", "\n", "\t", "\r"]
    },
    "end_time": {
      "doc_value": true,
      "alias": "",
      "type": "long"
    },
    "request_time": {
      "doc_value": true,
      "alias": "",
      "type": "double"
    }
  },
  "line": {
    "caseSensitive": false,
    "chn": true
  }
}
```

**CLI**: Pass both `--line` and `--keys` as JSON strings. For complex JSON, write the config to a file and pass it (e.g. with `$(cat index-config.json)` or your shell’s equivalent), or escape quotes carefully:

```bash
# Example: create index with line + keys (simplified; adjust escaping for your shell)
aliyun sls create-index --project my-project --logstore my-logstore \
  --line '{"caseSensitive":false,"chn":true}' \
  --keys '{"region":{"doc_value":true,"alias":"","type":"text","caseSensitive":false,"chn":false,"token":[","," ",";","="]},\"end_time\":{\"doc_value\":true,\"alias\":\"\",\"type\":\"long\"},\"request_time\":{\"doc_value\":true,\"alias\":\"\",\"type\":\"double\"}}'
```

For production, prefer building the JSON in a script or file and passing it to avoid quoting errors.

---

## Summary

| Item        | Meaning |
|-------------|--------|
| **line**    | Full-text index; at least one of line/keys required |
| **keys**    | Field index; one entry per field, type text/long/double/json |
| **text/json** | Set caseSensitive, chn (recommend false), token |
| **All types** | Prefer doc_value: true for SQL; alias optional |
| **create-index** | `--line '...'` and/or `--keys '...'` as JSON strings |
