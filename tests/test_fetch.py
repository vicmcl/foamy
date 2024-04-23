import sys
sys.path.append(__file__.split("tests")[0])

from pathlib import Path
from utils.fetch import fetch_postprocessing_data, fetch_residuals

def main():
    # Define the run path
    project_path = "/home/victorien/openfoam9/motorBike"
    run_id = "run002"
    run_path = Path(f"{project_path}/{run_id}")
    
    # Fetch the postprocessing data
    data = fetch_postprocessing_data(run_path, directory='probes')
    print(data)

    # Fetch the residuals
    residuals = fetch_residuals(run_path)
    print(residuals)

if __name__ == "__main__":
    main()