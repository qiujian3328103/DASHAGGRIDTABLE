from components.table import create_table, query_data_by_date_range
from dash import html, callback, Output, Input, State, dcc 
from dash.exceptions import PreventUpdate
import feffery_antd_components as fac
import datetime
import plotly.graph_objs as go 

def create_card_with_graph():
    data = [188.00, 188.10, 188.20, 188.30, 188.40, 188.50, 188.60, 188.70, 188.76]
    fig = go.Figure(go.Scatter(x=list(range(len(data)), y=data, mode='lines', fill='tozeroy', line=dict(color='red'))))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=60,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        showlegend=False,
    )
    graph = dcc.Graph(
        figure=fig,
        config={"displayModeBar": False},
        style={"height": "70px", "width": "100%"}
    )
    return fac.AntdCard(
        [
            fac.AntdRow(
                [
                    fac.AntdCol([
                        fac.AntdCard([graph])
                    ], span=12),
                ]
            )
        ]
    )