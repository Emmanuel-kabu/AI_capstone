"""
Automated Workflow Runner
=========================
Runs the entire AI-powered data quality pipeline end-to-end:

  Step 1: Load the Chat AI-generated spec (data_quality_spec.json)
  Step 2: Execute the IDE AI-generated ETL pipeline (etl_pipeline.py)
  Step 3: Run the CLI AI summarizer (summarize_results.py)

Usage:
  python run_workflow.py
"""

import subprocess
import sys
import time
from pathlib import Path


BASE_DIR = Path(__file__).parent
PYTHON = sys.executable  # Use the same Python interpreter running this script


def banner(text: str):
    width = 60
    print()
    print("=" * width)
    print(f"  {text}")
    print("=" * width)
    print()


def check_dependencies():
    """Ensure required packages are installed."""
    missing = []
    for pkg in ["pandas", "numpy"]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"[SETUP] Installing missing packages: {', '.join(missing)} ...")
        subprocess.check_call(
            [PYTHON, "-m", "pip", "install", *missing],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("[SETUP] Packages installed successfully.\n")
    else:
        print("[SETUP] All dependencies are available.\n")


def check_input_files():
    """Verify that required input files exist."""
    spec_file = BASE_DIR / "specs" / "data_quality_spec.json"
    data_file = BASE_DIR / "data" / "raw_sales_data.csv"

    errors = []
    if not spec_file.exists():
        errors.append(f"  Missing: {spec_file}")
    if not data_file.exists():
        errors.append(f"  Missing: {data_file}")

    if errors:
        print("[ERROR] Required input files not found:")
        for e in errors:
            print(e)
        print("\nPlease ensure the Chat AI spec and raw data are in place.")
        sys.exit(1)

    print(f"[CHECK] Spec file:  {spec_file.name}  ... OK")
    print(f"[CHECK] Data file:  {data_file.name}  ... OK\n")


def run_step(step_num: int, description: str, script: str):
    """Run a Python script as a subprocess and stream its output."""
    banner(f"STEP {step_num}: {description}")

    script_path = BASE_DIR / script
    if not script_path.exists():
        print(f"[ERROR] Script not found: {script_path}")
        sys.exit(1)

    start = time.time()
    result = subprocess.run(
        [PYTHON, str(script_path)],
        cwd=str(BASE_DIR),
        capture_output=False,  # stream output live
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"\n[FAILED] Step {step_num} exited with code {result.returncode}")
        sys.exit(result.returncode)

    print(f"\n[DONE] Step {step_num} completed in {elapsed:.1f}s")


def show_final_summary():
    """Show the final output file listing."""
    banner("WORKFLOW COMPLETE")

    output_files = {
        "Cleaned data":   BASE_DIR / "data" / "cleaned_sales_data.csv",
        "Flagged rows":   BASE_DIR / "data" / "flagged_rows.csv",
        "Quality report": BASE_DIR / "data" / "quality_report.json",
    }

    print("  Output files generated:")
    for label, path in output_files.items():
        status = "OK" if path.exists() else "MISSING"
        size = f"({path.stat().st_size:,} bytes)" if path.exists() else ""
        print(f"    [{status}] {label}: {path.name} {size}")

    print()
    print("  Workflow steps completed:")
    print("    1. Chat AI spec loaded       (data_quality_spec.json)")
    print("    2. ETL pipeline executed      (etl_pipeline.py)")
    print("    3. CLI summary generated      (summarize_results.py)")
    print()
    print("  All done! Review the outputs in the data/ folder.")
    print()


def main():
    banner("AI-POWERED DATA QUALITY WORKFLOW")
    print("  This script runs the full pipeline automatically.")
    print("  Workflow: Chat AI (spec) -> IDE AI (pipeline) -> CLI AI (summary)\n")

    # Pre-flight checks
    check_dependencies()
    check_input_files()

    # Execute the 2-step pipeline
    # (Step 1 is the Chat AI spec, which is already a file on disk)
    run_step(
        step_num=1,
        description="ETL Pipeline — Apply quality rules from Chat AI spec",
        script="etl_pipeline.py",
    )

    run_step(
        step_num=2,
        description="CLI Summarizer — Generate anomaly report",
        script="summarize_results.py",
    )

    # Final summary
    show_final_summary()


if __name__ == "__main__":
    main()
