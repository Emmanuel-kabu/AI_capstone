# AI-Powered Data Quality Pipeline — Capstone Documentation

## 1. Problem Statement

**Domain:** Data Engineering  
**Problem:** When new raw CSV datasets arrive for ingestion into a data warehouse, data engineers must manually inspect the data, identify quality issues (nulls, duplicates, type mismatches, outliers, format inconsistencies), write validation rules, and build an ETL pipeline. This process is **repetitive, error-prone, and time-consuming** — often taking hours for each new dataset.

**Goal:** Automate this end-to-end process using an AI-powered workflow that chains three different AI UX types to go from **raw CSV → validated, clean dataset** in minutes instead of hours.

---

## 2. Workflow Overview

The workflow chains outputs between **three AI UX types**:

| Step | AI UX Type | Tool Used | Input | Output (Handoff) |
|------|-----------|-----------|-------|-------------------|
| **1** | **Chat AI** | Claude / ChatGPT | Raw CSV sample + prompt | `data_quality_spec.json` |
| **2** | **IDE AI** | GitHub Copilot (VS Code) | JSON spec from Step 1 | `etl_pipeline.py` + `summarize_results.py` |
| **3** | **CLI AI** | Copilot in Terminal | Pipeline execution output | CLI summary report |

### Data Flow Diagram

```
Raw CSV  ──►  [Chat AI]  ──►  JSON Spec  ──►  [IDE AI]  ──►  Python Pipeline  ──►  [CLI AI]  ──►  Summary Report
                                  │                                │                                    │
                          data_quality_spec.json           etl_pipeline.py                    quality_report.json
                                                           cleaned_sales_data.csv              CLI text summary
                                                           flagged_rows.csv
```

---

## 3. Step-by-Step Workflow Instructions

### Step 1: Chat AI — Generate Data Quality Specification

**Tool:** Claude (Chat AI)

**Prompt Used:**
> *"I have a raw sales CSV dataset with these columns: order_id, customer_name, email, product, quantity, unit_price, order_date, shipping_country, payment_method, status. The data has quality issues including nulls, duplicates, inconsistent date formats (YYYY-MM-DD, YYYY/MM/DD, MM-DD-YYYY), negative quantities, negative prices, invalid emails, invalid payment methods, and inconsistent status casing. Please generate a comprehensive JSON data quality specification that includes: (1) a schema definition with types, constraints, and validation rules for each column, (2) a list of 10 quality rules covering deduplication, null checks, format validation, range checks, and enrichment, (3) a 14-step transformation sequence. Output the result as a single JSON file I can feed to a Python pipeline."*

**Output:** `specs/data_quality_spec.json` — A structured JSON containing 10 quality rules (R001–R010) and 14 transformation steps.

**Key Handoff:** The JSON spec file is the contract between the Chat AI and the IDE AI. It defines *what* to validate without specifying *how* to implement it in code.

---

### Step 2: IDE AI — Generate ETL Pipeline Code

**Tool:** GitHub Copilot in VS Code (IDE AI)

**Prompt Used:**
> *"I have a data_quality_spec.json file that defines 10 data quality rules and 14 transformation steps for a sales CSV dataset. Generate a complete Python ETL pipeline (etl_pipeline.py) that: (1) loads and parses this JSON spec dynamically, (2) implements each quality rule as a separate function (deduplication, null checks, email validation, quantity/price range checks, date standardization, status normalization, payment validation, total computation), (3) flags invalid rows without dropping them, (4) separates clean vs flagged rows, (5) exports cleaned_sales_data.csv, flagged_rows.csv, and a quality_report.json with issue details. Also generate a summarize_results.py CLI script that reads quality_report.json and prints a formatted summary with anomaly recommendations."*

**Output:** Two Python files:
- `etl_pipeline.py` — 250-line pipeline with 8 validation functions and an orchestrator
- `summarize_results.py` — CLI summarizer that reads the pipeline output

**Key Handoff:** The pipeline produces `quality_report.json` which is consumed by the CLI summarizer.

---

### Step 3: CLI AI — Run Pipeline & Summarize

**Tool:** GitHub Copilot in Terminal (CLI AI)

**Commands Run:**
```bash
python etl_pipeline.py
python summarize_results.py
```

**Output:** 
- `data/cleaned_sales_data.csv` — Validated, clean rows
- `data/flagged_rows.csv` — Rows with quality issues
- `data/quality_report.json` — Machine-readable report
- Terminal summary with pass rate, issue breakdown, and recommendations

---

## 4. Prompts Summary

| Stage | Prompt Purpose | Key Instruction |
|-------|---------------|-----------------|
| Chat AI | Data profiling + rule generation | "Generate a JSON data quality spec with schema, 10 rules, 14 steps" |
| IDE AI | Code generation from spec | "Generate Python ETL pipeline that reads and applies the JSON spec" |
| CLI AI | Execution + summarization | "Run the pipeline and summarize key anomalies" |

---

## 5. Results & Efficiency Gains

| Metric | Manual Process | AI Workflow |
|--------|---------------|-------------|
| Time to profile data | ~30 min | ~2 min (Chat AI) |
| Time to write validation code | ~2 hours | ~5 min (IDE AI) |
| Time to run & interpret results | ~20 min | ~1 min (CLI AI) |
| **Total** | **~3 hours** | **~8 minutes** |
| Error rate | High (manual inspection) | Low (systematic rules) |
| Reusability | Low (hardcoded) | High (spec-driven) |

---

## 6. Adaptability

This workflow is **tool-agnostic** by design:

- **Step 1** can use *any* Chat AI (ChatGPT, Claude, Gemini) — the output format (JSON) is the contract
- **Step 2** can use *any* IDE AI (Copilot, Cursor, Cody) — the prompt is the same
- **Step 3** can use *any* CLI tool (terminal, shell script, or CI/CD pipeline)
- The JSON spec acts as a **universal interface** — swap any tool without changing the others

---

## 7. Project Structure

```
AI capstone/
├── data/
│   ├── raw_sales_data.csv          ← Input: Raw dataset (25 rows, 10 columns)
│   ├── cleaned_sales_data.csv      ← Output: Validated clean rows
│   ├── flagged_rows.csv            ← Output: Rows with quality issues
│   └── quality_report.json         ← Output: Machine-readable report
├── specs/
│   └── data_quality_spec.json      ← Handoff artifact: Chat AI → IDE AI
├── etl_pipeline.py                 ← Step 2 output: ETL pipeline code
├── summarize_results.py            ← Step 3 input: CLI summarizer
└── DOCUMENTATION.md                ← This file
```
