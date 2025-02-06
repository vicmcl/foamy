import streamlit as st
import pandas as pd
from utils.plot import figure_in_tab
from typing import Any, List


def iteration_slider(dataset: pd.DataFrame, key: str) -> pd.DataFrame:
    st.markdown('### Filter last N iterations')
    lim = st.select_slider(
        'Filter last N iterations',
        options=range(100, dataset.shape[0] + 1, 100),
        key=key + '_slider',
        label_visibility='hidden'
    )
    if isinstance(lim, int):
        return dataset.iloc[- (lim + 1):, :]
    return dataset


def show_stats(dataset: pd.DataFrame) -> Any:
    st.markdown('### Stats')
    stats_df = dataset.describe().loc[['mean', 'std', 'min', 'max']]
    st.table(stats_df)
    return stats_df


def filter_columns(tab) -> List:
    if 'forceCoeffs' in tab:
        return ['Cd', 'Cl', 'Cm', 'Cl(f)', 'Cl(r)']
    return []
    
                
class TabContent():
    
    def __init__(
        self,
        dataset: pd.DataFrame,
        key: str,
        title: str = "",
        logscale: bool = False,
        columns: List[str] = None,
        stats: bool = True,
        slider: bool = True
    ):
        self.dataset = dataset
        self.key = key
        self.title = title
        self.logscale = logscale
        self.columns = columns if columns else []
        self.stats = stats
        self.slider = slider
    
    def __call__(self):
        if self.dataset is not None:
            if self.columns:
                self.dataset = self.dataset[self.columns]
            sliced_dataset = self.dataset
            
            if self.slider:
                sliced_dataset = iteration_slider(self.dataset, self.key)
                st.divider()
            
            if self.stats:
                self.stats_table = show_stats(sliced_dataset)
                st.divider()
            
            st.markdown('### Plot')

            selected_columns = st.multiselect(
                'Select the fields to plot',
                sliced_dataset.columns,
                key=self.key + '_selector',
                placeholder='Default: All Fields Selected',
            )

            if not selected_columns:
                selected_columns = sliced_dataset.columns.tolist()

            figure_in_tab(
                sliced_dataset,
                columns=selected_columns,
                logscale=self.logscale,
                title=self.title,
            )
        else:
            st.write("No data found in this run.")
