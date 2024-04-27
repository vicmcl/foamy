import plotly.graph_objs as go
import streamlit as st


def figure_in_tab(
        dataset, columns, logscale=False, ylabel=None, title=''
    ): 
    # Plot the fields
    traces = []
    for col in columns:
        trace = go.Scatter(
            x=dataset[columns].index,
            y=dataset[columns][col],
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