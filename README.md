# TechQuant Pro: Multi-Factor Analysis of US Tech Stocks

---

## 1. Problem & User

Most retail investment platforms focus heavily on price trends or single indicators, which makes it difficult for users to form a structured and well-rounded investment decision. This often leads to biased or incomplete analysis, as important financial dimensions such as profitability and valuation are ignored.

This project targets **retail investors, finance/economics students, and junior analysts**. It provides an interactive platform that integrates multiple financial indicators into a unified system, helping users make more informed and systematic investment decisions.

---

## 2. Data

- **Source**: WRDS (Wharton Research Data Services)  
- **Databases Used**: CRSP (market data) and Compustat (financial fundamentals)  
- **Access Date**: Apr 20, 2026  

The dataset covers the **top 50 US technology companies** over the period **2010–2025**, providing a long-term perspective on firm performance across different market cycles.

file_path = os.path.join("wrds_output_v3", "us_tech_top50_2026.csv")

### Key Variables

- `prc` — Stock price  
  → Represents market valuation over time and is used for trend analysis.  

- `ret` — Monthly return  
  → Captures investment performance and is used for risk-return analysis.  

- `roa` — Return on assets  
  → Measures how efficiently a firm generates profit from its assets, reflecting operational quality.  

- `gross_margin` — Gross margin  
  → Indicates cost efficiency and pricing power, which are critical for long-term competitiveness.  

- `rnd_to_rev` — R&D intensity  
  → Reflects the firm’s investment in innovation, particularly important in the technology sector.  

- `bm_ratio` — Book-to-market ratio  
  → Serves as a valuation metric, where higher values may indicate undervaluation.  

The dataset is constructed by linking CRSP and Compustat via the CCM table, with a **6-month reporting lag** applied to financial data to better reflect real-world information availability.

---

## 3. Methods

### 1. Data Extraction

Data is retrieved directly from WRDS using SQL queries. CRSP provides monthly stock prices and returns, while Compustat provides firm-level financial statements. These datasets are merged using the CCM linking table to ensure accurate alignment between market and accounting data.

### 2. Feature Engineering

Key financial indicators are constructed to capture different dimensions of firm performance:

- Profitability (ROA) reflects how efficiently firms generate earnings  
- Innovation (R&D intensity) captures long-term growth potential  
- Margin (gross margin) measures operational strength  
- Valuation (book-to-market ratio) identifies potential mispricing  

In addition, a 12-month rolling volatility measure is computed to capture risk.

### 3. Data Processing

The dataset is cleaned by handling missing values and ensuring consistent time alignment. All variables are normalized using min-max scaling to make them comparable, as raw financial metrics operate on different scales.

### 4. Multi-Factor Model

A composite score is constructed as:

Score = w₁·ROA + w₂·R&D + w₃·Margin + w₄·B/M

Each weight is user-defined, allowing flexibility across different investment styles. This transforms the model into a customizable tool rather than a fixed ranking system.

### 5. Visualization

The results are presented through an interactive Streamlit dashboard:

- Time-series charts show how firm performance evolves  
- Risk-return scatter plots illustrate trade-offs  
- Correlation heatmaps support diversification analysis  
- Ranking tables provide clear investment signals  

---

## 4. Key Findings

- **R&D intensity is a strong driver of growth**  
  Companies that consistently invest in R&D tend to perform better over the long term, especially in the technology sector where innovation is critical.

- **High profitability and margins lead to better rankings**  
  Firms with strong ROA and stable margins are consistently ranked higher, indicating that operational efficiency plays a key role in valuation.

- **Risk-return trade-off is clearly observed**  
  Stocks with higher average returns tend to exhibit higher volatility, confirming the fundamental finance principle that higher returns come with higher risk.

- **Diversification depends on correlation structure**  
  Correlation analysis shows that not all tech stocks move together, and selecting low-correlation assets can significantly reduce portfolio risk.

- **Multi-factor models provide more stable insights**  
  Compared to single indicators, the multi-factor approach produces more balanced and interpretable rankings, reducing noise from any one metric.

---

## 5. How to Run

### Install dependencies

pip install -r requirements.txt

This installs all required Python libraries including pandas, numpy, plotly, and streamlit.

### Launch the application

streamlit run app.py

This command starts the interactive dashboard locally in your browser.

### Notes

- Ensure the dataset file (`us_tech_top50_2026.csv`) is placed in the correct directory  
- WRDS connection is only required if you want to regenerate the dataset  
- The app is fully functional with the provided dataset  

---

## 6. Product Link / Demo

-  Interactive dashboard built with Streamlit  
  → Users can explore trends, adjust model weights, and view rankings in real time
  
-  GitHub repository  

---

## 7. Limitations & Next Steps

### Limitations

- **Limited stock universe**  
  The analysis focuses only on 50 technology firms, which may introduce selection bias and limit applicability to other sectors.

- **Lagged financial data**  
  Financial variables are delayed to reflect reporting cycles, which may reduce responsiveness to recent changes.

- **Simplified factor model**  
  Only four factors are included, while real-world models often incorporate additional signals such as momentum and liquidity.

- **Subjective weight selection**  
  User-defined weights introduce bias, as results depend on personal preferences rather than optimization.

- **Linear assumption**  
  The model assumes linear relationships between variables, which may oversimplify real-world financial dynamics.

### Next Steps

- **Add more factors**  
  Incorporate momentum, volatility, and sentiment indicators to enhance model robustness.

- **Use machine learning models**  
  Apply non-linear methods to capture more complex relationships between variables.

- **Portfolio optimization**  
  Extend the model to construct optimal portfolios rather than just ranking stocks.

- **Expand dataset**  
  Include more sectors or global markets to improve generalizability.

- **Integrate macroeconomic data**  
  Add variables such as interest rates and inflation to better reflect market conditions.

---

