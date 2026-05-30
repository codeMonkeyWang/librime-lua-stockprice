#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys

try:
    from pypinyin import pinyin, Style
except ImportError:
    print("错误: 请先安装 pypinyin 库 (pip install pypinyin)")
    sys.exit(1)

# 小鹤双拼映射表
FLYPY_INITIALS = {'zh': 'v', 'ch': 'i', 'sh': 'u'}
FLYPY_FINALS = {
    'iu': 'q', 'ei': 'w', 'uan': 'r', 'ue': 't', 've': 't', 'un': 'y', 'uo': 'o', 'ie': 'p',
    'ong': 's', 'iong': 's', 'ai': 'd', 'en': 'f', 'eng': 'g', 'ang': 'h', 'an': 'j',
    'ing': 'k', 'uai': 'k', 'iang': 'l', 'uang': 'l', 'ou': 'z', 'ia': 'x', 'ua': 'x',
    'ao': 'c', 'ui': 'v', 'in': 'b', 'iao': 'n', 'ian': 'm', 'ü': 'v', 'v': 'v'
}
FLYPY_ZERO_INITIALS = {
    'a': 'aa', 'ai': 'ai', 'an': 'an', 'ang': 'ah', 'ao': 'ao',
    'e': 'ee', 'ei': 'ei', 'en': 'en', 'eng': 'eg', 'er': 'er',
    'o': 'oo', 'ou': 'ou'
}

def pinyin_to_flypy(pinyin_list):
    """
    将全拼列表转换为小鹤双拼编码
    """
    res = []
    for s in pinyin_list:
        if s in FLYPY_ZERO_INITIALS:
            res.append(FLYPY_ZERO_INITIALS[s])
            continue
        
        initial = ""
        # 匹配声母
        for i in ['zh', 'ch', 'sh', 'b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x', 'r', 'z', 'c', 's', 'y', 'w']:
            if s.startswith(i):
                initial = i
                break
        
        final = s[len(initial):]
        if not initial:
            res.append(s)
            continue
            
        code_i = FLYPY_INITIALS.get(initial, initial[0])
        # 处理 ü 的特殊情况
        if final == 'ü': final = 'v'
        code_f = FLYPY_FINALS.get(final, final)
        res.append(code_i + code_f)
    return "".join(res)

def generate_pinyin_variants(name, mode='full'):
    """
    为股票名称生成拼音变体
    mode: 'full' (全拼) 或 'flypy' (小鹤双拼)
    """
    # 彻底去除名称中的所有空格，并转为半写（处理全角字符）
    clean_name = name.replace(" ", "").replace("　", "")
    # 处理全角 A-Z
    clean_name = clean_name.translate(str.maketrans('ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    
    # 进一步清理用于拼音生成的名称（去除 *ST 等非中文前缀，以及末尾的 A/B）
    pinyin_name = re.sub(r'[*STst0-9]+', '', clean_name)
    pinyin_name = re.sub(r'[ABab]$', '', pinyin_name).strip()
    
    if not pinyin_name:
        return "", ""

    # 获取全拼列表
    py_list = [i[0] for i in pinyin(pinyin_name, style=Style.NORMAL)]
    
    initials = "".join([i[0][0] for i in pinyin(pinyin_name, style=Style.FIRST_LETTER)])
    
    if mode == 'flypy':
        full = pinyin_to_flypy(py_list)
    else:
        full = "".join(py_list)
    
    return full.lower(), initials.lower()

def parse_lua_file(file_path):
    """
    解析 lua/all_stocks.lua 文件提取股票名称和代码
    """
    stocks = []
    if not os.path.exists(file_path):
        print(f"错误: 找不到文件 {file_path}")
        return stocks

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则匹配 { name = "...", code = "..." } 或 { name = '...', code = '...' }
    pattern = r'\{\s*name\s*=\s*["\'](.*?)["\']\s*,\s*code\s*=\s*["\'](.*?)["\']'
    matches = re.findall(pattern, content)
    
    for name, code in matches:
        stocks.append({'name': name, 'code': code})
    
    return stocks

def export_to_dict(stocks, output_path, dict_name, base_table, mode='full'):
    """
    导出为 Rime 扩展词库格式
    """
    header = f"""# Rime dictionary
# encoding: utf-8
#
# 自动生成的股票扩展词库 ({mode})
# 包含基础词库 ({base_table}) 和股票数据
# 来源: lua/all_stocks.lua

---
name: {dict_name}
version: "1.0"
sort: by_weight
use_preset_vocabulary: true
import_tables:
  - {base_table}
...

"""
    
    entries = []
    print(f"正在为 {len(stocks)} 个股票生成词库条目 ({mode})...")
    
    for stock in stocks:
        name = stock['name']
        code = stock['code']
        
        # 生成拼音变体
        full, initials = generate_pinyin_variants(name, mode=mode)
        
        # 使用高权重确保匹配项排在第一位
        weight = "1000000"
        
        if mode == 'flypy':
            # 小鹤双拼模式：保留双拼全码
            # 只有当编码长度大于 4 位（3字词及以上）时，才生成“去末位”的兼容项
            # 1-2字词（<=4位）去末位容易造成冲突，故跳过
            if full:
                entries.append(f"{name}\t{full}\t{weight}")
                if len(full) > 4:
                    entries.append(f"{name}\t{full[:-1]}\t{weight}")
        else:
            # 全拼模式：只保留简拼和全拼
            if initials:
                entries.append(f"{name}\t{initials}\t{weight}")
            if full:
                entries.append(f"{name}\t{full}\t{weight}")

    # 去重并保持顺序
    seen = set()
    unique_entries = []
    for e in entries:
        if e not in seen:
            unique_entries.append(e)
            seen.add(e)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write("\n".join(unique_entries))
        f.write("\n")

def main():
    # 获取项目根目录
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lua_file = os.path.join(base_dir, 'lua', 'all_stocks.lua')
    
    stocks = parse_lua_file(lua_file)
    if not stocks:
        print("未发现任何股票数据。")
        return

    # 1. 导出全拼扩展词库
    luna_dict = os.path.join(base_dir, 'luna_pinyin.extended.dict.yaml')
    export_to_dict(stocks, luna_dict, 'luna_pinyin.extended', 'luna_pinyin', mode='full')
    print(f"成功! 已生成全拼词库文件: {luna_dict}")

    # 2. 导出小鹤双拼扩展词库
    flypy_dict = os.path.join(base_dir, 'double_pinyin_flypy.extended.dict.yaml')
    export_to_dict(stocks, flypy_dict, 'double_pinyin_flypy.extended', 'luna_pinyin', mode='flypy')
    print(f"成功! 已生成小鹤双拼词库文件: {flypy_dict}")

    print("\n提示: 请将生成的 .dict.yaml 文件放入 Rime 用户目录，并在方案中引用它们。")

if __name__ == "__main__":
    main()
