📊 YouTube Data Pipeline (ETL)
📌 Project Overview

This project simulates a modern Data Engineering pipeline by extracting data from the YouTube Data API v3, transforming it, and preparing it for analysis in a Business Intelligence tool.

The goal is to build an end-to-end pipeline similar to a real-world data architecture.

🎯 Objectives
Work with a REST API and JSON data
Handle pagination and API constraints
Build a complete data ingestion pipeline
Secure API credentials using environment variables
Transform raw data into an analytical dataset
Visualize insights using Power BI
🏗️ Pipeline Architecture
YouTube API → Python Ingestion → Raw JSON → Transformation → Structured Dataset → Power BI
🪜 Project Steps
1. Environment Setup
Create a Python virtual environment
Install dependencies (requests, pandas, dotenv, etc.)
Organize project structure (code, data, config)
2. API Configuration
Enable YouTube Data API v3 (Google Cloud)
Generate API key
Understand quotas, rate limits, and pagination
3. Secure Credentials
Store API key in a .env file
Load environment variables securely
Follow best practices (no hardcoding)
4. Data Extraction
Retrieve channel data (playlists → videos)
Extract video IDs using pagination
Fetch detailed video data in batches:
Title
Publish date
Duration
Engagement metrics (views, likes, comments)
5. Data Transformation
Convert JSON → tabular format
Clean and normalize data (dates, types)
Handle missing values
Build a structured dataset ready for analysis
6. Data Storage
Save data locally (CSV or JSON)
Maintain a clean and consistent data structure
7. Data Visualization
Import dataset into Power BI
Build dashboards:
Video performance
Views over time
Engagement analysis
🚀 Bonus (Advanced)
Docker: Containerize the pipeline
Airflow: Automate and schedule ETL workflows
Database Integration: PostgreSQL / SQL Server
Data Warehouse: Transition to ELT architecture
Monitoring: Track pipeline performance
🛠️ Tech Stack
Python (requests, pandas)
YouTube Data API v3
Power BI
(Optional) Docker, Airflow, PostgreSQL# YouTube-data-ingestion-and-transformation-pipeline-for-decision-making-analysis
