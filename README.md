# E-Commerce Sales Analyzer

**Project No.:** 5  
**Language:** Python 3  
**Concepts:** Pandas, CSV, Matplotlib, Aggregation
**Project Title:** E-commerce sales analyzer 
**Student Name:** Satyam Kumar
**ERP:** RU-26-02546
**Section:** B2
**E-mail:** satyam.kumar8@rungta.org

## Objective
Analyze e-commerce order data from CSV to calculate total revenue, order count, units sold, best-selling products and category-wise revenue, then visualize the results.

## Features
- Reads Order_ID, Product, Category, Quantity and Price.
- Calculates row revenue as Quantity × Price.
- Calculates total revenue, valid order rows and total units sold.
- Lists the top five products ranked by revenue.
- Aggregates revenue and percentage by category.
- Skips invalid quantity/price values and non-positive quantities/prices.
- Generates a top-products bar chart and category-revenue pie chart.

## Run
Python 3, Pandas and Matplotlib are needed. No `requirements.txt` is included.

Install the libraries if not already installed:
```bash
python -m pip install pandas matplotlib
```
Run from this folder:
```bash
python one.py
```
Or specify another CSV:
```bash
python one.py another_orders.csv
```

## Menu
1. Sales Summary
2. Category-wise Revenue
3. Generate Charts
4. Exit

## CSV format
```csv
Order_ID,Product,Category,Quantity,Price
O1,Phone,Electronics,2,10000
O2,Shirt,Fashion,5,500
O3,Phone,Electronics,1,10000
```

## Assignment test cases

### Test Case 1 – Normal
Expected total revenue 32500, orders 3, units sold 8, top product Phone (30000).

### Test Case 2 – Boundary
Use `boundary_orders.csv`. Expected total revenue 10, orders 1, units sold 1, top product Pen (10).

### Test Case 3 – Invalid
Use `invalid_orders.csv`. Row 2 is skipped for invalid quantity; Row 3 is skipped with `Price must be positive`. Expected total revenue 20000 and orders 1.

### Test Case 4 – Category-wise
Use `orders.csv`, select menu option 2. Expected:
```text
Electronics:30000(92.31%)
Fashion:2500(7.69%)
```
Select option 3 to generate `top_products.png` and `category_revenue.png`.

## Notes
- The Orders count is the number of valid CSV order rows, matching the assignment sample.
- Product ranking is by total revenue.
- Category percentages are calculated against total valid revenue.

Project Mentor:-

Mentored by: Mr.Satyam Prakash
Sethy[https://GitHub.com/SATYAPRAKASHSETHY]
GitHub:@satyaprakashsethy[https://gitHub.com/SATYAPRAKASHSETHY]
Role:Python Mentor/Technical Guide
