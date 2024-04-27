from pathlib import Path
from utils.fetch import fetch_postprocessing_data, fetch_residuals
from utils.impute import impute_data
from utils.report import report
from utils.content import TabContent

import streamlit as st


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

        # Fetch the data
        residuals = impute_data(fetch_residuals(run_path))
        forceCoeffs = impute_data(fetch_postprocessing_data(
            run_path, directory='forceCoeffs'
        ))
        probes = impute_data(fetch_postprocessing_data(
            run_path, directory='probe'
        ))

        # Create the tabs
        tabs = ['Residuals', 'Force Coefficients', 'Probes', 'Report']
        residuals_tab, forceCoeffs_tab, probes_tab, report_tab = st.tabs(tabs)
        
        # Force coefficients tab
        with forceCoeffs_tab:
            forceCoeffs_content = TabContent(
                forceCoeffs,
                key='forceCoeffs',
                title='Force Coefficients',
                logscale=False,
                columns=['Cd', 'Cl', 'Cm', 'Cl(f)', 'Cl(r)'],
                stats=True,
                slider=True
            )
            forceCoeffs_content()

        # Residuals tab
        with residuals_tab:
            residuals_content = TabContent(
                residuals,
                key='residuals',
                title='Residuals',
                logscale=True,
                stats=False,
                slider=False
            )
            residuals_content()

        # Probes tab
        with probes_tab:
            probes_content = TabContent(
                probes,
                key='probes',
                title='Probes',
                logscale=False,
                stats=True,
                slider=True
            )
            probes_content()

        # Report tab
        with report_tab:
            df = report(run_path)
            df['Cd'] = round(
                forceCoeffs_content.stats_table.loc['mean', 'Cd'], 4
            )
            df['Cl'] = round(
                forceCoeffs_content.stats_table.loc['mean', 'Cl'], 4
            )
            df = df.set_index('Run ID').astype(str)
            st.table(df)
            st.download_button(
                'Export CSV',
                df.to_csv(),
                f'{run_path.name}.csv',
                'Download report'
            )

if __name__=='__main__':
    main()