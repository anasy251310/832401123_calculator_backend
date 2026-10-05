# 后端代码规范

本项目后端代码规范参考 PEP 8。

## 1. 命名规范

- 变量：小写下划线，如 expression、record_id
- 函数：小写下划线，如 calculate_expression
- 常量：全大写，如 DB_PATH
- 类名：大驼峰，如 CalculatorService

## 2. 缩进

- 使用 4 个空格，不使用 Tab。

## 3. 导入

- 标准库、第三方库、本地模块分组，组间空一行。

import sqlite3
import os

from flask import Flask, request, jsonify
from flask_cors import CORS

from calculator import calculate_expression
from database import init_db, save_history

## 4. 函数与注释

- 每个函数用 docstring 说明用途、参数、返回值。

def calculate_expression(expression: str):
    """解析并计算数学表达式。

    Args:
        expression: 数学表达式字符串。

    Returns:
        计算结果，整数或浮点数。

    Raises:
        ValueError: 表达式为空、非法或除零时抛出。
    """

## 5. 字符串

- 统一使用双引号，项目内保持一致。

## 6. 行长度

- 每行不超过 79 个字符。

## 7. 异常处理

- 不使用裸 except，要指明具体异常类型。

try:
    result = calculate_expression(expression)
except ValueError as e:
    return jsonify({"success": False, "message": str(e)}), 400

## 8. 安全

- 禁止使用 eval、exec 执行用户输入。
- 使用 asteval 等安全库解析数学表达式。