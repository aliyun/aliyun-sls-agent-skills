# Index Configuration

Index configuration enables query and SQL analytics on a Logstore. You must create an index before using query syntax or SQL on logs.

## Index types

- **line**: Full-text index. Enables searching log content by keyword (e.g. `"someWord"` in query).
- **keys**: Field index. Index specific log fields for filtering (e.g. `key: "value"`) and SQL analytics.

At least one of `line` or `keys` must be specified when calling `create-index` or `update-index`.

## Field index types & options

| Type | Use for |
|------|---------|
| **text** | String content; supports full-text and key-value search |
| **long** | Integer values |
| **double** | Floating-point values |
| **json** | JSON content; supports full-text and key-value search |

**Options for all types**:

- **doc_value**: Enable analytics so the field can be used in SQL (`GROUP BY`, `WHERE`). **Recommended: true.**
- **alias**: Alias name for the field (optional).

**Additional options for text and json**:

- **caseSensitive**: Case-sensitive matching (boolean).
- **chn**: Whether the content contains Chinese (boolean). **Recommended: false** if not needed.
- **token**: List of token delimiters for full-text split (e.g. `[","," ",";","=",...]`).

## Rules

1. **Overwrite update**: `update-index` replaces the entire index configuration — it does not merge or patch. Always call `get-index` first, then send the complete desired config with `update-index`.
2. Index changes (create or update) take effect **within 1 minute**.

## Examples

### Get current index configuration

```bash
aliyun sls get-index --project my-project --logstore my-logstore
```

### Create index: full-text only

```bash
aliyun sls create-index --project my-project --logstore my-logstore \
  --line '{"chn":false,"caseSensitive":false,"token":[","," ",";","=","(",")","[","]","{","}",":","\n","\t","\r"]}'
```

### Create index: full-text + field indexes

For complex JSON, write the config to a file to avoid shell quoting issues:

```bash
cat > /tmp/keys.json << 'EOF'
{
  "region": {
    "doc_value": true,
    "alias": "",
    "type": "text",
    "caseSensitive": false,
    "chn": false,
    "token": [",", " ", ";", "=", "(", ")", "[", "]", "{", "}", ":", "\n", "\t", "\r"]
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
}
EOF

aliyun sls create-index --project my-project --logstore my-logstore \
  --line '{"caseSensitive":false,"chn":false}' \
  --keys "$(cat /tmp/keys.json)"
```

### Update index workflow

Always get-then-update to avoid losing existing configuration:

```bash
aliyun sls get-index --project my-project --logstore my-logstore

# Modify the returned JSON as needed, then pass the full config back:
aliyun sls update-index --project my-project --logstore my-logstore \
  --line '{"caseSensitive":false,"chn":false}' \
  --keys "$(cat /tmp/keys.json)"
```

### Delete index

```bash
aliyun sls delete-index --project my-project --logstore my-logstore
```
