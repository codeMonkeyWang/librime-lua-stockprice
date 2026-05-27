-- test_stock.lua
local stock_data = require("stock_data")

local codes = {"sh600519", "hk00700", "gb_aapl"}
print("Fetching data for: " .. table.concat(codes, ", "))

local results, err = stock_data.fetch(codes)

if err then
    print("Error: " .. err)
    os.exit(1)
end

if results then
    for _, item in ipairs(results) do
        print(string.format("[%s] %s (%s):", item.market, item.name, item.code))
        print(string.format("  Price: %.2f", item.price))
        print(string.format("  Change: %.2f", item.change))
        print(string.format("  Percent: %.2f%%", item.percent))
        print("--------------------")
    end
else
    print("No results found.")
end
