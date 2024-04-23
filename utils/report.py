import pandas as pd 

from functools import partial
from pathlib import Path
from utils.fetch import fetch_postprocessing_dirs
from typing import Any


def get_line(run_path: Path, start_line: str) -> Any:
    with open(run_path / 'log.simpleFoam', 'r') as f:
        for line in f:
            if line.startswith(start_line):
                return line.split(':')[-1].strip()
    return None


def get_last_line(run_path: Path, file_name: str) -> Any:
    log_file = [
        log for log in fetch_postprocessing_dirs(run_path)['logs']
        if file_name in log.name
    ][-1]
    return pd.read_csv(log_file, sep='\t', header=None).iloc[-1,1]


get_iterations = partial(get_last_line, file_name='Separator')
get_duration = partial(get_last_line, file_name='executionTime')
get_date = partial(get_line, start_line='Date')
get_solver = partial(get_line, start_line='Exec')
get_n_cpu = partial(get_line, start_line='nProcs')



def report(run_path: Path):
    df = pd.DataFrame(
        {       
            'Project': [run_path.parent.name],
            'Run ID': [run_path.name],
            'Iterations': [get_iterations(run_path)],
            'Date': [get_date(run_path)],
            'Duration': [get_duration(run_path)],
            'Solver': [get_solver(run_path).split()[0]],
            'CPU': [get_n_cpu(run_path)]
        }
    )
    return df
