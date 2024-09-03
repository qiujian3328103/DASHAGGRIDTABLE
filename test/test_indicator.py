import dash
from dash import html, dcc
from feffery_antd_components import AntdCard, AntdStatistic, AntdIcon, AntdSpace
import plotly.graph_objs as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Sample data for the graph
data = [188.00, 188.10, 188.20, 188.30, 188.40, 188.50, 188.60, 188.70, 188.76]

# Create the graph figure
fig = go.Figure(go.Scatter(x=list(range(len(data))), y=data, mode='lines', fill='tozeroy', line=dict(color='red')))
fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    height=60,
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    showlegend=False,
)

# Layout of the Dash app
app.layout = html.Div([
    AntdCard(
        [
            AntdSpace(
                [
                    html.Div(
                        [
                            html.Strong("Amazon.com Inc", style={"fontSize": "16px", "color": "#003000"}),
                            html.Span("AMZN", style={"float": "right", "fontSize": "12px", "color": "#666"})
                        ]
                    ),
                    html.Div(
                        [
                            AntdIcon(icon='arrow-up', style={"color": "green"}),  # Updated to use `icon`
                            html.Span("0.03 %", style={"color": "green", "fontSize": "14px"})
                        ]
                    ),
                    html.Div(
                        [
                            html.Span("Current Value", style={"color": "#666", "fontSize": "12px"})
                        ]
                    ),
                    html.Div(
                        [
                            AntdStatistic(
                                value=188.76,
                                prefix="$",
                                valueStyle={"fontSize": "24px", "color": "#003000"}
                            )
                        ]
                    ),
                    dcc.Graph(
                        figure=fig,
                        config={"displayModeBar": False},
                        style={"height": "70px", "width": "100%"}  # Adjusted to fit within the card
                    )
                ],
                direction="vertical",
                align="start"
            )
        ],
        style={
            "width": "300px", 
            "borderRadius": "10px",
            "padding": "10px",  # Adjusted padding to wrap content better
            "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.1)"  # Optional: Adds a slight shadow for better visualization
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)