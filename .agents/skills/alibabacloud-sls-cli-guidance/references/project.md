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

### Update project

```bash
aliyun sls update-project --project my-project --description "Updated description"
```

### Delete project

```bash
aliyun sls delete-project --project my-project
```
