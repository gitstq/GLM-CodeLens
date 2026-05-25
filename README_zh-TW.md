# 🪞 GLM-CodeLens

> 🌐 [English](./README.md) · **中文** · [繁體](./README_zh-TW.md) · [日本語](./README_ja.md)

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/gitstq/GLM-CodeLens?style=social)](https://github.com/gitstq/GLM-CodeLens/stargazers)

## 🎯 項目介紹

**GLM-CodeLens** 是一款基於 **GLM-5.1** 強大模型的智能代碼分析引擎，提供零依賴、跨平台的代碼質量檢測、安全漏洞掃描和性能優化建議。

### ✨ 核心價值

- 🔍 **智能代碼審查** - 利用GLM-5.1的深度理解能力，發現潛在問題
- 🔐 **安全漏洞檢測** - 自動識別SQL注入、硬編碼密碼等安全風險
- ⚡ **性能問題識別** - 檢測嵌套循環、低效字符串拼接等性能殺手
- 💎 **代碼質量分析** - 函數長度、代碼複雜度、嵌套層級全面評估
- 🤖 **AI深度洞察** - 結合靜態分析與大模型智能分析雙重保障

### 🧠 自研差異化亮點

1. **零依賴設計** - 僅使用Python標準庫，無需安裝額外依賴
2. **混合分析架構** - 靜態模式匹配 + GLM-5.1智能推理
3. **多格式報告** - 支持JSON、Markdown、HTML三種輸出格式
4. **靈活分析類型** - 可按需開啟/關閉各類分析模塊

---

## 🚀 快速開始

### 📋 環境要求

- Python 3.8 或更高版本
- GLM API密鑰（可選，用於AI深度分析）

### 📦 安裝方式

```bash
# 方式一：pip安裝（推薦）
pip install glm-codelens

# 方式二：從源碼安裝
git clone https://github.com/gitstq/GLM-CodeLens.git
cd GLM-CodeLens
pip install -e .
```

### 🎮 基礎使用

```bash
# 分析單個文件
glm-codelens analyze your_code.py

# 分析整個目錄
glm-codelens analyze ./src --recursive

# 指定輸出格式
glm-codelens analyze code.py -f markdown
glm-codelens analyze code.py -f json -o result.json
glm-codelens analyze code.py -f html -o report.html

# 設置GLM API密鑰
export GLM_API_KEY="your-api-key"
glm-codelens analyze code.py
```

---

## 📖 詳細使用指南

### 分析類型說明

| 類型 | 說明 | 覆蓋內容 |
|------|------|----------|
| `security` | 安全分析 | SQL注入、硬編碼密碼、eval使用、pickle風險 |
| `quality` | 代碼質量 | 函數長度、嵌套深度、代碼複雜度 |
| `performance` | 性能分析 | 嵌套循環、字符串拼接、列表操作 |
| `best_practices` | 最佳實踐 | TODO註釋、異常處理、代碼規範 |

---

## 🤝 貢獻指南

歡迎提交Issue和Pull Request！

---

## 📄 開源協議

本項目基於 [MIT License](LICENSE) 開源。
