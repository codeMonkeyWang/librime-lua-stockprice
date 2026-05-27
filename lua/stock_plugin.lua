-- stock_plugin.lua
local stock_data = require("lua/stock_data")

local stock_plugin = {}
local stock_index = {}

-- 加载股票索引
local function init_index()
    -- 使用 pcall 避免加载失败导致插件崩溃
    local status, stocks = pcall(require, "lua/all_stocks")
    if status and type(stocks) == "table" then
        for _, stock in ipairs(stocks) do
            stock_index[stock.name] = stock.code
        end
    end
end

init_index()

--- 股票行情过滤器
--- @param input Translation
--- @param env Environment
function stock_plugin.stock_filter(input, env)
    local count = 0
    local first_cand = nil
    local stock_cand = nil

    for cand in input:iter() do
        count = count + 1
        
        -- 识别第一个候选词是否为股票名称
        if count == 1 then
            local code = stock_index[cand.text]
            if code then
                local results = stock_data.fetch({code})
                if results and #results > 0 then
                    local data = results[1]
                    local sign = data.percent > 0 and "+" or ""
                    -- 格式：价格  涨跌幅 (例如：93.45  -2.5%)
                    local info = string.format("%.2f  %s%.2f%%", data.price, sign, data.percent)
                    
                    -- 创建行情候选词，显示在第 2 位
                    stock_cand = Candidate("stock", cand.start, cand._end, info, " [股票]")
                end
            end
            yield(cand)
            -- 如果有股票行情，紧接着 yield
            if stock_cand then
                yield(stock_cand)
            end
        else
            -- 其他候选词原样输出
            yield(cand)
        end
    end
end

return stock_plugin
