# alibabacloud-sls-query Installation

How to install and load the `alibabacloud-sls-query` skill when it is not already available.

## Install

```bash
# Global install (recommended)
npx skills add aliyun/alibabacloud-aiops-skills \
  --skill alibabacloud-sls-query \
  -g -y --full-depth
```

```bash
# Project-level install
npx skills add aliyun/alibabacloud-aiops-skills \
  --skill alibabacloud-sls-query \
  -y --full-depth
```

## Load in current session

Some agents cannot auto-load a newly installed skill without a restart. After installation, explicitly locate and read the installed `alibabacloud-sls-query/SKILL.md` completely to ensure the skill's workflow is loaded in the current session, then follow that workflow to complete the user's task.
