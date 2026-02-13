"""
============================================================================
FILE: 04_time_series_analysis.py
PURPOSE: Analyze sales patterns, seasonality, and time-based trends
AUTHOR: yusufehtesham29
============================================================================
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

print("="*80)
print("TIME-SERIES & SEASONALITY ANALYSIS")
print("="*80)

conn = sqlite3.connect('database/superstore.db')

# ============================================================================
# ANALYSIS 1: Day of Week Performance
# ============================================================================
print("\n" + "="*80)
print("SECTION 1: SALES BY DAY OF WEEK")
print("="*80)

query1 = """
SELECT 
    CASE CAST(strftime('%w', order_date) AS INTEGER)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day_of_week,
    CAST(strftime('%w', order_date) AS INTEGER) AS day_num,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(sales), 2) AS avg_order_value
FROM superstore
GROUP BY day_num
ORDER BY day_num;
"""

df_dow = pd.read_sql_query(query1, conn)
print("\n[Analysis 1] Sales Performance by Day of Week:")
print(df_dow[['day_of_week', 'orders', 'total_sales', 'total_profit', 'avg_order_value']].to_string(index=False))

best_day = df_dow.loc[df_dow['total_sales'].idxmax()]
print(f"\n💡 Insight:")
print(f"   • Best Day: {best_day['day_of_week']} (${best_day['total_sales']:,.2f})")

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Chart 1: Orders by Day
axes[0, 0].bar(df_dow['day_of_week'], df_dow['orders'], color='steelblue')
axes[0, 0].set_title('Orders by Day of Week', fontweight='bold')
axes[0, 0].set_ylabel('Number of Orders')
axes[0, 0].tick_params(axis='x', rotation=45)
for i, v in enumerate(df_dow['orders']):
    axes[0, 0].text(i, v, str(v), ha='center', va='bottom')

# Chart 2: Sales by Day
axes[0, 1].bar(df_dow['day_of_week'], df_dow['total_sales'], color='green', alpha=0.7)
axes[0, 1].set_title('Sales by Day of Week', fontweight='bold')
axes[0, 1].set_ylabel('Total Sales ($)')
axes[0, 1].tick_params(axis='x', rotation=45)

# Chart 3: Avg Order Value
axes[1, 0].plot(df_dow['day_of_week'], df_dow['avg_order_value'], marker='o', linewidth=2, color='purple')
axes[1, 0].set_title('Average Order Value by Day', fontweight='bold')
axes[1, 0].set_ylabel('Avg Order Value ($)')
axes[1, 0].tick_params(axis='x', rotation=45)
axes[1, 0].grid(True, alpha=0.3)

# Chart 4: Profit by Day
axes[1, 1].bar(df_dow['day_of_week'], df_dow['total_profit'], color='orange', alpha=0.7)
axes[1, 1].set_title('Profit by Day of Week', fontweight='bold')
axes[1, 1].set_ylabel('Total Profit ($)')
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('visualizations/09_day_of_week_analysis.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n✅ Visualization saved: 09_day_of_week_analysis.png")

# ============================================================================
# ANALYSIS 2: Monthly Seasonality
# ============================================================================
print("\n" + "="*80)
print("SECTION 2: MONTHLY SEASONALITY PATTERNS")
print("="*80)

query2 = """
SELECT 
    CAST(strftime('%m', order_date) AS INTEGER) AS month_num,
    CASE CAST(strftime('%m', order_date) AS INTEGER)
        WHEN 1 THEN 'January' WHEN 2 THEN 'February' WHEN 3 THEN 'March'
        WHEN 4 THEN 'April' WHEN 5 THEN 'May' WHEN 6 THEN 'June'
        WHEN 7 THEN 'July' WHEN 8 THEN 'August' WHEN 9 THEN 'September'
        WHEN 10 THEN 'October' WHEN 11 THEN 'November' WHEN 12 THEN 'December'
    END AS month_name,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM superstore
GROUP BY month_num
ORDER BY month_num;
"""

df_monthly = pd.read_sql_query(query2, conn)
print("\n[Analysis 2] Sales by Month:")
print(df_monthly[['month_name', 'orders', 'total_sales', 'total_profit']].to_string(index=False))

peak_month = df_monthly.loc[df_monthly['total_sales'].idxmax()]
low_month = df_monthly.loc[df_monthly['total_sales'].idxmin()]
print(f"\n💡 Seasonality Insights:")
print(f"   • Peak Month: {peak_month['month_name']} (${peak_month['total_sales']:,.2f})")
print(f"   • Lowest Month: {low_month['month_name']} (${low_month['total_sales']:,.2f})")
print(f"   • Variation: {((peak_month['total_sales'] - low_month['total_sales']) / low_month['total_sales'] * 100):.1f}%")

# Visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))

# Sales by Month
ax1.plot(df_monthly['month_name'], df_monthly['total_sales'], marker='o', linewidth=2.5, color='blue', markersize=8)
ax1.fill_between(range(len(df_monthly)), df_monthly['total_sales'], alpha=0.3, color='blue')
ax1.set_title('Monthly Sales Seasonality', fontweight='bold', fontsize=14)
ax1.set_ylabel('Total Sales ($)')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, alpha=0.3)
ax1.axhline(y=df_monthly['total_sales'].mean(), color='red', linestyle='--', label=f"Average: ${df_monthly['total_sales'].mean():,.0f}")
ax1.legend()

# Profit by Month
ax2.bar(df_monthly['month_name'], df_monthly['total_profit'], color='green', alpha=0.7)
ax2.set_title('Monthly Profit Patterns', fontweight='bold', fontsize=14)
ax2.set_ylabel('Total Profit ($)')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('visualizations/10_monthly_seasonality.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n✅ Visualization saved: 10_monthly_seasonality.png")

# ============================================================================
# ANALYSIS 3: Shipping Time Analysis
# ============================================================================
print("\n" + "="*80)
print("SECTION 3: SHIPPING TIME PERFORMANCE")
print("="*80)

query3 = """
SELECT 
    ship_mode,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(AVG(JULIANDAY(ship_date) - JULIANDAY(order_date)), 1) AS avg_ship_days,
    ROUND(MIN(JULIANDAY(ship_date) - JULIANDAY(order_date)), 1) AS min_ship_days,
    ROUND(MAX(JULIANDAY(ship_date) - JULIANDAY(order_date)), 1) AS max_ship_days,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(sales), 2) AS avg_order_value
FROM superstore
GROUP BY ship_mode
ORDER BY avg_ship_days;
"""

df_shipping = pd.read_sql_query(query3, conn)
print("\n[Analysis 3] Shipping Performance by Mode:")
print(df_shipping.to_string(index=False))

print(f"\n💡 Shipping Insights:")
for _, row in df_shipping.iterrows():
    print(f"   • {row['ship_mode']}: Avg {row['avg_ship_days']:.1f} days, Avg Order ${row['avg_order_value']:,.2f}")

# ============================================================================
# ANALYSIS 4: Quarter Performance
# ============================================================================
print("\n" + "="*80)
print("SECTION 4: QUARTERLY PERFORMANCE")
print("="*80)

query4 = """
SELECT 
    CAST(strftime('%Y', order_date) AS INTEGER) AS year,
    CASE 
        WHEN CAST(strftime('%m', order_date) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
        WHEN CAST(strftime('%m', order_date) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
        WHEN CAST(strftime('%m', order_date) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
        ELSE 'Q4'
    END AS quarter,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY year, quarter
ORDER BY year, quarter;
"""

df_quarterly = pd.read_sql_query(query4, conn)
print("\n[Analysis 4] Quarterly Performance:")
print(df_quarterly.to_string(index=False))

# Create year-quarter label
df_quarterly['year_quarter'] = df_quarterly['year'].astype(str) + '-' + df_quarterly['quarter']

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Sales by Quarter
ax1.bar(df_quarterly['year_quarter'], df_quarterly['total_sales'], color='teal', alpha=0.7)
ax1.set_title('Quarterly Sales Performance', fontweight='bold', fontsize=14)
ax1.set_ylabel('Total Sales ($)')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(axis='y', alpha=0.3)

# Profit Margin by Quarter
ax2.plot(df_quarterly['year_quarter'], df_quarterly['profit_margin_percent'], 
         marker='o', linewidth=2.5, color='red', markersize=8)
ax2.set_title('Quarterly Profit Margin Trend', fontweight='bold', fontsize=14)
ax2.set_ylabel('Profit Margin (%)')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, alpha=0.3)
ax2.axhline(y=df_quarterly['profit_margin_percent'].mean(), color='black', linestyle='--', 
            label=f"Avg: {df_quarterly['profit_margin_percent'].mean():.2f}%")
ax2.legend()

plt.tight_layout()
plt.savefig('visualizations/11_quarterly_performance.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n✅ Visualization saved: 11_quarterly_performance.png")

print(f"\n💡 Quarterly Insight:")
best_q = df_quarterly.loc[df_quarterly['total_sales'].idxmax()]
print(f"   • Best Quarter: {best_q['year_quarter']} (${best_q['total_sales']:,.2f})")

conn.close()

print("\n" + "="*80)
print("TIME-SERIES ANALYSIS COMPLETED")
print("="*80)
