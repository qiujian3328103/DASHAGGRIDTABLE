import dash
import feffery_antd_components as fac
from dash import html, dcc
import plotly.express as px
import numpy as np
from utilities.data_process import query_and_group_tat_time

def create_indicator_card(title, get_cached_data):
    np.random.seed(1)
    # y = np.random.random_sample(24) * 100
    # x = np.arange(len(y))
    df = get_cached_data()
    
    # Create the plot with hover information
    x = df['year-week'].tolist()
    y = df['tat_time'].tolist()
    fig = px.line(x=x, y=y, labels={"x": "Year-Week", "y": "Average TAT Time"})

    
    fig.update_traces(line=dict(color="red", width=2),
                       hovertemplate='Year-Week: %{x}<br>TAT: %{y} days')
    
    layout = {
        "plot_bgcolor": "rgba(0, 0, 0, 0)",
        "paper_bgcolor": "rgba(0, 0, 0, 0)",
        "yaxis": {
            "visible": False,
            "fixedrange": True
        },
        "xaxis": {
            "visible": False,
            "fixedrange": True,
            "range": [0, len(x)-1],
        },
        "showlegend": False,
        "margin": {"l": 0, "r": 0, "t": 0, "b": 0}
    }

    fig.update_layout(layout)

    indicator_title = title
    indicator_description = "Open 9/20"
    statiscs_title = "WW28"
    statiscs_value = "0.23%"
    icon_color = "red"
    icon_type = "antd-caret-up"
    
    return fac.AntdCard(
        [
            html.Div([
                fac.AntdRow(
                    [
                        fac.AntdCol([
                            html.H2(indicator_title),
                            fac.AntdStatistic(title=statiscs_title, value=statiscs_value, prefix=fac.AntdIcon(icon=icon_type, style={"color": icon_color})),
                        ], span=12),
                        fac.AntdCol([
                            dcc.Graph(figure=fig, config={"displayModeBar": False}, style={"height": "90px", "width": "100%", "marginTop": "20px"}),
                        ], span=12),
                    ],
                    gutter=10,
                    style={"textAlign": "center"}
                ),
            ],
            style={"width": "100%"}
            ),
        ], 
        style={
                "height": "160px",
                "border": "1px solid #e8e8e8", 
                "borderRadius": "10px", 
                "margin": "10px",
        },
        bodyStyle={'padding': '10px'},
        headStyle={'display': 'none'},
        hoverable=True,
    )