import json
import dash
import feffery_antd_components as fac
from dash import dcc, html, Input, Output, State, ClientsideFunction, ALL
import pandas as pd 
import dash_ag_grid as dag
from dash import no_update
from utilities.wafer_map import create_wafer_data

def read_wafer_map_data():
    root_lot_id = "ABCDEF"
    wafer_data, shot_data, width, height = create_wafer_data(root_lot_id)
    return wafer_data, shot_data, width, height

def generate_card_child(num_of_cards=25):
    children = []
    for i in range(1, num_of_cards+1):
        children.append(
            fac.AntdCard(
                [
                    html.Div(
                        children=[],
                        id={'type':'wafer-container', 'index': f'wafer-map-{i}'},
                        style={'height': '200px', 'width': '200px'},
                    )
                ],
                style={'margin': '10px 0'},
                headStyle={'display': 'none'},
            )
        )
    return children


app = dash.Dash(__name__)

app.layout = fac.AntdLayout(
    [
        dcc.Store(id='data-store'),
        fac.AntdHeader(
            fac.AntdTitle(
                '页首示例', level=2, style={'color': 'white', 'margin': '0'}
            ),
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
            },
        ),
        fac.AntdLayout(
            [
                fac.AntdSider(
                    fac.AntdCenter(
                        fac.AntdTitle(
                            '侧边栏示例', level=2, style={'margin': '0'}
                        ),
                        style={
                            'height': '100%',
                        },
                    ),
                    style={
                        'backgroundColor': 'rgb(240, 242, 245)',
                        'display': 'flex',
                        'justifyContent': 'center',
                    },
                ),
                fac.AntdLayout(
                    [
                        fac.AntdContent(
                            fac.AntdSplitter(
                                items=[
                                    {
                                        'children': [
                                            fac.AntdFlex(
                                                generate_card_child(),
                                                id='flex-align',
                                                wrap='wrap',
                                                style={
                                                    'width': '100%',
                                                    # 'height': '100%',
                                                    'borderRadius': 6,
                                                    'border': '1px solid #40a9ff',
                                                },
                                                
                                            ),
                                        ],
                                        'defaultSize': '70%',
                                    },
                                    {
                                        'children': fac.AntdCenter(
                                            '70%', style={'height': '100%'}
                                        ),
                                        'defaultSize': '30%',
                                    },
                                ],
                                style={
                                    'height': '100%',
                                    'boxShadow': '0 0 10px rgba(0, 0, 0, 0.1)',
                                },
                            ),
                            style={'backgroundColor': 'white'},
                        ),
                        fac.AntdFooter(
                            fac.AntdCenter(
                                fac.AntdTitle(
                                    '页尾示例',
                                    level=2,
                                    style={'margin': '0'},
                                ),
                                style={
                                    'height': '100%',
                                },
                            ),
                            style={
                                'backgroundColor': 'rgb(193, 193, 193)',
                                'height': '10px',
                            },
                        ),
                    ]
                ),
            ],
            style={'height': '100%'},
        ),
    ],
    style={'height': '100vh'},
)


# Callback to store all wafer data in a single dcc.Store
@app.callback(
    # Output('data-store', 'data'),
    Input({'type': 'wafer-container', 'index': ALL}, 'id'),
)
def update_wafer_map(ids):
    print(ids)
    # Get the wafer data from your utility function
    wafer_data, shot_data, width, height = create_wafer_data("ABCDEF")
    
    # Create a dictionary with IDs as keys and serialize it
    data = {id['index']: {'wafer_data': wafer_data, 'width': width, 'height': height} for id in ids}
    
    # Manually JSON dump the dictionary to handle nested dictionaries
    # return json.dumps(data)

# This triggers the clientside D3 function to render the wafer map
# app.clientside_callback(
#     ClientsideFunction(namespace='clientside_d3', function_name='render_wafer_map'),
#     Output({'type': 'wafer-container', 'index': ALL}, 'children'),
#     Input('data-store', 'data'),
#     [State({'type': 'wafer-container', 'index': ALL}, 'id')],
# )
   

if __name__ == "__main__":
    app.run(debug=True)