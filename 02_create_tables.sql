/*
============================================================
Retail Sales Analytics
02 - Create Tables
============================================================
*/

USE RetailAnalytics;
GO

/* ==========================================================
   CUSTOMERS
   ========================================================== */

CREATE TABLE dbo.Customers
(
    Customer_ID  VARCHAR(20)    NOT NULL,
    Customer_Name VARCHAR(150)  NULL,
    Gender       VARCHAR(20)    NULL,
    Age          INT            NULL,
    Email        VARCHAR(255)   NULL,
    Phone        VARCHAR(20)    NULL,
    City         VARCHAR(100)   NULL,
    Signup_Date  DATE           NULL
);
GO


/* ==========================================================
   PRODUCTS
   ========================================================== */

CREATE TABLE dbo.Products
(
    Product_ID    VARCHAR(20)    NOT NULL,
    Product_Name  VARCHAR(200)   NULL,
    Category      VARCHAR(50)    NULL,
    Brand         VARCHAR(100)   NULL,
    Unit_Price    DECIMAL(18,2)  NULL
);
GO


/* ==========================================================
   STORES
   ========================================================== */

CREATE TABLE dbo.Stores
(
    Store_ID      VARCHAR(20)    NOT NULL,
    Store_Name    VARCHAR(150)   NULL,
    Store_City    VARCHAR(100)   NULL,
    Store_Region  VARCHAR(100)   NULL,
    Store_Type    VARCHAR(50)    NULL
);
GO


/* ==========================================================
   ORDERS
   ========================================================== */

CREATE TABLE dbo.Orders
(
    Order_ID        VARCHAR(20)    NOT NULL,
    Order_Date      DATE           NULL,
    Customer_ID     VARCHAR(20)    NULL,
    Product_ID      VARCHAR(20)    NULL,
    Store_ID        VARCHAR(20)    NULL,
    Quantity        INT            NULL,
    Unit_Price      DECIMAL(18,2)  NULL,
    Discount        DECIMAL(5,2)   NULL,
    Tax             DECIMAL(18,2)  NULL,
    Shipping_Cost   DECIMAL(18,2)  NULL,
    Total_Amount    DECIMAL(18,2)  NULL,
    Payment_Method  VARCHAR(50)    NULL,
    Payment_Status  VARCHAR(50)    NULL,
    Order_Status    VARCHAR(50)    NULL,
    Sales_Channel   VARCHAR(50)    NULL
);
GO