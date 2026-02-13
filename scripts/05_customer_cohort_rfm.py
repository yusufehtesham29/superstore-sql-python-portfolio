"""
============================================================================
FILE: 05_customer_cohort_rfm.py
PURPOSE: Advanced customer segmentation using RFM and cohort analysis
AUTHOR: yusufehtesham29
============================================================================
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

print("="*80)
print("CUSTOMER COHORT & RFM ANALYSIS")
print("="*80)

conn = sqlite3.connect('database/superstore.db')

# ============================================================================
# ANALYSIS 1: Customer Purchase Frequency
# ============================================================================
print("\n" + "="*80)
print("SECTION 1: CUSTOMER PURCHASE FREQUENCY DISTRIBUTION")
print("="*80)

query1 = """
SELECT 
    purchase_count,
    customer_count,
    ROUND(customer_count * 100.0 / SUM(customer_count) OVER (), 2) AS percentage,
    ROUND(SUM(customer_count) OVER (ORDER BY purchase_count DESC) * 100.0 / 
          SUM(customer_count) OVER (), 2) AS cumulative_percentage
FROM (
    SELECT 
        CASE 
            WHEN order_count = 1 THEN '1 (One-time)'
            WHEN order_count BETWEEN 2 AND 3 THEN '2-3 (Occasional)'
            WHEN order_count BETWEEN 4 AND 6 THEN '4-6 (Regular)'
            WHEN order_count BETWEEN 7 AND 10 THEN '7-10 (Frequent)'
            ELSE '11+ (VIP)'
        END AS purchase_count,
        COUNT(*) AS customer_count
    FROM (
        SELECT 
            customer_id,
            COUNT(DISTINCT order_id) AS order_count
        FROM superstore
        GROUP BY customer_id
    )
    GROUP BY purchase_count
)
ORDER BY 
    CASE purchase_count
        WHEN '1 (One-time)' THEN 1
        WHEN '2-3 (Occasional)' THEN 2
        WHEN '4-6 (Regular)' THEN 3
        WHEN '7-10 (Frequent)' THEN 4
        ELSE 5
    END;
"""

df_frequency = pd.read_sql_query(query1, conn)
print("\n[Analysis 1] Customer Purchase Frequency:")
print(df_frequency.to_string(index=False))

one_time = df_frequency[df_frequency['purchase_count'].str.contains('One-time')]['percentage'].values[0]
print(f"\n⚠️  Customer Retention Insight:")
print(f"   • {one_time}% of customers made only ONE purchase")
print(f"   • High customer acquisition cost not being recovered")
print(f"   • Need retention strategy for one-time buyers")

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Frequency Distribution
colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
ax1.bar(df_frequency['purchase_count'], df_frequency['customer_count'], color=colors)
ax1.set_title('Customer Purchase Frequency Distribution', fontweight='bold', fontsize=14)
ax1.set_ylabel('Number of Customers')
ax1.set_xlabel('Purchase Frequency')
ax1.tick_params(axis='x', rotation=45)
for i, v in enumerate(df_frequency['customer_count']):
    ax1.text(i, v, f'{v}\n({df_frequency["percentage"].iloc[i]}%)', ha='center', va='bottom')

# Cumulative Percentage
ax2.plot(df_frequency['purchase_count'], df_frequency['cumulative_percentage'], 
         marker='o', linewidth=2.5, markersize=10, color='blue')
ax2.fill_between(range(len(df_frequency)), df_frequency['cumulative_percentage'], alpha=0.3, color='blue')
ax2.set_title('Cumulative Customer Distribution', fontweight='bold', fontsize=14)
ax2.set_ylabel('Cumulative %')
ax2.set_xlabel('Purchase Frequency')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 105)

plt.tight_layout()
plt.savefig('visualizations/12_customer_frequency.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n✅ Visualization saved: 12_customer_frequency.png")

# ============================================================================
# ANALYSIS 2: Customer Lifetime Value (CLV)
# ============================================================================
print("\n" + "="*80)
print("SECTION 2: CUSTOMER LIFETIME VALUE ANALYSIS")
print("="*80)

query2 = """
SELECT 
    customer_id,
    customer_name,
    segment,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS lifetime_value,
    ROUND(SUM(profit), 2) AS lifetime_profit,
    ROUND(AVG(sales), 2) AS avg_order_value,
    ROUND(SUM(profit) / COUNT(DISTINCT order_id), 2) AS avg_profit_per_order
FROM superstore
GROUP BY customer_id, customer_name, segment
ORDER BY lifetime_value DESC
LIMIT 20;
"""

df_clv = pd.read_sql_query(query2, conn)
print("\n[Analysis 2] Top 20 Customers by Lifetime Value:")
print(df_clv.to_string(index=False))

print(f"\n💰 CLV Insights:")
print(f"   • Top Customer Lifetime Value: ${df_clv['lifetime_value'].iloc[0]:,.2f}")
print(f"   • Top 10 Customers Combined: ${df_clv['lifetime_value'].head(10).sum():,.2f}")
print(f"   • Average Orders (Top 20): {df_clv['total_orders'].mean():.1f}")

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Top 20 by Lifetime Value
ax1.barh(range(len(df_clv)), df_clv['lifetime_value'], color='gold')
ax1.set_yticks(range(len(df_clv)))
ax1.set_yticklabels(df_clv['customer_name'], fontsize=8)
ax1.set_title('Top 20 Customers by Lifetime Value', fontweight='bold', fontsize=14)
ax1.set_xlabel('Lifetime Value ($)')
ax1.invert_yaxis()

# Lifetime Profit
colors_profit = ['green' if x > 0 else 'red' for x in df_clv['lifetime_profit']]
ax2.barh(range(len(df_clv)), df_clv['lifetime_profit'], color=colors_profit, alpha=0.7)
ax2.set_yticks(range(len(df_clv)))
ax2.set_yticklabels(df_clv['customer_name'], fontsize=8)
ax2.set_title('Top 20 Customers by Lifetime Profit', fontweight='bold', fontsize=14)
ax2.set_xlabel('Lifetime Profit ($)')
ax2.invert_yaxis()
ax2.axvline(x=0, color='black', linestyle='-', linewidth=1)

plt.tight_layout()
plt.savefig('visualizations/13_customer_lifetime_value.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n✅ Visualization saved: 13_customer_lifetime_value.png")

# ============================================================================
# ANALYSIS 3: Customer Segment Comparison
# ============================================================================
print("\n" + "="*80)
print("SECTION 3: DETAILED SEGMENT COMPARISON")
print("="*80)

query3 = """
SELECT 
    segment,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(AVG(customer_orders), 1) AS avg_orders_per_customer,
    ROUND(AVG(customer_sales), 2) AS avg_lifetime_value,
    ROUND(AVG(customer_profit), 2) AS avg_lifetime_profit,
    ROUND(SUM(total_sales), 2) AS segment_total_sales,
    ROUND(SUM(total_profit), 2) AS segment_total_profit
FROM (
    SELECT 
        segment,
        customer_id,
        COUNT(DISTINCT order_id) AS customer_orders,
        SUM(sales) AS customer_sales,
        SUM(profit) AS customer_profit,
        SUM(sales) AS total_sales,
        SUM(profit) AS total_profit
    FROM superstore
    GROUP BY segment, customer_id
)
GROUP BY segment
ORDER BY segment_total_sales DESC;
"""

df_segment_detail = pd.read_sql_query(query3, conn)
print("\n[Analysis 3] Segment Comparison:")
print(df_segment_detail.to_string(index=False))

print(f"\n💡 Segment Insights:")
for _, row in df_segment_detail.iterrows():
    print(f"   • {row['segment']}: {row['customers']} customers, ")
    print(f"     Avg {row['avg_orders_per_customer']:.1f} orders/customer, ${row['avg_lifetime_value']:,.2f} avg CLV")

# ============================================================================
# ANALYSIS 4: At-Risk Customers (Haven't Ordered Recently)
# ============================================================================
print("\n" + "="*80)
print("SECTION 4: AT-RISK CUSTOMER IDENTIFICATION")
print("="*80)

query4 = """
WITH customer_last_order AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        MAX(order_date) AS last_order_date,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(SUM(sales), 2) AS lifetime_value,
        ROUND(SUM(profit), 2) AS lifetime_profit
    FROM superstore
    GROUP BY customer_id, customer_name, segment
)
SELECT 
    customer_id,
    customer_name,
    segment,
    last_order_date,
    ROUND(JULIANDAY((SELECT MAX(order_date) FROM superstore)) - JULIANDAY(last_order_date)) AS days_since_last_order,
    total_orders,
    lifetime_value,
    lifetime_profit,
    CASE 
        WHEN JULIANDAY((SELECT MAX(order_date) FROM superstore)) - JULIANDAY(last_order_date) > 365 THEN 'High Risk'
        WHEN JULIANDAY((SELECT MAX(order_date) FROM superstore)) - JULIANDAY(last_order_date) > 180 THEN 'Medium Risk'
        ELSE 'Active'
    END AS risk_status
FROM customer_last_order
WHERE total_orders >= 3 
  AND JULIANDAY((SELECT MAX(order_date) FROM superstore)) - JULIANDAY(last_order_date) > 180
ORDER BY days_since_last_order DESC, lifetime_value DESC
LIMIT 20;
"""

df_at_risk = pd.read_sql_query(query4, conn)

if len(df_at_risk) > 0:
    print("\n[Analysis 4] Top 20 At-Risk Valuable Customers (3+ orders, no purchase in 180+ days):")
    print(df_at_risk[['customer_name', 'segment', 'days_since_last_order', 'total_orders', 
                      'lifetime_value', 'risk_status']].to_string(index=False))
    
    print(f"\n⚠️  Customer Retention Alert:")
    print(f"   • {len(df_at_risk)} valuable customers at risk of churning")
    print(f"   • Combined lifetime value: ${df_at_risk['lifetime_value'].sum():,.2f}")
    print(f"   • Recommended: Re-engagement campaign immediately")
else:
    print("\n✅ No at-risk customers identified (all active within 180 days)")

conn.close()

print("\n" + "="*80)
print("CUSTOMER COHORT & RFM ANALYSIS COMPLETED")
print("="*80)

print("\n🎯 CUSTOMER STRATEGY RECOMMENDATIONS:")
print("\n1. ONE-TIME BUYER RETENTION")
print(f"   • {one_time}% of customers never return after first purchase")
print("   • Implement: Email follow-up campaign within 30 days")
print("   • Offer: 10% discount on second purchase")

print("\n2. VIP CUSTOMER PROGRAM")
print("   • Create exclusive benefits for 11+ order customers")
print("   • Dedicated account manager for top 20 customers")

print("\n3. RE-ENGAGEMENT CAMPAIGN")
if len(df_at_risk) > 0:
    print(f"   • Target {len(df_at_risk)} at-risk valuable customers")
    print(f"   • Potential recovery: ${df_at_risk['lifetime_value'].sum():,.2f}")

print("\n4. SEGMENT-SPECIFIC STRATEGIES")
for _, row in df_segment_detail.iterrows():
    if row['avg_orders_per_customer'] < 5:
        print(f"   • {row['segment']}: Increase purchase frequency through loyalty program")
