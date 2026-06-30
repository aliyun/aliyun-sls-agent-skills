
# Aliyun SLS Agent Skills

English | [简体中文](README_CN.md)

[Alibaba Cloud SLS (Simple Log Service)](https://help.aliyun.com/zh/sls/) is an intelligent cloud-native observability and analytics platform, providing data collection, processing, query and analysis, visualization, alerting, consumption, and delivery.

This repository provides **Aliyun SLS** Agent Skills and aims to deliver an intelligent SLS operations and control solution. SLS Agent Skills are designed for typical SLS ops and development scenarios, enabling AI assistants to perform project and Logstore management, log query, and related operations in a standardized, reliable way via the Aliyun CLI.

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Install

Install via [`npx skills`](https://skills.sh):

```bash
npx skills add aliyun/aliyun-sls-agent-skills --skill alibabacloud-sls-cli-guidance -g
```

Also recommended — install **alibabacloud-sls-query** for advanced SLS log query capabilities:

```bash
npx skills add aliyun/alibabacloud-aiops-skills \
  --skill alibabacloud-sls-query \
  -g --full-depth
```

## Skill 使用方法

### alibabacloud-sls-cli-guidance

Manage Alibaba Cloud SLS (Simple Log Service) resources via `aliyun-cli`. Covers high-frequency operations including Project, Logstore, Index, log query/analysis, log ingestion, Logtail collection config, and machine groups.

**Credential Configuration:**

This skill relies on `aliyun-cli` to access SLS. It supports AK, OAuth, RamRole, and other authentication methods. See the official docs for configuration: <https://help.aliyun.com/zh/cli/configure-credentials>.

**Usage:**

Automatically triggered when the conversation mentions Aliyun Log, SLS, LogStore, Logtail, log collection, etc. Just describe your needs in natural language. Examples:

Log query & analysis:

```text
Query logs with status=500 from my-app-logs/nginx-access in the past 1 hour, sorted by time descending, top 100
Show Top 10 request_uri by 5xx error count for yesterday
```

Project management:

```text
List projects in cn-hangzhou whose names start with prod-
Create a project named my-app-logs in cn-shanghai with description "application log archive"
```

Logstore management:

```text
Create a logstore named nginx-access under project my-app-logs with 30-day retention and 4 shards
Change the retention of logstore nginx-access from 30 to 90 days
```

Write logs:

```text
Write a JSON log to my-app-logs/test-store: {"level":"info","msg":"hello"}
```

[Skill doc](skills/alibabacloud-sls-cli-guidance/SKILL.md)

## Contributing & Feedback

Contributions via Issue or Pull Request are welcome.

For questions or suggestions, visit [GitHub Issues](https://github.com/aliyun/aliyun-sls-agent-skills/issues).
