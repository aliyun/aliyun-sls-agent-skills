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

## Delegate Log Query and Analysis

For SLS log query and analysis tasks, use the dedicated `alibabacloud-sls-query` skill instead of handling the workflow in this skill.

Delegate when the user asks to:

- query logs, analyze logs, or troubleshoot query results
- write, explain, optimize, or execute SLS index search, SQL, SQL scan, or SPL
- translate natural language into an SLS query, SQL, or SPL statement
- debug `get-logs-v2`, query syntax, index/statistics prerequisites, or `ProjectNotExist` during query work

If `alibabacloud-sls-query` is not installed, install it with `npx skills` before doing the query work.

Global Codex install:

```bash
npx skills add aliyun/alibabacloud-aiops-skills \
  --skill alibabacloud-sls-query \
  --agent codex \
  -g -y --full-depth
```

Project-level Codex install:

```bash
npx skills add aliyun/alibabacloud-aiops-skills \
  --skill alibabacloud-sls-query \
  --agent codex \
  -y --full-depth
```

After installation, actively locate and read the installed `alibabacloud-sls-query/SKILL.md` completely, then follow that skill's workflow for the query task. Keep this skill for project, logstore, index management, Logtail config, machine group, shard, put-logs, and other SLS CLI operations outside query analysis.

| Reference | Related commands | Description |
|-----------|------------------|-------------|
| [project](references/project.md) | `list-project` `create-project` `get-project` `update-project` `delete-project` | Manage SLS projects (create, list, update, delete) |
| [logstore](references/logstore.md) | `list-log-stores` `create-log-store` `get-log-store` `update-log-store` `delete-log-store` | Manage logstores within a project |
| [index](references/index.md) | `get-index` `create-index` `update-index` `delete-index` | Configure indexes to enable query and SQL analytics |
| [query-logs](references/query-logs.md) | `get-logs-v2` `get-histograms` | Query API quick reference; delegate query workflows to `alibabacloud-sls-query` |
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

## Rules

1. **Do not use deprecated APIs** — use the current replacement so behavior stays supported and predictable.

    | Deprecated | Use instead  |
    |------------|--------------|
    | `get-logs` | `get-logs-v2`|

2. **Obtain explicit user approval before any delete** — delete operations are irreversible.
3. **Use `--cli-dry-run` first** for destructive operations (delete, update).
4. **Update APIs require full parameters** — first call the corresponding **Get** API to retrieve current parameters, then include **all** meaningful parameters in the update call (including unchanged ones). Omitting parameters may reset them to defaults.
5. **If a command fails**: check required parameters with `--cli-dry-run`, verify credentials via `aliyun configure list`, read the error message, and compare your command with the corresponding reference file. If the sub-command is not recognized, upgrade the plugin via `aliyun plugin update sls`.
