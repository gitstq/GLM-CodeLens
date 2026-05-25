# 🪞 GLM-CodeLens

> 🌐 [English](./README.md) · [中文](./README_zh-CN.md) · [繁體](./README_zh-TW.md) · **日本語**

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/gitstq/GLM-CodeLens?style=social)](https://github.com/gitstq/GLM-CodeLens/stargazers)

## 🎯 プロジェクト紹介

**GLM-CodeLens** は、**GLM-5.1** の強力なモデルに基づいたインテリジェントなコード分析エンジンで、ゼロ依存症、クロスプラットフォームのコード品質検出、セキュリティ脆弱性スキャン、パフォーマンス最適化提案を提供します。

### ✨ コアバリュー

- 🔍 **インテリジェントコードレビュー** - GLM-5.1の深い理解力を活用して潜在的な問題を検出
- 🔐 **セキュリティ脆弱性検出** - SQLインジェクション、ハードコードされたパスワードなどのセキュリティリスクを自動識別
- ⚡ **パフォーマンス問題識別** - ネストされたループ、非効率的な文字列連結などのパフォーマンスキラー検出
- 💎 **コード品質分析** - 関数長、コード複雑さ、ネストレベルを包括的に評価
- 🤖 **AI-deepインサイト** - 静的解析と大規模モデル知的解析の二重保証

### 🧠 自社開発の差別化ポイント

1. **ゼロ依存設計** - Python標準ライブラリのみを使用し、追加の依存関係をインストール不要
2. **ハイブリッド分析アーキテクチャ** - 静的パターンマッチング + GLM-5.1知的推論
3. **マルチフォーマットレポート** - JSON、Markdown、HTMLの3つの出力形式をサポート
4. **柔軟な分析タイプ** - 必要に応じて各分析モジュールを有効/無効にできます

---

## 🚀 クイックスタート

### 📋 環境要件

- Python 3.8以上
- GLM APIキー（AI深度分析用、オプション）

### 📦 インストール方法

```bash
# 方法1：pipインストール（推奨）
pip install glm-codelens

# 方法2：ソースからインストール
git clone https://github.com/gitstq/GLM-CodeLens.git
cd GLM-CodeLens
pip install -e .
```

### 🎮 基本的な使用法

```bash
# 单一ファイルを分析
glm-codelens analyze your_code.py

# ディレクトリ全体を分析
glm-codelens analyze ./src --recursive

# 出力形式を指定
glm-codelens analyze code.py -f markdown
glm-codelens analyze code.py -f json -o result.json
glm-codelens analyze code.py -f html -o report.html

# GLM APIキーを設定
export GLM_API_KEY="your-api-key"
glm-codelens analyze code.py
```

---

## 📖 詳細な使用ガイド

### 分析タイプの説明

| タイプ | 説明 | カバー内容 |
|--------|------|------------|
| `security` | セキュリティ分析 | SQLインジェクション、ハードコードされたパスワード、eval使用、pickleリスク |
| `quality` | コード品質 | 関数長、ネスト深度、コード複雑さ |
| `performance` | パフォーマンス分析 | ネストされたループ、文字列連結、リスト操作 |
| `best_practices` | ベストプラクティス | TODOコメント、例外処理、コード規範 |

---

## 🤝 コントリビューションガイド

IssueとPull Requestの提出を歓迎します！

---

## 📄 オープンソースライセンス

このプロジェクトは [MIT License](LICENSE) に基づいてオープンソースです。
