import dash
import json
from dash import html, dcc
import feffery_antd_components as fac
from dash.dependencies import Input, Output, State, ClientsideFunction

app = dash.Dash(__name__)

with open('./stock-DJI.json', encoding='utf-8') as j:
    data = json.load(j)

app.layout = html.Div(
    [
        # 依赖的数据
        dcc.Store(
            id='chart-data',
            data=data
        ),

        fac.AntdSpace(
            [
                fac.AntdButton(
                    '渲染图表',
                    id='render-chart',
                    type='primary'
                ),
                html.Div(
                    id='chart-container',
                    style={
                        'height': 600
                    }
                ),
                html.Div(
                    id='show-brush-range'
                ),
                html.Div(
                    id='show-slider-range'
                )
            ],
            direction='vertical',
            style={
                'width': '100%'
            }
        )
    ],
    style={
        'padding': '25px 50px'
    }
)

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='renderChart'
    ),
    Output('chart-container', 'children'),
    Input('render-chart', 'nClicks'),
    [State('chart-data', 'data'),
     State('chart-container', 'id')],
    prevent_initial_call=True
)

if __name__ == '__main__':
    app.run(debug=True)
