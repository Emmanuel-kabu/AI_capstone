# AI-Powered Data Quality Pipeline

> **Capstone Project** — Data Engineering Specialization  
> An end-to-end AI workflow that chains three AI UX types (Chat AI, IDE AI, CLI AI) to automate raw data profiling, validation, and cleaning.

---

## Problem Statement

When new raw CSV datasets arrive for ingestion into a data warehouse, data engineers must **manually**:
1. Inspect and profile the data
2. Identify quality issues (nulls, duplicates, type mismatches, outliers)
3. Write validation rules and ETL code
4. Run the pipeline and interpret results

This process is **repetitive, error-prone, and time-consuming** — often taking 2–3 hours per dataset. This project reduces that to **under 10 minutes** using a chained AI workflow.

---

## Workflow Architecture

```
Raw CSV  ──►  [Chat AI]  ──►  JSON Spec  ──►  [IDE AI]  ──►  Python Pipeline  ──►  [CLI AI]  ──►  Summary Report
```

| Step | AI UX Type | Tool | Input | Output (Handoff) |
|------|-----------|------|-------|-------------------|
| **1** | Chat AI | Claude / ChatGPT | Raw CSV + prompt | `data_quality_spec.json` |
| **2** | IDE AI | GitHub Copilot (VS Code) | JSON spec | `etl_pipeline.py` + `summarize_results.py` |
| **3** | CLI AI | Copilot in Terminal | Pipeline execution | CLI summary report + cleaned data |

### Key Design: The JSON Spec as a Universal Interface

The `data_quality_spec.json` acts as the **contract** between all three AI stages. It defines:
- **Schema** — column types, constraints, and validation patterns
- **10 Quality Rules** (R001–R010) — deduplication, null checks, email validation, range checks, date standardization, status normalization, payment validation, and enrichment
- **14 Transformation Steps** — ordered pipeline execution sequence

---

## Quick Start

### Prerequisites

- Python 3.10+
- `pandas` and `numpy`

### Option 1: Automated (Recommended)

```bash
# Run the entire workflow with one command
python run_workflow.py
```

### Option 2: Step-by-Step

```bash
# Install dependencies
pip install pandas numpy

# Step 1: Run ETL pipeline (reads spec, validates data, exports results)
python etl_pipeline.py

# Step 2: Generate CLI summary report
python summarize_results.py
```

---

## Project Structure

```
AI capstone/
├── data/
│   ├── raw_sales_data.csv          # Input: Raw dataset (25 rows, 10 columns)
│   ├── cleaned_sales_data.csv      # Output: Validated clean rows
│   ├── flagged_rows.csv            # Output: Rows with quality issues
│   └── quality_report.json         # Output: Machine-readable report
├── specs/
│   └── data_quality_spec.json      # Handoff artifact: Chat AI → IDE AI
├── etl_pipeline.py                 # Step 2 output: ETL pipeline code
├── summarize_results.py            # Step 3 input: CLI summarizer
├── run_workflow.py                 # One-click workflow runner
├── workflow_diagram.html           # Interactive flowchart (open in browser)
├── DOCUMENTATION.md                # Full project documentation
└── README.md                       # This file
```

---

## Sample Output

Running the pipeline on the sample dataset (25 rows with intentional quality issues):

```
=======================================================
  PIPELINE COMPLETE — QUALITY SUMMARY
=======================================================
  Input rows:        25
  After dedup:       25
  Clean rows:        14
  Flagged rows:      11
  Pass rate:         56.0%
  Issues detected:   9
=======================================================
```

### Issues Detected

| Rule | Issue | Count |
|------|-------|-------|
| R002 | Missing customer names | 1 |
| R002 | Missing emails | 2 |
| R002 | Missing shipping country | 1 |
| R003 | Invalid email format | 3 |
| R004 | Quantity out of range [1, 1000] | 4 |
| R005 | Negative unit price | 1 |
| R006 | Unparseable dates (e.g., month 13) | 1 |
| R008 | Inconsistent status casing | 1 |
| R009 | Invalid payment method | 1 |

---

## Adaptability

This workflow is **tool-agnostic** by design:

- **Step 1** — Any Chat AI (ChatGPT, Claude, Gemini) can generate the JSON spec
- **Step 2** — Any IDE AI (Copilot, Cursor, Cody) can generate the pipeline code
- **Step 3** — Any CLI or terminal can run and summarize results
- The **JSON spec** is the universal interface — swap any tool without changing the others

---

## Efficiency Gains

| Metric | Manual Process | AI Workflow |
|--------|---------------|-------------|
| Data profiling | ~30 min | ~2 min |
| Validation code | ~2 hours | ~5 min |
| Run & interpret | ~20 min | ~1 min |
| **Total** | **~3 hours** | **~8 minutes** |

---

## Tech Stack

- **Python 3.10+** — Core language
- **pandas** — Data manipulation and validation
- **numpy** — Numeric operations
- **JSON** — Spec format and reporting

---

## License

This project is submitted as a capstone deliverable for the AI Tools for Professionals course.
