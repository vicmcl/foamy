import plotly.graph_objs as go
import streamlit as st

def figure_in_tab(
        dataset, logscale=False, preselect_all=False, ylabel=None, title=''
    ):
    # Select the fields to plot
    selected_columns = st.multiselect(
        'Select the fields to plot',
        dataset.columns,
        default=dataset.columns.tolist() if preselect_all else None
    )

    # Plot the fields
    traces = []
    for col in selected_columns:
        trace = go.Scatter(
            x=dataset[selected_columns].index,
            y=dataset[selected_columns][col],
            mode='lines',
            name=col,
        )
        traces.append(trace)

    # Set the y-axis parameters
    y_params = dict(
        title=ylabel, type='log', dtick=1
    ) if logscale else dict(title=ylabel)

    # Create the figure
    layout = go.Layout(
        title=title,
        xaxis=dict(title='Time / Iterations'),
        yaxis=y_params
    )
    fig = go.Figure(data=traces, layout=layout)
    st.plotly_chart(fig)