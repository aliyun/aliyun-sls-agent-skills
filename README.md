
# 🧩 Project Overview

English | [简体中文](README_CN.md)

[Alibaba Cloud SLS (Simple Log Service)](https://help.aliyun.com/zh/sls/) is an intelligent cloud-native observability and analytics platform, providing data collection, processing, query and analysis, visualization, alerting, consumption, and delivery.

This repository provides **Aliyun SLS** Agent Skills and aims to deliver an intelligent SLS operations and control solution. SLS Agent Skills are designed for typical SLS ops and development scenarios, enabling AI assistants to perform project and Logstore management, log query, and related operations in a standardized, reliable way via the Aliyun CLI.

[![PyPI](https://img.shields.io/pypi/v/aliyun-sls-agent-skills.svg)](https://pypi.org/project/aliyun-sls-agent-skills/) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📁 SLS Agent Skills

SLS Agent Skills include the following:

### ✅ alibabacloud-sls-cli-guidance

**Use cases:**

- Query and manage SLS projects, Logstores, index configuration, etc.
- Write logs to and query logs from SLS Logstores
- All other SLS OpenAPI capabilities, e.g. alerting, dashboards, processing jobs

**Trigger:**

When the user mentions Aliyun Log, SLS, logstore, or log service–related operations. **Example prompts:**

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

[Skill doc](.agents/skills/alibabacloud-sls-cli-guidance/SKILL.md)

## 📦 Install Skill

You can install the skill in one of the following ways:

### Install via sls-agent-skills (recommended)

The sls-agent-skills helper simplifies installation and requires pip in your environment.

**Supported targets:**

- Claude Code
- OpenClaw
- Cursor
- Codex
- OpenCode
- GitHub Copilot
- Qoder
- Trae
- Iflow
- Kiro

Install the sls-agent-skills helper:

```bash
pip install aliyun-sls-agent-skills
```

Install the skill using **interactive mode**:

```bash
# You will be prompted to choose target tool, scope (project / global), and skills to install.
sls-agent-skills
```

**Headless install:**

```bash
# Install to Cursor, project scope, all skills
sls-agent-skills -b --scope project --tool Cursor -y

# Install to Codex, global scope, only alibabacloud-sls-cli-guidance
sls-agent-skills -b --scope global --tool codex --skills alibabacloud-sls-cli-guidance -y
```

### Copy skill directory to install location

You can manually copy the skill directories under [.agents/skills](.agents/skills) to your target tool’s install path. Project paths are relative to the project root; global paths are relative to the user home directory `~`:

| Tool | Project install path | Global install path |
|------|----------------------|----------------------|
| Claude Code | `.claude/skills` | `~/.claude/skills` |
| OpenClaw | `skills` | `~/.openclaw/skills` |
| Cursor | `.cursor/skills` | `~/.cursor/skills` |
| Codex | `.agents/skills` | `~/.agents/skills` |
| OpenCode | `.opencode/skills` | `~/.config/opencode/skills` |
| GitHub Copilot | `.github/skills` | `~/.copilot/skills` |
| Qoder | `.qoder/skills` | `~/.qoder/skills` |
| Trae | `.trae/skills` | `~/.trae/skills` |
| Iflow | `.iflow/skills` | `~/.iflow/skills` |
| Kiro | `.kiro/skills` | `~/.kiro/skills` |

## 🛠️ Contributing & Feedback

Contributions via Issue or Pull Request are welcome.

For questions or suggestions, visit [GitHub Issues](https://github.com/aliyun/aliyun-sls-agent-skills/issues).
