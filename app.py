from pathlib import Path
from utils.plot import figure_in_tab
from utils.fetch import fetch_postprocessing_data, fetch_residuals
from utils.impute import impute_data

import streamlit as st


def iteration_slider(dataset, key):
    st.markdown('### Filter last N iterations')
    lim = st.select_slider(
        'Filter last N iterations',
        options=range(100, dataset.shape[0] + 1, 100),
        key=key + '_slider',
        label_visibility='hidden'
    )
    if type(lim) == int:
        return dataset.iloc[- (lim + 1):, :]
    return dataset


def show_stats(dataset):
    st.markdown('### Stats')
    st.table(dataset.describe().loc[['mean', 'std', 'min', 'max']])


def tab_content(
    dataset, key, title='', logscale=False, columns=[], stats=True, slider=True
):
    if dataset is not None:
        if columns:
            dataset = dataset[columns]
        sliced_dataset = dataset
        # =====================================================================
        if slider:
            sliced_dataset = iteration_slider(dataset, key)
            st.divider()
        # =====================================================================
        if stats:
            show_stats(sliced_dataset)
            st.divider()
        # =====================================================================
        st.markdown('### Plot')
        col_selector, col_toggle = st.columns([2, 1], gap='large')

        with col_toggle:
            for _ in range(2): st.write("")
            toggle = st.toggle("Select all fields", key=key + '_toggle')

        with col_selector:
            figure_in_tab(
                sliced_dataset,
                preselect_all=toggle,
                logscale=logscale,
                title=title,
            )
    else:
        st.write("No data found in this run.")


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
        tabs = ['Residuals', 'Force Coefficients', 'Probes']
        residuals_tab, forceCoeffs_tab, probes_tab = st.tabs(tabs)

        # Residuals tab
        with residuals_tab:
            tab_content(
                residuals,
                key='residuals',
                title='Residuals',
                logscale=True,
                stats=False,
                slider=False
            )

        # Force coefficients tab
        with forceCoeffs_tab:
            tab_content(
                forceCoeffs,
                key='forceCoeffs',
                title='Force Coefficients',
                logscale=False,
                columns=['Cd', 'Cl', 'Cm', 'Cl(f)', 'Cl(r)'],
                stats=True,
                slider=True
            )

        # Probes tab
        with probes_tab:
            tab_content(
                probes,
                key='probes',
                title='Probes',
                logscale=False,
                stats=True,
                slider=True
            )


if __name__=='__main__':
    main()