# 🚀 Chat-Data-Analyst: 基于 LLM 的智能数据分析助手

## 📖 项目简介
这是一个基于 **Streamlit** 和 **DeepSeek (LLM)** 构建的对话式数据分析工具。
它旨在解决传统数据分析门槛高、流程繁琐的问题。用户只需上传 Excel/CSV 文件，即可通过**自然语言**与数据交互，实现：
- 📊 **自动绘图**：说出需求，自动生成 Matplotlib/Seaborn 图表。
- 🧠 **智能洞察**：AI 自动分析数据趋势，提供商业建议。
- 📝 **自动清洗**：智能识别 CSV/Excel 格式并处理乱码。

## 🛠️ 技术栈
- **Frontend**: Streamlit (Python Web 框架)
- **Backend**: Python 3.9+
- **AI Engine**: DeepSeek V3 (通过 OpenAI SDK 调用)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn

## ⚡️ 核心功能展示
1. **数据预览**：自动识别文件编码，展示前 10 行数据。
2. **Text-to-Code**：利用 LLM 编写 Python 绘图代码，并使用 `exec()` 动态执行。
3. **AI Insight**：结合图表数据，自动生成商业分析报告。

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/your-username/chat-data-analyst.git