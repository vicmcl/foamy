import sys
sys.path.append(__file__.split("tests")[0])

from utils.report import report
from pathlib import Path



def main():
    # Define the run path
    project_path = "/home/victorien/openfoam9/motorBike"
    run_id = "run002"
    run_path = Path(f"{project_path}/{run_id}")

    df = report(run_path)
    print(df)
    

if __name__ == "__main__":
    main()