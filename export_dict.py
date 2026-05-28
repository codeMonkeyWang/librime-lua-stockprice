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

def generate_pinyin_variants(name):
    """
    为股票名称生成拼音全拼和简拼
    """
    # 彻底去除名称中的所有空格，并转为半写（处理全角字符）
    clean_name = name.replace(" ", "").replace("　", "")
    # 处理全角 A-Z
    clean_name = clean_name.translate(str.maketrans('ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    
    # 进一步清理用于拼音生成的名称（去除 *ST 等非中文前缀）
    pinyin_name = re.sub(r'[*STst0-9]+', '', clean_name).strip()
    
    if not pinyin_name:
        return "", ""

    # 全拼
    full_pinyin = "".join([i[0] for i in pinyin(pinyin_name, style=Style.NORMAL)])
    # 简拼 (首字母)
    initials = "".join([i[0][0] for i in pinyin(pinyin_name, style=Style.FIRST_LETTER)])
    
    return full_pinyin.lower(), initials.lower()

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

def export_to_dict(stocks, output_path):
    """
    导出为 Rime 扩展词库格式 (luna_pinyin.extended.dict.yaml)
    """
    header = """# Rime dictionary
# encoding: utf-8
#
# 自动生成的股票扩展词库
# 包含基础词库 (luna_pinyin) 和股票数据
# 来源: lua/all_stocks.lua

---
name: luna_pinyin.extended
version: "1.0"
sort: by_weight
use_preset_vocabulary: true
import_tables:
  - luna_pinyin
...

"""
    
    entries = []
    print(f"正在为 {len(stocks)} 个股票生成词库条目...")
    
    for stock in stocks:
        name = stock['name']
        code = stock['code']
        
        # 1. 原始名称与代码的映射 (支持直接输入代码)
        # 去除代码中的市场前缀 (如 sz000001 -> 000001)
        pure_code = re.sub(r'^[a-z]+', '', code)
        
        # 2. 生成拼音
        full, initials = generate_pinyin_variants(name)
        
        # 写入词库： 词语 <tab> 编码
        # 我们为同一个股票提供多种触发方式
        if initials:
            entries.append(f"{name}\t{initials}")
        if full:
            entries.append(f"{name}\t{full}")
        
        # 同时也允许直接输入代码触发
        entries.append(f"{name}\t{pure_code}")
        # 以及带市场前缀的代码
        entries.append(f"{name}\t{code}")

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
    lua_file = 'lua/all_stocks.lua'
    dict_file = 'luna_pinyin.extended.dict.yaml'
    
    print(f"开始导出: {lua_file} -> {dict_file}")
    
    stocks = parse_lua_file(lua_file)
    if not stocks:
        print("未发现任何股票数据。")
        return

    export_to_dict(stocks, dict_file)
    print(f"成功! 已生成词库文件: {dict_file}")
    print("提示: 请将该文件放入 Rime 用户目录，并在方案中引用它。")

if __name__ == "__main__":
    main()
