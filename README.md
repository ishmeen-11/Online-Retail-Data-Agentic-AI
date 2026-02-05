# Retail Database Agent - n8n Workflow

**Author:** Ishmeen Garewal  
**Course:** Forecasting, Columbia University  
**Assignment:** Agentic AI Workflow (60 pts)

## Overview
Agentic AI workflow in n8n using online retail data which responds to questions in the chat with SQL queries and runs those queries and returns responses for it. 


## Dataset
- **Source:** UCI Online Retail Dataset
- **Rows:** 397,924 transactions
- **Customers:** 4,339

## Tech Stack
- n8n (workflow automation)
- PostgreSQL (database)
- Groq LLM (natural language processing)
- Docker (n8n runtime)

## Files
- `load_data.py` - Script to load data into PostgreSQL
- `workflow.json` - n8n workflow configuration
- `setup_commands.md` - All commands used
- `screenshots/` - Demo images

## Resources Used
1. n8n workflow template: https://n8n.io/workflows/2090-chat-with-a-database-using-ai/
2. Dataset: https://archive.ics.uci.edu/ml/datasets/online+retail
3. Groq API: https://console.groq.com/

## System Prompt Used
```
You are a helpful assistant that can query an online retail database.

Database Schema:
Table: transactions
Columns:
- InvoiceNo (bigint): Invoice number
- StockCode (text): Product code
- Description (text): Product name
- Quantity (bigint): Quantity purchased
- InvoiceDate (timestamp): Purchase date
- UnitPrice (double precision): Price per unit
- CustomerID (bigint): Unique customer identifier
- Country (text): Customer country

When users ask questions, generate SQL queries to answer them.
Always explain your findings clearly.
```

## Sample Queries Generated
Prompt: How many entries in the database

Response: There are 397,924 rows in the transactions table, which represents the total number of individual transaction records stored in the database. This count includes every entry regardless of the product, customer, or date.

Prompt 2: How many countries in the database?

Response: There are 122 distinct countries represented in the transactions table.

Explanation

The query:

SELECT COUNT(DISTINCT Country) AS country_count
FROM transactions;
counts how many unique country names appear in the Country column of the table. The result 122 tells us that customers from 122 different countries have made purchases in the dataset.

Prompt 3: What is the average value of quantites used?

Response: Metric	Value
Average quantity per transaction	5.73 units

Explanation
The query SELECT AVG(Quantity) AS avg_quantity FROM transactions; calculates the mean of the Quantity column across all rows in the transactions table. This gives a single number representing the typical number of items purchased per transaction. In this dataset, the average quantity is about 5.73 items per transaction.

Prompt 4: What is the most recent item bought based on the InvoiceDate?

Result – most recent purchase

InvoiceNo	StockCode	Description	Quantity	InvoiceDate	UnitPrice	CustomerID	Country
536295	85123A	WHITE HANGING HEART T‑LIGHT HOLDER	6	2009‑12‑10 10:47:00	2.55	17850	United Kingdom
Explanation

Query used

SELECT InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country
FROM transactions
ORDER BY InvoiceDate DESC
LIMIT 1;
This orders all transactions by InvoiceDate from newest to oldest and returns the top record.

What it tells us
The single row returned is the transaction that occurred most recently in the dataset.

InvoiceNo 536295 – the invoice identifier.
StockCode 85123A – the product code.
Description WHITE HANGING HEART T‑LIGHT HOLDER – the item’s name.
Quantity 6 – the number of units purchased.
InvoiceDate 2009‑12‑10 10:47:00 – the timestamp of the purchase.
UnitPrice 2.55 – price per unit.
CustomerID 17850 – the customer who made the purchase.
Country United Kingdom – the customer’s location.
If you’d like to see more details about this transaction or filter by a specific customer or country, just let me know!
