-- ============================================================================
-- FILE: 01_create_table.sql
-- PURPOSE: Create the superstore table with appropriate data types
-- AUTHOR: yusufehtesham29
-- ============================================================================

-- Drop table if exists (for re-running the script)
DROP TABLE IF EXISTS superstore;

-- Create the superstore table
CREATE TABLE superstore (
    -- Order Information
    row_id INTEGER PRIMARY KEY,
    order_id TEXT NOT NULL,
    order_date TEXT NOT NULL,           -- Will be converted to DATE format
    ship_date TEXT NOT NULL,            -- Will be converted to DATE format
    ship_mode TEXT,
    
    -- Customer Information
    customer_id TEXT NOT NULL,
    customer_name TEXT,
    segment TEXT,
    
    -- Location Information
    country TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    region TEXT,
    
    -- Product Information
    product_id TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    product_name TEXT,
    
    -- Business Metrics
    sales REAL NOT NULL,
    quantity INTEGER NOT NULL,
    discount REAL DEFAULT 0,
    profit REAL
);

-- Create indexes for better query performance
CREATE INDEX idx_order_date ON superstore(order_date);
CREATE INDEX idx_customer_id ON superstore(customer_id);
CREATE INDEX idx_category ON superstore(category);
CREATE INDEX idx_region ON superstore(region);
CREATE INDEX idx_product_id ON superstore(product_id);

-- ============================================================================
-- EXPLANATION:
-- 
-- 1. DROP TABLE IF EXISTS: Removes existing table to allow fresh creation
-- 2. PRIMARY KEY (row_id): Unique identifier for each row
-- 3. TEXT data type: Used for strings (Order ID, Customer Name, etc.)
-- 4. REAL data type: Used for decimal numbers (Sales, Profit, Discount)
-- 5. INTEGER data type: Used for whole numbers (Quantity)
-- 6. NOT NULL constraints: Ensures critical fields always have values
-- 7. DEFAULT 0: Sets default value for discount if not provided
-- 8. Indexes: Speed up queries that filter by these columns
-- ============================================================================
