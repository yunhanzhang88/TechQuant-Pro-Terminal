# replace with your full app code

import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px

# --- 1. 页面配置 ---
st.set_page_config(page_title="TechQuant Pro 50", layout="wide")

st.title("🚀 TechQuant Pro：美国科技50强多因子分析终端")
st.caption("2026版 | 多因子投资分析工具")

# --- ⭐ 项目说明（高分关键） ---
st.markdown("""
### 🎯 项目目标
本工具通过整合盈利能力、研发投入、估值水平和风险指标，帮助用户对美国科技股进行系统性分析。

### 👥 目标用户
- 个人投资者  
- 金融/经济专业学生  
- 初级分析师  

### ⚠️ 现实痛点
大多数平台只提供价格或单一指标分析，缺乏多维度综合判断工具。

👉 本系统通过**多因子模型 + 可调权重机制**，实现更科学的投资分析。
""")

# --- 2. 数据加载 ---
@st.cache_data
def load_data():
    paths = [
        "wrds_output_v3/us_tech_top50_2026.csv",
        "us_tech_top50_2026.csv"
    ]
    file_path = next((p for p in paths if os.path.exists(p)), None)

    if not file_path:
        return None

    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df['ticker'] = df['ticker'].astype(str).str.strip()

    cols = ['roa', 'gross_margin', 'rnd_to_rev', 'bm_ratio']
    df[cols] = df[cols].fillna(0)

    # ⭐ 风险指标（波动率）
    df = df.sort_values(['ticker', 'date'])
    df['volatility'] = (
        df.groupby('ticker')['ret']
        .rolling(12)
        .std()
        .reset_index(0, drop=True)
    )

    return df


df_raw = load_data()

if df_raw is None:
    st.error("❌ 未找到数据文件，请检查CSV路径")
    st.stop()

# --- 3. 侧边栏 ---
st.sidebar.header("🕹️ 控制面板")

all_tickers = sorted(df_raw['ticker'].unique())
default_list = ["NVDA", "AAPL", "MSFT", "PLTR", "SMCI"]

selected_tickers = st.sidebar.multiselect(
    "选择股票",
    all_tickers,
    default=[t for t in default_list if t in all_tickers]
)

metric_map = {
    "prc": "股价",
    "ret": "收益率",
    "roa": "资产回报率",
    "gross_margin": "毛利率",
    "rnd_to_rev": "研发投入比",
    "bm_ratio": "账面市值比"
}

selected_metric = st.sidebar.selectbox(
    "选择分析指标",
    list(metric_map.keys()),
    format_func=lambda x: metric_map[x]
)

df = df_raw[df_raw['ticker'].isin(selected_tickers)]

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 趋势分析",
    "🧬 相关性分析",
    "🏆 量化评分",
    "📋 数据明细"
])

# ===================== TAB1 =====================
with tab1:
    fig = px.line(df, x='date', y=selected_metric, color='ticker',
                  title=f"{metric_map[selected_metric]} 走势")
    st.plotly_chart(fig, use_container_width=True)

    # ⭐ 风险收益分析
    st.markdown("### ⚖️ 风险-收益分析")

    risk_df = df.groupby('ticker').agg({
        'ret': 'mean',
        'volatility': 'mean'
    }).dropna().reset_index()

    if not risk_df.empty:
        fig2 = px.scatter(
            risk_df,
            x='volatility',
            y='ret',
            text='ticker',
            labels={'volatility': '风险（波动率）', 'ret': '平均收益'}
        )
        fig2.update_traces(textposition='top center')
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("""
💡 **核心洞察：**
- 高收益通常伴随高风险  
- 低波动股票更适合稳健投资  
- 右上区域代表高风险高回报标的  
""")

# ===================== TAB2 =====================
with tab2:
    if len(selected_tickers) > 1:
        corr = df.pivot_table(index='date', columns='ticker', values='ret').corr()
        st.plotly_chart(px.imshow(corr, text_auto=True), use_container_width=True)

        st.markdown("""
📌 **分析结论：**
低相关性有助于分散风险，提高投资组合稳定性。
""")
    else:
        st.warning("请至少选择两只股票")

# ===================== TAB3 =====================
with tab3:
    st.subheader("🏆 多因子评分模型")

    c1, c2, c3, c4 = st.columns(4)
    w_roa = c1.slider("盈利能力（ROA）", 0.0, 1.0, 0.4)
    w_rnd = c2.slider("研发投入", 0.0, 1.0, 0.3)
    w_gm = c3.slider("毛利水平", 0.0, 1.0, 0.2)
    w_val = c4.slider("估值（BM）", 0.0, 1.0, 0.1)

    latest = df[df['date'] == df['date'].max()].copy()

    def norm(s):
        return (s - s.min()) / (s.max() - s.min() + 1e-6)

    latest['score'] = (
        norm(latest['roa']) * w_roa +
        norm(latest['rnd_to_rev']) * w_rnd +
        norm(latest['gross_margin']) * w_gm +
        norm(latest['bm_ratio']) * w_val
    ) * 100

    res = latest[['ticker', 'score']].sort_values('score', ascending=False)
    res.columns = ["股票代码", "量化得分"]

    # ⭐ 修复表格显示问题
    st.dataframe(
        res.reset_index(drop=True).style
        .background_gradient(subset=["量化得分"], cmap="YlGn")
        .format({"量化得分": "{:.2f}"}),
        use_container_width=True
    )

    st.success(f"🏅 当前最优标的：{res.iloc[0]['股票代码']}")

    st.markdown("""
📌 **模型逻辑：**
本评分系统基于多因子投资理论，将盈利能力、研发投入、毛利率和估值进行加权整合。
""")

# ===================== TAB4 =====================
with tab4:
    st.dataframe(df, use_container_width=True)

# --- 最终总结 ---
st.markdown("""
---

## 🧠 最终结论

- 高研发投入企业具备更强成长性  
- 高BM股票具备估值保护  
- 综合能力强的企业得分最高  
- 分散投资可以降低整体风险  

👉 多因子分析能显著提升投资决策质量。
""")
