# Machine Group

Manage machine groups within an SLS project. A machine group defines a set of machines for log collection. After creating a Logtail pipeline config, you must create a machine group and apply the config to it for collection to take effect.

## Key parameters

| Parameter | Description |
|-----------|-------------|
| `--project` | Project name (required) |
| `--group-name` | Machine group name (required) |
| `--machine-identify-type` | Identification type: `ip` (IP address) or `userdefined` (custom identifier) (required) |
| `--machine-list` | List of machine IPs or custom identifiers (required) |

## Rules

1. **Overwrite update**: `update-machine-group` replaces the entire machine list. Always call `get-machine-group` first, then pass all parameters back.
2. **Deleting a machine group** automatically unbinds all applied Logtail configs.

## Examples

### List machine groups

```bash
aliyun sls list-machine-group --project my-project
```

Pagination: `--offset` (default 0) and `--size` (max 500).

Filter by name (partial match):

```bash
aliyun sls list-machine-group --project my-project --group-name "container"
```

### Create machine group (IP-based)

```bash
aliyun sls create-machine-group --project my-project \
  --group-name container \
  --machine-identify-type ip \
  --machine-list 192.168.5.2
```

Multiple machines:

```bash
aliyun sls create-machine-group --project my-project \
  --group-name my-app-group \
  --machine-identify-type ip \
  --machine-list 192.168.5.2 192.168.5.3 192.168.5.4
```

### Create machine group (custom identifier)

```bash
aliyun sls create-machine-group --project my-project \
  --group-name my-custom-group \
  --machine-identify-type userdefined \
  --machine-list my-app-identifier
```

### Apply Logtail config to machine group

```bash
aliyun sls apply-config-to-machine-group --project my-project \
  --config-name my-config \
  --machine-group container
```

### List applied configs on a machine group

```bash
aliyun sls get-applied-configs --project my-project --machine-group container
```

### Remove Logtail config from machine group

```bash
aliyun sls remove-config-from-machine-group --project my-project \
  --config-name my-config \
  --machine-group container
```
