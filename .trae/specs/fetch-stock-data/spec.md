# 获取股票实时数据 Lua 脚本 Spec

## Why
在 Rime 输入法中集成股票行情查询功能，允许用户通过 Lua 脚本快速获取 A 股、港股及美股的实时价格和涨跌幅数据。

## What Changes
- 创建一个独立的 Lua 脚本 `stock_data.lua`，用于从新浪财经 API 获取股票数据。
- 支持 A 股（沪/深/北）、港股、美股的行情查询。
- 实现解析逻辑，提取价格、涨跌额、涨跌幅等关键信息。
- 提供简单的测试脚本验证功能。

## Impact
- 该脚本可作为 Rime Lua 插件的基础组件，被翻译器（Translator）或其他 Lua 模块调用。

## ADDED Requirements
### Requirement: 股票行情获取
系统应能够根据输入的股票代码列表，通过网络请求获取最新的行情数据。

#### Scenario: 成功获取 A 股数据
- **WHEN** 调用 `fetch_stock_data({"sh600519"})`
- **THEN** 返回包含“贵州茅台”的当前价格、涨跌幅等信息的表格。

#### Scenario: 成功获取多只股票数据
- **WHEN** 调用 `fetch_stock_data({"sh000001", "hk00700", "gb_aapl"})`
- **THEN** 返回包含上证指数、腾讯控股、苹果公司实时数据的列表。

## MODIFIED Requirements
无（新项目）

## REMOVED Requirements
无
