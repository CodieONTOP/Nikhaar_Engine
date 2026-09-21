# 🧹 Nikhaar Engine™ — Sales Data Cleaning & Executive Reporting Engine

> **Transforming chaotic, messy commercial data into clean datasets and interactive executive dashboards.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.0%2B-3F4F75.svg)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Overview

**Nikhaar Engine™** is an end-to-end Python pipeline designed to ingest raw, unformatted commercial data, execute automated sanitization workflows, and produce self-contained, interactive HTML dashboards. 

Instead of forcing stakeholders to look at raw spreadsheets or rely on manual spreadsheet updates, the engine standardizes data quality, imputes missing or invalid values, and compiles real-time executive analytics into a dark-themed visual web dashboard.

---

## ✨ Key Features

- ⚡ **Automated Data Sanitization Pipeline**:
  - Removes duplicate entries automatically.
  - Normalizes customer names and regions (casing, trailing whitespace, `NaN`/`None` replacement).
  - Converts invalid or negative transaction values into median-imputed numbers.
  - Standardizes date formats and handles missing timestamps safely.
- 📐 **Data Quality Integrity Index**: Computes cell-level data completeness and data health scores prior to report generation.
- 📊 **Embedded High-End Plotly Visualizations**:
  - **Regional Revenue Breakdown**: Interactive bar chart displaying sales distributions across territories.
  - **Revenue Growth Trajectory**: Time-series area chart tracking sales over time.
  - **Market Volume Share**: Donut chart breaking down order volume percentage by region.
  - **Account Leaderboard**: Horizontal bar chart identifying top enterprise clients.
- 🔍 **Interactive Data Inspector Table**: Embedded HTML table equipped with real-time JavaScript text filtering for fast record lookups.
- 📄 **Zero-Dependency PDF Exporting**: Built-in CSS print media queries designed to print or save crisp, print-ready executive PDFs directly from the browser.

---

## 🛠️ Tech Stack & Dependencies

| Layer | Technology | Function |
| :--- | :--- | :--- |
| **Language** | Python 3.9+ | Core script execution |
| **Data Processing** | Pandas, NumPy | Deduplication, type conversion, median imputation |
| **Visualization Engine** | Plotly Express, Plotly IO | Dynamic, interactive web charts |
| **Frontend Output** | HTML5, Modern CSS3, JavaScript | Dark glassmorphism executive report dashboard |

---

## 📁 Project Structure

```text
.
├── clean_and_report.py        # Core ingestion, data cleaning, & dashboard generator
├── messy_sales_data.csv       # Incoming raw data input file
├── cleaned_sales_data.csv     # Exported sanitized dataset output
├── executive_summary_report.html # Generated self-contained visual dashboard
└── README.md                  # Project documentation
