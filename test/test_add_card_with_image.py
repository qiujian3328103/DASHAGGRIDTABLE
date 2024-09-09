import dash
from dash import html, dcc
import feffery_antd_components as fac
from dash.dependencies import Input, Output, State, ALL
import uuid
from flask import Flask, request, jsonify
import base64

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

def create_image_div(image_url, div_id):
    return html.Div(
        id=div_id,
        style={'position': 'relative', 'display': 'inline-block', 'margin': '10px'},
        children=[
            fac.AntdImage(
                src=image_url,
                style={'width': '100px', 'height': '100px'}
            ),
            fac.AntdIcon(
                icon='antd-close-circle-two-tone',
                style={'position': 'absolute', 'top': '5px', 'right': '5px', 'fontSize': '20px', 'color': 'red', 'cursor': 'pointer'},
                id={"type": "close-button", "index": div_id}  # Dynamic ID
            )
        ]
    )

# Define the layout
app.layout = html.Div([
    create_image_div("https://via.placeholder.com/200", "image-div-1")
])

# Callback to test icon click
@app.callback(
    Input({'type': 'close-button', 'index': ALL}, 'nClicks'),
    prevent_initial_call=True
)
def test_icon_click(nClicks):
    if any(nClicks):
        print("pass")

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
