
# 阿里云 SLS Agent Skills

[English](README.md) | 简体中文

[阿里云 SLS（日志服务）](https://help.aliyun.com/zh/sls/) 是智能化云原生观测与分析平台，提供数据采集、加工、查询与分析、可视化、告警、消费与投递等功能。

本仓库提供面向 **阿里云 SLS** 的 SLS Agent Skills，旨在提供智能化的 SLS 运维管控方案。SLS Agent Skills 面向 SLS 典型运维与开发场景设计，使 AI 助手能够基于 Aliyun CLI 规范、可靠地完成项目与 Logstore 管理、日志查询等操作。

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 安装

通过 [`npx skills`](https://skills.sh) 安装：

```bash
npx skills add aliyun/aliyun-sls-agent-skills --skill alibabacloud-sls-cli-guidance -g
```

同时推荐安装 **alibabacloud-sls-query**，提供更强大的 SLS 日志查询能力：

```bash
npx skills add aliyun/alibabacloud-aiops-skills \
  --skill alibabacloud-sls-query \
  -g --full-depth
```

## Skill 使用方法

### alibabacloud-sls-cli-guidance

通过 `aliyun-cli` 管理阿里云 SLS（日志服务）资源。覆盖 Project、Logstore、Index、日志查询/分析、日志写入、Logtail 采集配置、机器组等高频操作。

**凭证配置：**

Skill 依赖 `aliyun-cli` 访问 SLS，支持 AK、OAuth、RamRole 等多种鉴权方式，具体配置参见阿里云官方文档：<https://help.aliyun.com/zh/cli/configure-credentials>。

**使用方法：**

当对话中提到阿里云日志服务、SLS、LogStore、Logtail、日志采集等关键词时会自动触发。直接用自然语言描述需求即可，示例：

日志查询与分析：

```text
查询过去 1 小时 my-app-logs/nginx-access 中 status=500 的日志，按时间倒序返回前 100 条
统计昨天每个 request_uri 的 5xx 错误数 Top 10
```

Project 管理：

```text
列出 cn-hangzhou 下名字以 prod- 开头的 project
帮我在 cn-shanghai 创建一个名为 my-app-logs 的 project，描述为"应用日志归档"
```

Logstore 管理：

```text
在 project my-app-logs 下创建一个名为 nginx-access 的 logstore，保留 30 天，4 个 shard
把 logstore nginx-access 的保留天数从 30 天改成 90 天
```

写入日志：

```text
往 my-app-logs/test-store 写一条 JSON 日志：{"level":"info","msg":"hello"}
```

[文档链接](skills/alibabacloud-sls-cli-guidance/SKILL.md)

## 参与与反馈

欢迎通过 Issue 或 Pull Request 参与贡献。

如有问题或建议，请前往 [GitHub Issues](https://github.com/aliyun/aliyun-sls-agent-skills/issues)。
