# 🪞 GLM-CodeLens

> 🌐 [English](./README.md) · [中文](./README_zh-CN.md) · [繁體](./README_zh-TW.md) · [日本語](./README_ja.md)

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/gitstq/GLM-CodeLens?style=social)](https://github.com/gitstq/GLM-CodeLens/stargazers)

## 🎯 项目介绍

**GLM-CodeLens** 是一款基于 **GLM-5.1** 强大模型的智能代码分析引擎，提供零依赖、跨平台的代码质量检测、安全漏洞扫描和性能优化建议。

### ✨ 核心价值

- 🔍 **智能代码审查** - 利用GLM-5.1的深度理解能力，发现潜在问题
- 🔐 **安全漏洞检测** - 自动识别SQL注入、硬编码密码等安全风险
- ⚡ **性能问题识别** - 检测嵌套循环、低效字符串拼接等性能杀手
- 💎 **代码质量分析** - 函数长度、代码复杂度、嵌套层级全面评估
- 🤖 **AI深度洞察** - 结合静态分析与大模型智能分析双重保障

### 🧠 自研差异化亮点

1. **零依赖设计** - 仅使用Python标准库，无需安装额外依赖
2. **混合分析架构** - 静态模式匹配 + GLM-5.1智能推理
3. **多格式报告** - 支持JSON、Markdown、HTML三种输出格式
4. **灵活分析类型** - 可按需开启/关闭各类分析模块

### 💡 灵感来源

参考了GitHub Copilot Code Review、CodiumAI PR-Agent等AI代码审查工具的设计理念，结合GLM-5.1强大的代码理解和推理能力，打造更适合中国开发者的代码分析工具。

---

## 🚀 快速开始

### 📋 环境要求

- Python 3.8 或更高版本
- GLM API密钥（可选，用于AI深度分析）

### 📦 安装方式

**方式一：pip安装（推荐）**
```bash
pip install glm-codelens
```

**方式二：从源码安装**
```bash
git clone https://github.com/gitstq/GLM-CodeLens.git
cd GLM-CodeLens
pip install -e .
```

### 🎮 基础使用

**分析单个文件**
```bash
glm-codelens analyze your_code.py
```

**分析整个目录**
```bash
glm-codelens analyze ./src --recursive
```

**指定输出格式**
```bash
# Markdown格式（默认）
glm-codelens analyze code.py -f markdown

# JSON格式
glm-codelens analyze code.py -f json -o result.json

# HTML格式
glm-codelens analyze code.py -f html -o report.html
```

**指定分析类型**
```bash
glm-codelens analyze code.py --types security quality
```

**设置GLM API密钥（启用AI深度分析）**
```bash
export GLM_API_KEY="your-api-key"
glm-codelens analyze code.py
```

---

## 📖 详细使用指南

### 分析类型说明

| 类型 | 说明 | 覆盖内容 |
|------|------|----------|
| `security` | 安全分析 | SQL注入、硬编码密码、eval使用、pickle风险 |
| `quality` | 代码质量 | 函数长度、嵌套深度、代码复杂度 |
| `performance` | 性能分析 | 嵌套循环、字符串拼接、列表操作 |
| `best_practices` | 最佳实践 | TODO注释、异常处理、代码规范 |

### 命令行参数详解

```
位置参数:
  path                  要分析的代码文件或目录路径

选项:
  -r, --recursive       递归分析目录
  -f, --format          报告格式 [json|markdown|html] (默认: markdown)
  -o, --output          输出文件路径
  -t, --types           分析类型列表
  --api-key             GLM API密钥
  --model               模型名称 (默认: glm-5)
  --exclude             排除的目录列表
  --extensions          要分析的文件扩展名列表
```

### 典型使用场景

**场景1：CI/CD集成**
```yaml
# .github/workflows/code-analysis.yml
- name: Run Code Analysis
  run: |
    pip install glm-codelens
    glm-codelens analyze ./src --recursive -f json -o analysis.json
```

**场景2：Git Pre-commit Hook**
```bash
#!/bin/bash
# .git/hooks/pre-commit
glm-codelens analyze ./src --recursive --types security
```

**场景3：本地开发自检**
```bash
# 分析新添加的文件
glm-codelens analyze new_feature.py --types security quality performance
```

---

## 💡 设计思路与迭代规划

### 设计理念

1. **简洁至上** - 零依赖设计，降低使用门槛
2. **可扩展性** - 模块化架构，易于添加新的分析规则
3. **用户友好** - 清晰的输出格式，友好的错误提示
4. **隐私优先** - 本地运行，数据不外传

### 技术选型

- **Python标准库** - 确保零依赖运行
- **正则表达式** - 高效的代码模式匹配
- **GLM-5.1 API** - 强大的代码理解和推理能力

### 后续迭代计划

- [ ] 支持更多编程语言（Go、Rust、C++）
- [ ] 添加交互式TUI界面
- [ ] 支持自定义分析规则
- [ ] 与主流IDE插件集成
- [ ] 添加增量分析模式
- [ ] 支持团队代码质量趋势分析

### 社区贡献

欢迎提交Issue和Pull Request！

---

## 📦 打包与部署

### 构建发布版本
```bash
# 安装构建工具
pip install build

# 构建wheel包
python -m build
```

### 跨平台使用

GLM-CodeLens可在以下平台使用：
- ✅ Windows (x64)
- ✅ macOS (x64, ARM64)
- ✅ Linux (x64, ARM64)

---

## 🤝 贡献指南

### 提交问题

发现Bug或有新功能建议？请提交 [Issue](https://github.com/gitstq/GLM-CodeLens/issues)！

### 提交代码

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码规范

- 使用 PEP 8 代码规范
- 所有新功能需要添加测试
- 确保 `python -m pytest` 通过

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

---

<p align="center">
  <strong>Made with ❤️ by GitHub Developer</strong>
  <br>
  <sub>Powered by <a href="https://www.zhipuai.cn/">GLM-5.1</a></sub>
</p>
