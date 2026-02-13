"""
============================================================================
FILE: 02_sql_analysis.py
PURPOSE: Execute SQL queries and display results using Python
AUTHOR: yusufehtesham29
============================================================================
"""

import pandas as pd
import sqlite3
import os

print("="*80)
print("SUPERSTORE SQL ANALYSIS")
print("="*80)

# ============================================================================
# Connect to Database
# ============================================================================
print("\n[1] Connecting to database...")

db_path = 'database/superstore.db'

if not os.path.exists(db_path):
    print(f"❌ Error: Database not found at {db_path}")
    print("Please run 01_database_setup.py first")
    exit(1)

conn = sqlite3.connect(db_path)
print(f"✅ Connected to: {db_path}\n")

# ============================================================================
# BUSINESS METRICS QUERIES
# ============================================================================
print("="*80)
print("SECTION 1: BUSINESS METRICS")
print("="*80)

# Query 1: Overall Business Performance
print("\n[Query 1] Overall Business Performance")
print("-"*80)

query1 = """
SELECT 
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent,
    SUM(quantity) AS total_quantity_sold,
    ROUND(AVG(sales), 2) AS avg_order_value,
    ROUND(AVG(profit), 2) AS avg_profit_per_order
FROM superstore;
"""

df1 = pd.read_sql_query(query1, conn)
print(df1.to_string(index=False))

print("\n💡 Business Insight:")
print(f"   • Total Revenue: ${df1['total_sales'].values[0]:,.2f}")
print(f"   • Total Profit: ${df1['total_profit'].values[0]:,.2f}")
print(f"   • Profit Margin: {df1['profit_margin_percent'].values[0]:.2f}%")
print(f"   • Average Order Value: ${df1['avg_order_value'].values[0]:,.2f}")

# Query 2: Sales and Profit by Year
print("\n\n[Query 2] Sales and Profit by Year")
print("-"*80)

query2 = """
SELECT 
    CAST(strftime('%Y', order_date) AS INTEGER) AS year,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY year
ORDER BY year;
"""

df2 = pd.read_sql_query(query2, conn)
print(df2.to_string(index=False))

print("\n💡 Business Insight:")
if len(df2) > 1:
    sales_growth = ((df2['total_sales'].iloc[-1] - df2['total_sales'].iloc[0]) / 
                    df2['total_sales'].iloc[0] * 100)
    print(f"   • Sales Growth: {sales_growth:.2f}% from {df2['year'].iloc[0]} to {df2['year'].iloc[-1]}")
    print(f"   • Best Year: {df2.loc[df2['total_profit'].idxmax(), 'year']} (${df2['total_profit'].max():,.2f} profit)")

# Query 3: Sales and Profit by Region
print("\n\n[Query 3] Sales and Profit by Region")
print("-"*80)

query3 = """
SELECT 
    region,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent,
    ROUND(AVG(sales), 2) AS avg_sales_per_order
FROM superstore
GROUP BY region
ORDER BY total_sales DESC;
"""

df3 = pd.read_sql_query(query3, conn)
print(df3.to_string(index=False))

print("\n💡 Business Insight:")
print(f"   • Top Region by Sales: {df3.iloc[0]['region']} (${df3.iloc[0]['total_sales']:,.2f})")
print(f"   • Most Profitable Region: {df3.loc[df3['total_profit'].idxmax(), 'region']}")
print(f"   • Highest Profit Margin: {df3.loc[df3['profit_margin_percent'].idxmax(), 'region']} ({df3['profit_margin_percent'].max():.2f}%)")

# Query 4: Sales and Profit by Category
print("\n\n[Query 4] Sales and Profit by Category")
print("-"*80)

query4 = """
SELECT 
    category,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent,
    SUM(quantity) AS units_sold
FROM superstore
GROUP BY category
ORDER BY total_profit DESC;
"""

df4 = pd.read_sql_query(query4, conn)
print(df4.to_string(index=False))

print("\n💡 Business Insight:")
print(f"   • Most Profitable Category: {df4.iloc[0]['category']} (${df4.iloc[0]['total_profit']:,.2f})")
print(f"   • Highest Volume: {df4.loc[df4['units_sold'].idxmax(), 'category']} ({df4['units_sold'].max():,} units)")

# Query 5: Sales and Profit by Sub-Category (Top 10)
print("\n\n[Query 5] Sales and Profit by Sub-Category (Top 10)")
print("-"*80)

query5 = """
SELECT 
    category,
    sub_category,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY category, sub_category
ORDER BY total_profit DESC
LIMIT 10;
"""

df5 = pd.read_sql_query(query5, conn)
print(df5.to_string(index=False))

print("\n💡 Business Insight:")
print(f"   • Top Sub-Category: {df5.iloc[0]['sub_category']} (${df5.iloc[0]['total_profit']:,.2f} profit)")

# Query 6: Loss-Making Sub-Categories
print("\n\n[Query 6] Loss-Making Sub-Categories ⚠️")
print("-"*80)

query6 = """
SELECT 
    category,
    sub_category,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY category, sub_category
HAVING SUM(profit) < 0
ORDER BY total_profit ASC;
"""

df6 = pd.read_sql_query(query6, conn)

if len(df6) > 0:
    print(df6.to_string(index=False))
    print("\n⚠️  Critical Insight:")
    print(f"   • {len(df6)} sub-categories are LOSING MONEY!")
    print(f"   • Worst Performer: {df6.iloc[0]['sub_category']} (${df6.iloc[0]['total_profit']:,.2f} loss)")
    print(f"   • Total Loss: ${df6['total_profit'].sum():,.2f}")
    print(f"   • Action Required: Review pricing, discounts, or discontinue these products")
else:
    print("✅ No loss-making sub-categories found!")

# ============================================================================
# CUSTOMER ANALYSIS QUERIES
# ============================================================================
print("\n\n" + "="*80)
print("SECTION 2: CUSTOMER ANALYSIS")
print("="*80)

# Query 7: Top 10 Customers by Sales
print("\n[Query 7] Top 10 Customers by Sales")
print("-"*80)

query7 = """
SELECT 
    customer_id,
    customer_name,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(sales), 2) AS avg_order_value
FROM superstore
GROUP BY customer_id, customer_name
ORDER BY total_sales DESC
LIMIT 10;
"""

df7 = pd.read_sql_query(query7, conn)
print(df7.to_string(index=False))

print("\n💡 Business Insight:")
print(f"   • Top Customer: {df7.iloc[0]['customer_name']} (${df7.iloc[0]['total_sales']:,.2f})")
print(f"   • Average Orders per VIP: {df7['total_orders'].mean():.1f} orders")

# Query 8: Customer Segmentation
print("\n\n[Query 8] Customer Segmentation Analysis")
print("-"*80)

query8 = """
SELECT 
    segment,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(sales), 2) AS avg_order_value,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY segment
ORDER BY total_sales DESC;
"""

df8 = pd.read_sql_query(query8, conn)
print(df8.to_string(index=False))

print("\n💡 Business Insight:")
print(f"   • Largest Segment: {df8.iloc[0]['segment']} ({df8.iloc[0]['total_customers']:,} customers)")
print(f"   • Most Profitable: {df8.loc[df8['total_profit'].idxmax(), 'segment']}")

# ============================================================================
# PRODUCT ANALYSIS QUERIES
# ============================================================================
print("\n\n" + "="*80)
print("SECTION 3: PRODUCT ANALYSIS")
print("="*80)

# Query 9: Top 10 Products by Profit
print("\n[Query 9] Top 10 Products by Profit")
print("-"*80)

query9 = """
SELECT 
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY product_name, category, sub_category
ORDER BY total_profit DESC
LIMIT 10;
"""

df9 = pd.read_sql_query(query9, conn)
print(df9.to_string(index=False))

# Query 10: Discount Impact Analysis
print("\n\n[Query 10] Discount Impact on Profitability")
print("-"*80)

query10 = """
SELECT 
    CASE 
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount > 0 AND discount <= 0.1 THEN '1-10% Discount'
        WHEN discount > 0.1 AND discount <= 0.2 THEN '11-20% Discount'
        WHEN discount > 0.2 AND discount <= 0.3 THEN '21-30% Discount'
        ELSE 'Over 30% Discount'
    END AS discount_range,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_percent,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY discount_range
ORDER BY avg_discount_percent;
"""

df10 = pd.read_sql_query(query10, conn)
print(df10.to_string(index=False))

print("\n💡 Business Insight:")
print(f"   • Higher discounts correlate with lower profit margins")
no_discount_margin = df10[df10['discount_range'] == 'No Discount']['profit_margin_percent'].values
if len(no_discount_margin) > 0:
    print(f"   • No Discount Profit Margin: {no_discount_margin[0]:.2f}%")

# Query 11: Sales by Ship Mode
print("\n\n[Query 11] Sales by Shipping Mode")
print("-"*80)

query11 = """
SELECT 
    ship_mode,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(sales), 2) AS avg_order_value
FROM superstore
GROUP BY ship_mode
ORDER BY total_sales DESC;
"""

df11 = pd.read_sql_query(query11, conn)
print(df11.to_string(index=False))

print("\n💡 Business Insight:")
print(f"   • Most Popular: {df11.iloc[0]['ship_mode']} ({df11.iloc[0]['total_orders']:,} orders)")

# ============================================================================
# Close Database Connection
# ============================================================================
conn.close()

print("\n\n" + "="*80)
print("SQL ANALYSIS COMPLETED SUCCESSFULLY!")
print("="*80)
print("\n📊 All queries executed and results displayed above")
print("✅ Next step: Open Jupyter Notebook for visualizations")
print("\nTo create visualizations, run:")
print("   jupyter notebook notebooks/superstore_analysis.ipynb")
