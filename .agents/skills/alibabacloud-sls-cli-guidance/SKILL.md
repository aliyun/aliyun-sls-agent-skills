---
name: alibabacloud-sls-cli-guidance
description: Manage Alibaba Cloud SLS (Simple Log Service) resources using aliyun-cli. Use when working with SLS projects, logstores, log queries, or when the user mentions Aliyun Log, Aliyun SLS, or log service operations.
---

# Aliyun SLS CLI

Command-line interface for managing Alibaba Cloud Simple Log Service (SLS) resources including projects, logstores, and log queries.

## Prerequisites Check

**Before starting**, verify that aliyun-cli and sls plugin are installed:

```bash
# Check if aliyun-cli installed
aliyun version
# Check if sls plugin for aliyun-cli is installed
aliyun sls version
```

Expected output: `aliyun-cli-sls 0.1.0 (5e6288421)` or similar

### Installation (if not installed)

If the check fails, install aliyun-cli:

```bash
/bin/bash -c "$(curl -fsSL https://aliyuncli.alicdn.com/install.sh)"
```

Then install the SLS plugin:

```bash
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

## Basic Usage

### List all available SLS APIs

```bash
aliyun help sls
```

### Get help for specific API

```bash
aliyun help sls <apiName>
```

Example:

```bash
aliyun help sls list-project
```

### Validate command syntax (dry-run)

Add `--cli-dry-run` to validate parameters without executing:

```bash
aliyun sls list-project --offset 0 --size 50 --cli-dry-run
```

This prints request details but doesn't send the actual API call.

## Common Operations

### Quick Reference

| Operation           | Command Pattern |
|---------------------|----------------|
| **List projects**   | `aliyun sls list-project [--offset 0] [--size 50]` |
| **Get project**     | `aliyun sls get-project --project <name>` |
| **Create project**  | `aliyun sls create-project --project-name <name> --description <desc>` |
| **List logstores**  | `aliyun sls list-log-stores --project <name>` |
| **Get logstore**    | `aliyun sls get-log-store --project <name> --logstore <name>` |
| **Create logstore** | `aliyun sls create-log-store --project <name> --logstore-name <name> --ttl <days> --shard-count <n>` |
| **Update logstore** | `aliyun sls update-log-store --project <name> --logstore <name> --logstore-name <name> --ttl <days>` |
| **Query logs**      | `aliyun sls get-logs-v2 --project <name> --logstore <name> --from <unix_timestamp> --to <unix_timestamp> --offset 0 --line 100 --query "*" --accept-encoding lz4` |

### Output Format

All commands return JSON format output by default.

### JMESPath Query Filtering

Use `--cli-query` with JMESPath expressions to filter output:

```bash
aliyun sls list-project --cli-query "projects[*].name"
```

## Detailed Examples

**Required**: Before calling an SLS API, check whether a related detailed example exists under the `references/` directory. If it does, **you must read that example** and follow its usage (parameters, patterns, and best practices) before constructing or executing the command.

Reference files in `references/`:

- **Project operations**: [references/project-example.md](references/project-example.md)
- **Logstore operations**: [references/logstore-example.md](references/logstore-example.md)
- **Log query operations**: [references/query-logs-example.md](references/query-logs-example.md)
- **Index configuration**: [references/index-example.md](references/index-example.md)
- **Put logs**: [references/put-logs-example.md](references/put-logs-example.md)

## Important Notes

### Safety Tips

1. **Use --cli-dry-run first** for destructive operations (delete, update)
2. **Grant Before Delete** Delete operations are **irreversible and very dangerous**. You **must** obtain explicit approval from the user before executing any delete command; do not proceed until the user has granted permission.

### Update APIs

When using Update-type APIs (e.g. `update-project`, `update-log-store`): first call the corresponding **Get** API to retrieve the current parameters, then include **all** meaningful parameters in the update call—including those that are not changing. Omitting parameters may reset them to defaults or cause unintended changes.

## Error Handling

If a command fails:

1. Ensure required parameters are provided, use `--cli-dry-run` to validate syntax
2. Check credential configuration: `aliyun configure list`
3. Check error message for specific failure reason
4. **Check relevant examples** – If a detailed example exists under the `references/` directory for the operation, compare your command with it to ensure usage and parameters match.

## Common Parameters

**Global parameters available for all commands**:

- `--cli-dry-run`: Validate command without execution
- `--cli-query <jmespath>`: Filter output with JMESPath
- `--region <region>`: Override region
- `--log-level <level>`: Set log level (DEBUG, INFO, WARN, ERROR)
- `--quiet`: Disable output
- `--help`: Show command help
