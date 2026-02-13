Executive Summary: Superstore Sales & Profit Analysis

Project Overview

Objective: Analyze 9,995 retail transactions to identify profit optimization opportunities and provide data-driven business recommendations.

Tools: SQL (SQLite), Python (Pandas, Matplotlib), Jupyter Notebook  
Author: Yusuf Ehtesham  
Date: February 2026


Key Findings

1. CRITICAL: Loss-Making Products

Three sub-categories are actively losing money:

Sub-Category: Tables
Sales: $206,965
Loss: -$17,725
Margin: -8.56%

Sub-Category: Bookcases
Sales: $114,880
Loss: -$3,473
Margin: -3.02%

Sub-Category: Supplies
Sales: $46,674
Loss: -$1,189
Margin: -2.55%

Total Annual Loss: $22,387

Immediate Action Required: These products are destroying profitability despite generating $368,000 in revenue.


2. Discount Strategy Issues

Products with discounts over 30% have negative or minimal profit margins
Transactions with no discount show 15-20% higher margins
High discounts on Furniture are the primary cause of losses
Estimated annual loss from excessive discounting: $15,000-$20,000

Recommendation: Cap all discounts at 20% maximum, especially for low-margin categories.


3. Category Performance Analysis

Category: Technology
Sales: $836,154
Profit: $145,455
Margin: 17.40%
Status: Strong

Category: Office Supplies
Sales: $719,047
Profit: $122,491
Margin: 17.04%
Status: Strong

Category: Furniture
Sales: $741,999
Profit: $18,451
Margin: 2.49%
Status: Weak

Insight: Furniture generates high revenue but contributes only 6.4% of total profit due to excessive discounting and loss-making products.


4. Regional Performance

Best Performing Regions: West and East regions lead in both sales and profitability
Profit margins consistent across regions at 11-13%
Geographic expansion opportunity exists in underperforming areas


5. Customer Insights

Customer Retention Crisis:
- 48-52% of customers make only ONE purchase and never return
- High customer acquisition costs not being recovered
- Top 10 customers contribute 10-15% of total revenue
- At-risk customers: 20+ valuable customers haven't purchased in 180+ days

Potential Lost Revenue: $50,000-$100,000 annually from churn


6. Seasonality Patterns

Key Findings:
- November-December: Highest sales (holiday season)
- Q4: Strongest quarter consistently
- Weekday patterns: Mid-week shows higher order values
- Monthly variation: 40-50% between peak and low months

Opportunity: Plan inventory and marketing around seasonal peaks.


7. Shipping Performance

Standard Class: Most popular (60% of orders), most profitable
Same Day: Low volume but high order values
Average shipping time: 4-5 days across modes
No significant profit difference by shipping mode


Strategic Recommendations

IMMEDIATE ACTIONS (Next 30 Days)

1. Product Portfolio Cleanup

Discontinue Tables sub-category → Save $17,725 annually
Reprice or discontinue Bookcases → Save $3,473 annually
Investigate Supplies losses → Save $1,189 annually
Expected Impact: $22,387 profit increase (7.6%)

2. Discount Policy Reform

Cap all discounts at 20% (currently some go to 40-80%)
Eliminate discounts on Furniture (already low margin)
Focus discounts on Technology (high margin products)
Expected Impact: $15,000-$20,000 profit increase (5-7%)

3. Customer Retention Program

Email campaign for one-time buyers (within 30 days of purchase)
10% welcome-back offer for second purchase
VIP program for customers with 7+ orders
Expected Impact: 15-20% reduction in churn rate


MEDIUM-TERM ACTIONS (Next 90 Days)

4. Re-engagement Campaign

Target 20+ at-risk valuable customers (no purchase in 180+ days)
Potential recovery: $50,000-$70,000 in lifetime value
Personal outreach from account managers
Exclusive "We Miss You" offers

5. Product Mix Optimization

Increase inventory of Technology products (highest margin)
Reduce inventory of Furniture (lowest margin)
Shift marketing budget to high-margin categories
Expected Impact: 10-15% improvement in overall margin

6. Seasonal Planning

Stock up in Q3 for Q4 holiday rush
Increase marketing in Nov-Dec (peak season)
Adjust staffing for seasonal demand
Expected Impact: Capture 10-20% more seasonal revenue


LONG-TERM STRATEGIC ACTIONS (Next 6-12 Months)

7. Customer Segmentation Strategy

Consumer Segment: Focus on retention (largest base)
Corporate Segment: Develop B2B exclusive offerings
Home Office: Target with small-business bundles

8. Regional Expansion

Analyze success factors in West/East regions
Replicate in underperforming regions
Expected Impact: 15-25% revenue growth

9. Data-Driven Culture

Implement monthly performance dashboards
Real-time profitability tracking by product
Automated alerts for loss-making transactions


Financial Impact Summary

Action: Eliminate loss-making products
Profit Increase: +$22,387
Timeline: Immediate

Action: Optimize discount strategy
Profit Increase: +$17,500
Timeline: 30 days

Action: Customer retention program
Profit Increase: +$30,000
Timeline: 90 days

Action: Product mix optimization
Profit Increase: +$25,000
Timeline: 90 days

Action: Re-engage at-risk customers
Profit Increase: +$15,000
Timeline: 90 days

Total Potential Increase: +$109,887
Timeline: 12 months

Current Annual Profit: approximately $286,000  
Projected Annual Profit: approximately $396,000  
Improvement: 38.4% increase


Technical Approach

Data Analysis Workflow:

1. Data Loading: CSV to SQLite database (9,995 records)
2. Data Cleaning: Date parsing, type validation, null handling
3. SQL Analysis: 20+ complex queries (window functions, CTEs, aggregations)
4. Python Analysis: Pandas for manipulation, Matplotlib for visualization
5. Business Intelligence: Insight extraction and recommendation generation

SQL Techniques Demonstrated:

Window functions (RANK, ROW_NUMBER, LAG, LEAD)
Common Table Expressions (CTEs)
Complex aggregations and GROUP BY
Date/time functions
CASE statements for bucketing
Subqueries and joins

Python Skills Demonstrated:

Database connectivity (sqlite3, sqlalchemy)
Data manipulation (Pandas)
Data visualization (Matplotlib, Seaborn)
Statistical analysis
Jupyter notebooks for interactive analysis


Visualizations Created

Total: 13 Professional Charts

1. Yearly sales and profit trends
2. Regional performance comparison (4-panel)
3. Category sales and profit analysis
4. Loss-making products identification
5. Customer segmentation distribution
6. Top customers ranking
7. Discount impact analysis (4-panel)
8. Monthly discount and margin trends
9. Day-of-week performance
10. Monthly seasonality patterns
11. Quarterly performance trends
12. Customer purchase frequency distribution
13. Customer lifetime value analysis


Business Value Delivered

Identified critical profit leaks ($22K annual loss)  
Quantified discount inefficiencies ($17K potential savings)  
Revealed customer retention issues (50% one-time buyers)  
Discovered seasonality patterns for inventory planning  
Provided actionable roadmap for 38% profit improvement  
Created reusable analysis framework for ongoing monitoring  


Data Quality and Limitations

Data Quality:
- No missing values in critical fields
- Date fields validated and parsed correctly
- Numerical fields within expected ranges
- 9,995 complete transaction records

Limitations:
- Analysis based on historical data (past performance)
- External factors (competition, economy) not included
- Customer acquisition costs not available in dataset
- Product costs not itemized (margin calculated on totals)

Recommendations for Future Analysis:
- Include customer acquisition cost (CAC) data
- Add product cost data for true margin calculation
- Integrate competitor pricing information
- Add customer satisfaction/NPS scores


Skills Demonstrated

Technical Skills:
- SQL (SQLite): Database design, complex queries, optimization
- Python: Data analysis, visualization, scripting
- Data Visualization: Chart design, storytelling with data
- Statistical Analysis: Trend analysis, correlation, segmentation
- Version Control: Git/GitHub workflow

Business Skills:
- Business intelligence and insight extraction
- Financial analysis and profit optimization
- Customer segmentation and retention strategy
- Strategic recommendation development
- Executive communication and reporting


Project Repository

GitHub: https://github.com/yusufehtesham29/superstore-sql-python-portfolio

Project Structure:

data/                    Source dataset
database/                SQLite database
sql_queries/            5 organized SQL files
scripts/                5 Python analysis scripts
notebooks/              Jupyter notebook
visualizations/         13 charts
README.md               Project documentation
EXECUTIVE_SUMMARY.md    This document
requirements.txt        Dependencies


Conclusion

This analysis demonstrates end-to-end data analytics capabilities, from database design through insight generation to strategic recommendation. The identification of $22,000 in preventable losses and a roadmap to 38% profit improvement showcases the tangible business value of data-driven decision making.

The project serves as a portfolio piece demonstrating proficiency in SQL, Python, data visualization, and business analysis—essential skills for data analyst and business intelligence roles.


Prepared by: Yusuf Ehtesham  
Contact: [Your Email] | [LinkedIn] | GitHub: @yusufehtesham29  
Date: February 2026

"Turning data into actionable insights that drive business results."
