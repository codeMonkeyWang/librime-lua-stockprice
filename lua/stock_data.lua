-- stock_data.lua
-- 通过新浪财经 API 获取股票实时数据
-- 支持 A 股、港股、美股

local stock_data = {}

--- 解析 A 股数据 (沪/深/北)
function stock_data.parse_a_share(data)
    local parts = {}
    for part in string.gmatch(data .. ",", "([^,]*),") do
        table.insert(parts, part)
    end
    if #parts < 4 then return nil end
    
    local name = parts[1]
    local pre_close = tonumber(parts[3]) or 0
    local price = tonumber(parts[4]) or 0
    
    if price == 0 then price = pre_close end
    
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
function stock_data.parse_hk_share(data)
    local parts = {}
    for part in string.gmatch(data .. ",", "([^,]*),") do
        table.insert(parts, part)
    end
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
function stock_data.parse_us_share(data)
    local parts = {}
    for part in string.gmatch(data .. ",", "([^,]*),") do
        table.insert(parts, part)
    end
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
function stock_data.fetch(codes)
    if not codes or #codes == 0 then
        return nil, "Error: No stock codes provided"
    end

    local sanitized_codes = {}
    for _, code in ipairs(codes) do
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
    
    -- 添加超时限制 --connect-timeout 1 -m 2
    local cmd = string.format('curl -s --connect-timeout 1 -m 2 -H "Referer: http://finance.sina.com.cn" "%s" | iconv -f GBK -t UTF-8', url)
    
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
