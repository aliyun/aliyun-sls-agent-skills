# 🧩 Project Overview

[Alibaba Cloud SLS (Simple Log Service)](https://help.aliyun.com/zh/sls/) is an intelligent cloud-native observability and analytics platform, providing data collection, processing, query and analysis, visualization, alerting, consumption, and delivery.

This repository provides **Aliyun SLS** Agent Skills and aims to deliver an intelligent SLS operations and control solution. SLS Agent Skills are designed for typical SLS ops and development scenarios, enabling AI assistants to perform project and Logstore management, log query, and related operations in a standardized, reliable way via the Aliyun CLI.

## 📁 SLS Agent Skills

SLS Agent Skills include the following:

### ✅ aliyun-sls-cli-guidance

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

> aliyun-sls-cli-guidance depends on an installed and configured [aliyun-cli](https://github.com/aliyun/aliyun-cli) and the SLS plugin. The skill docs include installation and usage; the agent will handle setup and configuration as needed.

[Skill doc](.agents/skills/aliyun-sls-cli-guidance/SKILL.md)

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

# Install to Codex, global scope, only aliyun-sls-cli-guidance
sls-agent-skills -b --scope global --tool codex --skills aliyun-sls-cli-guidance -y
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
