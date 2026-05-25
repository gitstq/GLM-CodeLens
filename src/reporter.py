#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成器 - 生成多种格式的分析报告
"""

import json
from datetime import datetime
from typing import Dict, Any


class ReportGenerator:
    """分析报告生成器"""
    
    def generate(self, analysis_result: Dict, format: str = "json") -> str:
        """
        生成分析报告
        
        Args:
            analysis_result: 分析结果
            format: 报告格式 ["json", "markdown", "html"]
            
        Returns:
            报告内容字符串
        """
        if format == "json":
            return self._generate_json(analysis_result)
        elif format == "markdown":
            return self._generate_markdown(analysis_result)
        elif format == "html":
            return self._generate_html(analysis_result)
        else:
            raise ValueError(f"不支持的报告格式: {format}")
            
    def _generate_json(self, result: Dict) -> str:
        """生成JSON格式报告"""
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    def _generate_markdown(self, result: Dict) -> str:
        """生成Markdown格式报告"""
        lines = []
        
        # 标题
        lines.append("# 📊 GLM-CodeLens 分析报告")
        lines.append("")
        lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # 文件信息
        if "file" in result:
            file_info = result["file"]
            lines.append("## 📄 文件信息")
            lines.append("")
            lines.append(f"| 属性 | 值 |")
            lines.append(f"|------|-----|")
            lines.append(f"| 文件名 | {file_info.get('name', 'N/A')} |")
            lines.append(f"| 路径 | `{file_info.get('path', 'N/A')}` |")
            lines.append(f"| 扩展名 | {file_info.get('extension', 'N/A')} |")
            lines.append(f"| 代码行数 | {file_info.get('lines', 0)} |")
            lines.append(f"| 文件大小 | {file_info.get('size', 0)} bytes |")
            lines.append("")
            
        # 摘要
        if "summary" in result:
            summary = result["summary"]
            lines.append("## 📈 问题摘要")
            lines.append("")
            
            severity_emojis = {
                "critical": "🔴",
                "high": "🟠",
                "medium": "🟡",
                "low": "🟢",
                "info": "🔵"
            }
            
            total = summary.get("total_issues", 0)
            lines.append(f"**总计问题**: {total}")
            lines.append("")
            
            for severity, emoji in severity_emojis.items():
                count = summary.get(severity, 0)
                if count > 0:
                    lines.append(f"{emoji} **{severity.upper()}**: {count}")
            lines.append("")
            
        # 详细分析
        if "analysis" in result:
            lines.append("## 🔍 详细分析")
            lines.append("")
            
            for analysis_type, data in result["analysis"].items():
                if not isinstance(data, dict):
                    continue
                    
                type_names = {
                    "security": "🔐 安全分析",
                    "quality": "💎 代码质量",
                    "performance": "⚡ 性能分析",
                    "best_practices": "✨ 最佳实践",
                    "glm_insights": "🤖 GLM智能分析"
                }
                
                lines.append(f"### {type_names.get(analysis_type, analysis_type)}")
                lines.append("")
                
                # GLM分析特殊处理
                if analysis_type == "glm_insights":
                    if "error" in data:
                        lines.append(f"⚠️ {data.get('message', '分析出错')}")
                        if "tip" in data:
                            lines.append(f"💡 提示: {data['tip']}")
                    elif "message" in data:
                        lines.append(f"ℹ️ {data['message']}")
                        if "tip" in data:
                            lines.append(f"💡 提示: {data['tip']}")
                    elif "insights" in data:
                        lines.append(data["insights"])
                    lines.append("")
                    continue
                    
                # 常规分析结果
                issues = data.get("issues", [])
                if not issues:
                    lines.append("✅ 未发现问题")
                    lines.append("")
                    continue
                    
                for issue in issues:
                    severity_emoji = {
                        "critical": "🔴",
                        "high": "🟠",
                        "medium": "🟡",
                        "low": "🟢",
                        "info": "🔵"
                    }.get(issue.get("severity", "info"), "⚪")
                    
                    lines.append(f"{severity_emoji} **{issue.get('type', 'unknown').replace('_', ' ').title()}**")
                    
                    if "line" in issue:
                        lines.append(f"   📍 行号: `{issue['line']}`")
                    lines.append(f"   📝 {issue.get('description', 'N/A')}")
                    if "suggestion" in issue:
                        lines.append(f"   💡 建议: {issue['suggestion']}")
                    if "code_snippet" in issue:
                        lines.append(f"   💻 代码: ```\n   {issue['code_snippet']}\n   ```")
                    lines.append("")
                    
        # 目录分析
        if "directory" in result:
            lines.append("## 📁 目录分析")
            lines.append("")
            lines.append(f"**目录**: `{result.get('directory', 'N/A')}`")
            lines.append(f"**分析文件数**: {result.get('total_files', 0)}")
            lines.append("")
            
            if "overall_summary" in result:
                overall = result["overall_summary"]
                lines.append("### 问题统计")
                lines.append("")
                lines.append(f"| 严重级别 | 数量 |")
                lines.append(f"|----------|------|")
                for severity, count in overall.get("by_severity", {}).items():
                    lines.append(f"| {severity.upper()} | {count} |")
                lines.append("")
                
        return "\n".join(lines)
        
    def _generate_html(self, result: Dict) -> str:
        """生成HTML格式报告"""
        # 生成标题ASCII艺术
        ascii_art = """
  ____     ___    __  _____   _   _ _____ 
 |  _ \\  / _ \\  / / | ____| | \\ | | ____|
 | |_) || | | |/ /  |  _|   |  \\| |  _|  
 |  _ < | |_| / /   | |___  | |\\  | |___ 
 |_| \\_\\ ___/_/    |_____| |_| \\_|_____|
                                    v1.0.0
        """
        
        # 生成HTML内容
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GLM-CodeLens 分析报告</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        h3 { color: #7f8c8d; }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th { background: #3498db; color: white; }
        tr:nth-child(even) { background: #f9f9f9; }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        pre {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .severity-critical { color: #e74c3c; font-weight: bold; }
        .severity-high { color: #e67e22; font-weight: bold; }
        .severity-medium { color: #f39c12; }
        .severity-low { color: #27ae60; }
        .severity-info { color: #3498db; }
        .badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
        }
        .badge-critical { background: #e74c3c; color: white; }
        .badge-high { background: #e67e22; color: white; }
        .badge-medium { background: #f39c12; color: white; }
        .badge-low { background: #27ae60; color: white; }
        .badge-info { background: #3498db; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <pre style="background: #2c3e50; color: #3498db; font-size: 18px; white-space: pre-wrap;">""" + ascii_art + """</pre>
        <p style="text-align: center; color: #7f8c8d;">
            Powered by <strong>GLM-5.1</strong> - Intelligent Code Analysis Engine
        </p>
        <hr>
    </div>
</body>
</html>"""
        return html
