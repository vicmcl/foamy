import streamlit as st
import pandas as pd

from pathlib import Path
from utils.content import TabContent, filter_columns
from utils.impute import impute_data
from utils.report import get_report
from utils.fetch import (
    fetch_postprocessing_dirs,
    fetch_postprocessing_data,
    fetch_residuals
)

SKIP_DIRS = ['cuttingPlane', 'sets']

def main():

    st.title('OpenFoam Data Viewer')
   
    # Define the run path
    selected_run = st.sidebar.selectbox(
        'Select the run',
        sorted([d for d in Path('.').iterdir() if d.is_dir()])
    )
    st.markdown(
        f'### Run ID: <font color="#FF4B4B">{selected_run}</font>',
        unsafe_allow_html=True)
    
    # If a run is selected
    if selected_run is not None:

        run_path = selected_run.resolve()
        residuals = impute_data(fetch_residuals(run_path))
        report = get_report(run_path)

        pdirs = fetch_postprocessing_dirs(run_path)['postProcessing']
        tabs_id = [pdir.name for pdir in pdirs if pdir.name not in SKIP_DIRS]
        tabs_id += ['Residuals', 'Report']
        tabs = st.tabs(tabs_id)

        for tab in tabs_id:
            with tabs[tabs_id.index(tab)]:

                if tab == 'Residuals':
                    residuals_content = TabContent(
                        residuals,
                        key='residuals',
                        title='Residuals',
                        logscale=True,
                        stats=False,
                        slider=False
                    )
                    residuals_content()

                elif tab == 'Report':
                    st.dataframe(report)

                else:
                    data = impute_data(
                        fetch_postprocessing_data(run_path, directory=tab)
                    )
                    content = TabContent(
                        data,
                        key=tab,
                        title=tab,
                        logscale=False,
                        columns=filter_columns(tab),
                        stats=True,
                        slider=True
                    )
                    content()
                    content_report = pd.DataFrame(
                        content.stats_table.loc['mean']
                    ).T.set_index(report.index)
                    content_report.columns = [
                        tab + '_' + col for col in content_report.columns
                    ]
                    report = pd.concat([report, content_report], axis=1)

if __name__=='__main__':
    main()