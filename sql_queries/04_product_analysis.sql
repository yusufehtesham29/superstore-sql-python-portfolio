-- ============================================================================
-- FILE: 04_product_analysis.sql
-- PURPOSE: Analyze product performance and shipping methods
-- AUTHOR: yusufehtesham29
-- ============================================================================

-- Query 1: Top 10 Products by Sales
-- Identify best-selling products
SELECT 
    product_id,
    product_name,
    category,
    sub_category,
    COUNT(DISTINCT order_id) AS times_ordered,
    SUM(quantity) AS total_quantity_sold,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY product_id, product_name, category, sub_category
ORDER BY total_sales DESC
LIMIT 10;

-- EXPLANATION:
-- Groups by product_id to analyze individual product performance
-- times_ordered: How many orders included this product
-- total_quantity_sold: Total units sold
-- Reveals which specific products drive the most revenue
-- ============================================================================


-- Query 2: Top 10 Products by Profit
-- Identify most profitable products
SELECT 
    product_id,
    product_name,
    category,
    sub_category,
    COUNT(DISTINCT order_id) AS times_ordered,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY product_id, product_name, category, sub_category
ORDER BY total_profit DESC
LIMIT 10;

-- EXPLANATION:
-- Focuses on profit instead of just revenue
-- High-margin products are more valuable to the business
-- These products should be promoted and kept in stock
-- ============================================================================


-- Query 3: Loss-Making Products
-- Identify products that are losing money
SELECT 
    product_id,
    product_name,
    category,
    sub_category,
    COUNT(DISTINCT order_id) AS times_ordered,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_percent
FROM superstore
GROUP BY product_id, product_name, category, sub_category
HAVING SUM(profit) < 0
ORDER BY total_profit ASC
LIMIT 20;

-- EXPLANATION:
-- HAVING SUM(profit) < 0: Filters only unprofitable products
-- avg_discount_percent: Shows if high discounts are causing losses
-- Business decision needed: discontinue, reprice, or reduce discounts
-- Critical for inventory and pricing strategy
-- ============================================================================


-- Query 4: Sales by Ship Mode
-- Analyze shipping method preferences and performance
SELECT 
    ship_mode,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(sales), 2) AS avg_order_value,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY ship_mode
ORDER BY total_sales DESC;

-- EXPLANATION:
-- Compares Standard Class, Second Class, First Class, Same Day shipping
-- Shows which shipping methods customers prefer
-- Reveals if faster shipping correlates with higher order values
-- Helps optimize shipping strategy and costs
-- ============================================================================


-- Query 5: Discount Impact Analysis
-- Understand the relationship between discounts and profitability
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

-- EXPLANATION:
-- CASE statement: Creates discount buckets/ranges
-- Shows if higher discounts lead to lower profits
-- Critical insight: Are discounts helping or hurting the business?
-- Helps optimize pricing and promotion strategy
-- ============================================================================


-- Query 6: State-wise Performance
-- Top 10 states by sales
SELECT 
    state,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY state
ORDER BY total_sales DESC
LIMIT 10;

-- EXPLANATION:
-- Identifies top-performing states (geographic market analysis)
-- Shows customer concentration by state
-- Helps plan regional marketing and distribution strategies
-- Can reveal untapped markets or areas needing attention
-- ============================================================================
