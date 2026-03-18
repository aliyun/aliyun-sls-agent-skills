# 🧩 项目概览

[English](README.md) | 简体中文

[阿里云 SLS（日志服务）](https://help.aliyun.com/zh/sls/) 是智能化云原生观测与分析平台，提供数据采集、加工、查询与分析、可视化、告警、消费与投递等功能。

本仓库提供面向 **阿里云 SLS** 的 SLS Agent Skills，旨在提供智能化的 SLS 运维管控方案。SLS Agent Skills 面向 SLS 典型运维与开发场景设计，使 AI 助手能够基于 Aliyun CLI 规范、可靠地完成项目与 Logstore 管理、日志查询等操作。

## 📁 SLS Agent Skills

SLS Agent Skills 提供了如下的 skills：

### ✅ alibabacloud-sls-cli-guidance

**使用场景：**

- 查询与管理 SLS 项目、Logstore、索引配置等
- 向 SLS Logstore 写入日志、查询日志
- 其他所有 SLS 支持的 OpenAPI，例如告警、仪表盘、加工任务等

**触发方法：**

当用户提到阿里云日志、SLS、日志库或日志服务相关操作时触发。**示例 Prompt：**

```text
查看我在杭州地域下有哪些 sls project
帮我在 aliyun-test-project 下创建一个名叫 test 的日志库，并创建全文索引
帮我向 aliyun-test-project test 日志库写入一条日志，内容为 hello: world
帮我查询 aliyun-test-project test 日志库最近两分钟的日志
```

> alibabacloud-sls-cli-guidance 依赖已安装并配置的 [aliyun-cli](https://github.com/aliyun/aliyun-cli) 及 SLS 插件，技能文档中已包含安装与使用说明，AGENT 会自行处理安装与配置。

[文档链接](.agents/skills/alibabacloud-sls-cli-guidance/SKILL.md)

## 📦 安装 Skill

您可以通过以下任意一种方式安装 Skill：

### 通过 sls-agent-skills 助手安装（推荐）

sls-agent-skills 助手可以简化安装步骤，这需要您的环境中安装了 pip。
**支持安装到以下软件：**

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

安装 sls-agent-skills 助手：

```bash
pip install aliyun-sls-agent-skills
```

使用**交互模式**安装 Skill：

```bash
# 交互模式下会依次选择目标工具、安装范围（项目 / 全局）及要安装的 skills。
sls-agent-skills
```

### 复制 Skill 目录到安装目录

您可以手动将 [.agents/skills](.agents/skills) 下的技能目录复制到目标工具的安装目录，完成技能的安装。各工具对应的目录如下（项目目录相对于项目根，全局目录相对于用户主目录 `~`）：

| 工具 | 项目安装目录 | 全局安装目录 |
|------|----------------|----------------|
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

## 🛠️ 参与与反馈

欢迎通过 Issue 或 Pull Request 参与贡献。

如有问题或建议，请前往 [GitHub Issues](https://github.com/aliyun/aliyun-sls-agent-skills/issues)。
