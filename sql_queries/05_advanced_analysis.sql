-- ============================================================================
-- FILE: 05_advanced_analysis.sql
-- PURPOSE: Advanced SQL analysis using window functions and complex queries
-- AUTHOR: yusufehtesham29
-- ============================================================================

-- Query 1: Rank Products by Profit within Each Category
-- Use window functions to rank products
SELECT 
    category,
    sub_category,
    product_name,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    RANK() OVER (PARTITION BY category ORDER BY SUM(profit) DESC) AS profit_rank
FROM superstore
GROUP BY category, sub_category, product_name
ORDER BY category, profit_rank
LIMIT 30;

-- EXPLANATION:
-- PARTITION BY category: Separates ranking by each category
-- ORDER BY SUM(profit) DESC: Ranks highest profit first
-- RANK(): Assigns rank numbers (1, 2, 3...) within each category
-- Shows top performers in each category separately
-- Window functions allow ranking without grouping away other columns
-- ============================================================================


-- Query 2: Running Total of Sales by Date
-- Calculate cumulative sales over time
SELECT 
    order_date,
    ROUND(SUM(sales), 2) AS daily_sales,
    ROUND(SUM(SUM(sales)) OVER (ORDER BY order_date), 2) AS running_total_sales
FROM superstore
GROUP BY order_date
ORDER BY order_date
LIMIT 50;

-- EXPLANATION:
-- Inner SUM(sales): Calculates daily sales
-- Outer SUM(...) OVER: Calculates running total (cumulative sum)
-- ORDER BY order_date: Running total increases chronologically
-- Shows business growth trajectory over time
-- Useful for tracking progress toward annual goals
-- ============================================================================


-- Query 3: Month-over-Month Sales Growth
-- Calculate monthly sales and percentage growth
WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', order_date) AS year_month,
        ROUND(SUM(sales), 2) AS monthly_sales,
        ROUND(SUM(profit), 2) AS monthly_profit
    FROM superstore
    GROUP BY year_month
)
SELECT 
    year_month,
    monthly_sales,
    monthly_profit,
    LAG(monthly_sales) OVER (ORDER BY year_month) AS previous_month_sales,
    ROUND(
        (monthly_sales - LAG(monthly_sales) OVER (ORDER BY year_month)) / 
        LAG(monthly_sales) OVER (ORDER BY year_month) * 100, 
        2
    ) AS sales_growth_percent
FROM monthly_sales
ORDER BY year_month;

-- EXPLANATION:
-- WITH (CTE - Common Table Expression): Creates temporary result set
-- strftime('%Y-%m', order_date): Extracts year-month (e.g., "2024-03")
-- LAG(): Window function that accesses previous row's value
-- Calculates month-over-month growth rate percentage
-- Identifies growth trends and seasonality patterns
-- ============================================================================


-- Query 4: Top 5 Customers per Region
-- Identify VIP customers in each region
WITH customer_sales AS (
    SELECT 
        region,
        customer_id,
        customer_name,
        ROUND(SUM(sales), 2) AS total_sales,
        ROW_NUMBER() OVER (PARTITION BY region ORDER BY SUM(sales) DESC) AS rank
    FROM superstore
    GROUP BY region, customer_id, customer_name
)
SELECT 
    region,
    customer_id,
    customer_name,
    total_sales,
    rank
FROM customer_sales
WHERE rank <= 5
ORDER BY region, rank;

-- EXPLANATION:
-- ROW_NUMBER(): Assigns unique sequential numbers
-- PARTITION BY region: Separate ranking for each region
-- WHERE rank <= 5: Filters only top 5 per region
-- Identifies regional VIP customers for targeted marketing
-- Unlike RANK(), ROW_NUMBER() never gives ties
-- ============================================================================


-- Query 5: Product Performance with Category Average
-- Compare each product to its category average
SELECT 
    category,
    sub_category,
    product_name,
    ROUND(SUM(profit), 2) AS product_profit,
    ROUND(AVG(SUM(profit)) OVER (PARTITION BY category), 2) AS category_avg_profit,
    ROUND(
        SUM(profit) - AVG(SUM(profit)) OVER (PARTITION BY category),
        2
    ) AS diff_from_category_avg
FROM superstore
GROUP BY category, sub_category, product_name
HAVING SUM(profit) IS NOT NULL
ORDER BY category, product_profit DESC
LIMIT 50;

-- EXPLANATION:
-- Calculates each product's profit
-- AVG(...) OVER (PARTITION BY category): Category average profit
-- diff_from_category_avg: Shows if product is above/below average
-- Helps identify over-performers and under-performers
-- Products below average may need attention or discontinuation
-- ============================================================================


-- Query 6: Quarterly Performance Summary
-- Aggregate sales by quarter
SELECT 
    CAST(strftime('%Y', order_date) AS INTEGER) AS year,
    CASE 
        WHEN CAST(strftime('%m', order_date) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
        WHEN CAST(strftime('%m', order_date) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
        WHEN CAST(strftime('%m', order_date) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
        ELSE 'Q4'
    END AS quarter,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percent
FROM superstore
GROUP BY year, quarter
ORDER BY year, quarter;

-- EXPLANATION:
-- strftime('%m', order_date): Extracts month number (1-12)
-- CASE BETWEEN: Groups months into quarters (Q1, Q2, Q3, Q4)
-- Q1 = Jan-Mar, Q2 = Apr-Jun, Q3 = Jul-Sep, Q4 = Oct-Dec
-- Reveals seasonal business patterns
-- Useful for quarterly business reviews and planning
-- ============================================================================
