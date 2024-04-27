import streamlit as st
import pandas as pd
from utils.plot import figure_in_tab
from typing import Any


def iteration_slider(dataset: pd.DataFrame, key: str) -> pd.DataFrame:
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


def show_stats(dataset: pd.DataFrame) -> Any:
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
