/*
============================================================
Retail Sales Analytics
01 - Create Database
============================================================
*/

IF DB_ID('RetailAnalytics') IS NULL
BEGIN
    CREATE DATABASE RetailAnalytics;
END;
GO

USE RetailAnalytics;
GO