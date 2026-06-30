---
name: alibabacloud-sls-cli-guidance
description: Manage Alibaba Cloud SLS (Simple Log Service) resources using aliyun-cli. Use when working with SLS projects, logstores, log queries, or when the user mentions Aliyun Log, Aliyun SLS, LogStore, Log Collection, or log service operations.
---

# Aliyun SLS CLI

Command-line interface for managing Alibaba Cloud Simple Log Service (SLS) resources including projects, logstores, Logtail configs, machine groups, and other non-query operations.

## Prerequisites

**Before starting**, verify that aliyun-cli and sls plugin are installed:

```bash
aliyun version
aliyun sls version
```

Expected output: `aliyun-cli-sls 0.1.0 (5e6288421)` or similar

### Installation (if not installed)

If the check fails, follow [references/cli-installation-guide.md](references/cli-installation-guide.md) to install aliyun-cli, then install the sls plugin:

```bash
aliyun plugin install --names sls
```

### Update Plugins

```bash
aliyun plugin update sls
```

### Check Alibaba Cloud credentials configured

Run `aliyun configure list` to check if credentials configured.
If no valid profile is shown, **STOP** here and ask the user to run `aliyun configure` outside of this session.

**Security rules:**

- **NEVER** read, echo, or print AK/SK values
- **NEVER** ask the user to paste AK/SK into the conversation
- **ONLY** use `aliyun configure list` to check credential status

## Observability

When this skill is loaded, generate one random session ID for the session: a 32-character lowercase hex string.

Every `aliyun` command that calls a cloud API must include this User-Agent flag:

```bash
--user-agent "AlibabaCloud-Agent-Skills/alibabacloud-sls-cli-guidance/{session-id}"
```

Local utility commands do not call cloud APIs and should not include `--user-agent`, including `aliyun version`, `aliyun configure ...`, `aliyun plugin ...`, and `aliyun help ...`.

Example:

```bash
aliyun sls list-project \
  --offset 0 --size 50 \
  --user-agent "AlibabaCloud-Agent-Skills/alibabacloud-sls-cli-guidance/a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
```

## Log Query and Analysis

Use the `alibabacloud-sls-query` skill for all log query and analysis tasks. It covers SLS query & analysis syntax (index search, SQL, SPL), scenario examples, troubleshooting, and end-to-end query workflows — it is the required skill for querying SLS logs.

Use `alibabacloud-sls-query` when the user asks to:

- query logs, analyze logs, or troubleshoot query results
- write, explain, optimize, or execute SLS index search, SQL, SQL scan, or SPL
- translate natural language into an SLS query, SQL, or SPL statement
- debug `get-logs-v2`, query syntax, index/statistics prerequisites

If the skill is already available, use it directly. If not, see [alibabacloud-sls-query-installation](references/alibabacloud-sls-query-installation.md) to install and load it.

## Common Operations

For project, logstore, index management, Logtail config, machine group, put-logs, and other non-query SLS operations, stay in this skill and refer to the reference docs below. **Read the corresponding reference file first** before executing any of them.

| Reference | Related commands | Description |
|-----------|------------------|-------------|
| [project](references/project.md) | `list-project` `create-project` `get-project` `update-project` `delete-project` | Manage SLS projects |
| [logstore](references/logstore.md) | `list-log-stores` `create-log-store` `get-log-store` `update-log-store` `delete-log-store` | Manage logstores within a project |
| [index](references/index.md) | `get-index` `create-index` `update-index` `delete-index` | Configure indexes to enable query and SQL analytics |
| [put-json-logs](references/put-json-logs.md) | `put-json-logs` | Write logs to a logstore |
| [logtail-config](references/logtail-config.md) | `create-logtail-pipeline-config` `update-logtail-pipeline-config` `get-logtail-pipeline-config` `list-logtail-pipeline-config` `delete-logtail-pipeline-config` | Manage Logtail pipeline configs for log collection (file input, JSON/delimiter/regex parsing, multiline, time extraction) |
| [machine-group](references/machine-group.md) | `create-machine-group` `update-machine-group` `get-machine-group` `list-machine-group` `delete-machine-group` `apply-config-to-machine-group` `remove-config-from-machine-group` `get-applied-configs` | Manage machine groups and apply Logtail configs to them |

## CLI Usage

### Discover APIs

```bash
aliyun help sls
aliyun help sls <apiName>
```

### Validate command syntax (dry-run)

Add `--cli-dry-run` to validate parameters without executing:

```bash
aliyun sls list-project --offset 0 --size 50 --cli-dry-run
```

### Output format

All commands return JSON by default. Use `--cli-query` with JMESPath expressions to filter output:

```bash
aliyun sls list-project --cli-query "projects[*].name"
```

### Global parameters

- `--cli-dry-run`: Validate command without execution
- `--cli-query <jmespath>`: Filter output with JMESPath
- `--region <region>`: Override region
- `--help`: Show command help

## Troubleshooting

When a command fails or returns unexpected results, read [references/troubleshooting.md](references/troubleshooting.md) for the full checklist, including:

- CLI and plugin version issues
- Credentials and region configuration
- Common errors (`ProjectNotExist`, `Unauthorized`, `InvalidParameter`, etc.)
- Cross-region project discovery (for `ProjectNotExist`)

## Rules

1. **Do not use deprecated APIs** — use the current replacement so behavior stays supported and predictable.

    | Deprecated | Use instead  |
    |------------|--------------|
    | `get-logs` | `get-logs-v2`|

2. **Obtain explicit user approval before any delete** — delete operations are irreversible.
3. **Use `--cli-dry-run` first** for destructive operations (delete, update).
4. **Update APIs require full parameters** — first call the corresponding **Get** API to retrieve current parameters, then include **all** meaningful parameters in the update call (including unchanged ones). Omitting parameters may reset them to defaults.
5. **If a command fails**: follow [references/troubleshooting.md](references/troubleshooting.md).
6. Use skill `alibabacloud-sls-query` for log query and analysis.
