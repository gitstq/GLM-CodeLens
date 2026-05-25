#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码分析器 - 基于GLM-5.1的智能代码分析
"""

import os
import re
import hashlib
from typing import Dict, List, Optional
from urllib.parse import quote


class CodeAnalyzer:
    """代码分析器"""
    
    # 常见的安全漏洞模式
    SECURITY_PATTERNS = {
        "sql_injection": {
            "pattern": r"(execute|exec|query)\s*\(\s*[\"'].*?%s.*?[\"']",
            "severity": "critical",
            "description": "可能的SQL注入风险"
        },
        "hardcoded_password": {
            "pattern": r"(password|passwd|pwd)\s*=\s*[\"'][^\"']+[\"']",
            "severity": "high",
            "description": "发现硬编码密码"
        },
        "eval_usage": {
            "pattern": r"\beval\s*\(",
            "severity": "high",
            "description": "使用eval可能存在安全风险"
        },
        "pickle_untrusted": {
            "pattern": r"pickle\.load|pickle\.loads",
            "severity": "medium",
            "description": "使用pickle加载不可信数据"
        },
        "hardcoded_api_key": {
            "pattern": r"(api_key|apikey|api-key)\s*=\s*[\"'][^\"']+[\"']",
            "severity": "high",
            "description": "发现硬编码API密钥"
        }
    }
    
    # 代码质量模式
    QUALITY_PATTERNS = {
        "long_function": {
            "pattern": r"def\s+\w+\s*\([^)]*\)\s*:",
            "threshold": 50,
            "severity": "medium",
            "description": "函数过长，建议拆分"
        },
        "complex_condition": {
            "pattern": r"if\s+.+?(and|or).+?:",
            "threshold": 4,
            "severity": "low",
            "description": "条件表达式过于复杂"
        },
        "deep_nesting": {
            "pattern": r"^\s{16,}",
            "severity": "low",
            "description": "代码嵌套过深"
        },
        "unused_import": {
            "pattern": r"^import\s+|^from\s+",
            "severity": "info",
            "description": "可能的未使用导入"
        }
    }
    
    # 性能问题模式
    PERFORMANCE_PATTERNS = {
        "nested_loop": {
            "pattern": r"for\s+.*?:\s*[\s\S]*?for\s+.*?:",
            "severity": "medium",
            "description": "发现嵌套循环，可能影响性能"
        },
        "list_concatenation": {
            "pattern": r"\+\s*=\s*\[\]",
            "severity": "low",
            "description": "使用+=拼接列表，建议使用extend"
        },
        "string_concatenation_loop": {
            "pattern": r"for.*?:\s*.*?\+=",
            "severity": "medium",
            "description": "循环中使用字符串拼接，建议使用join"
        }
    }
    
    def __init__(self, api_key: Optional[str] = None, model: str = "glm-5"):
        """
        初始化分析器
        
        Args:
            api_key: GLM API密钥
            model: 模型名称
        """
        self.api_key = api_key
        self.model = model
        self._api_base = os.environ.get("GLM_API_BASE", "https://open.bigmodel.cn/api/paas/v4")
        
    def analyze(self, code: str, file_info: Dict, analysis_types: List[str]) -> Dict:
        """
        执行代码分析
        
        Args:
            code: 代码内容
            file_info: 文件信息字典
            analysis_types: 分析类型列表
            
        Returns:
            分析结果字典
        """
        results = {}
        
        # 静态模式分析
        if "security" in analysis_types:
            results["security"] = self._analyze_security(code)
            
        if "quality" in analysis_types:
            results["quality"] = self._analyze_quality(code)
            
        if "performance" in analysis_types:
            results["performance"] = self._analyze_performance(code)
            
        if "best_practices" in analysis_types:
            results["best_practices"] = self._analyze_best_practices(code)
            
        # 基于GLM-5.1的深度分析
        if self.api_key:
            try:
                glm_analysis = self._glm_analyze(code, file_info, analysis_types)
                results["glm_insights"] = glm_analysis
            except Exception as e:
                results["glm_insights"] = {
                    "error": str(e),
                    "message": "GLM分析暂时不可用，将使用静态分析结果"
                }
        else:
            results["glm_insights"] = {
                "message": "未配置GLM API密钥，跳过AI深度分析",
                "tip": "设置GLM_API_KEY环境变量以启用GLM-5.1智能分析"
            }
            
        return results
        
    def _analyze_security(self, code: str) -> Dict:
        """安全分析"""
        issues = []
        
        for vuln_type, config in self.SECURITY_PATTERNS.items():
            matches = re.finditer(config["pattern"], code, re.IGNORECASE)
            for match in matches:
                line_num = code[:match.start()].count("\n") + 1
                issues.append({
                    "type": vuln_type,
                    "severity": config["severity"],
                    "description": config["description"],
                    "line": line_num,
                    "match": match.group()[:50]
                })
                
        return {
            "total": len(issues),
            "issues": issues,
            "summary": self._summarize_issues(issues)
        }
        
    def _analyze_quality(self, code: str) -> Dict:
        """代码质量分析"""
        issues = []
        lines = code.split("\n")
        
        # 检查函数长度
        current_function = None
        function_lines = 0
        
        for i, line in enumerate(lines):
            func_match = re.match(r"(def|class)\s+(\w+)", line)
            if func_match:
                if current_function and function_lines > 50:
                    issues.append({
                        "type": "long_function",
                        "severity": "medium",
                        "description": f"函数 {current_function} 超过50行 ({function_lines}行)",
                        "line": i - function_lines + 1
                    })
                current_function = func_match.group(2)
                function_lines = 1
            elif current_function:
                function_lines += 1
                
        # 检查嵌套深度
        for i, line in enumerate(lines):
            indent = len(line) - len(line.lstrip())
            if indent > 16:
                issues.append({
                    "type": "deep_nesting",
                    "severity": "low",
                    "description": f"嵌套层级过深 (缩进{indent}空格)",
                    "line": i + 1
                })
                
        return {
            "total": len(issues),
            "issues": issues,
            "summary": self._summarize_issues(issues)
        }
        
    def _analyze_performance(self, code: str) -> Dict:
        """性能分析"""
        issues = []
        
        for issue_type, config in self.PERFORMANCE_PATTERNS.items():
            matches = re.finditer(config["pattern"], code, re.DOTALL)
            for match in matches:
                line_num = code[:match.start()].count("\n") + 1
                issues.append({
                    "type": issue_type,
                    "severity": config["severity"],
                    "description": config["description"],
                    "line": line_num
                })
                
        return {
            "total": len(issues),
            "issues": issues,
            "summary": self._summarize_issues(issues)
        }
        
    def _analyze_best_practices(self, code: str) -> Dict:
        """最佳实践分析"""
        issues = []
        
        # 检查TODO/FIXME注释
        todo_matches = re.finditer(r"#\s*(TODO|FIXME|HACK|XXX):", code, re.IGNORECASE)
        for match in todo_matches:
            line_num = code[:match.start()].count("\n") + 1
            issues.append({
                "type": "todo_comment",
                "severity": "info",
                "description": f"发现未完成的TODO: {match.group()}",
                "line": line_num
            })
            
        # 检查异常处理
        if "except:" in code and "except Exception" not in code:
            issues.append({
                "type": "bare_except",
                "severity": "medium",
                "description": "使用裸except子句，建议指定异常类型",
                "line": code.count("except:")
            })
            
        return {
            "total": len(issues),
            "issues": issues,
            "summary": self._summarize_issues(issues)
        }
        
    def _glm_analyze(self, code: str, file_info: Dict, analysis_types: List[str]) -> Dict:
        """
        使用GLM-5.1进行深度代码分析
        
        Args:
            code: 代码内容
            file_info: 文件信息
            analysis_types: 分析类型
            
        Returns:
            GLM分析结果
        """
        # 构建分析提示
        prompt = self._build_glm_prompt(code, file_info, analysis_types)
        
        # 调用GLM API
        try:
            import urllib.request
            import urllib.error
            
            url = f"{self._api_base}/chat/completions"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "你是一个专业的代码审查助手。请分析代码并提供结构化的反馈。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 2000
            }
            
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))
                return {
                    "insights": result["choices"][0]["message"]["content"],
                    "model": self.model
                }
                
        except Exception as e:
            return {
                "error": str(e),
                "message": "GLM API调用失败"
            }
            
    def _build_glm_prompt(self, code: str, file_info: Dict, analysis_types: List[str]) -> str:
        """构建GLM分析提示"""
        
        type_names = {
            "quality": "代码质量",
            "security": "安全漏洞",
            "performance": "性能问题",
            "best_practices": "最佳实践"
        }
        
        types_to_analyze = ", ".join([type_names.get(t, t) for t in analysis_types])
        
        prompt = f"""请分析以下{file_info.get('name', '代码文件')}，进行{types_to_analyze}分析。

代码内容：
```{file_info.get('extension', '').lstrip('.')} 
{code[:3000]}
```

请按以下JSON格式返回分析结果：
{{
    "overall_score": 0-100的评分,
    "strengths": ["代码优点列表"],
    "issues": [
        {{
            "severity": "critical/high/medium/low/info",
            "category": "问题类别",
            "description": "问题描述",
            "suggestion": "改进建议",
            "code_snippet": "相关代码片段"
        }}
    ],
    "summary": "总结"
}}

只返回JSON格式，不要有其他内容。
"""
        return prompt
        
    def _summarize_issues(self, issues: List[Dict]) -> Dict:
        """汇总问题"""
        summary = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }
        
        for issue in issues:
            severity = issue.get("severity", "info")
            if severity in summary:
                summary[severity] += 1
                
        return summary
