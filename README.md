# Rime 股票行情插件 (rime-plugin-AH)

这是一个为 Rime 输入法设计的 Lua 插件，能够在输入股票名称时，在候选词列表中实时显示该股票的最新价格及涨跌幅行情。

## 1. 插件特性
- **实时行情**：基于新浪财经 API 获取实时股票数据。
- **多市场支持**：支持 A 股（沪/深/北）、港股及美股。
- **匹配鲁棒性**：自动忽略名称中的空格（如“万  科Ａ”可直接匹配），确保查询准确。
- **性能优化**：
  - 异步感官体验：通过 `curl` 超时控制（1s连接/2s执行），防止网络波动导致输入法卡顿。
  - 智能过滤：仅对首个候选词进行匹配，且仅处理前 20 个候选词，保证长列表下的流畅度。

## 2. 安装指南
将本项目中的 Lua 文件复制到您的 Rime 用户配置目录（User Data Directory）下的 `lua` 文件夹中（如果没有请手动创建）：

**文件同步路径：**
- `lua/stock_plugin.lua` -> `(Rime目录)/lua/stock_plugin.lua`
- `lua/stock_data.lua` -> `(Rime目录)/lua/stock_data.lua`
- `lua/all_stocks.lua` -> `(Rime目录)/lua/all_stocks.lua`
- `rime.lua` -> `(Rime目录)/rime.lua` (若已存在，请将本项目内容合并进去)

## 3. 配置指南
由于不同方案（如朙月拼音、小鹤双拼）可能会覆盖全局过滤器配置，建议为每个使用的方案单独添加补丁。

### 示例 1：为朙月拼音配置
创建或编辑 `luna_pinyin.custom.yaml`：
```yaml
patch:
  "engine/filters/@next": lua_filter@stock_filter
```

### 示例 2：为小鹤双拼配置
创建或编辑 `double_pinyin_flypy.custom.yaml`：
```yaml
patch:
  "engine/filters/@next": lua_filter@stock_filter
```

### 示例 3：全局配置（可能被方案配置覆盖）
编辑 `default.custom.yaml`：
```yaml
patch:
  "engine/filters/@next": lua_filter@stock_filter
```

修改完成后，执行 Rime 的 **“重新部署 / Deploy”** 操作即可生效。

## 4. 依赖说明
本插件依赖以下系统命令（macOS 通常自带）：
- **curl**: 用于发送网络请求。
- **iconv**: 用于处理 API 返回值的编码转换（GBK 转 UTF-8）。

## 5. 使用示例
输入股票名称，行情将紧跟在首个候选词之后：

- **输入**：`pingan`
- **候选词列表**：
  1. 平安银行
  2. 12.34  +1.50% [股票]
  3. ...

- **输入**：`byd`
- **候选词列表**：
  1. 比亚迪
  2. 268.50  -0.85% [股票]
  3. ...

---
*注：本项目中的 `examples/rime_config` 目录下提供了完整的配置示例文件供参考。*
