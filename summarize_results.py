"""
CLI AI Results Summarizer
=========================
Step 3 of the AI-powered workflow.
This script is invoked from the CLI after the ETL pipeline runs.
It reads the quality_report.json (output of Step 2) and produces
a concise, human-readable summary of data quality findings.

Workflow:  Chat AI (spec) --> IDE AI (pipeline) --> CLI AI (this summarizer)
"""

import json
import sys
from pathlib import Path


def summarize_report(report_path: str) -> str:
    """Read the quality report JSON and produce a CLI-friendly summary."""
    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    s = report["summary"]
    lines = []

    lines.append("")
    lines.append("╔══════════════════════════════════════════════════════════╗")
    lines.append("║     CLI AI — DATA QUALITY SUMMARY REPORT               ║")
    lines.append("╚══════════════════════════════════════════════════════════╝")
    lines.append("")
    lines.append(f"  Pipeline:       {report['pipeline_name']}")
    lines.append(f"  Run at:         {report['run_timestamp']}")
    lines.append(f"  Spec from:      {report['spec_generated_by']}")
    lines.append("")
    lines.append("  ┌─────────────── OVERVIEW ───────────────┐")
    lines.append(f"  │  Total input rows:     {s['total_input_rows']:>6}          │")
    lines.append(f"  │  Rows after dedup:     {s['rows_after_dedup']:>6}          │")
    lines.append(f"  │  Clean rows:           {s['clean_rows']:>6}          │")
    lines.append(f"  │  Flagged rows:         {s['flagged_rows']:>6}          │")
    lines.append(f"  │  Pass rate:            {s['pass_rate_pct']:>5}%          │")
    lines.append(f"  │  Issues detected:      {s['total_issues_found']:>6}          │")
    lines.append("  └─────────────────────────────────────────┘")
    lines.append("")

    # Issue breakdown
    if report["issues"]:
        lines.append("  ┌─────────────── ISSUES DETAIL ──────────────┐")
        for i, issue in enumerate(report["issues"], 1):
            lines.append(f"  │  [{issue['rule_id']}] {issue['rule_name']}")
            lines.append(f"  │     → {issue['detail']}")
            if "sample_values" in issue:
                vals = ", ".join(str(v) for v in issue["sample_values"][:3])
                lines.append(f"  │     → Samples: {vals}")
            lines.append("  │")
        lines.append("  └──────────────────────────────────────────────┘")
    else:
        lines.append("  ✓ No data quality issues detected!")

    lines.append("")

    # Anomaly highlights
    lines.append("  ┌─────── KEY ANOMALIES & RECOMMENDATIONS ───────┐")

    anomalies = []
    for issue in report["issues"]:
        rid = issue["rule_id"]
        if rid == "R001":
            anomalies.append("  │  ⚠ DUPLICATES: Exact duplicate orders found.")
            anomalies.append("  │    → Check upstream system for double-submission bugs.")
        elif rid == "R002":
            anomalies.append(f"  │  ⚠ MISSING DATA: {issue['detail']}.")
            anomalies.append("  │    → Enforce NOT NULL constraints at ingestion.")
        elif rid == "R003":
            anomalies.append(f"  │  ⚠ INVALID EMAILS: {issue['detail']}.")
            anomalies.append("  │    → Add email validation to the order form.")
        elif rid == "R004":
            anomalies.append(f"  │  ⚠ QUANTITY OUTLIERS: {issue['detail']}.")
            anomalies.append("  │    → Review for data entry errors or fraud.")
        elif rid == "R005":
            anomalies.append(f"  │  ⚠ NEGATIVE PRICES: {issue['detail']}.")
            anomalies.append("  │    → Investigate returns vs pricing errors.")
        elif rid == "R006":
            anomalies.append(f"  │  ⚠ DATE ISSUES: {issue['detail']}.")
            anomalies.append("  │    → Standardize date format at source.")
        elif rid == "R009":
            anomalies.append(f"  │  ⚠ BAD PAYMENT METHOD: {issue['detail']}.")
            anomalies.append("  │    → Restrict payment_method to enum values.")

    if anomalies:
        lines.extend(anomalies)
    else:
        lines.append("  │  ✓ No significant anomalies detected.")

    lines.append("  └─────────────────────────────────────────────────┘")
    lines.append("")

    # Output files
    lines.append("  Output files:")
    for name, path in report["output_files"].items():
        lines.append(f"    • {name}: {path}")
    lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    # Default path or accept CLI argument
    if len(sys.argv) > 1:
        rpt_path = sys.argv[1]
    else:
        rpt_path = str(Path(__file__).parent / "data" / "quality_report.json")

    summary = summarize_report(rpt_path)
    print(summary)
