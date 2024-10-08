from dash import Dash, dcc, html, Input, Output, callback_context, State, ALL
import base64
import os
from dash.exceptions import PreventUpdate
import feffery_antd_components as fac
import feffery_utils_components as fuc
import uuid
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

def create_modal_content():
    return fac.AntdModal(
        [
        fac.AntdRow(
            [
                fac.AntdSpace(
                    [
                        fac.AntdSpace(
                            [
                                fac.AntdText('Date'),
                                fac.AntdDatePicker(
                                    id='date-picker',
                                    style={'width': '100%'}
                                ),
                            ], 
                            direction='vertical', 
                            wrap=True,
                            style={'width': '100%',}
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdText('Date'),
                                fac.AntdDatePicker(
                                    id='date-picker',
                                    style={'width': '100%'}
                                ),
                            ], 
                            direction='vertical', 
                            wrap=True,  
                            style={'width': '100%'}
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdText('Date'),
                                fac.AntdDatePicker(
                                    id='date-picker',
                                    style={'width': '100%'}
                                ),
                            ], 
                            direction='vertical', 
                            wrap=True,    
                            style={'width': '100%'}
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdText('Date'),
                                fac.AntdDatePicker(
                                    id='date-picker',
                                    style={'width': '100%'}
                                ),
                            ], 
                            direction='vertical',    
                            wrap=True,
                            style={'width': '100%'}
                        )
                    ],
                    style={'width': '100%', 'margin-bottom': '10px'},
                ),
                fac.AntdCol(
                    [
                        fac.AntdSpace(
                            [
                                fac.AntdText('Date'),
                                fac.AntdDatePicker(
                                    id='date-picker',
                                    style={'width': '100%'}
                                ),
                            ], 
                            direction='vertical', 
                            wrap=True,
                            style={'width': '100%',}
                        )
                    ], 
                    style={'margin-bottom': '10px'},
                    span=6
                ),
                fac.AntdCol(
                    [
                        fac.AntdSpace(
                            [
                                fac.AntdText('Date'),
                                fac.AntdDatePicker(
                                    id='date-picker',
                                    style={'width': '100%'}
                                ),
                            ], 
                            direction='vertical', 
                            wrap=True,
                            style={'width': '100%'}
                        )       
                    ], 
                    style={'margin-bottom': '10px'},
                    span=6
                ),
                fac.AntdCol(
                    [
                        fac.AntdSpace(
                            [   
                                fac.AntdText('Date'),
                                fac.AntdInput(
                                    id='input-field',
                                    placeholder='Enter text here',
                                    style={'width': '100%'}
                                ),
                            ], 
                            direction='vertical', 
                            wrap=True,
                            style={'width': '100%'}         
                        )
                    ], 
                    style={ 'margin-bottom': '10px'},
                    span=6
                ),
                fac.AntdCol(
                    [
                        fac.AntdSpace(                
                            [
                                fac.AntdText('Date'),
                                fac.AntdSelect(
                                    options=[
                                        {'label': 'Option 1', 'value': 'option1'},
                                        {'label': 'Option 2', 'value': 'option2'},
                                        {'label': 'Option 3', 'value': 'option3'}
                                    ],
                                    style={'width': '100%'}
                                ),
                            ], 
                            direction='vertical',       
                            wrap=True,
                            style={'width': '100%'}
                        )
                    ], 
                    style={'margin-bottom': '10px'},
                    span=6
                ),
            ]   
        )
    ],
    visible=False,
    id='modal-content',
    width="85vw",
    # closable=False,
    # centered=True,
    # maskClosable=False,
    style={'width': '100%'}
)

app.layout = html.Div([
    fac.AntdButton(
        'Open Modal',
        id='open-modal-button',
        type='primary'
    ),
    create_modal_content()
])

@app.callback(
    Output('modal-content', 'visible'),
    Input('open-modal-button', 'nClicks'),
    prevent_initial_call=True
)
def open_modal(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    return True

if __name__ == '__main__':
    app.run_server(debug=True)
    
    