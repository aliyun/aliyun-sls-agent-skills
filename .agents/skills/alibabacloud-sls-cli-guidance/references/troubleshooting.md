# Troubleshooting

Use this checklist when an SLS CLI command fails, returns no result, or behaves differently from the expected API reference.

## 1. CLI and Plugin

- Run `aliyun version` to verify the CLI exists.
- Run `aliyun sls version` to verify the SLS plugin exists.
- If a subcommand or flag is not recognized, update the plugin:

```bash
aliyun plugin update sls
```

- If the plugin is missing, install it:

```bash
aliyun plugin install --names sls
```

## 2. Credentials and Region

- Run only `aliyun configure list` to check credential status.
- Do not read, echo, print, or ask the user to paste AccessKey IDs, AccessKey secrets, STS tokens, or other credentials.
- If no valid profile or region is shown, ask the user to run `aliyun configure` outside this session.
- Use `--region <region-id>` to override the configured region for a single command.

## 3. Command Shape

- Read the operation reference before retrying.
- Use `aliyun help sls <apiName>` to confirm supported flags.
- Use `--cli-dry-run` before destructive or update operations.
- For update APIs, call the corresponding Get API first and include all meaningful parameters in the update call.

## 4. Common Errors

| Error | Likely cause | Action |
|-------|--------------|--------|
| `ProjectNotExist` | Project is in another region or the project name is wrong | Use cross-region discovery below |
| `LogStoreNotExist` | Logstore name or project is wrong | Confirm project and logstore names |
| `Unauthorized` / `Forbidden` | Missing RAM permission or wrong account | Stop and ask the user to verify permissions |
| `InvalidParameter` | Missing, malformed, or incomplete parameter | Compare with the reference doc and `aliyun help sls <apiName>` |
| `unknown command` / `unknown flag` | Old or missing SLS plugin | Run `aliyun plugin update sls` |
| timeout / connection failure | Public endpoint is unreachable from the environment | Retry with an internal endpoint when running inside Alibaba Cloud VPC |

## 5. Cross-Region Project Discovery

When `ProjectNotExist` is returned — or the user does not know which region a project belongs to — use `get-project` with `--cross-region true` to locate the project across all regions in a single call.

**Constraint:** This API is **only** available via the `cn-zhangjiakou` endpoint. Do not use any other endpoint with `--cross-region true`.

### Prerequisites

- **SLS plugin version** >= `0.5.2`. Upgrade if needed:

```bash
aliyun plugin update sls
```

- **RAM permission**: action `log:GetProject`, resource `acs:log:{#regionId}:{#accountId}:project/{#ProjectName}`.

### Usage

```bash
aliyun sls get-project \
  --project <project-name> \
  --cross-region true \
  --endpoint cn-zhangjiakou.log.aliyuncs.com \
  --user-agent "AlibabaCloud-Agent-Skills/alibabacloud-sls-cli-guidance/{session-id}"
```

### Response (key fields)

| Field | Type | Description |
|-------|------|-------------|
| `region` | string | Region ID where the project actually resides, e.g. `cn-shanghai` |
| `internetEndpoint` | string | Public endpoint for the project, e.g. `cn-shanghai.log.aliyuncs.com` |

### Workflow After Discovery

Once the project is found, use the returned `internetEndpoint` as `--endpoint` in subsequent commands:

```bash
aliyun sls get-log-store \
  --endpoint cn-shanghai.log.aliyuncs.com \
  --project <project-name> \
  --logstore <logstore-name> \
  --user-agent "AlibabaCloud-Agent-Skills/alibabacloud-sls-cli-guidance/{session-id}"
```

### When to Use

1. A CLI call returns `ProjectNotExist` and the user cannot confirm the region.
2. The user explicitly asks "which region is my project in?".
3. The configured `--region` / `--endpoint` does not match the project's actual location.

### Limitations

- Only the `cn-zhangjiakou` endpoint supports cross-region discovery.
- The command queries project metadata only — it does **not** return Logstore data.
- Network access to `cn-zhangjiakou.log.aliyuncs.com` must be available from the caller's environment.

## 6. Query and Analysis Failures

Use the `alibabacloud-sls-query` skill for log query troubleshooting. Do not troubleshoot log query work in this skill.
