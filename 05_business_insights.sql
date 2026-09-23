/*
============================================================
Retail Sales Analytics
05 - Business Insights
============================================================

Purpose:
    Generate business-oriented metrics from validated sales data.

Database:
    RetailAnalytics
============================================================
*/

USE RetailAnalytics;
GO


/* ==========================================================
   1. MONTHLY SALES WITH MONTH-OVER-MONTH GROWTH
   ========================================================== */

WITH MonthlySales AS
(
    SELECT
        DATEFROMPARTS(
            YEAR(Order_Date),
            MONTH(Order_Date),
            1
        ) AS Sales_Month,

        SUM(Total_Amount) AS Total_Sales

    FROM dbo.Orders

    GROUP BY
        YEAR(Order_Date),
        MONTH(Order_Date)
),

MonthlySalesWithPrevious AS
(
    SELECT
        Sales_Month,
        Total_Sales,

        LAG(Total_Sales) OVER (
            ORDER BY Sales_Month
        ) AS Previous_Month_Sales

    FROM MonthlySales
)

SELECT
    Sales_Month,
    Total_Sales,
    Previous_Month_Sales,

    CASE
        WHEN Previous_Month_Sales IS NULL
            THEN NULL

        WHEN Previous_Month_Sales = 0
            THEN NULL

        ELSE
            (
                (Total_Sales - Previous_Month_Sales)
                / Previous_Month_Sales
            ) * 100
    END AS MoM_Growth_Percentage

FROM MonthlySalesWithPrevious

ORDER BY
    Sales_Month;
GO


/* ==========================================================
   2. REGION SALES CONTRIBUTION
   ========================================================== */

WITH RegionSales AS
(
    SELECT
        s.Store_Region,
        SUM(o.Total_Amount) AS Total_Sales

    FROM dbo.Orders AS o

    INNER JOIN dbo.Stores AS s
        ON o.Store_ID = s.Store_ID

    GROUP BY
        s.Store_Region
)

SELECT
    Store_Region,
    Total_Sales,

    (
        Total_Sales
        / SUM(Total_Sales) OVER ()
    ) * 100 AS Sales_Contribution_Percentage

FROM RegionSales

ORDER BY
    Total_Sales DESC;
GO


/* ==========================================================
   3. CHANNEL SALES CONTRIBUTION
   ========================================================== */

WITH ChannelSales AS
(
    SELECT
        Sales_Channel,
        SUM(Total_Amount) AS Total_Sales

    FROM dbo.Orders

    GROUP BY
        Sales_Channel
)

SELECT
    Sales_Channel,
    Total_Sales,

    (
        Total_Sales
        / SUM(Total_Sales) OVER ()
    ) * 100 AS Sales_Contribution_Percentage

FROM ChannelSales

ORDER BY
    Total_Sales DESC;
GO


/* ==========================================================
   4. CATEGORY PERFORMANCE
   ========================================================== */

SELECT
    p.Category,

    COUNT(DISTINCT o.Order_ID) AS Total_Orders,

    SUM(o.Quantity) AS Total_Quantity,

    SUM(o.Total_Amount) AS Total_Sales,

    AVG(o.Total_Amount) AS Average_Order_Value,

    (
        SUM(o.Total_Amount)
        / SUM(SUM(o.Total_Amount)) OVER ()
    ) * 100 AS Sales_Contribution_Percentage

FROM dbo.Orders AS o

INNER JOIN dbo.Products AS p
    ON o.Product_ID = p.Product_ID

GROUP BY
    p.Category

ORDER BY
    Total_Sales DESC;
GO


/* ==========================================================
   5. CUSTOMER VALUE SEGMENTS
   ========================================================== */

WITH CustomerSales AS
(
    SELECT
        Customer_ID,

        COUNT(DISTINCT Order_ID) AS Total_Orders,

        SUM(Total_Amount) AS Total_Sales

    FROM dbo.Orders

    GROUP BY
        Customer_ID
)

SELECT
    Customer_ID,
    Total_Orders,
    Total_Sales,

    CASE
        WHEN Total_Sales >= 1000000
            THEN 'High Value'

        WHEN Total_Sales >= 500000
            THEN 'Medium Value'

        ELSE 'Standard Value'
    END AS Customer_Value_Segment

FROM CustomerSales

ORDER BY
    Total_Sales DESC;
GO


/* ==========================================================
   6. REPEAT CUSTOMER ANALYSIS
   ========================================================== */

WITH CustomerOrders AS
(
    SELECT
        Customer_ID,
        COUNT(DISTINCT Order_ID) AS Order_Count

    FROM dbo.Orders

    GROUP BY
        Customer_ID
)

SELECT
    COUNT(*) AS Total_Customers,

    SUM(
        CASE
            WHEN Order_Count = 1
                THEN 1
            ELSE 0
        END
    ) AS One_Order_Customers,

    SUM(
        CASE
            WHEN Order_Count > 1
                THEN 1
            ELSE 0
        END
    ) AS Repeat_Customers

FROM CustomerOrders;
GO


/* ==========================================================
   7. CANCELLATION AND RETURN ANALYSIS
   ========================================================== */

SELECT
    Order_Status,

    COUNT(DISTINCT Order_ID) AS Total_Orders,

    SUM(Total_Amount) AS Total_Order_Value,

    (
        COUNT(DISTINCT Order_ID) * 100.0
        / SUM(COUNT(DISTINCT Order_ID)) OVER ()
    ) AS Order_Percentage

FROM dbo.Orders

GROUP BY
    Order_Status

ORDER BY
    Total_Orders DESC;
GO


/* ==========================================================
   8. PAYMENT FAILURE ANALYSIS
   ========================================================== */

SELECT
    Payment_Method,

    COUNT(DISTINCT Order_ID) AS Total_Orders,

    SUM(
        CASE
            WHEN Payment_Status = 'Failed'
                THEN 1
            ELSE 0
        END
    ) AS Failed_Orders,

    (
        SUM(
            CASE
                WHEN Payment_Status = 'Failed'
                    THEN 1
                ELSE 0
            END
        ) * 100.0
        / COUNT(DISTINCT Order_ID)
    ) AS Failure_Rate_Percentage

FROM dbo.Orders

GROUP BY
    Payment_Method

ORDER BY
    Failure_Rate_Percentage DESC;
GO


/* ==========================================================
   9. STORE PERFORMANCE
   ========================================================== */

SELECT
    s.Store_ID,
    s.Store_Name,
    s.Store_Region,
    s.Store_Type,

    COUNT(DISTINCT o.Order_ID) AS Total_Orders,

    SUM(o.Quantity) AS Total_Quantity,

    SUM(o.Total_Amount) AS Total_Sales,

    AVG(o.Total_Amount) AS Average_Order_Value

FROM dbo.Orders AS o

INNER JOIN dbo.Stores AS s
    ON o.Store_ID = s.Store_ID

GROUP BY
    s.Store_ID,
    s.Store_Name,
    s.Store_Region,
    s.Store_Type

ORDER BY
    Total_Sales DESC;
GO


/* ==========================================================
   10. DISCOUNT BAND PERFORMANCE
   ========================================================== */

SELECT

    CASE
        WHEN Discount = 0
            THEN 'No Discount'

        WHEN Discount <= 0.10
            THEN '0-10%'

        WHEN Discount <= 0.20
            THEN '10-20%'

        ELSE '20%+'
    END AS Discount_Band,

    COUNT(DISTINCT Order_ID) AS Total_Orders,

    SUM(Total_Amount) AS Total_Sales,

    AVG(Total_Amount) AS Average_Order_Value

FROM dbo.Orders

GROUP BY

    CASE
        WHEN Discount = 0
            THEN 'No Discount'

        WHEN Discount <= 0.10
            THEN '0-10%'

        WHEN Discount <= 0.20
            THEN '10-20%'

        ELSE '20%+'
    END

ORDER BY
    Total_Sales DESC;
GO


/* ==========================================================
   11. EXECUTIVE KPI SUMMARY
   ========================================================== */

SELECT

    COUNT(DISTINCT Order_ID) AS Total_Orders,

    COUNT(DISTINCT Customer_ID) AS Active_Customers,

    COUNT(DISTINCT Product_ID) AS Products_Sold,

    SUM(Quantity) AS Total_Quantity_Sold,

    SUM(Total_Amount) AS Total_Sales,

    AVG(Total_Amount) AS Average_Order_Value,

    SUM(
        CASE
            WHEN Order_Status = 'Completed'
                THEN 1
            ELSE 0
        END
    ) AS Completed_Orders,

    SUM(
        CASE
            WHEN Order_Status = 'Cancelled'
                THEN 1
            ELSE 0
        END
    ) AS Cancelled_Orders,

    SUM(
        CASE
            WHEN Order_Status = 'Returned'
                THEN 1
            ELSE 0
        END
    ) AS Returned_Orders

FROM dbo.Orders;
GO