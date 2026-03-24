# Logtail Pipeline Config

Manage Logtail pipeline configs for log collection. A pipeline config defines **what to collect** (inputs), **how to parse** (processors), and **where to send** (flushers). After creation, you must create a machine group and apply the config to it for collection to take effect.

## Key parameters

| Parameter | Description |
|-----------|-------------|
| `--project` | Project name (required) |
| `--config-name` | Config name (required) |
| `--inputs` | Input plugin list (required) |
| `--processors` | Processing plugin list (optional) |
| `--flushers` | Output plugin list (required) |
| `--log-sample` | Sample log content for reference (optional) |

## Examples

### Create: JSON log parsing

```bash
aliyun sls create-logtail-pipeline-config --project my-project \
  --config-name json-log-config \
  --inputs '{"Type":"input_file","FilePaths":["/app/**/output.json"],"EnableContainerDiscovery":false,"MaxDirSearchDepth":1,"FileEncoding":"utf8"}' \
  --processors '{"Type":"processor_parse_json_native","SourceKey":"content"}' \
  --flushers '{"Type":"flusher_sls","Logstore":"my-logstore","TelemetryType":"logs","Region":"cn-hangzhou","Endpoint":"cn-hangzhou-intranet.log.aliyuncs.com"}' \
  --log-sample '{"status": 200, "latency": 4152, "method": "GetUserConfig", "user": "Alice"}'
```

### Create: Delimiter log parsing

```bash
aliyun sls create-logtail-pipeline-config --project my-project \
  --config-name delimiter-log-config \
  --inputs '{"Type":"input_file","FilePaths":["/app/**/access.log"],"EnableContainerDiscovery":false,"MaxDirSearchDepth":1,"FileEncoding":"utf8"}' \
  --processors '{"Type":"processor_parse_delimiter_native","SourceKey":"content","Separator":"|","Quote":"\u0000","KeepingSourceWhenParseFail":true,"Keys":["remote_addr","time_iso8601","method","uri","protocol","status","sent_bytes","user_agent","latency"]}' \
  --flushers '{"Type":"flusher_sls","Logstore":"my-logstore","TelemetryType":"logs","Region":"cn-hangzhou","Endpoint":"cn-hangzhou-intranet.log.aliyuncs.com"}' \
  --log-sample '192.168.1.10 | 2026-03-24T10:52:01+08:00 | GET | /api/v1/products | HTTP/1.1 | 200 | 1240  | Mozilla/5.0 | 0.045'
```

### Create: Regex parsing + time parsing

For complex regex, write each processor to a separate file to avoid quoting issues:

```bash
cat > /tmp/processor_regex.json << 'ENDOFFILE'
{
  "Type": "processor_parse_regex_native",
  "SourceKey": "content",
  "Regex": "(\\d+-\\d+-\\d+\\s\\S+)\\s\\S+\\s\\[(\\w+)]\\s\\S+\\s(\\w+)\\s\\S+\\s(\\S+)\\s\\S+\\s(.*)",
  "Keys": ["time", "level", "func", "class", "content"]
}
ENDOFFILE

cat > /tmp/processor_time.json << 'ENDOFFILE'
{
  "Type": "processor_parse_timestamp_native",
  "SourceKey": "time",
  "SourceFormat": "%Y-%m-%d %H:%M:%S,%f"
}
ENDOFFILE

aliyun sls create-logtail-pipeline-config --project my-project \
  --config-name regex-time-config \
  --inputs '{"Type":"input_file","FilePaths":["/app/**/app.log"],"EnableContainerDiscovery":false,"MaxDirSearchDepth":1,"FileEncoding":"utf8"}' \
  --processors "$(cat /tmp/processor_regex.json)" \
  --processors "$(cat /tmp/processor_time.json)" \
  --flushers '{"Type":"flusher_sls","Logstore":"my-logstore","TelemetryType":"logs","Region":"cn-hangzhou","Endpoint":"cn-hangzhou-intranet.log.aliyuncs.com"}' \
  --log-sample '2026-03-24 11:15:02,456 | [INFO] | main | com.app.OrderService | User [1001] placed an order.'
```

### Create: Regex + multiline + time parsing + timezone

```bash
cat > /tmp/input.json << 'ENDOFFILE'
{
  "Type": "input_file",
  "FilePaths": ["/app/**/app.log"],
  "EnableContainerDiscovery": false,
  "MaxDirSearchDepth": 1,
  "FileEncoding": "utf8",
  "Multiline": {
    "Mode": "custom",
    "StartPattern": "\\d{4}-\\d{2}-\\d{2}\\s\\d{2}:\\d{2}:\\d{2},\\d{3}\\s\\|\\s\\[[A-Z]+\\]\\s\\|.*",
    "UnmatchedContentTreatment": "single_line"
  }
}
ENDOFFILE

cat > /tmp/processor_regex.json << 'ENDOFFILE'
{
  "Type": "processor_parse_regex_native",
  "SourceKey": "content",
  "KeepingSourceWhenParseFail": true,
  "Regex": "(\\d+-\\d+-\\d+\\s\\S+)\\s\\S+\\s\\[(\\w+)]\\s\\S+\\s(\\w+)\\s\\S+\\s(\\S+)\\s\\S+\\s(.*)",
  "Keys": ["time", "level", "func", "class", "content"]
}
ENDOFFILE

cat > /tmp/processor_time.json << 'ENDOFFILE'
{
  "Type": "processor_parse_timestamp_native",
  "SourceKey": "time",
  "SourceFormat": "%Y-%m-%d %H:%M:%S,%f",
  "SourceTimezone": "GMT+08:00"
}
ENDOFFILE

aliyun sls create-logtail-pipeline-config --project my-project \
  --config-name regex-multiline-config \
  --inputs "$(cat /tmp/input.json)" \
  --processors "$(cat /tmp/processor_regex.json)" \
  --processors "$(cat /tmp/processor_time.json)" \
  --flushers '{"Type":"flusher_sls","Logstore":"my-logstore","TelemetryType":"logs","Region":"cn-hangzhou","Endpoint":"cn-hangzhou-intranet.log.aliyuncs.com"}' \
  --log-sample '2026-03-24 11:15:02,456 | [INFO] | main | com.app.OrderService | User [1001] placed an order.'
```

## Config structure

### Input: `input_file`

| Field | Description |
|-------|-------------|
| `FilePaths` | File path patterns, supports `**` glob; exactly **1** path required |
| `FileEncoding` | File encoding: `utf8`, `gbk` |
| `MaxDirSearchDepth` | Max directory search depth (0–1000, lower is better) |
| `EnableContainerDiscovery` | Enable container auto-discovery |
| `Multiline` | Multiline log config (see [Multiline logs](#multiline-logs)) |

### Flusher: `flusher_sls`

| Field | Description |
|-------|-------------|
| `Logstore` | Target logstore name (required) |
| `TelemetryType` | `logs` or `metrics` (required) |
| `Region` | Region ID, e.g. `cn-hangzhou` (required) |
| `Endpoint` | SLS endpoint, e.g. `cn-hangzhou-intranet.log.aliyuncs.com` (required) |

### Processors

First processor must be a parsing plugin. After that, optionally add **1** time-parsing plugin, **1** filter plugin, and multiple desensitization plugins.

| Type | Description |
|------|-------------|
| `processor_parse_json_native` | Parse JSON-formatted logs |
| `processor_parse_delimiter_native` | Parse delimiter-separated logs |
| `processor_parse_regex_native` | Parse logs with regex |
| `processor_parse_timestamp_native` | Extract log time from a parsed field |

## Multiline logs

When logs span multiple lines, configure `Multiline` in the input plugin to combine them. Set `StartPattern` to a regex matching the **first line** of each log entry.

| Field | Description |
|-------|-------------|
| `Mode` | `custom` for custom regex |
| `StartPattern` | Regex matching the beginning of a log entry |
| `UnmatchedContentTreatment` | How to handle unmatched lines: `single_line` (treat as individual logs) or `discard` |

## Time parsing

Use `processor_parse_timestamp_native` to extract log time from a parsed field. Without it, log time defaults to collection time.

| Field | Description |
|-------|-------------|
| `SourceKey` | Field name containing the timestamp (required) |
| `SourceFormat` | Time format string (required, see table below) |
| `SourceTimezone` | Source timezone, e.g. `GMT+08:00` (optional, defaults to machine timezone) |

**Common time formats:**

| Example | Format |
|---------|--------|
| `2017-12-11 15:05:07,456` | `%Y-%m-%d %H:%M:%S,%f` |
| `2006-01-02T15:04:05Z07:00` | `%Y-%m-%dT%H:%M:%S` |
| `Mon, 02 Jan 2006 15:04:05 MST` | `%A, %d %b %Y %H:%M:%S` |

## Rules

1. **Overwrite update**: `update-logtail-pipeline-config` replaces the entire config. Always call `get-logtail-pipeline-config` first, then send the complete config with `update-logtail-pipeline-config`.
2. **Apply to machine group**: A config alone does not collect logs. You must create a machine group and apply the config to it (see [Apply Logtail config to machine group](machine-group.md)).
3. **Processor ordering**: The first processor must be a parsing plugin (JSON / delimiter / regex). Time-parsing must come after the parsing plugin.
4. For complex JSON parameters with special characters (regex, etc.), write to a temp file to avoid shell quoting issues.
5. For more Logtail pipeline config types (container stdout, syslog, MySQL, etc.), see [CreateLogtailPipelineConfig API reference](https://help.aliyun.com/zh/sls/developer-reference/api-sls-2020-12-30-createlogtailpipelineconfig).
