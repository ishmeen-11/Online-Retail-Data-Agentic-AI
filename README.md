# Retail Database Agent - n8n Workflow

**Author:** Ishmeen Garewal  
**Course:** Forecasting, Columbia University  
**Assignment:** Agentic AI Workflow

## Overview
Agentic AI workflow in n8n using online retail data which responds to questions in the chat with SQL queries and runs those queries and returns responses for it. 

## Demo
Click here to see demo [https://drive.google.com/file/d/1PlZL91mGSBMtVO2exxRl47YBz_V1vbrs/view?usp=sharing]

## Dataset
- **Source:** UCI Online Retail Dataset
- **Rows:** 1,067,371 transactions

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
2. Dataset: [https://archive.ics.uci.edu/ml/datasets/online+retail](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
3. Groq API: https://console.groq.com/

## System Prompt Used
```
You are a helpful assistant that can query an online retail database.

Database Schema:
Table: transactions
Columns (CASE-SENSITIVE - use double quotes):
- "InvoiceNo" (text): Invoice number
- "StockCode" (text): Product code  
- "Description" (text): Product name
- "Quantity" (bigint): Quantity purchased
- "InvoiceDate" (timestamp): Purchase date and time
- "UnitPrice" (double precision): Price per unit (£)
- "CustomerID" (bigint): Unique customer identifier (can be NULL)
- "Country" (text): Customer's country

CRITICAL SQL RULES:
1. ALWAYS use double quotes around column names: "Country" not country
2. Column names are case-sensitive - use EXACT capitalization as shown above
3. Example: SELECT "Country", COUNT(*) FROM transactions GROUP BY "Country"

Dataset Notes:
- Contains ~1 million transactions from 2009-2011
- Includes NULLs, cancellations (InvoiceNo starting with 'C'), and negative quantities
- Use WHERE "CustomerID" IS NOT NULL to filter out missing customers
- Use WHERE "Quantity" > 0 for valid sales only

When users ask questions:
- Generate valid PostgreSQL queries
- Always use double quotes around column names
- Handle NULLs appropriately
- Explain your results clearly
```
