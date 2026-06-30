
# Aliyun SLS Agent Skills

English | [简体中文](README_CN.md)

[Alibaba Cloud SLS (Simple Log Service)](https://help.aliyun.com/zh/sls/) is an intelligent cloud-native observability and analytics platform, providing data collection, processing, query and analysis, visualization, alerting, consumption, and delivery.

This repository provides **Aliyun SLS** Agent Skills and aims to deliver an intelligent SLS operations and control solution. SLS Agent Skills are designed for typical SLS ops and development scenarios, enabling AI assistants to perform project and Logstore management, log query, and related operations in a standardized, reliable way via the Aliyun CLI.

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## SLS Agent Skills

### alibabacloud-sls-cli-guidance

**Use cases:**

- Query and manage SLS projects, Logstores, index configuration, etc.
- Write logs to and query logs from SLS Logstores
- All other SLS OpenAPI capabilities, e.g. alerting, dashboards, processing jobs

**Trigger:**

When the user mentions Aliyun Log, SLS, logstore, or log service-related operations. **Example prompts:**

```text
List my SLS projects in the Hangzhou region
Create a logstore named test under aliyun-test-project and create a full-text index
Write a log to aliyun-test-project / test with content hello: world
Query the last two minutes of logs from aliyun-test-project / test
```

> The aliyun CLI and SLS plugin installation instructions are included in the skill. After installing the skill, the agent will automatically check the environment and install the required dependencies. To install manually:
>
> ```bash
> sudo /bin/bash -c "$(curl -fsSL https://aliyuncli.alicdn.com/install.sh)"
> aliyun plugin install --names sls
> ```

[Skill doc](skills/alibabacloud-sls-cli-guidance/SKILL.md)

## Install

Install via [`npx skills`](https://skills.sh):

```bash
npx skills add alibabacloud-sls-cli-guidance -g
```

Also recommended — install **alibabacloud-sls-query** for advanced SLS log query capabilities:

```bash
npx skills add aliyun/alibabacloud-aiops-skills \
  --skill alibabacloud-sls-query \
  -g --full-depth
```

## Contributing & Feedback

Contributions via Issue or Pull Request are welcome.

For questions or suggestions, visit [GitHub Issues](https://github.com/aliyun/aliyun-sls-agent-skills/issues).
