# AI-Powered Data Quality Pipeline — Workflow Diagram

```mermaid
flowchart TD
    A["Raw CSV Dataset\n(raw_sales_data.csv)\n25 rows with quality issues"] -->|Input| B

    subgraph STEP1["STEP 1: Chat AI - Claude / ChatGPT"]
        B["Prompt: Profile this dataset\nand generate data quality\nrules as a JSON spec"]
        B --> C["data_quality_spec.json\n10 quality rules\n14 transformation steps\nSchema definitions"]
    end

    C -->|"Handoff: JSON spec file"| D

    subgraph STEP2["STEP 2: IDE AI - GitHub Copilot in VS Code"]
        D["Prompt: Generate a Python\nETL pipeline that reads\nthis JSON spec and applies\nall quality rules"]
        D --> E["etl_pipeline.py\nLoads spec dynamically\nValidates all 10 rules\nOutputs clean CSV + report"]
    end

    E -->|"Handoff: quality_report.json"| F

    subgraph STEP3["STEP 3: CLI AI - Terminal / Copilot CLI"]
        F["Run pipeline and summarize:\npython etl_pipeline.py\npython summarize_results.py"]
        F --> G["CLI Summary Report\nPass rate percentage\nIssue breakdown\nAnomaly recommendations"]
    end

    G --> H["Final Outputs\ncleaned_sales_data.csv\nflagged_rows.csv\nquality_report.json\nCLI summary"]

    style STEP1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style STEP2 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style STEP3 fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style A fill:#fce4ec,stroke:#c62828
    style H fill:#e8eaf6,stroke:#283593
```

## Workflow Legend

| Step | AI UX Type | Tool | Input | Output (Handoff) |
|------|-----------|------|-------|-------------------|
| **Step 1** | Chat AI | Claude / ChatGPT | Raw CSV + prompt | data_quality_spec.json |
| **Step 2** | IDE AI | GitHub Copilot (VS Code) | JSON spec from Step 1 | etl_pipeline.py + summarize_results.py |
| **Step 3** | CLI AI | Copilot in Terminal | Pipeline execution | CLI summary + cleaned outputs |
