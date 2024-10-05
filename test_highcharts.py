import json
import dash
import feffery_antd_components as fac
from dash import dcc, html, Input, Output, State, ClientsideFunction
import pandas as pd 
import dash_ag_grid as dag
from dash import no_update

def process_csv_data():
    df = pd.read_csv("/Users/JianQiu/Dropbox/pythonprojects/DashAggridTable/test/test_yield_data.csv")
    unique_dates = df['date'].unique()
    date_mapping = {date: idx for idx, date in enumerate(unique_dates)}
    df['x_value'] = df['date'].map(date_mapping)
    data = df.to_dict(orient='records')
    return data

def create_ag_grid_table():
    rowData = [
        {"root_lot_id": "lot1", "wafer_id": "01", "yield": 35000},
        {"root_lot_id": "lot2", "wafer_id": "02", "yield": 35000},
        {"root_lot_id": "lot3", "wafer_id": "03", "yield": 35000},
        {"root_lot_id": "lot4", "wafer_id": "04", "yield": 35000},
    ]
    columnDefs = [
        {"headerName": "Root Lot ID", "field": "root_lot_id", "cellStyle": {
            "color": "blue",
            "textDecoration": "underline",
            "cursor": "pointer"
        }},
        {"headerName": "Wafer ID", "field": "wafer_id"},
        {"headerName": "Yield", "field": "yield"},
    ]
    return html.Div([
        dag.AgGrid(
            id='ag-grid-table',
            columnDefs=columnDefs,
            rowData=rowData,
            style={'height': 400},
            className='custom-ag-grid',
        ),
    ])

# Create an Ag-Grid table for the modal
def create_modal_ag_grid_table(row_data):
    columnDefs = [
        {"headerName": "Root Lot ID", "field": "root_lot_id"},
        {"headerName": "Wafer ID", "field": "wafer_id"},
        {"headerName": "Yield", "field": "yield"},
    ]
    return dag.AgGrid(
        columnDefs=columnDefs,
        rowData=[row_data],
        style={'height': 200},
        className='modal-ag-grid',
    )

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
        fac.AntdRow(
            [
                fac.AntdCol(
                    [
                        create_ag_grid_table()
                    ],
                    flex='none',
                    style={'height': '300px', 'width': '100%'},
                ),
            ],
            gutter=10,
            justify='center',
            align='middle',
            style={
                'width': '100%',
                'height': 300,
                'borderRadius': 6,
                'border': '1px solid #40a9ff',
            },
        ),
        dcc.Store(id='data-store'),
        dcc.Store(id='table-data-store'),
        # Modal for showing clicked cell details
        fac.AntdModal(
            id='cell-modal',
            title='Cell Details',
            visible=False,
            children=html.Div(id='modal-content'),
            renderFooter=None,
        )
    ]
)

# Store the row data of the Ag-Grid in a dcc.Store
@app.callback(
    Output('table-data-store', 'data'),
    Input('ag-grid-table', 'rowData'),
)
def store_table_data(row_data):
    return row_data

@app.callback(
    Output('data-store', 'data'),
    Input('segmented', 'value')
)
def get_echarts_options(segmented_value):
    data = process_csv_data()
    json_string = json.dumps(data)
    return json_string

@app.callback(
    Output('cell-modal', 'visible'),
    Output('modal-content', 'children'),
    Input('ag-grid-table', 'cellClicked'),
    State('table-data-store', 'data'),
    prevent_initial_call=True
)
def display_cell_modal(cell_data, table_data):
    if cell_data and table_data:
        # Retrieve rowIndex from the cellClicked event
        row_index = cell_data['rowIndex']
        
        # Get the row data corresponding to the rowIndex
        row_data = table_data[row_index] if row_index < len(table_data) else {}

        # Create a new Ag-Grid table inside the modal with the clicked row's data
        modal_content = create_modal_ag_grid_table(row_data)
        return True, modal_content
    return False, no_update

app.clientside_callback(
    ClientsideFunction(namespace='clientside_highchart', function_name='render_charts'),
    Output('highchart-container', 'children'),
    Input('data-store', 'data'), 
    State('segmented', 'value'),
)

if __name__ == "__main__":
    app.run(debug=True)
