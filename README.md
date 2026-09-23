# Retail Sales Analytics

## 📌 Project Overview

Retail Sales Analytics is an end-to-end Data Analyst / BI project built to simulate a real-world retail analytics environment.

The project demonstrates the complete journey from raw and inconsistent retail data to cleaned, validated data, SQL Server analysis, and an interactive Power BI dashboard.

The project covers:

**Raw Data → Data Profiling → Extraction → Transformation → Validation → SQL Server → SQL Analysis → Power BI → Business Insights**

---

## 🎯 Business Problem

Retail organizations often receive data from multiple sources with data-quality issues such as:

- Duplicate records
- Missing values
- Inconsistent text formats
- Invalid numeric values
- Invalid dates
- Invalid categorical values
- Invalid foreign-key references
- Duplicate business keys

These issues can lead to inaccurate reporting and unreliable business decisions.

This project implements a structured data-quality and ETL workflow to clean, validate, and transform retail data before using it for business analysis and reporting.

---

## 🎯 Project Objectives

The main objectives of this project are:

- Profile raw retail datasets
- Identify data-quality issues
- Extract data using Python
- Clean and standardize entity-level data
- Apply business validation rules
- Separate valid and rejected records
- Handle duplicate business keys
- Validate referential integrity
- Load clean data into SQL Server
- Perform SQL-based business analysis
- Build an interactive Power BI dashboard
- Generate meaningful business insights

---

## 🔄 End-to-End Workflow

```text
Raw CSV Data
     ↓
Pandas Data Profiling
     ↓
Data Extraction
     ↓
Entity-Level Transformation
     ↓
Business Rule Validation
     ↓
Rejected Data
     ↓
Duplicate Removal
     ↓
Referential Integrity Validation
     ↓
Clean Processed Data
     ↓
SQL Server
     ↓
SQL Business Analysis
     ↓
Power BI
     ↓
Business Insights
