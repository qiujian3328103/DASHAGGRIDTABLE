import json
import random
import dash
import feffery_antd_components as fac
from dash import dcc, html, Input, Output, State, ClientsideFunction
import pandas as pd 
from dash import no_update

def process_csv_data():
    # Read the CSV file using pandas (assumes the CSV is in the same directory)
    df = pd.read_csv("/Users/JianQiu/Dropbox/pythonprojects/DashAggridTable/test/test_yield_data.csv")  # Replace with your actual CSV file path
    unique_dates = df['date'].unique()
    print(unique_dates)
    date_mapping = {date: idx for idx, date in enumerate(unique_dates)}

    # Map the `date` column to the new x values
    df['x_value'] = df['date'].map(date_mapping)
    
    data = df.to_dict(orient='records')
    
    return data



app = dash.Dash(__name__)

app.layout = html.Div(
    [
        fac.AntdRow(
            [
                fac.AntdCol(
                    [
                        fac.AntdSegmented(
                                id='segmented',
                                options=[
                                    {'label': i, 'value': i}
                                    for i in ['Bar', 'Scatter', 'Line', 'CDF', 'Perato', 'Boxplot']
                                ],
                                defaultValue='Scatter',
                            ),
                        html.Div(
                            id='highchart-container',
                            style={
                                'width': '500px',
                                'height': '500px'
                            }
                        ),   
                    ],
                    flex='none',
                    style={'height': 'fit-content'},
                ),
            ],
            gutter=10,
            justify='center',
            align='middle',
            style={
                'width': '100%',
                'height': 600,
                'borderRadius': 6,
                'border': '1px solid #40a9ff',
            },
        ),
        dcc.Store(id='data-store')
    ]
)

@app.callback(
    Output('data-store', 'data'),
    Input('segmented', 'value')
)
def get_echarts_options(segmented_value):
    data = process_csv_data()

    # Convert to JSON string
    json_string = json.dumps(data)
    return json_string
    

app.clientside_callback(
    ClientsideFunction(namespace='clientside_highchart', function_name='render_charts'),
    Output('highchart-container', 'children'),
    Input('data-store', 'data'), 
    State('segmented', 'value'),
)

if __name__ == "__main__":
    app.run(debug=True)