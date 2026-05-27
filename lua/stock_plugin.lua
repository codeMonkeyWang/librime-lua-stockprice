-- stock_plugin.lua
local stock_data = require("stock_data")

local stock_plugin = {}
local stock_index = {}

-- 加载股票索引
local function init_index()
    local status, stocks = pcall(require, "all_stocks")
    if status and type(stocks) == "table" then
        for _, stock in ipairs(stocks) do
            -- 去除可能的空格，确保匹配鲁棒性
            local name = stock.name:gsub("%s+", "")
            stock_index[name] = stock.code
        end
    end
end

init_index()

--- 股票行情过滤器
function stock_plugin.stock_filter(input, env)
    local count = 0
    local stock_cand = nil

    for cand in input:iter() do
        count = count + 1
        
        -- 仅匹配第一个候选词
        if count == 1 then
            -- 同时也去除候选词文本中的空格进行匹配
            local clean_text = cand.text:gsub("%s+", "")
            local code = stock_index[clean_text]
            
            if code then
                local status, results = pcall(stock_data.fetch, {code})
                if status and results and #results > 0 then
                    local data = results[1]
                    local sign = data.percent > 0 and "+" or ""
                    local info = string.format("%.2f  %s%.2f%%", data.price, sign, data.percent)
                    
                    -- 创建行情候选词
                    stock_cand = Candidate("stock", cand.start, cand._end, info, " [股票]")
                end
            end
            
            yield(cand)
            if stock_cand then
                yield(stock_cand)
            end
        else
            yield(cand)
        end
        
        -- 性能优化：处理完前 20 个候选词后停止介入，避免长列表卡顿
        if count > 20 then
            for rest in input:iter() do
                yield(rest)
            end
            break
        end
    end
end

return stock_plugin
