Reflective Report

1. Analytical Problem and Intended Audience  
The core analytical problem of this project was to design a structured, data-driven framework for evaluating the performance and investment potential of major U.S. technology companies. The technology sector is highly volatile and often influenced by narratives rather than fundamentals, making it difficult for investors to make rational decisions. Therefore, the objective was to reduce noise and provide a systematic multi-factor evaluation tool.

The intended audience includes undergraduate students studying finance or data science, beginner quantitative analysts, and individual investors who want to understand how financial data can be translated into actionable insights. The project also serves as a demonstration of how Python-based data analysis can support financial decision-making.

2. Dataset Selection and Rationale  
The dataset was obtained from WRDS (Wharton Research Data Services), combining CRSP and Compustat databases. CRSP provides reliable stock price and market capitalization data, while Compustat contains detailed firm-level financial statements such as revenue, net income, and R&D expenditure.

This dataset was chosen for three main reasons. First, it is academically rigorous and widely used in financial research, ensuring data credibility. Second, it provides both market and fundamental data, which is essential for multi-factor analysis. Third, the time span (2010–2025) captures multiple market cycles, including technological booms and downturns, making the analysis more robust.

3. Python Methods and Workflow  
The project followed a structured data analysis workflow implemented in Python.

- Data Cleaning and Preprocessing: Using pandas to handle missing values, standardize variables, and align different datasets.  
- Time Alignment: A backward-merge method was applied to match quarterly financial data with monthly stock returns, avoiding look-ahead bias.  
- Feature Engineering: Key financial indicators such as ROA, R&D intensity, gross margin, and book-to-market ratio were calculated.  
- Normalization: Min-Max scaling was used to standardize different metrics to a comparable range.  
- Scoring System: A multi-factor scoring model was built by combining normalized indicators.  
- Visualization: matplotlib and seaborn were used to generate charts, including correlation heatmaps.  
- Interface (Streamlit): The results were presented through an interactive interface.

4. Main Findings and Outputs  
Companies with consistently high R&D investment showed stronger long-term resilience. Correlation analysis revealed diversification benefits within the tech sector. The main output was an interactive dashboard displaying rankings and insights.

5. Difficulties and Challenges  
Challenges included missing data, aligning datasets with different frequencies, and building the Streamlit interface.

6. Solutions  
Missing data was handled with appropriate imputation. A backward matching logic avoided look-ahead bias. Documentation and iterative testing improved the interface.

7. Limitations and Improvements  
The model is relatively simple and limited to top 50 firms. Future improvements include adding more factors and using machine learning.

8. Learning Outcomes  
This project improved my understanding of financial data analysis, Python skills, and the importance of avoiding bias.

AI Disclosure
AI tools used: ChatGPT, Gemini  
Purpose: debugging, writing improvement, concept understanding  
Example prompts:  
- How to avoid look-ahead bias  
- Debug python merge issue

How used: I tested all suggestions in Python to ensure they ran correctly and produced expected results, making adjustments where necessary.

Model/version: ChatGPT-5.3, Gemini 3 Flash

Access date: April 2026
