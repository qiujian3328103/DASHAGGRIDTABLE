import dash
from dash import html, dcc
from feffery_antd_components import AntdCard, AntdStatistic, AntdIcon, AntdSpace, AntdRow, AntdCol
import plotly.graph_objs as go
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)

# Sample data for the graph
data = [188.00, 188.10, 188.20, 188.30, 188.40, 188.50, 188.60, 188.70, 188.76]

# Create the graph figure
fig = px.area(x=list(range(len(data))), y=data, labels={"x": "Year-Week", "y": "Average TAT Time"})
# fig = go.Figure(go.Scatter(x=list(range(len(data))), y=data, mode='lines', fill='tozeroy', line=dict(color='red')))
layout = {
        "plot_bgcolor": "rgba(0, 0, 0, 0)",
        "paper_bgcolor": "rgba(0, 0, 0, 0)",
        "yaxis": {
            "visible": False,
            "fixedrange": True,
            "range": [min(data), max(data)]
        },
        "xaxis": {
            "visible": False,
            "fixedrange": True,
            "range": [0, len(data)-1],
        },
        "showlegend": False,
        "margin": {"l": 0, "r": 0, "t": 0, "b": 0}
    }
fig.update_layout(layout)

# Layout of the Dash app
app.layout = html.Div([
    AntdCard(
        [
            AntdRow([
                AntdCol([
                    AntdSpace(
                        [
                            html.Div(
                                [
                                    html.Strong("EDS", style={"fontSize": "16px", "color": "#003000"}),
                                    # html.Span("AMZN", style={"float": "right", "fontSize": "12px", "color": "#666"})
                                ]
                            ),
                            html.Div(
                                [
                                    AntdIcon(icon="antd-caret-up", style={"color": "green"}),  # Updated to use `icon`
                                    html.Span("0.03 %", style={"color": "green", "fontSize": "14px"})
                                ]
                            ),
                            html.Div(
                                [
                                    html.Span("Current Week", style={"color": "#666", "fontSize": "12px"})
                                ]
                            ),
                            html.Div(
                                [
                                    AntdStatistic(
                                        value=50,
                                        prefix="CNT",
                                        valueStyle={"fontSize": "20px", "color": "#003000"}
                                    )
                                ]
                            ),
                        ],
                        direction="vertical",
                        align="start",
                        style={"width": "100%"}
                    )                   
                    ], span=12),
                AntdCol([
                        dcc.Graph(
                                figure=fig,
                                config={"displayModeBar": False},
                                style={"height": "70px", "width": "100%"}
                            )
                    ], span=12,
                       style={
                        "display": "flex",
                        "justifyContent": "center",
                        "alignItems": "center",  # Align center vertically
                        "textAlign": "center"   # Align center horizontally
                    })
            ], style={"width": "100%"}),

        ],
        style={
            "width": "300px", 
            "borderRadius": "10px",
            "padding": "5px",  # Adjusted padding to wrap content better
            "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.1)"  # Optional: Adds a slight shadow for better visualization
        },
        hoverable=True,
        headStyle={'display': 'none'}  # Optional: Hides the card header
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)