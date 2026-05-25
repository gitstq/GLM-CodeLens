#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM-CodeLens CLI - 命令行接口
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional

from .codelens import CodeLensEngine


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    
    parser = argparse.ArgumentParser(
        prog="glm-codelens",
        description="🪞 GLM-CodeLens - 基于GLM-5.1的智能代码分析引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s analyze file.py                    # 分析单个文件
  %(prog)s analyze file.py --format markdown  # 生成Markdown报告
  %(prog)s analyze ./src --recursive          # 分析整个目录
  %(prog)s analyze file.py --types security quality  # 指定分析类型

分析类型:
  security      - 安全漏洞检测
  quality       - 代码质量分析
  performance   - 性能问题识别
  best_practices - 最佳实践检查

环境变量:
  GLM_API_KEY  - GLM API密钥
  GLM_API_BASE - GLM API地址 (默认: https://open.bigmodel.cn/api/paas/v4)
        """
    )
    
    parser.add_argument("--version", "-v", action="version", version="%(prog)s 1.0.0")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # analyze命令
    analyze_parser = subparsers.add_parser("analyze", help="分析代码文件或目录")
    analyze_parser.add_argument("path", help="要分析的代码文件或目录路径")
    analyze_parser.add_argument("--recursive", "-r", action="store_true", 
                                help="递归分析目录")
    analyze_parser.add_argument("--format", "-f", choices=["json", "markdown", "html"],
                                default="markdown", help="报告格式")
    analyze_parser.add_argument("--output", "-o", help="输出文件路径")
    analyze_parser.add_argument("--types", "-t", nargs="+",
                                choices=["security", "quality", "performance", "best_practices"],
                                default=["security", "quality", "performance", "best_practices"],
                                help="分析类型")
    analyze_parser.add_argument("--api-key", help="GLM API密钥 (也可以设置GLM_API_KEY环境变量)")
    analyze_parser.add_argument("--model", default="glm-5", help="使用的模型名称")
    analyze_parser.add_argument("--exclude", nargs="+", default=[],
                                help="排除的目录")
    analyze_parser.add_argument("--extensions", nargs="+", 
                                default=[".py", ".js", ".ts", ".java", ".go", ".rs"],
                                help="要分析的文件扩展名")
    
    return parser


def analyze_file(args) -> int:
    """分析单个文件"""
    if not os.path.exists(args.path):
        print(f"❌ 错误: 文件不存在: {args.path}")
        return 1
        
    engine = CodeLensEngine(api_key=args.api_key, model=args.model)
    
    print(f"🔍 正在分析: {args.path}")
    print(f"📊 分析类型: {', '.join(args.types)}")
    print()
    
    result = engine.analyze_file(args.path, args.types)
    report = engine.generate_report(result, args.format)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ 报告已保存到: {args.output}")
    else:
        print(report)
        
    # 打印摘要
    summary = result.get("summary", {})
    total = summary.get("total_issues", 0)
    print()
    print("=" * 50)
    print("📈 问题摘要")
    print("=" * 50)
    
    if total == 0:
        print("✅ 太棒了！没有发现问题！")
    else:
        print(f"🔴 严重 (Critical): {summary.get('critical', 0)}")
        print(f"🟠 高危 (High):     {summary.get('high', 0)}")
        print(f"🟡 中危 (Medium):  {summary.get('medium', 0)}")
        print(f"🟢 低危 (Low):     {summary.get('low', 0)}")
        print(f"🔵 提示 (Info):    {summary.get('info', 0)}")
        print()
        print(f"总计问题: {total}")
        
    return 0


def analyze_directory(args) -> int:
    """分析目录"""
    if not os.path.isdir(args.path):
        print(f"❌ 错误: 目录不存在: {args.path}")
        return 1
        
    exclude_dirs = args.exclude + ["node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build"]
    
    engine = CodeLensEngine(api_key=args.api_key, model=args.model)
    
    print(f"🔍 正在分析目录: {args.path}")
    print(f"📊 分析类型: {', '.join(args.types)}")
    print(f"📁 文件扩展名: {', '.join(args.extensions)}")
    print(f"🚫 排除目录: {', '.join(exclude_dirs)}")
    print()
    print("⏳ 分析中，请稍候...")
    
    result = engine.analyze_directory(
        args.path, 
        extensions=args.extensions,
        exclude_dirs=exclude_dirs
    )
    
    report = engine.generate_report(result, args.format)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ 报告已保存到: {args.output}")
    else:
        print(report)
        
    # 打印摘要
    overall = result.get("overall_summary", {})
    total = overall.get("total_files", 0)
    total_issues = overall.get("total_issues", 0)
    
    print()
    print("=" * 50)
    print("📈 目录分析摘要")
    print("=" * 50)
    print(f"📁 分析文件数: {total}")
    print(f"🔍 发现问题数: {total_issues}")
    print()
    
    by_severity = overall.get("by_severity", {})
    print(f"🔴 严重 (Critical): {by_severity.get('critical', 0)}")
    print(f"🟠 高危 (High):     {by_severity.get('high', 0)}")
    print(f"🟡 中危 (Medium):  {by_severity.get('medium', 0)}")
    print(f"🟢 低危 (Low):     {by_severity.get('low', 0)}")
    print(f"🔵 提示 (Info):    {by_severity.get('info', 0)}")
    
    return 0


def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command == "analyze" or args.command is None:
        if args.path:
            if os.path.isfile(args.path):
                return analyze_file(args)
            elif os.path.isdir(args.path):
                return analyze_directory(args)
            else:
                print(f"❌ 错误: 路径不存在: {args.path}")
                return 1
        else:
            parser.print_help()
            return 0
            
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
