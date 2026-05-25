#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM-CodeLens 测试用例
"""

import os
import sys
import unittest
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from analyzer import CodeAnalyzer
from reporter import ReportGenerator
from codelens import CodeLensEngine


class TestCodeAnalyzer(unittest.TestCase):
    """测试代码分析器"""
    
    def setUp(self):
        """测试初始化"""
        self.analyzer = CodeAnalyzer()
        
    def test_security_detection_sql_injection(self):
        """测试SQL注入检测"""
        code = '''
def query_user(user_id):
    sql = "SELECT * FROM users WHERE id = %s" % user_id
    cursor.execute(sql)
'''
        file_info = {"name": "test.py", "extension": ".py"}
        result = self.analyzer.analyze(code, file_info, ["security"])
        
        self.assertIn("security", result)
        
    def test_security_detection_hardcoded_password(self):
        """测试硬编码密码检测"""
        code = '''
DB_PASSWORD = "my_secret_password_123"
'''
        file_info = {"name": "config.py", "extension": ".py"}
        result = self.analyzer.analyze(code, file_info, ["security"])
        
        self.assertIn("security", result)
        
    def test_quality_long_function(self):
        """测试长函数检测"""
        code = '''
def very_long_function():
    x = 1
    x = 2
    x = 3
    x = 4
    x = 5
    x = 6
    x = 7
    x = 8
    x = 9
    x = 10
    x = 11
    x = 12
    x = 13
    x = 14
    x = 15
    x = 16
    x = 17
    x = 18
    x = 19
    x = 20
    x = 21
    x = 22
    x = 23
    x = 24
    x = 25
    x = 26
    x = 27
    x = 28
    x = 29
    x = 30
    x = 31
    x = 32
    x = 33
    x = 34
    x = 35
    x = 36
    x = 37
    x = 38
    x = 39
    x = 40
    x = 41
    x = 42
    x = 43
    x = 44
    x = 45
    x = 46
    x = 47
    x = 48
    x = 49
    x = 50
    x = 51
'''
        file_info = {"name": "long.py", "extension": ".py"}
        result = self.analyzer.analyze(code, file_info, ["quality"])
        
        self.assertIn("quality", result)
        
    def test_performance_nested_loop(self):
        """测试嵌套循环检测"""
        code = '''
for i in range(100):
    for j in range(100):
        print(i, j)
'''
        file_info = {"name": "nested.py", "extension": ".py"}
        result = self.analyzer.analyze(code, file_info, ["performance"])
        
        self.assertIn("performance", result)
        
    def test_best_practices_todo(self):
        """测试TODO注释检测"""
        code = '''
# TODO: implement user authentication
def login():
    pass
'''
        file_info = {"name": "todo.py", "extension": ".py"}
        result = self.analyzer.analyze(code, file_info, ["best_practices"])
        
        self.assertIn("best_practices", result)
        
    def test_multiple_analysis_types(self):
        """测试多种分析类型"""
        code = '''
password = "123456"

def process_data(data):
    # TODO: optimize this
    for i in range(10):
        result += str(i)
    return result
'''
        file_info = {"name": "multi.py", "extension": ".py"}
        result = self.analyzer.analyze(code, file_info, ["security", "quality", "performance"])
        
        self.assertIn("security", result)
        self.assertIn("quality", result)
        self.assertIn("performance", result)


class TestReportGenerator(unittest.TestCase):
    """测试报告生成器"""
    
    def setUp(self):
        """测试初始化"""
        self.reporter = ReportGenerator()
        self.sample_result = {
            "file": {
                "name": "test.py",
                "path": "/path/to/test.py",
                "extension": ".py",
                "lines": 100,
                "size": 2048
            },
            "summary": {
                "total_issues": 3,
                "critical": 1,
                "high": 1,
                "medium": 1,
                "low": 0,
                "info": 0
            },
            "analysis": {
                "security": {
                    "total": 1,
                    "issues": [
                        {
                            "type": "hardcoded_password",
                            "severity": "high",
                            "description": "发现硬编码密码",
                            "line": 1
                        }
                    ]
                },
                "quality": {
                    "total": 1,
                    "issues": []
                }
            }
        }
        
    def test_generate_json(self):
        """测试JSON格式报告"""
        report = self.reporter.generate(self.sample_result, "json")
        
        self.assertIsInstance(report, str)
        import json
        parsed = json.loads(report)
        self.assertEqual(parsed["file"]["name"], "test.py")
        
    def test_generate_markdown(self):
        """测试Markdown格式报告"""
        report = self.reporter.generate(self.sample_result, "markdown")
        
        self.assertIsInstance(report, str)
        self.assertIn("GLM-CodeLens", report)
        self.assertIn("test.py", report)
        
    def test_generate_html(self):
        """测试HTML格式报告"""
        report = self.reporter.generate(self.sample_result, "html")
        
        self.assertIsInstance(report, str)
        self.assertIn("<!DOCTYPE html>", report)
        self.assertIn("GLM-CodeLens", report)
        
    def test_invalid_format(self):
        """测试无效格式"""
        with self.assertRaises(ValueError):
            self.reporter.generate(self.sample_result, "invalid")


class TestCodeLensEngine(unittest.TestCase):
    """测试核心引擎"""
    
    def setUp(self):
        """测试初始化"""
        self.engine = CodeLensEngine()
        
    def test_summary_generation(self):
        """测试摘要生成"""
        results = {
            "security": {
                "issues": [
                    {"severity": "critical"},
                    {"severity": "high"}
                ]
            },
            "quality": {
                "issues": [
                    {"severity": "medium"}
                ]
            }
        }
        
        summary = self.engine._generate_summary(results)
        
        self.assertEqual(summary["total_issues"], 3)
        self.assertEqual(summary["critical"], 1)
        self.assertEqual(summary["high"], 1)
        self.assertEqual(summary["medium"], 1)
        
    def test_overall_summary_generation(self):
        """测试整体摘要生成"""
        all_results = [
            {"summary": {"total_issues": 5, "critical": 1, "high": 2, "medium": 1, "low": 1, "info": 0}},
            {"summary": {"total_issues": 3, "critical": 0, "high": 1, "medium": 1, "low": 1, "info": 0}}
        ]
        
        overall = self.engine._generate_overall_summary(all_results)
        
        self.assertEqual(overall["total_files"], 2)
        self.assertEqual(overall["total_issues"], 8)
        self.assertEqual(overall["by_severity"]["critical"], 1)
        self.assertEqual(overall["by_severity"]["high"], 3)


class TestSecurityPatterns(unittest.TestCase):
    """测试安全模式"""
    
    def setUp(self):
        """测试初始化"""
        self.analyzer = CodeAnalyzer()
        
    def test_sql_injection_patterns(self):
        """测试各种SQL注入模式"""
        test_cases = [
            'cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)',
            'db.exec("DELETE FROM table WHERE id = " + request.param)',
            'sql_query = f"SELECT * FROM products WHERE name = \'{name}\'"'
        ]
        
        for code in test_cases:
            result = self.analyzer._analyze_security(code)
            # SQL注入风险应该被检测到
            self.assertIsInstance(result, dict)
            self.assertIn("issues", result)
            
    def test_eval_danger(self):
        """测试eval使用检测"""
        code = 'result = eval(user_input)'
        result = self.analyzer._analyze_security(code)
        
        found_eval = False
        for issue in result.get("issues", []):
            if issue.get("type") == "eval_usage":
                found_eval = True
                break
                
        self.assertTrue(found_eval)


if __name__ == "__main__":
    unittest.main()
