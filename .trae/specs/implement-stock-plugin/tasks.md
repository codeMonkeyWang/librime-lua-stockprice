# Tasks
- [x] Task 1: 准备股票名称索引
  - [x] SubTask 1.1: 在 `stock_plugin.lua` 中实现加载 `all_stocks.lua` 的逻辑。
  - [x] SubTask 1.2: 构建一个从 `name` 到 `code` 的高效查找映射表。
- [x] Task 2: 实现 Rime Lua 过滤器逻辑
  - [x] SubTask 2.1: 编写 `stock_filter` 函数，遍历候选词流。
  - [x] SubTask 2.2: 识别第一个候选词是否为股票名称。
  - [x] SubTask 2.3: 调用 `stock_data.fetch` 获取实时数据，并处理网络延迟/错误。
  - [x] SubTask 2.4: 格式化行情字符串，并使用 `Candidate` 对象插入到第二个位置。
- [x] Task 3: 注册并导出插件
  - [x] SubTask 3.1: 创建 `rime.lua` 文件。
  - [x] SubTask 3.2: 在 `rime.lua` 中导出 `stock_filter`。
- [x] Task 4: 验证与测试
  - [x] SubTask 4.1: 编写简单的 Lua 测试脚本验证 `stock_plugin.lua` 的逻辑（模拟 Rime 环境）。
  - [x] SubTask 4.2: 确保在没有匹配到股票时，候选词列表不受影响。

# Task Dependencies
- Task 2 依赖于 Task 1。
- Task 3 依赖于 Task 2。
- Task 4 依赖于所有任务。
