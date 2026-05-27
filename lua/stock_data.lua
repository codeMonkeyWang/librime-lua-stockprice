-- stock_data.lua
-- 参考 leek-fund 逻辑，通过新浪财经 API 获取股票实时数据
-- 支持 A 股、港股、美股

local stock_data = {}

--- 解析 A 股数据 (沪/深/北)
--- @param data string 新浪 API 返回的逗号分隔字符串
--- @return table|nil 包含名称、价格、涨跌额、涨跌幅的表格
function stock_data.parse_a_share(data)
    local parts = {}
    for part in string.gmatch(data .. ",", "([^,]*),") do
        table.insert(parts, part)
    end
    -- A 股格式: 名字, 开盘, 昨收, 现价, 最高, 最低...
    if #parts < 4 then return nil end
    
    local name = parts[1]
    local pre_close = tonumber(parts[3]) or 0
    local price = tonumber(parts[4]) or 0
    
    if price == 0 then price = pre_close end -- 处理停牌
    
    local change = price - pre_close
    local percent = (pre_close > 0) and (change / pre_close * 100) or 0
    
    return {
        name = name,
        price = price,
        change = change,
        percent = percent,
        market = "A"
    }
end

--- 解析港股数据
--- @param data string 新浪 API 返回的逗号分隔字符串
function stock_data.parse_hk_share(data)
    local parts = {}
    for part in string.gmatch(data .. ",", "([^,]*),") do
        table.insert(parts, part)
    end
    -- 港股格式: 英文名, 中文名, 开盘, 昨收, 最高, 最低, 现价, 涨跌额, 涨跌幅...
    if #parts < 9 then return nil end
    
    local name = parts[2]
    local price = tonumber(parts[7]) or 0
    local change = tonumber(parts[8]) or 0
    local percent = tonumber(parts[9]) or 0
    
    return {
        name = name,
        price = price,
        change = change,
        percent = percent,
        market = "HK"
    }
end

--- 解析美股数据
--- @param data string 新浪 API 返回的逗号分隔字符串
function stock_data.parse_us_share(data)
    local parts = {}
    for part in string.gmatch(data .. ",", "([^,]*),") do
        table.insert(parts, part)
    end
    -- 美股格式: 名字, 现价, 涨跌幅, 时间, 涨跌额, 开盘, 最高, 最低...
    if #parts < 5 then return nil end
    
    local name = parts[1]
    local price = tonumber(parts[2]) or 0
    local percent = tonumber(parts[3]) or 0
    local change = tonumber(parts[5]) or 0
    
    return {
        name = name,
        price = price,
        change = change,
        percent = percent,
        market = "US"
    }
end

--- 获取股票实时数据
--- @param codes table 股票代码列表，如 {"sh600519", "hk00700", "gb_aapl"}
--- @return table|nil, string|nil 返回结果列表或错误信息
function stock_data.fetch(codes)
    if not codes or #codes == 0 then
        return nil, "Error: No stock codes provided"
    end

    local sanitized_codes = {}
    for _, code in ipairs(codes) do
        -- 只允许字母、数字和下划线，防止 shell 注入
        local sanitized = code:match("^([%w_]+)$")
        if sanitized then
            table.insert(sanitized_codes, sanitized)
        end
    end

    if #sanitized_codes == 0 then
        return nil, "Error: No valid stock codes provided"
    end

    local code_list = table.concat(sanitized_codes, ",")
    local url = "http://hq.sinajs.cn/list=" .. code_list
    
    -- 使用 curl 获取数据，并通过 iconv 转换为 UTF-8
    -- Sina API 必须包含 Referer 头部以避免 403
    local cmd = string.format('curl -s -H "Referer: http://finance.sina.com.cn" "%s" | iconv -f GBK -t UTF-8', url)
    
    local f = io.popen(cmd)
    if not f then
        return nil, "Error: Failed to execute curl"
    end
    
    local res = f:read("*all")
    f:close()

    if not res or res == "" then
        return nil, "Error: Empty response from API"
    end

    local results = {}
    -- 正则匹配 var hq_str_xxx="..."
    for code, data in string.gmatch(res, "var hq_str_([%w_]+)=\"([^\"]+)\";") do
        local info = nil
        if code:find("^sh") or code:find("^sz") or code:find("^bj") then
            info = stock_data.parse_a_share(data)
        elseif code:find("^hk") then
            info = stock_data.parse_hk_share(data)
        elseif code:find("^gb_") then
            info = stock_data.parse_us_share(data)
        end

        if info then
            info.code = code
            table.insert(results, info)
        end
    end

    return results
end

return stock_data
