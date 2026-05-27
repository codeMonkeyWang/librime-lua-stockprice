# Rime 股票行情插件 (rime-plugin-AH)

这是一个为 Rime 输入法设计的 Lua 插件，能够在输入股票名称时，在候选词列表中实时显示该股票的最新价格及涨跌幅行情。

## 1. 插件简介
- **实时行情**：基于新浪财经 API 获取实时股票数据。
- **多市场支持**：支持 A 股（沪/深/北）、港股及美股。
- **无感集成**：作为 Rime 的 `lua_filter` 集成，不影响正常的打字体验。
- **AH 股支持**：特别优化了 AH 股对照查询（可选）。

## 2. 安装指南
将本项目中的 `rime.lua` 文件和 `lua` 文件夹复制到您的 Rime 用户配置目录（User Data Directory）：
- macOS: `~/Library/Rime/`
- Windows: `%APPDATA%\Rime\`
- Linux: `~/.config/ibus/rime/` 或 `~/.config/fcitx/rime/`

**所需文件：**
- [rime.lua](file:///Users/wangwang/Documents/AIProject/rime-plugin-AH/rime.lua) (若已存在，请合并内容)
- `lua/` 文件夹（包含 `stock_plugin.lua`, `stock_data.lua`, `all_stocks.lua` 等）

## 3. 配置指南
在您的输入方案自定义配置文件中（例如 `luna_pinyin.custom.yaml`），将 `stock_filter` 添加到过滤器列表中：

```yaml
patch:
  engine/filters/+:
    - lua_filter@stock_filter
```

修改完成后，执行 Rime 的 **“重新部署/Deploy”** 操作即可生效。

## 4. 依赖说明
本插件依赖以下系统命令：
- **curl**: 用于发送网络请求获取行情数据。
- **iconv**: 用于处理 API 返回值的编码转换（GBK 转 UTF-8）。

*在 macOS 和大多数 Linux 发行版中，这些工具通常是预装的。*

## 5. 使用示例
在输入法中输入股票名称，行情将紧跟在股票名称候选词之后：

- **输入**：`pingan` 或 `pinganyinhang`
- **候选词列表**：
  1. 平安银行
  2. 12.34  +1.50% [股票]
  3. ...

- **输入**：`biyadi`
- **候选词列表**：
  1. 比亚迪
  2. 268.50  -0.85% [股票]
  3. ...

---
*注：行情显示可能受网络环境影响有轻微延迟（默认超时设置为 1 秒以保证打字流畅）。*
