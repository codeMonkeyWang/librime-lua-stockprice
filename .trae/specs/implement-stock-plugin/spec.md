# Rime 股票查询插件 Spec

## Why
在 Rime 输入法中集成股票实时行情查询功能。当用户输入的内容匹配到股票名称时，自动获取最新股价和涨跌幅，并将其作为候选词的第二个选项展示，方便用户快速查看。

## What Changes
- 创建 `stock_plugin.lua`，实现 Rime Lua 过滤器（Filter）逻辑。
- 在 `stock_plugin.lua` 中加载并索引 `all_stocks.lua` 数据。
- 调用已有的 `stock_data.lua` 获取实时行情。
- 创建 `rime.lua`，将过滤器注册并导出。
- 实现股价候选词的格式化输出（价格 + 涨跌幅）。

## Impact
- 影响 Rime 输入法的候选词列表，在匹配到股票名称时增加一个行情候选词。
- 依赖网络请求，可能会对打字响应速度产生轻微影响（通过优化和缓存减轻）。

## ADDED Requirements
### Requirement: 股票名称匹配与行情展示
系统应检测候选词列表中的第一个选项。如果该选项是已知的股票名称，则获取行情并在第二个位置插入行情候选词。

#### Scenario: 匹配成功
- **WHEN** 用户输入 `byd`，候选词第一个为 `比亚迪`
- **THEN** 候选词列表变为：
  1. 比亚迪
  2. 93.45  -2.5%

#### Scenario: 格式化展示
- **WHEN** 获取到比亚迪的价格为 93.45，跌幅为 2.5%
- **THEN** 第二个候选词的文本显示为 `93.45  -2.5%`

## MODIFIED Requirements
无

## REMOVED Requirements
无
