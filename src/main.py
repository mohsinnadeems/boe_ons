"""
main.py

Orchestrates the end-to-end execution of the BOE ONS Data Pipeline:
1. Fetches historical vacancy data from the ONS website.
2. Cleans and structures the data for analysis.
3. Generates monthly vacancy visualizations.
4. Runs a forecasting model to predict future vacancy trends.

Each step is executed as a separate module or script, and progress is displayed in the console.
Outputs (cleaned data, plots, forecasts) are saved in the respective directories under the project root.
"""

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
ANALYSIS_DIR = ROOT_DIR / "analysis"

sys.path.insert(0, str(SRC_DIR))

import fetch_data
import data_cleaning_structuring


def run_script(script_path: Path, script_name: str) -> bool:
    """
    Executes a standalone Python script using subprocess.

    Args:
        script_path (Path): The path to the Python script to run.
        script_name (str): A human-readable name for the script (used for logging).

    Returns:
        bool: True if the script ran successfully (exit code 0), False otherwise.

    Side Effects:
        Prints progress and error messages to the console.
    """
    try:
        print(f"\n[Running] {script_name}")
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=ROOT_DIR
        )

        if result.returncode == 0:
            print(f"{script_name} completed successfully!")
            if result.stdout.strip():
                print(result.stdout)
        else:
            print(f"{script_name} failed (exit code {result.returncode})")
            if result.stderr:
                print("Error details:")
                print(result.stderr)
            return False
    except Exception as e:
        print(f"Error while running {script_name}: {e}")
        return False
    return True


def main():
    """
    Runs the complete data pipeline in four steps:
    1. Fetch data from the ONS website.
    2. Clean and structure the downloaded data.
    3. Generate plots of monthly vacancies.
    4. Produce vacancy forecasts.

    Outputs:
        - Cleaned dataset saved in /data
        - Plots saved in /plots
        - Forecast results saved in /data

    Side Effects:
        Prints pipeline progress and error messages to the console.

    Exits:
        Exits with status code 1 if any step fails.
    """
    print("=" * 75)
    print("BOE ONS Data Analysis — Full Run")
    print("=" * 75)

    try:
        # STEP 1: Fetch ONS data
        print("\n[STEP 1] Fetching data from ONS website...")
        fetch_data.main()
        print("Data fetching completed successfully!")

        # STEP 2: Clean and structure the data
        print("\n[STEP 2] Cleaning and structuring data...")
        data_cleaning_structuring.main()
        print("Data cleaning and structuring completed successfully!")

        # STEP 3: Plotting
        print("\n[STEP 3] Generating monthly vacancy plots...")
        plotting_script = ANALYSIS_DIR / "plot_vacancies.py"
        run_script(plotting_script, "Monthly Vacancy Plots")

        # STEP 4: Forecasting
        print("\n[STEP 4] Running forecasting model...")
        forecasting_script = ANALYSIS_DIR / "forecasting.py"
        run_script(forecasting_script, "Forecasting Model")

        print("\n" + "=" * 75)
        print("Analysis completed successfully!")
        print("Data downloaded, cleaned, analyzed, and visualized.")
        print("Check /data for outputs and /plot for generated visuals.")
        print("=" * 75)

    except Exception as e:
        print(f"\n Analysis failed due to error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
