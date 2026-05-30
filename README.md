# librime-lua-stockprice: Rime 股票行情插件

这是一个为 Rime 输入法设计的 Lua 插件，能够在输入股票名称时，在候选词列表中实时显示该股票的最新价格及涨跌幅行情。

## 0. 快速开始
如果您还没有本项目，可以通过以下命令获取：
```bash
git clone git@github.com:codeMonkeyWang/librime-lua-stockprice.git
cd librime-lua-stockprice
```

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

## 4. 词库导出与搜索增强
为了能通过拼音或代码快速搜索到股票，建议生成专门的 Rime 词库文件。

### 导出词库
本项目提供了一个 Python 脚本，可以将 `lua/all_stocks.lua` 中的数据一键导出为包含基础词库的扩展词库文件。

1. **安装依赖**：
   ```bash
   pip install -r scripts/requirements.txt
   ```
2. **执行导出**：
   ```bash
   python scripts/export_dict.py
   ```
   执行后将自动生成以下两个文件：
   - `luna_pinyin.extended.dict.yaml`：适用于全拼方案。
   - `double_pinyin_flypy.extended.dict.yaml`：适用于小鹤双拼方案。

### 配置词库
为了不破坏您原有的输入法词库，该脚本生成的词库已自动配置为 **“扩展词库”** 模式，并自动包含了基础词库（`import_tables: [luna_pinyin]`）。

#### 1. 部署扩展词库文件
将生成的对应词库文件复制到 Rime 用户配置目录。
- **全拼用户**：复制 `luna_pinyin.extended.dict.yaml`。
- **小鹤双拼用户**：复制 `double_pinyin_flypy.extended.dict.yaml`。

#### 2. 在方案补丁中引用
修改您的方案补丁文件（如 `luna_pinyin.custom.yaml` 或 `double_pinyin_flypy.custom.yaml`）：

```yaml
patch:
  # 注册过滤器以显示行情
  "engine/filters/@next": lua_filter@stock_filter
  # 切换到对应的扩展词库
  "translator/dictionary": luna_pinyin.extended  # 小鹤双拼用户改为 double_pinyin_flypy.extended
```

## 5. 依赖说明
本插件依赖以下工具：
- **curl**: 用于发送网络请求。
- **iconv**: 用于处理 API 返回值的编码转换（GBK 转 UTF-8）。
- **Python 3**: 用于执行数据抓取和词库导出脚本。
- **pypinyin (Python库)**: 用于生成股票名称的拼音。

## 6. 使用示例
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

## 7. 更新日志

- **2026-05-30**: 优化小鹤双拼导出逻辑，仅当双拼编码长度大于 4 位（3字词及以上）时生成去末位兼容项，显著减少 2 字词的拼音冲突。
- **2026-05-29**: 优化导出脚本，支持清理名称末尾的 A/B 标识，改进优先匹配逻辑。
- **2026-05-28**: 项目结构重构，将所有 Python 脚本迁移至 `scripts` 目录。
- **2026-05-25**: 新增小鹤双拼方案支持，同步更新导出脚本与配置文档。
- **2026-05-20**: 新增股票词库导出工具，支持一键生成 Rime 扩展词库。
- **2026-05-15**: 优化插件显示效果，提供完整的 `examples` 配置示例。
- **2026-05-10**: 项目初始化，实现基于新浪财经 API 的实时股票行情查询功能。

---
*注：本项目中的 `examples/rime_config` 目录下提供了完整的配置示例文件供参考。*
