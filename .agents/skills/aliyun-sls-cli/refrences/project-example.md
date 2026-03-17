# Project Operations Examples

Complete examples for managing SLS Projects using aliyun-cli.

## List Projects

### Basic listing

```bash
aliyun sls list-project
```

### List with pagination

```bash
aliyun sls list-project --offset 0 --size 50
```

### Filter by project name (fuzzy match)

```bash
aliyun sls list-project --project-name "my-project"
```

## Create Project

### Prefer to create with recycle bin enabled

```bash
aliyun sls create-project \
  --project-name my-new-project \
  --description "Project with recycle bin" \
  --recycle-bin-enabled true
```

## Project Naming Requirements

- **Globally unique** across all Alibaba Cloud regions
- Lowercase letters, numbers, and hyphens (`-`) only
- Must start and end with lowercase letter or number
- Length: 3-63 characters
- **Cannot be modified** after creation

**Valid examples**:

- `my-app-logs`
- `prod-server-2024`
- `test123`

**Invalid examples**:

- `My-App-Logs` (uppercase not allowed)
- `my_app_logs` (underscore not allowed for projects)
- `ab` (too short, minimum 3 characters)
- `-myapp` (cannot start with hyphen)
- `myapp-` (cannot end with hyphen)
