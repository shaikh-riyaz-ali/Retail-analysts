/*
============================================================
Retail Sales Analytics
04 - Business Analysis Queries
============================================================

Purpose:
    Analyze validated retail sales data stored in SQL Server.

Database:
    RetailAnalytics

============================================================
*/

USE RetailAnalytics;
GO


/* ==========================================================
   1. OVERALL BUSINESS SUMMARY
   ========================================================== */

SELECT
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    SUM(Quantity) AS Total_Quantity_Sold,
    SUM(Total_Amount) AS Total_Order_Value,
    AVG(Total_Amount) AS Average_Order_Value
FROM dbo.Orders;
GO


/* ==========================================================
   2. COMPLETED SALES SUMMARY
   ========================================================== */

SELECT
    COUNT(DISTINCT Order_ID) AS Completed_Orders,
    SUM(Quantity) AS Completed_Quantity,
    SUM(Total_Amount) AS Completed_Sales,
    AVG(Total_Amount) AS Average_Completed_Order_Value
FROM dbo.Orders
WHERE Order_Status = 'Completed';
GO


/* ==========================================================
   3. MONTHLY SALES TREND
   ========================================================== */

SELECT
    YEAR(Order_Date) AS Order_Year,
    MONTH(Order_Date) AS Order_Month,
    SUM(Total_Amount) AS Total_Sales,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    SUM(Quantity) AS Total_Quantity
FROM dbo.Orders
GROUP BY
    YEAR(Order_Date),
    MONTH(Order_Date)
ORDER BY
    Order_Year,
    Order_Month;
GO


/* ==========================================================
   4. SALES BY REGION
   ========================================================== */

SELECT
    s.Store_Region,
    SUM(o.Total_Amount) AS Total_Sales,
    COUNT(DISTINCT o.Order_ID) AS Total_Orders,
    SUM(o.Quantity) AS Total_Quantity
FROM dbo.Orders AS o
INNER JOIN dbo.Stores AS s
    ON o.Store_ID = s.Store_ID
GROUP BY
    s.Store_Region
ORDER BY
    Total_Sales DESC;
GO


/* ==========================================================
   5. SALES BY STORE
   ========================================================== */

SELECT
    s.Store_ID,
    s.Store_Name,
    s.Store_City,
    s.Store_Region,
    s.Store_Type,
    SUM(o.Total_Amount) AS Total_Sales,
    COUNT(DISTINCT o.Order_ID) AS Total_Orders
FROM dbo.Orders AS o
INNER JOIN dbo.Stores AS s
    ON o.Store_ID = s.Store_ID
GROUP BY
    s.Store_ID,
    s.Store_Name,
    s.Store_City,
    s.Store_Region,
    s.Store_Type
ORDER BY
    Total_Sales DESC;
GO


/* ==========================================================
   6. SALES BY PRODUCT CATEGORY
   ========================================================== */

SELECT
    p.Category,
    SUM(o.Total_Amount) AS Total_Sales,
    SUM(o.Quantity) AS Total_Quantity,
    COUNT(DISTINCT o.Order_ID) AS Total_Orders
FROM dbo.Orders AS o
INNER JOIN dbo.Products AS p
    ON o.Product_ID = p.Product_ID
GROUP BY
    p.Category
ORDER BY
    Total_Sales DESC;
GO


/* ==========================================================
   7. TOP 10 PRODUCTS BY SALES
   ========================================================== */

SELECT TOP 10
    p.Product_ID,
    p.Product_Name,
    p.Category,
    p.Brand,
    SUM(o.Quantity) AS Quantity_Sold,
    SUM(o.Total_Amount) AS Total_Sales,
    COUNT(DISTINCT o.Order_ID) AS Total_Orders
FROM dbo.Orders AS o
INNER JOIN dbo.Products AS p
    ON o.Product_ID = p.Product_ID
GROUP BY
    p.Product_ID,
    p.Product_Name,
    p.Category,
    p.Brand
ORDER BY
    Total_Sales DESC;
GO


/* ==========================================================
   8. SALES BY CHANNEL
   ========================================================== */

SELECT
    Sales_Channel,
    SUM(Total_Amount) AS Total_Sales,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    SUM(Quantity) AS Total_Quantity,
    AVG(Total_Amount) AS Average_Order_Value
FROM dbo.Orders
GROUP BY
    Sales_Channel
ORDER BY
    Total_Sales DESC;
GO


/* ==========================================================
   9. PAYMENT STATUS ANALYSIS
   ========================================================== */

SELECT
    Payment_Status,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    SUM(Total_Amount) AS Total_Order_Value
FROM dbo.Orders
GROUP BY
    Payment_Status
ORDER BY
    Total_Orders DESC;
GO


/* ==========================================================
   10. ORDER STATUS ANALYSIS
   ========================================================== */

SELECT
    Order_Status,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    SUM(Total_Amount) AS Total_Order_Value,
    SUM(Quantity) AS Total_Quantity
FROM dbo.Orders
GROUP BY
    Order_Status
ORDER BY
    Total_Orders DESC;
GO


/* ==========================================================
   11. TOP 10 CUSTOMERS BY SALES
   ========================================================== */

SELECT TOP 10
    c.Customer_ID,
    c.Customer_Name,
    c.City,
    c.Gender,
    COUNT(DISTINCT o.Order_ID) AS Total_Orders,
    SUM(o.Quantity) AS Total_Quantity,
    SUM(o.Total_Amount) AS Total_Sales
FROM dbo.Orders AS o
INNER JOIN dbo.Customers AS c
    ON o.Customer_ID = c.Customer_ID
GROUP BY
    c.Customer_ID,
    c.Customer_Name,
    c.City,
    c.Gender
ORDER BY
    Total_Sales DESC;
GO


/* ==========================================================
   12. CUSTOMER ORDER FREQUENCY
   ========================================================== */

SELECT
    Customer_ID,
    COUNT(DISTINCT Order_ID) AS Order_Count,
    SUM(Total_Amount) AS Total_Sales
FROM dbo.Orders
GROUP BY
    Customer_ID
ORDER BY
    Order_Count DESC;
GO


/* ==========================================================
   13. DISCOUNT ANALYSIS
   ========================================================== */

SELECT
    CASE
        WHEN Discount = 0 THEN 'No Discount'
        WHEN Discount > 0 AND Discount <= 0.10 THEN '0-10%'
        WHEN Discount > 0.10 AND Discount <= 0.20 THEN '10-20%'
        ELSE '20%+'
    END AS Discount_Band,

    COUNT(DISTINCT Order_ID) AS Total_Orders,
    SUM(Total_Amount) AS Total_Sales,
    AVG(Total_Amount) AS Average_Order_Value

FROM dbo.Orders

GROUP BY
    CASE
        WHEN Discount = 0 THEN 'No Discount'
        WHEN Discount > 0 AND Discount <= 0.10 THEN '0-10%'
        WHEN Discount > 0.10 AND Discount <= 0.20 THEN '10-20%'
        ELSE '20%+'
    END

ORDER BY
    Total_Sales DESC;
GO


/* ==========================================================
   14. STORE TYPE PERFORMANCE
   ========================================================== */

SELECT
    s.Store_Type,
    COUNT(DISTINCT o.Order_ID) AS Total_Orders,
    SUM(o.Quantity) AS Total_Quantity,
    SUM(o.Total_Amount) AS Total_Sales,
    AVG(o.Total_Amount) AS Average_Order_Value
FROM dbo.Orders AS o
INNER JOIN dbo.Stores AS s
    ON o.Store_ID = s.Store_ID
GROUP BY
    s.Store_Type
ORDER BY
    Total_Sales DESC;
GO