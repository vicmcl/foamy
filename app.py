from pathlib import Path
from utils.plot import figure_in_tab
from utils.fetch import fetch_postprocessing_data, fetch_residuals
from utils.impute import impute_data

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
        probes = impute_data(
            fetch_postprocessing_data(run_path, directory='probe')
        )
        forceCoeffs = impute_data(
            fetch_postprocessing_data(run_path, directory='forceCoeffs')
        )

        # Create the tabs
        tabs = ['Residuals', 'Force Coefficients', 'Probes']
        residuals_tab, forceCoeffs_tab, probes_tab = st.tabs(tabs)

        # Residuals tab
        with residuals_tab:
            col_selector, col_toggle = st.columns([2, 1], gap='large')

            with col_toggle:
                for _ in range(2): st.write("")
                toggle = st.toggle("Select all fields", key='residuals')

            with col_selector:
                figure_in_tab(
                    residuals,
                    logscale=True,
                    preselect_all=toggle,
                    title='Residuals'
                )

        # Force coefficients tab
        with forceCoeffs_tab:
            if forceCoeffs is not None:
                dataset = forceCoeffs[['Cd', 'Cl', 'Cm', 'Cl(f)', 'Cl(r)']]

                st.markdown('### Filter last N iterations')
                lim = st.select_slider(
                    'Filter last N iterations',
                    options=range(100, dataset.shape[0] + 1, 100),
                    key='forceCoeffs_slider',
                    label_visibility='hidden'
                )
                if type(lim) == int:
                    sliced_dataset = dataset.iloc[-lim-1:, :]
                else:
                    sliced_dataset = dataset

                st.divider()
                st.markdown('### Stats')
                st.table(
                    sliced_dataset.describe().loc[
                        ['mean', 'std', 'min', 'max']
                    ]
                )
                
                st.divider()
                st.markdown('### Plot')
                col_selector, col_toggle = st.columns([2, 1], gap='large')

                with col_toggle:
                    for _ in range(2): st.write("")
                    toggle = st.toggle("Select all fields", key='forceCeoffs')

                with col_selector:
                    figure_in_tab(
                        sliced_dataset,
                        preselect_all=toggle,
                        title='Force Coefficients',
                    )
            else:
                st.write("No force coefficient found in this run.")

        # Probes tab
        with probes_tab:
            if probes is not None:

                st.markdown('### Filter last N iterations')
                lim = st.select_slider(
                    'Filter last N iterations',
                    options=range(100, dataset.shape[0] + 1, 100),
                    key='probes_slider',
                    label_visibility='hidden'
                )
                if type(lim) == int:
                    sliced_dataset = probes.iloc[-lim-1:, :]
                else:
                    sliced_dataset = probes

                st.divider()
                st.markdown('### Stats')
                st.table(
                    sliced_dataset.describe().loc[
                        ['mean', 'std', 'min', 'max']
                    ]
                )
                st.divider()
                st.markdown('### Plot')
                col_selector, col_toggle = st.columns([2, 1], gap='large')
                
                with col_toggle:
                    for _ in range(2): st.write("")
                    toggle = st.toggle("Select all fields", key='probes')
                
                with col_selector:
                    figure_in_tab(
                        sliced_dataset, preselect_all=toggle, title='Probes'
                    )
            else:
                st.write("No probe found in this run.")


if __name__=='__main__':
    main()