"""
============================================================================
FILE: 03_discount_analysis.py
PURPOSE: Deep dive into discount strategy and its impact on profitability
AUTHOR: yusufehtesham29
============================================================================
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

print("="*80)
print("ADVANCED DISCOUNT ANALYSIS")
print("="*80)

# Connect to database
conn = sqlite3.connect('database/superstore.db')

# ============================================================================
# ANALYSIS 1: Discount vs Profit Correlation
# ============================================================================
print("\n" + "="*80)
print("SECTION 1: DISCOUNT IMPACT ON PROFITABILITY")
print("="*80)

query1 = """
SELECT 
    CASE 
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount > 0 AND discount <= 0.1 THEN '1-10%'
        WHEN discount > 0.1 AND discount <= 0.2 THEN '11-20%'
        WHEN discount > 0.2 AND discount <= 0.3 THEN '21-30%'
        WHEN discount > 0.3 AND discount <= 0.4 THEN '31-40%'
        ELSE 'Over 40%'
    END AS discount_range,
    COUNT(*) AS transaction_count,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_percent,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(sales), 2) AS avg_transaction_value,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY discount_range
ORDER BY avg_discount_percent;
"""

df_discount = pd.read_sql_query(query1, conn)
print("\n[Analysis 1] Discount Impact Summary:")
print(df_discount.to_string(index=False))

print("\n💡 Key Insights:")
no_discount_margin = df_discount[df_discount['discount_range'] == 'No Discount']['profit_margin_percent'].values[0]
high_discount_margin = df_discount[df_discount['avg_discount_percent'] > 30]['profit_margin_percent'].values
if len(high_discount_margin) > 0:
    print(f"   • No Discount Margin: {no_discount_margin:.2f}%")
    print(f"   • High Discount Margin: {high_discount_margin[0]:.2f}%")
    print(f"   • Margin Degradation: {no_discount_margin - high_discount_margin[0]:.2f}% points")

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Chart 1: Sales by Discount Range
axes[0, 0].bar(range(len(df_discount)), df_discount['total_sales'], color='skyblue')
axes[0, 0].set_xticks(range(len(df_discount)))
axes[0, 0].set_xticklabels(df_discount['discount_range'], rotation=45, ha='right')
axes[0, 0].set_title('Total Sales by Discount Range', fontweight='bold')
axes[0, 0].set_ylabel('Sales ($)')
for i, v in enumerate(df_discount['total_sales']):
    axes[0, 0].text(i, v, f'${v:,.0f}', ha='center', va='bottom', fontsize=8)

# Chart 2: Profit Margin by Discount Range
colors = ['green' if x > 10 else 'orange' if x > 5 else 'red' for x in df_discount['profit_margin_percent']]
axes[0, 1].bar(range(len(df_discount)), df_discount['profit_margin_percent'], color=colors)
axes[0, 1].set_xticks(range(len(df_discount)))
axes[0, 1].set_xticklabels(df_discount['discount_range'], rotation=45, ha='right')
axes[0, 1].set_title('Profit Margin % by Discount Range', fontweight='bold')
axes[0, 1].set_ylabel('Profit Margin (%)')
axes[0, 1].axhline(y=0, color='black', linestyle='--', linewidth=1)
for i, v in enumerate(df_discount['profit_margin_percent']):
    axes[0, 1].text(i, v, f'{v:.1f}%', ha='center', va='bottom' if v > 0 else 'top', fontsize=8)

# Chart 3: Transaction Count
axes[1, 0].barh(df_discount['discount_range'], df_discount['transaction_count'], color='coral')
axes[1, 0].set_title('Transaction Count by Discount Range', fontweight='bold')
axes[1, 0].set_xlabel('Number of Transactions')
for i, v in enumerate(df_discount['transaction_count']):
    axes[1, 0].text(v, i, f' {v:,}', va='center', fontsize=8)

# Chart 4: Avg Transaction Value
axes[1, 1].plot(df_discount['avg_discount_percent'], df_discount['avg_transaction_value'], 
                marker='o', linewidth=2, markersize=8, color='purple')
axes[1, 1].set_title('Avg Transaction Value vs Discount %', fontweight='bold')
axes[1, 1].set_xlabel('Average Discount %')
axes[1, 1].set_ylabel('Avg Transaction Value ($)')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('visualizations/07_discount_impact_analysis.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n✅ Visualization saved: 07_discount_impact_analysis.png")

# ============================================================================
# ANALYSIS 2: Products with Highest Discounts
# ============================================================================
print("\n" + "="*80)
print("SECTION 2: PRODUCTS WITH EXCESSIVE DISCOUNTS")
print("="*80)

query2 = """
SELECT 
    category,
    sub_category,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_percent,
    ROUND(MAX(discount) * 100, 2) AS max_discount_percent,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
WHERE discount > 0
GROUP BY category, sub_category
HAVING AVG(discount) > 0.15
ORDER BY avg_discount_percent DESC
LIMIT 10;
"""

df_high_discount = pd.read_sql_query(query2, conn)
print("\n[Analysis 2] Top 10 Sub-Categories with Highest Average Discounts (>15%):")
print(df_high_discount.to_string(index=False))

if len(df_high_discount) > 0:
    print("\n⚠️  Warning:")
    print(f"   • {len(df_high_discount)} sub-categories have average discounts > 15%")
    unprofitable = df_high_discount[df_high_discount['profit_margin_percent'] < 5]
    if len(unprofitable) > 0:
        print(f"   • {len(unprofitable)} of these have profit margins < 5%")
        print(f"   • High discounts are destroying profitability!")

# ============================================================================
# ANALYSIS 3: Discount Strategy by Customer Segment
# ============================================================================
print("\n" + "="*80)
print("SECTION 3: DISCOUNT STRATEGY BY CUSTOMER SEGMENT")
print("="*80)

query3 = """
SELECT 
    segment,
    COUNT(DISTINCT customer_id) AS customers,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(AVG(CASE WHEN discount > 0 THEN discount END) * 100, 2) AS avg_discount_when_given,
    ROUND(SUM(CASE WHEN discount > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_orders_with_discount,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY segment
ORDER BY total_sales DESC;
"""

df_segment_discount = pd.read_sql_query(query3, conn)
print("\n[Analysis 3] Discount Strategy by Customer Segment:")
print(df_segment_discount.to_string(index=False))

print("\n💡 Insight:")
for _, row in df_segment_discount.iterrows():
    print(f"   • {row['segment']}: {row['pct_orders_with_discount']:.1f}% of orders have discounts")

# ============================================================================
# ANALYSIS 4: Monthly Discount Trends
# ============================================================================
print("\n" + "="*80)
print("SECTION 4: DISCOUNT TRENDS OVER TIME")
print("="*80)

query4 = """
SELECT 
    strftime('%Y-%m', order_date) AS year_month,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_percent,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY year_month
ORDER BY year_month;
"""

df_monthly_discount = pd.read_sql_query(query4, conn)
print("\n[Analysis 4] Monthly Discount Trends (First 12 months):")
print(df_monthly_discount.head(12).to_string(index=False))

# Visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))

# Chart 1: Discount % over time
ax1.plot(range(len(df_monthly_discount)), df_monthly_discount['avg_discount_percent'], 
         marker='o', linewidth=2, color='orange')
ax1.set_title('Average Discount % Trend Over Time', fontweight='bold', fontsize=14)
ax1.set_ylabel('Avg Discount %')
ax1.set_xlabel('Month')
ax1.grid(True, alpha=0.3)
ax1.set_xticks(range(0, len(df_monthly_discount), 3))
ax1.set_xticklabels(df_monthly_discount['year_month'].iloc[::3], rotation=45)

# Chart 2: Profit Margin over time
ax2.plot(range(len(df_monthly_discount)), df_monthly_discount['profit_margin_percent'], 
         marker='s', linewidth=2, color='green')
ax2.set_title('Profit Margin % Trend Over Time', fontweight='bold', fontsize=14)
ax2.set_ylabel('Profit Margin %')
ax2.set_xlabel('Month')
ax2.grid(True, alpha=0.3)
ax2.set_xticks(range(0, len(df_monthly_discount), 3))
ax2.set_xticklabels(df_monthly_discount['year_month'].iloc[::3], rotation=45)
ax2.axhline(y=df_monthly_discount['profit_margin_percent'].mean(), 
            color='red', linestyle='--', label=f"Avg: {df_monthly_discount['profit_margin_percent'].mean():.2f}%")
ax2.legend()

plt.tight_layout()
plt.savefig('visualizations/08_discount_trends.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n✅ Visualization saved: 08_discount_trends.png")

# ============================================================================
# FINAL RECOMMENDATIONS
# ============================================================================
print("\n" + "="*80)
print("🎯 DISCOUNT STRATEGY RECOMMENDATIONS")
print("="*80)

print("\n1. ELIMINATE EXCESSIVE DISCOUNTS")
print("   • Products with >30% discounts have significantly lower margins")
print("   • Cap discounts at 20% maximum")

print("\n2. TARGETED DISCOUNTING")
print("   • Focus discounts on high-margin products (Technology)")
print("   • Avoid discounting already low-margin items (Furniture)")

print("\n3. SEGMENT-SPECIFIC STRATEGIES")
for _, row in df_segment_discount.iterrows():
    if row['profit_margin_percent'] < 10:
        print(f"   • {row['segment']}: Reduce discount frequency from {row['pct_orders_with_discount']:.1f}%")

print("\n4. VOLUME-BASED DISCOUNTS")
print("   • Instead of blanket discounts, offer volume-based pricing")
print("   • Protects margins while incentivizing larger orders")

conn.close()

print("\n" + "="*80)
print("DISCOUNT ANALYSIS COMPLETED")
print("="*80)
