
# 阿里云 SLS Agent Skills

[English](README.md) | 简体中文

[阿里云 SLS（日志服务）](https://help.aliyun.com/zh/sls/) 是智能化云原生观测与分析平台，提供数据采集、加工、查询与分析、可视化、告警、消费与投递等功能。

本仓库提供面向 **阿里云 SLS** 的 SLS Agent Skills，旨在提供智能化的 SLS 运维管控方案。SLS Agent Skills 面向 SLS 典型运维与开发场景设计，使 AI 助手能够基于 Aliyun CLI 规范、可靠地完成项目与 Logstore 管理、日志查询等操作。

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## SLS Agent Skills

### alibabacloud-sls-cli-guidance

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

> aliyun CLI 和 SLS 插件的安装方法已在 Skill 中说明，安装 Skill 后，Agent 会自动检查环境并安装相应依赖。如需手动安装请使用：
>
> ```bash
> sudo /bin/bash -c "$(curl -fsSL https://aliyuncli.alicdn.com/install.sh)"
> aliyun plugin install --names sls
> ```

[文档链接](skills/alibabacloud-sls-cli-guidance/SKILL.md)

## 安装

通过 [`npx skills`](https://skills.sh) 安装：

```bash
npx skills add alibabacloud-sls-cli-guidance -g
```

同时推荐安装 **alibabacloud-sls-query**，提供更强大的 SLS 日志查询能力：

```bash
npx skills add aliyun/alibabacloud-aiops-skills \
  --skill alibabacloud-sls-query \
  -g --full-depth
```

## 参与与反馈

欢迎通过 Issue 或 Pull Request 参与贡献。

如有问题或建议，请前往 [GitHub Issues](https://github.com/aliyun/aliyun-sls-agent-skills/issues)。
