import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import process_uploaded_file, analyze_table_directly, generate_plot_code, generate_insight

# 1. 页面设置
st.set_page_config(page_title="AI 数据分析师 Pro", page_icon="🚀", layout="wide")
st.title("🚀 AI 智能数据分析助手 Pro")

# 2. 侧边栏
with st.sidebar:
    st.header("🔑 配置与数据")
    api_key = st.text_input("DeepSeek API Key", type="password")
    uploaded_file = st.file_uploader("上传 CSV/Excel", type=["csv", "xlsx"])
    st.info("💡 提示：Day 4 版本已支持自动商业洞察！")

# 3. 主流程
if not api_key:
    st.warning("👈 请输入 API Key")
elif uploaded_file is None:
    st.info("👈 请上传数据文件")
else:
    df = process_uploaded_file(uploaded_file)

    if df is not None:
        # 布局：左边看数据，右边看分析
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("📋 数据预览")
            st.dataframe(df.head(10))

            # 文字分析功能
            st.divider()
            if st.button("🧠 全局数据诊断"):
                with st.spinner("AI 正在扫描全表..."):
                    report = analyze_table_directly(df, api_key)
                    st.markdown(report)

        with col2:
            st.subheader("📊 智能绘图 & 洞察")

            # 输入框
            plot_query = st.text_input("你想看什么分析？(如：画出销售额趋势)", "统计不同产品的销售总额")

            if st.button("🚀 生成图表与洞察"):
                if not plot_query:
                    st.warning("请输入需求")
                else:
                    # A. 画图阶段
                    st.markdown("### 1️⃣ 可视化图表")
                    with st.spinner("AI 正在绘制图表..."):
                        # 清理画布，防止上一张图残留
                        plt.clf()
                        code = generate_plot_code(df, plot_query, api_key)

                        if code:
                            try:
                                # 执行绘图
                                exec(code)
                            except Exception as e:
                                st.error(f"绘图失败: {e}")
                        else:
                            st.error("代码生成失败")

                    # B. 洞察阶段 (Day 4 核心)
                    st.divider()
                    st.markdown("### 2️⃣ AI 商业洞察")
                    with st.spinner("AI 正在分析图表背后的趋势..."):
                        insight = generate_insight(df, plot_query, api_key)
                        st.info(insight)

    else:
        st.error("文件格式错误")