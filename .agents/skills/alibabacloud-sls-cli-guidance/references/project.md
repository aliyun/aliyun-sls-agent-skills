# Project Operations

Manage SLS projects. A project is the top-level resource that contains logstores, alerts, dashboards, and other SLS configurations.

## Naming requirements

- **Globally unique** across all Alibaba Cloud regions
- Lowercase letters, numbers, and hyphens (`-`) only
- Must start and end with a lowercase letter or number
- Length: 3–63 characters
- **Cannot be modified** after creation

## Key parameters

| Parameter | Description |
|-----------|-------------|
| `--project-name` | Project name (required for create; also used as fuzzy filter for list) |
| `--description` | Project description |
| `--recycle-bin-enabled` | Enable recycle bin for deleted logstores (recommended: `true`) |

## Examples

### List projects

```bash
aliyun sls list-project
```

Pagination: `--offset` (default 0) and `--size` (default 100, max 500).

Fuzzy filter by name:

```bash
aliyun sls list-project --project-name "my-project" --offset 0 --size 50
```

### Create project

```bash
aliyun sls create-project \
  --project-name my-new-project \
  --description "Project with recycle bin" \
  --recycle-bin-enabled true
```

### Get project

```bash
aliyun sls get-project --project my-project
```

### Cross-region project discovery

Use cross-region discovery when a command returns `ProjectNotExist`, or when the user does not know which region a project belongs to.

Important constraints:

- `--cross-region true` is only available through the `cn-zhangjiakou.log.aliyuncs.com` endpoint.
- The command returns project metadata only; it does not query Logstore data.
- The SLS plugin must support `--cross-region true`. If the flag is not recognized, run `aliyun plugin update sls`.
- The caller needs `log:GetProject` permission on the target project.

```bash
aliyun sls get-project \
  --project my-project \
  --cross-region true \
  --endpoint cn-zhangjiakou.log.aliyuncs.com \
  --user-agent "AlibabaCloud-Agent-Skills/alibabacloud-sls-cli-guidance/{session-id}"
```

Read the returned `region` and `internetEndpoint` fields. Use the returned endpoint or region in subsequent SLS commands:

```bash
aliyun sls get-log-store \
  --endpoint cn-shanghai.log.aliyuncs.com \
  --project my-project \
  --logstore my-logstore \
  --user-agent "AlibabaCloud-Agent-Skills/alibabacloud-sls-cli-guidance/{session-id}"
```

### Update project

```bash
aliyun sls update-project --project my-project --description "Updated description"
```

### Delete project

```bash
aliyun sls delete-project --project my-project
```
