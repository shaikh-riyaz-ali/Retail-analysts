/*
============================================================
Retail Sales Analytics
03 - Primary & Foreign Key Constraints
============================================================
*/

USE RetailAnalytics;
GO


/* ==========================================================
   PRIMARY KEYS
   ========================================================== */

ALTER TABLE dbo.Customers
ADD CONSTRAINT PK_Customers
PRIMARY KEY (Customer_ID);
GO


ALTER TABLE dbo.Products
ADD CONSTRAINT PK_Products
PRIMARY KEY (Product_ID);
GO


ALTER TABLE dbo.Stores
ADD CONSTRAINT PK_Stores
PRIMARY KEY (Store_ID);
GO


ALTER TABLE dbo.Orders
ADD CONSTRAINT PK_Orders
PRIMARY KEY (Order_ID);
GO


/* ==========================================================
   FOREIGN KEYS
   ========================================================== */

ALTER TABLE dbo.Orders
ADD CONSTRAINT FK_Orders_Customers
FOREIGN KEY (Customer_ID)
REFERENCES dbo.Customers (Customer_ID);
GO


ALTER TABLE dbo.Orders
ADD CONSTRAINT FK_Orders_Products
FOREIGN KEY (Product_ID)
REFERENCES dbo.Products (Product_ID);
GO


ALTER TABLE dbo.Orders
ADD CONSTRAINT FK_Orders_Stores
FOREIGN KEY (Store_ID)
REFERENCES dbo.Stores (Store_ID);
GO