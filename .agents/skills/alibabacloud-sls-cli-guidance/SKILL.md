---
name: alibabacloud-sls-cli-guidance
description: Manage Alibaba Cloud SLS (Simple Log Service) resources using aliyun-cli. Use when working with SLS projects, logstores, log queries, or when the user mentions Aliyun Log, Aliyun SLS, LogStore, Log Collection, or log service operations.
---

# Aliyun SLS CLI

Command-line interface for managing Alibaba Cloud Simple Log Service (SLS) resources including projects, logstores, and log queries.

## Prerequisites

**Before starting**, verify that aliyun-cli and sls plugin are installed:

```bash
aliyun version
aliyun sls version
```

Expected output: `aliyun-cli-sls 0.1.0 (5e6288421)` or similar

### Installation (if not installed)

If the check fails, install aliyun-cli using one of these methods:

**Option 1: Homebrew (macOS only)**

```bash
brew install aliyun-cli
aliyun plugin install --names sls
```

**Option 2: Official installer (Linux and macOS)**

```bash
# This method requires sudo permission to install to `/usr/local/bin/aliyun`.
sudo /bin/bash -c "$(curl -fsSL https://aliyuncli.alicdn.com/install.sh)"
aliyun plugin install --names sls
```

## Configuration

Configure access credentials (using AccessKey example) and region:

```bash
aliyun configure set \
  --access-key-id <access-key-id> \
  --access-key-secret <access-key-secret> \
  --region <region>
```

**Region examples**: `cn-hangzhou`, `cn-shanghai`, `cn-beijing`, `us-west-1`

**IMPORTANT**: If credentials or region are not provided by the user, **request them explicitly** before proceeding with any operations.

For other authentication methods(StsToken|RamRoleArn|EcsRamRole|...), check: `aliyun configure set --help`

## Common Operations

Below lists frequently used SLS operations. **Read the corresponding reference file first** before executing any of them.

| Reference | Related commands | Description |
|-----------|------------------|-------------|
| [project](references/project.md) | `list-project` `create-project` `get-project` `update-project` `delete-project` | Manage SLS projects (create, list, update, delete) |
| [logstore](references/logstore.md) | `list-log-stores` `create-log-store` `get-log-store` `update-log-store` `delete-log-store` | Manage logstores within a project |
| [index](references/index.md) | `get-index` `create-index` `update-index` `delete-index` | Configure indexes to enable query and SQL analytics |
| [query-logs](references/query-logs.md) | `get-logs-v2` `get-histograms` | Query and analyze logs with search or SQL |
| [put-logs](references/put-logs.md) | `put-json-logs` | Write logs to a logstore |
| [text-to-sql](references/text-to-sql.md) | `call-ai-tools` | Generate SQL from natural language via SLS Copilot |

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

## Rules

1. **Do not use deprecated APIs** — use the current replacement so behavior stays supported and predictable.

    | Deprecated | Use instead  |
    |------------|--------------|
    | `get-logs` | `get-logs-v2`|

2. **Obtain explicit user approval before any delete** — delete operations are irreversible.
3. **Use `--cli-dry-run` first** for destructive operations (delete, update).
4. **Update APIs require full parameters** — first call the corresponding **Get** API to retrieve current parameters, then include **all** meaningful parameters in the update call (including unchanged ones). Omitting parameters may reset them to defaults.
5. **If a command fails**: check required parameters with `--cli-dry-run`, verify credentials via `aliyun configure list`, read the error message, and compare your command with the corresponding reference file.
