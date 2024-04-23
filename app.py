from pathlib import Path
from utils.plot import figure_in_tab
from utils.fetch import fetch_postprocessing_data, fetch_residuals
from utils.impute import impute_data
from utils.report import report

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
    stats_df = dataset.describe().loc[['mean', 'std', 'min', 'max']]
    st.table(stats_df)
    return stats_df


class TabContent():

    def __init__(
        self,
        dataset,
        key,
        title='',
        logscale=False,
        columns=[],
        stats=True,
        slider=True
    ):
        self.dataset = dataset
        self.key = key
        self.title = title
        self.logscale = logscale
        self.columns = columns
        self.stats = stats
        self.slider = slider
    
    def __call__(self):
        if self.dataset is not None:
            if self.columns:
                self.dataset = self.dataset[self.columns]
            sliced_dataset = self.dataset
            # =================================================================
            if self.slider:
                sliced_dataset = iteration_slider(self.dataset, self.key)
                st.divider()
            # =================================================================
            if self.stats:
                self.stats_table = show_stats(sliced_dataset)
                st.divider()
            # =================================================================
            st.markdown('### Plot')
            col_selector, col_toggle = st.columns([2, 1], gap='large')

            with col_toggle:
                for _ in range(2): st.write("")
                toggle = st.toggle(
                    "Select all fields", key=self.key + '_toggle'
                )

            with col_selector:
                figure_in_tab(
                    sliced_dataset,
                    preselect_all=toggle,
                    logscale=self.logscale,
                    title=self.title,
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
                'Export .csv',
                df.to_csv(),
                f'{run_path.name}.csv',
                'Download report'
            )

if __name__=='__main__':
    main()