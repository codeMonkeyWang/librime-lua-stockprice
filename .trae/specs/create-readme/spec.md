# 创建项目使用文档 Spec

## Why
为项目提供清晰的使用说明文档，帮助用户了解插件功能、安装步骤及配置方法。

## What Changes
- 在项目根目录下创建 `README.md` 文件。

## Impact
- 无代码逻辑影响，仅提供文档支持。

## ADDED Requirements
### Requirement: 完善的使用说明
README 必须包含以下内容：
1. 项目简介：描述 Rime 股票查询插件的功能。
2. 安装步骤：说明如何将 Lua 文件放入 Rime 配置目录。
3. 配置说明：指导用户如何在 `.schema.yaml` 中启用 `lua_filter`。
4. 依赖说明：提到系统需要安装 `curl` 命令行工具。
5. 使用示例：展示输入股票名称后的预期效果。

## MODIFIED Requirements
无

## REMOVED Requirements
无
