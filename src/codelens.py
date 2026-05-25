#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM-CodeLens - 基于GLM-5.1的智能代码分析引擎
零依赖的CLI工具，提供代码质量分析、安全漏洞检测、性能优化建议
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# 处理相对导入
try:
    from .analyzer import CodeAnalyzer
    from .reporter import ReportGenerator
except ImportError:
    from analyzer import CodeAnalyzer
    from reporter import ReportGenerator


class CodeLensEngine:
    """GLM-CodeLens 核心引擎"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "glm-5"):
        """
        初始化代码分析引擎
        
        Args:
            api_key: GLM API密钥，如果为None则从环境变量读取
            model: 使用的模型名称
        """
        self.api_key = api_key or os.environ.get("GLM_API_KEY")
        self.model = model
        self.analyzer = CodeAnalyzer(api_key=self.api_key, model=model)
        self.reporter = ReportGenerator()
        
    def analyze_file(self, file_path: str, analysis_types: Optional[List[str]] = None) -> Dict:
        """
        分析单个代码文件
        
        Args:
            file_path: 代码文件路径
            analysis_types: 分析类型列表 ["quality", "security", "performance", "best_practices"]
            
        Returns:
            分析结果字典
        """
        if analysis_types is None:
            analysis_types = ["quality", "security", "performance", "best_practices"]
            
        # 读取文件内容
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 获取文件信息
        file_info = {
            "path": file_path,
            "name": Path(file_path).name,
            "extension": Path(file_path).suffix,
            "lines": len(content.splitlines()),
            "size": len(content)
        }
        
        # 执行分析
        results = self.analyzer.analyze(content, file_info, analysis_types)
        
        return {
            "file": file_info,
            "analysis": results,
            "summary": self._generate_summary(results)
        }
        
    def analyze_directory(self, dir_path: str, extensions: Optional[List[str]] = None,
                          exclude_dirs: Optional[List[str]] = None) -> Dict:
        """
        分析整个目录
        
        Args:
            dir_path: 目录路径
            extensions: 要分析的文件扩展名列表
            exclude_dirs: 要排除的目录列表
            
        Returns:
            目录分析结果
        """
        if extensions is None:
            extensions = [".py", ".js", ".ts", ".java", ".go", ".rs", ".cpp", ".c", ".rb"]
            
        if exclude_dirs is None:
            exclude_dirs = ["node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build"]
            
        files_analyzed = []
        all_results = []
        
        for ext in extensions:
            for file_path in Path(dir_path).rglob(f"*{ext}"):
                # 检查是否在排除目录中
                if any(excluded in str(file_path) for excluded in exclude_dirs):
                    continue
                    
                try:
                    result = self.analyze_file(str(file_path))
                    files_analyzed.append(result["file"])
                    all_results.append(result)
                except Exception as e:
                    print(f"Warning: Failed to analyze {file_path}: {e}")
                    
        return {
            "directory": dir_path,
            "total_files": len(files_analyzed),
            "files": files_analyzed,
            "results": all_results,
            "overall_summary": self._generate_overall_summary(all_results)
        }
        
    def _generate_summary(self, results: Dict) -> Dict:
        """生成单个文件的分析摘要"""
        summary = {
            "total_issues": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }
        
        for analysis_type, data in results.items():
            if isinstance(data, dict) and "issues" in data:
                for issue in data["issues"]:
                    summary["total_issues"] += 1
                    severity = issue.get("severity", "info").lower()
                    if severity in summary:
                        summary[severity] += 1
                        
        return summary
        
    def _generate_overall_summary(self, all_results: List[Dict]) -> Dict:
        """生成整个项目的分析摘要"""
        overall = {
            "total_files": len(all_results),
            "total_issues": 0,
            "by_severity": {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
            "by_type": {}
        }
        
        for result in all_results:
            summary = result.get("summary", {})
            overall["total_issues"] += summary.get("total_issues", 0)
            
            for severity, count in summary.items():
                if severity in overall["by_severity"]:
                    overall["by_severity"][severity] += count
                    
        return overall
        
    def generate_report(self, analysis_result: Dict, format: str = "json") -> str:
        """
        生成分析报告
        
        Args:
            analysis_result: 分析结果
            format: 报告格式 ["json", "markdown", "html"]
            
        Returns:
            报告内容
        """
        return self.reporter.generate(analysis_result, format)
