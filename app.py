import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(page_title="TechQuant Pro 50", layout="wide")

st.title("TechQuant Pro: US Tech Top 50 Multi-Factor Analysis Terminal")
st.caption("2026 Edition | Professional Multi-Factor Investment Analytics Tool")


# --- 2. Data Loading ---
@st.cache_data
def load_data():
    """Load and preprocess the dataset from local paths."""
    paths = ["wrds_output_v3/us_tech_top50_2026.csv", "us_tech_top50_2026.csv"]
    file_path = next((p for p in paths if os.path.exists(p)), None)
    if not file_path:
        return None

    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df['ticker'] = df['ticker'].astype(str).str.strip()

    # Fill missing values and ensure sorting to prevent broken line charts
    cols = ['roa', 'gross_margin', 'rnd_to_rev', 'bm_ratio', 'prc', 'ret']
    df = df.sort_values(['ticker', 'date'])
    df[cols] = df.groupby('ticker')[cols].transform(
        lambda g: g.ffill().bfill().interpolate()
    )

    # Calculate Volatility (12-month rolling standard deviation)
    df['volatility'] = df.groupby('ticker')['ret'].rolling(12, min_periods=1).std().reset_index(0, drop=True)
    # Calculate Rolling Return (12-month average)
    df['rolling_return'] = df.groupby('ticker')['ret'].rolling(12, min_periods=1).mean().reset_index(0, drop=True)

    return df


df_raw = load_data()
if df_raw is None:
    st.error("❌ Data file not found. Please ensure the CSV is in the directory.");
    st.stop()

# --- 3. Sidebar Control Panel ---
st.sidebar.header("🕹️ Control Panel")
all_tickers = sorted(df_raw['ticker'].unique())
default_list = ["NVDA", "AAPL", "MSFT", "PLTR", "SMCI"]
selected_tickers = st.sidebar.multiselect("Select Stocks", all_tickers,
                                          default=[t for t in default_list if t in all_tickers])

metric_map = {
    "prc": "Price", "ret": "Monthly Return", "roa": "ROA (Return on Assets)",
    "gross_margin": "Gross Margin", "rnd_to_rev": "R&D Intensity", "bm_ratio": "Book-to-Market"
}
selected_metric = st.sidebar.selectbox("Primary Metric", list(metric_map.keys()), format_func=lambda x: metric_map[x])

# Filter data based on selection
df = df_raw[df_raw['ticker'].isin(selected_tickers)].sort_values(['ticker', 'date'])

# --- 4. Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Trend Analysis",
    "🧬 Correlation",
    "🏆 Multi-Factor Model",
    "📋 Raw Data"
])

# ================= TAB 1: Trend Analysis =================
with tab1:
    fig = px.line(df, x='date', y=selected_metric, color='ticker',
                  title=f"Historical {metric_map[selected_metric]} Trend")
    fig.update_traces(connectgaps=True)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### ⚖️ Risk-Return Matrix")
    risk_df = df.groupby('ticker').agg({'ret': 'mean', 'volatility': 'mean'}).dropna().reset_index()
    risk_df['sharpe'] = risk_df['ret'] / (risk_df['volatility'] + 1e-6)

    col_chart, col_insight = st.columns([2, 1])
    with col_chart:
        st.plotly_chart(px.scatter(risk_df, x='volatility', y='ret', text='ticker', size='sharpe', color='sharpe'),
                        use_container_width=True)

    with col_insight:
        st.markdown("#### Automated Insights")
        latest_data = df[df['date'] == df['date'].max()]
        if not latest_data.empty:
            best_m = latest_data.sort_values(selected_metric, ascending=False).iloc[0]
            st.success(f"**Leader in {metric_map[selected_metric]}: {best_m['ticker']}**")
            best_s = risk_df.sort_values('sharpe', ascending=False).iloc[0]
            st.info(f"**Efficiency King: {best_s['ticker']}**")

# ================= TAB 2: Correlation Analysis (Updated) =================
with tab2:
    if len(selected_tickers) > 1:
        # Create Correlation Matrix
        corr = df.pivot_table(index='date', columns='ticker', values='ret').corr()

        col_mat, col_ana = st.columns([1.5, 1])

        with col_mat:
            st.plotly_chart(px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r'), use_container_width=True)

        with col_ana:
            st.markdown("#### 🤖 Correlation Intelligence")

            # Extract off-diagonal values to calculate average correlation
            mask = np.ones(corr.shape, dtype=bool)
            np.fill_diagonal(mask, 0)
            avg_corr = corr.values[mask].mean()

            st.metric("Average Portfolio Correlation", f"{avg_corr:.2f}")

            # Automated Interpretation
            if avg_corr > 0.7:
                st.warning(
                    "**High Concentration Risk:** Most selected stocks move in the same direction. Your portfolio lacks diversification.")
            elif 0.4 <= avg_corr <= 0.7:
                st.info(
                    "**Moderate Diversification:** There is a notable link between these stocks, common in the tech sector, but some idiosyncratic movement exists.")
            else:
                st.success(
                    "**Strong Diversification:** These stocks show low correlation, which helps in reducing overall portfolio volatility.")

            # Identify most/least correlated pairs
            corr_pairs = corr.unstack().sort_values(ascending=False).drop_duplicates()
            corr_pairs = corr_pairs[corr_pairs < 0.99]  # Exclude self-correlation

            st.write(
                f"**Highest Link:** {corr_pairs.index[0][0]} & {corr_pairs.index[0][1]} ({corr_pairs.iloc[0]:.2f})")
            st.write(
                f"**Best Pair for Hedging:** {corr_pairs.index[-1][0]} & {corr_pairs.index[-1][1]} ({corr_pairs.iloc[-1]:.2f})")
    else:
        st.warning("Please select at least 2 stocks to view the correlation matrix.")

# ================= TAB 3: Multi-Factor Model =================
with tab3:
    st.subheader("Multi-Factor Scoring Engine")
    c1, c2, c3, c4 = st.columns(4)
    w_roa = c1.slider("Profitability (ROA)", 0.0, 1.0, 0.4)
    w_rnd = c2.slider("Innovation (R&D)", 0.0, 1.0, 0.3)
    w_gm = c3.slider("Efficiency (Margin)", 0.0, 1.0, 0.2)
    w_val = c4.slider("Valuation (B/M)", 0.0, 1.0, 0.1)

    latest = df[df['date'] == df['date'].max()].copy()
    if not latest.empty:
        def zscore(s):
            return (s - s.mean()) / (s.std() + 1e-6)


        latest['score'] = (zscore(latest['roa']) * w_roa + zscore(latest['rnd_to_rev']) * w_rnd +
                           zscore(latest['gross_margin']) * w_gm + zscore(latest['bm_ratio']) * w_val)

        res = latest[['ticker', 'score', 'roa', 'rnd_to_rev', 'gross_margin', 'bm_ratio']].sort_values('score',
                                                                                                       ascending=False)
        res = res.reset_index(drop=True)
        res.index = res.index + 1
        res.index.name = "Rank"

        col_table, col_ana = st.columns([1.5, 1])
        with col_table:
            st.dataframe(res[['ticker', 'score']], use_container_width=True)

        with col_ana:
            st.markdown("#### Why is 1 Ranked Best?")
            top_stock = res.iloc[0]
            drivers = []
            if top_stock['roa'] > latest['roa'].mean(): drivers.append("Superior Profitability")
            if top_stock['rnd_to_rev'] > latest['rnd_to_rev'].mean(): drivers.append("High R&D Reinvestment")
            if top_stock['gross_margin'] > latest['gross_margin'].mean(): drivers.append("Strong Margins")

            st.success(f"**Top Ranked: {top_stock['ticker']}**")
            for d in drivers:
                st.write(f"✅ {d}")
            st.write(
                f"**{top_stock['ticker']}** leads due to its dominant statistical profile across your weighted factors.")

# ================= TAB 4: Raw Data =================
with tab4:
    st.dataframe(df.reset_index(drop=True), use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("2026 TechQuant Pro | Research Terminal | Data: WRDS")

