import pandas as pd
from openai import OpenAI


# ==========================================
# 1. 基础工具 (文件处理)
# ==========================================
def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                try:
                    return pd.read_csv(uploaded_file, encoding='utf-8')
                except UnicodeDecodeError:
                    return pd.read_csv(uploaded_file, encoding='gbk')
            elif uploaded_file.name.endswith('.xlsx'):
                return pd.read_excel(uploaded_file)
        except Exception:
            return None
    return None


# ==========================================
# 2. 文本分析工具 (Day 2)
# ==========================================
def analyze_table_directly(df, api_key):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    data_preview = df.head(10).to_markdown(index=False)

    system_prompt = "你是一位资深数据分析师。请根据数据概况，推测业务场景，并给出3个分析方向。"
    user_prompt = f"数据预览：\n{data_preview}"

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            stream=False, timeout=60
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"分析出错: {e}"


# ==========================================
# 3. 绘图代码生成工具 (Day 3)
# ==========================================
def dataframe_to_info(df):
    buffer = []
    buffer.append(f"Columns: {', '.join(df.columns)}")
    buffer.append("Dtypes:")
    for col, dtype in df.dtypes.items():
        buffer.append(f"  - {col}: {dtype}")
    return "\n".join(buffer)


def generate_plot_code(df, query, api_key):
    data_info = dataframe_to_info(df)

    system_prompt = """
    你是一个 Python 数据可视化专家。
    请生成绘图代码。
    【严格约束】
    1. 变量名使用 `df`。
    2. 必须解决中文乱码 (plt.rcParams['font.sans-serif']=['SimHei'])。
    3. 使用 `st.pyplot(plt.gcf())` 显示图表。
    4. 不要用 plt.show()。
    5. 不要输出 markdown 标记，只输出代码。
    """

    user_prompt = f"数据结构：\n{data_info}\n\n用户需求：{query}"

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            stream=False, timeout=60
        )
        code = response.choices[0].message.content
        return code.replace("```python", "").replace("```", "").strip()
    except Exception as e:
        print(f"代码生成失败: {e}")
        return None


# ==========================================
# 4. 智能洞察工具 (Day 4 新增核心)
# ==========================================
def generate_insight(df, query, api_key):
    """
    功能：根据用户的绘图需求，分析背后的商业价值
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # 我们把表头和用户的绘图意图发给 AI
    data_info = dataframe_to_info(df)

    system_prompt = """
    你是一位能够洞察数据的商业顾问。
    用户正在对数据进行可视化分析。
    请根据用户的问题和数据结构，给出一段深入的分析结论。

    【要求】
    1. 不要描述图表长什么样（比如“这是一个柱状图”），要讲图表说明了什么业务问题。
    2. 给出 2-3 条具体的行动建议。
    3. 语气专业、简练。
    """

    user_prompt = f"""
    数据结构：
    {data_info}

    用户的分析目标：{query}

    请结合数据逻辑，给出商业洞察和建议：
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            stream=False, timeout=60
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"洞察分析失败: {e}"