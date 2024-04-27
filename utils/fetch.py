import pandas as pd
from pathlib import Path
from typing import Dict

def parse_columns(file_path: Path) -> list:
    """Parse the columns from a file

    Args:
        file_path (Path): The path to the file
    
    Returns:
        list: A list containing the column names
    """
    with open(file_path, 'r') as f:

        # Check if the file is a residuals file
        if file_path.name.endswith('FinalRes_0'):
            return ['Time', file_path.name.split('FinalRes')[0]]
        
        for line in f:
            if line.startswith('# Probe'):
                match file_path.name:
                    case 'U':
                        return  ['Time', 'Ux', 'Uy', 'Uz']
                    case _:
                        return ['Time', file_path.name]
            if line.startswith('# Time'):
                columns = line.strip().split()[2:]
                break

    return ['Time'] + columns


def strip_parentheses(s: str):
    """Strip parentheses from a string

    Args:
        s (str): The string to strip parentheses from

    Returns:
        float: The float value of the string with parentheses stripped
    """
    while s.startswith("("):
        s = s[1:]
    while s.endswith(")"):
        s = s[:-1]
    
    return float(s)


def fetch_postprocessing_dirs(run_path: Path) -> Dict:
    """Fetch the postprocessing directories from the run directory

    Args:
        run_path (Path): The path to the run directory

    Returns:
        Dict: A dictionary containing the postprocessing directories and log files
    """
    run_id = run_path.name

    postprocessing_dir = run_path / 'postProcessing'
    postprocessing_outputs = [
        output for output in postprocessing_dir.iterdir() if output.is_dir()
    ]

    log_dir = run_path / 'logs'
    log_files = [log for log in log_dir.iterdir() if log.is_file()]

    return {
        'run_id': run_id,
        'postProcessing': postprocessing_outputs,
        'logs': log_files
    }


def fetch_residuals(run_path: Path) -> pd.DataFrame:
    """Fetch the residuals from the run directory

    Args:
        run_path (Path): The path to the run directory

    Returns:
        pd.DataFrame: A DataFrame containing the residuals data
    """

    # Fetch the residuals files
    residuals_files = [
        f for f in fetch_postprocessing_dirs(run_path)['logs'] 
        if f.name.endswith('Res_0')
    ]
    # Concatenate the residuals data
    residuals_df = pd.concat([
        pd.read_csv(
            f, sep=r'\s+', comment='#', names=parse_columns(f)
        ).set_index('Time') for f in residuals_files
    ], axis=1)

    return residuals_df


def fetch_postprocessing_data(
        run_path: Path, directory: str | None = None
) -> pd.DataFrame | None:
    """Fetch the postprocessing data from the run directory

    Args:
        run_path (Path): The path to the run directory
        directory (str): The directory to fetch the data from
    
    Returns:
        pd.DataFrame: A DataFrame containing the postprocessing data
    
    Raises:
        IndexError: If the directory is not found in the postProcessing directory
    """

    postProcessing = fetch_postprocessing_dirs(run_path)['postProcessing']
    if directory is not None:
        try:
            selected_dir = [d for d in postProcessing if directory in d.name][0]
        except IndexError:
            return None
    else:
        selected_dir = postProcessing

    # Loop through the postProcessing directories
    df = pd.DataFrame()

    # Loop through the timesteps in the directory
    for timestep in selected_dir.iterdir():
        all_files_data = pd.DataFrame()

        # Loop through the files in the timestep directory
        for f in timestep.iterdir():
            if f.is_file():
                file_path = selected_dir / timestep / f
                columns = parse_columns(file_path)

                # Read the data from the file
                new_data = pd.read_csv(
                    file_path, sep=r'\s+', comment='#', names=columns
                ).set_index('Time')

                # Strip parentheses from columns data
                for col in new_data.select_dtypes(include=['object']).columns:
                    new_data[col] = new_data[col].apply(strip_parentheses)
                
                # Concatenate the new file to the existing data
                all_files_data = pd.concat([all_files_data, new_data], axis=1)

        # Concatenate the data from the new timestep to the existing data
        df = pd.concat([df, all_files_data], axis=0)
    
    return df