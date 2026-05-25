#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例代码 - 包含一些常见问题的代码
"""

import sqlite3
import pickle

# ❌ 硬编码密码
DB_PASSWORD = "admin123"

# ❌ SQL注入风险
def get_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchone()

# ❌ 使用eval
def execute_code(code_str):
    result = eval(code_str)
    return result

# ❌ 嵌套循环
def find_common_elements(list1, list2):
    common = []
    for i in list1:
        for j in list2:
            if i == j:
                common.append(i)
    return common

# ❌ 字符串拼接
def concatenate_strings(strings):
    result = ""
    for s in strings:
        result += s + ", "
    return result

# ❌ pickle加载不可信数据
def load_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

# ✅ 正确的做法
def get_user_safe(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

def concatenate_strings_safe(strings):
    return ", ".join(strings)
