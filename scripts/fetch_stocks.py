import tushare as ts
import os
import pandas as pd
from dotenv import load_dotenv

# 获取项目根目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)

def format_code(ts_code):
    """
    将 Tushare 的代码格式 (000001.SZ) 转换为 Rime 插件常用的格式 (sz000001)
    """
    if not ts_code or '.' not in ts_code:
        return ts_code
    
    code, exchange = ts_code.split('.')
    exchange = exchange.lower()
    
    # 港股处理: 00700.HK -> hk00700
    if exchange == 'hk':
        return f"hk{code.zfill(5)}"
    # A 股处理: 600519.SH -> sh600519
    return f"{exchange}{code}"

def fetch_all_stocks():
    # 从环境变量获取 token
    token = os.getenv('')
    if not token:
        print("错误: 请在 .env 文件中设置 TUSHARE_TOKEN (可以参考 .env.example)")
        return None

    # 初始化 tushare
    ts.set_token(token)
    pro = ts.pro_api()

    print("正在从 Tushare 获取 A 股股票列表 (上海、深圳、科创板、创业板)...")
    try:
        # 分开获取上交所和深交所数据，确保不会触发 6000 行的单次提取限制
        df_sse = pro.stock_basic(exchange='SSE', list_status='L', fields='ts_code,symbol,name,market,exchange,list_date')
        df_szse = pro.stock_basic(exchange='SZSE', list_status='L', fields='ts_code,symbol,name,market,exchange,list_date')
        
        df_a = pd.concat([df_sse, df_szse], ignore_index=True)
        print(f"--- 获取 A 股完成: {len(df_a)} 条 ---")
    except Exception as e:
        print(f"获取 A 股数据失败: {e}")
        df_a = pd.DataFrame()

    print("正在获取港股股票列表...")
    try:
        # 尝试多种方式获取港股列表
        # 1. 标准 pro 调用 (带 fields)
        df_hk = pro.hk_basic(list_status='L', fields='ts_code,name,market,list_date')
        
        # 2. 如果返回为空，尝试不带 fields 的 query 方式
        if df_hk is None or df_hk.empty:
            print("警告: hk_basic (带 fields) 返回为空，尝试最简 query 接口...")
            df_hk = pro.query('hk_basic')
            
        if df_hk is not None and not df_hk.empty:
            print(f"--- 获取港股完成: {len(df_hk)} 条 ---")
            # 港股接口输出参数中没有 symbol，通常 ts_code 就是 symbol (如 00001.HK)
            df_hk['symbol'] = df_hk['ts_code'].str.split('.').str[0]
            df_hk['exchange'] = 'HK'
            # 确保字段存在
            if 'market' not in df_hk.columns:
                df_hk['market'] = 'HK'
        else:
            print("错误: 港股数据获取结果为空。")
            print("原因分析:")
            print("1. 积分不足: 港股列表 (hk_basic) 通常需要 2000 积分。")
            print("2. 账户权限: 请登录 tushare.pro 确认您的账户是否有港股数据权限。")
            df_hk = pd.DataFrame()
            
    except Exception as e:
        print(f"获取港股数据时发生异常: {e}")
        print("提示: 港股接口权限可能高于 A 股接口，请确认您的权限等级。")
        df_hk = pd.DataFrame()

    # 合并数据
    df_all = pd.concat([df_a, df_hk], ignore_index=True)
    return df_all

def to_lua_table(df):
    if df is None or df.empty:
        return "return {}"

    lua_lines = [
        "-- 股票列表数据",
        "-- 包含：上海、深圳、科创板、创业板、港股",
        "-- 格式：{ name = '名称', code = '代码', market = '市场' }",
        "return {"
    ]
    
    for _, row in df.iterrows():
        # 转义 Lua 字符串中的特殊字符
        name = str(row['name']).replace("'", "\\'")
        # 转换为插件通用代码格式 (如 sh600519, hk00700)
        code = format_code(str(row['ts_code']))
        market = str(row['market'])
        
        line = f"  {{ name = '{name}', code = '{code}', market = '{market}' }},"
        lua_lines.append(line)
    
    lua_lines.append("}")
    return "\n".join(lua_lines)

def main():
    df = fetch_all_stocks()
    if df is not None and not df.empty:
        print(f"成功合并共计 {len(df)} 条股票数据")
        
        # 按代码排序，方便查看
        df = df.sort_values('ts_code')
        
        lua_table = to_lua_table(df)
        
        output_file = os.path.join(base_dir, 'lua', 'all_stocks.lua')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(lua_table)
        
        print(f"数据已成功保存至 {output_file}")
    else:
        print("未获取到有效数据，请检查 Token 或积分是否足够。")

if __name__ == "__main__":
    main()
