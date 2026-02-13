-- ============================================================================
-- FILE: 02_business_metrics.sql
-- PURPOSE: Calculate core business KPIs and metrics
-- AUTHOR: yusufehtesham29
-- ============================================================================

-- Query 1: Overall Business Performance
-- Calculate total sales, total profit, and profit margin
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

-- EXPLANATION:
-- COUNT(DISTINCT order_id): Counts unique orders (not rows)
-- SUM(sales): Adds up all sales revenue
-- SUM(profit): Adds up all profit
-- Profit margin % = (Total Profit / Total Sales) * 100
-- AVG(sales): Average revenue per transaction
-- ============================================================================


-- Query 2: Sales and Profit by Year
-- Analyze performance trends over time
SELECT 
    CAST(strftime('%Y', order_date) AS INTEGER) AS year,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY year
ORDER BY year;

-- EXPLANATION:
-- strftime('%Y', order_date): Extracts year from date (e.g., "2024")
-- CAST(...AS INTEGER): Converts year from text to number
-- GROUP BY year: Aggregates data for each year separately
-- ORDER BY year: Sorts results chronologically
-- ============================================================================


-- Query 3: Sales and Profit by Region
-- Identify top-performing geographic areas
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

-- EXPLANATION:
-- GROUP BY region: Separates data by geographic region
-- ORDER BY total_sales DESC: Shows highest revenue regions first
-- This helps identify which regions to focus on for growth
-- ============================================================================


-- Query 4: Sales and Profit by Category
-- Understand product category performance
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

-- EXPLANATION:
-- Analyzes performance at the high-level category (Furniture, Office Supplies, Technology)
-- Shows which product categories are most profitable
-- Units sold helps understand volume vs. value
-- ============================================================================


-- Query 5: Sales and Profit by Sub-Category
-- Detailed product performance analysis
SELECT 
    category,
    sub_category,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent,
    SUM(quantity) AS units_sold
FROM superstore
GROUP BY category, sub_category
ORDER BY total_profit DESC;

-- EXPLANATION:
-- GROUP BY category, sub_category: Shows detailed breakdown
-- Identifies specific product types that drive profit
-- Can reveal unprofitable sub-categories that need attention
-- ============================================================================


-- Query 6: Loss-Making Sub-Categories
-- Identify products losing money
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

-- EXPLANATION:
-- HAVING SUM(profit) < 0: Filters to show only unprofitable sub-categories
-- These are products losing money - critical for business decisions
-- ASC order shows worst performers first
-- Management should consider discontinuing or repricing these items
-- ============================================================================
