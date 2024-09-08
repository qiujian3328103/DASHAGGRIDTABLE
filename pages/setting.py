from dash import html, callback, Input, Output, State, ctx, ALL, MATCH, no_update
from dash.exceptions import PreventUpdate
import feffery_antd_components as fac
import sqlite3
from config import DB_URL

# Function to query data from the SQLite3 database
def query_table_data(table_name):
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()

    # Dynamically query all rows from the provided table name
    cursor.execute(f'SELECT * FROM {table_name}')
    data = cursor.fetchall()

    # Get column names
    cursor.execute(f'PRAGMA table_info({table_name})')
    columns = cursor.fetchall()
    column_names = [
        {
            "title": col[1], "dataIndex": col[1],
            "key": col[1],
        }
        for col in columns
    ]

    # Close the connection
    conn.close()

    # Format the data for AntdTable
    formatted_data = [
        {column_names[i]["dataIndex"]: row[i] for i in range(len(row))}
        for row in data
    ]

    return column_names, formatted_data


# Function to create input components inside AntdSpace
def create_input_space(columns, table_name):
    return html.Div([
            fac.AntdSpace(
                # Create inputs for each column except 'id'
                children=[
                    fac.AntdInput(
                        # Use the column name combined with the table name as the ID
                        id={'type': 'input', 'index': f'{col["dataIndex"]}-{table_name}'},  # Use match pattern
                        placeholder=f'Enter {col["title"]}',
                        style={"width": "200px"}
                    )
                    for col in columns if col["dataIndex"] != 'id'
                ],
                direction="horizontal",
                size="middle"
            ),
            html.Div(
                children=[
                    fac.AntdButton(id={'type': 'button-add', 'id': table_name}, type="primary", children="Add"),
                    fac.AntdButton(id={'type': 'button-delete', 'id': table_name}, type="primary", children="Delete"),
                ],
                style={"margin-top": "10px", "textAlign": "right"}
            )
    ], style={"margin-bottom": "10px"})


# Function to insert data into the database
def insert_data(table_name, data):
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()

    # Extract column names and values from the data dict
    columns = ', '.join(data.keys())
    placeholders = ', '.join('?' for _ in data)
    values = tuple(data.values())

    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(query, values)
    conn.commit()
    conn.close()



# Function to delete data from the SQLite3 database
def delete_data(table_name, row_id_column, row_id_value):
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()

    # Delete the row based on the provided row ID
    query = f"DELETE FROM {table_name} WHERE {row_id_column} = ?"
    cursor.execute(query, (row_id_value,))
    conn.commit()
    conn.close()
    

# Function to create the settings page
def create_settings_page():
    # Query data for each table
    pgm_process_columns, pgm_process_data = query_table_data('pgm_process_table')
    status_columns, status_data = query_table_data('status_table')
    fit_status_columns, fit_status_data = query_table_data('fit_status_table')
    reference_columns, reference_data = query_table_data('product_reference')

    return html.Div([
        fac.AntdButton('新通知', id='fragment-demo-trigger', type='primary'),
        fac.AntdTabs(
            id='tab-selection',
            activeKey='pgm-process-tab',
            items=[
                {
                    'key': 'pgm-process-tab',
                    'label': 'pgm-process-tab',
                    'children': html.Div([
                        create_input_space(columns=pgm_process_columns, table_name='pgm_process_table'),
                        fac.AntdTable(
                            id={'type': 'table', 'index': 'table-pgm-process'},
                            columns=pgm_process_columns,
                            data=pgm_process_data,
                            locale="en-us",
                            bordered=True,
                            rowSelectionType='radio',
                            maxHeight=300,
                            pagination={
                                'pageSize': 50,
                                'showSizeChanger': True,
                                'pageSizeOptions': [5, 10, 20, 50],
                            },
                        ),
                    ])
                },
                {
                    'key': 'status-tab',
                    'label': 'status-tab',
                    'children': html.Div([
                        create_input_space(columns=status_columns, table_name='status_table'),
                        fac.AntdTable(
                            id={'type': 'table', 'index': 'table-status'},
                            columns=status_columns,
                            data=status_data,
                            locale="en-us",
                            bordered=True,
                            rowSelectionType='radio',
                            maxHeight=300,
                            pagination={
                                'pageSize': 50,
                                'showSizeChanger': True,
                                'pageSizeOptions': [5, 10, 20, 50],
                            },
                        ),
                    ])
                },
                {
                    'key': 'fit-tab',
                    'label': 'fit-tab',
                    'children': html.Div([
                        create_input_space(columns=fit_status_columns, table_name='fit_status_table'),
                        fac.AntdTable(
                            id={'type': 'table', 'index': 'table-fit-status'},
                            columns=fit_status_columns,
                            data=fit_status_data,
                            locale="en-us",
                            bordered=True,
                            rowSelectionType='radio',
                            maxHeight=300,
                            pagination={
                                'pageSize': 50,
                                'showSizeChanger': True,
                                'pageSizeOptions': [5, 10, 20, 50],
                            },
                        ),
                    ])
                },
                {
                    'key': 'reference-tab',
                    'label': 'reference-tab',
                    'children': html.Div([
                        create_input_space(columns=reference_columns, table_name='product_reference'),
                        fac.AntdTable(
                            id={'type': 'table', 'index': 'table-product-reference'},
                            columns=reference_columns,
                            data=reference_data,
                            locale="en-us",
                            bordered=True,
                            rowSelectionType='radio',
                            maxHeight=300,
                            pagination={
                                'pageSize': 50,
                                'showSizeChanger': True,
                                'pageSizeOptions': [5, 10, 20, 50],
                            },
                        ),
                    ])
                },
            ]
        )
    ])


@callback(
    [Output({'type': 'table', 'index': ALL}, 'data', allow_duplicate=True),
    Output('fragment-demo-trigger', 'children', allow_duplicate=True)],
    [Input({'type': 'button-add', 'id': ALL}, 'nClicks')],
    [State('tab-selection', 'activeKey'), 
    State({'type': 'input', 'index': ALL}, 'value'), 
    State({'type': 'input', 'index': ALL}, 'id'),
    State({'type': 'table', 'index': ALL}, 'id'),
    State({'type': 'table', 'index': ALL}, 'data')],
    prevent_initial_call=True
)
def test_match_callback(nClicks, active_tab, input_values, input_ids, table_ids, table_values):
    # print(input_values)
    # print(active_tab)
    # print(table_values)

    triggered_id = ctx.triggered_id
    # print(f"Triggered ID: {triggered_id}")

    # Identify which table's add button was clicked
    clicked_button_table = triggered_id['id']
    # print(f"Clicked button: {clicked_button_table}")

    # Ensure that the table name is valid and matches the expected table name
    valid_tables = ['pgm_process_table', 'status_table', 'fit_status_table', 'product_reference']
    # store the table and tab mapping
    valid_tables_dictions = {
        'pgm_process_table': 'table-pgm-process',
        'status_table': 'table-status',
        'fit_status_table': 'table-fit-status',
        'product_reference': 'table-product-reference'
    }
    
    if clicked_button_table not in valid_tables_dictions.keys():
        raise no_update

    # # Filter inputs based on the clicked button (i.e., table name)
    filtered_inputs = [
        (input_id, value) for input_id, value in zip(input_ids, input_values)
        if input_id['index'].endswith(clicked_button_table)  # Filter by table name
    ]

    # # Map input fields to their corresponding values
    input_dict = {input_id['index'].split('-')[0]: value for input_id, value in filtered_inputs if value}
    # print(f"Filtered Inputs: {input_dict}")

    # # Insert data into the appropriate table
    insert_data(table_name=clicked_button_table, data=input_dict)

    # # Re-query the updated table data
    _, updated_data = query_table_data(table_name=clicked_button_table)
    print(len(updated_data))
    # print('******************')
    # print(updated_data)
    # # Return the updated data for the table
    # print("-----------------")
    # print(table_ids)
    # print(table_values)
    
    all_table_data = []
    for index, table_id in enumerate(table_ids):
        if table_id['index'] == valid_tables_dictions[clicked_button_table]:
            all_table_data.append(updated_data)
        else:
            all_table_data.append(table_values[index])
            
    message = fac.AntdMessage(content='Data Updated', type='success')
    
    
    return all_table_data, message

@callback(
    [Output({'type': 'table', 'index': ALL}, 'data', allow_duplicate=True),
     Output('fragment-demo-trigger', 'children', allow_duplicate=True)],
    [Input({'type': 'button-delete', 'id': ALL}, 'nClicks')],  # Capture delete button clicks
    [State('tab-selection', 'activeKey'), 
     State({'type': 'table', 'index': ALL}, 'id'),
     State({'type': 'table', 'index': ALL}, 'data'),
     State({'type': 'table', 'index': ALL}, 'selectedRows')],  # Capture selected row(s)
    prevent_initial_call=True
)
def delete_select_id(nClicks_delete, active_tab, table_ids, table_values, selected_rows):
    # Determine which button was clicked
    triggered_id = ctx.triggered_id

    # Identify which table's add button was clicked
    clicked_button_table = triggered_id['id']
    print(f"Clicked button: {clicked_button_table}")
    
    # detemine the select rows 
    print(selected_rows)
    
    # since the order of the table_id and tab_id is same, build the dictionary
    # for later access the index in in the table_id to identify which data accessed 
    # in the selected_rows, since the selected_rows retrun a list of dictionary 
    # since use the ALL, all the selected rows in the tab will be get 
    
    valid_tables_dictions = {
        'pgm_process_table': 'table-pgm-process',
        'status_table': 'table-status',
        'fit_status_table': 'table-fit-status',
        'product_reference': 'table-product-reference'
    }

    # Ensure that the table name is valid and matches the expected table name
    current_select_tab_index = 0
    
    for index, table_id in enumerate(table_ids):
        if valid_tables_dictions[clicked_button_table] == table_id['index']:
            current_select_tab_index = index
            break
        
    print(f"Current Select Tab Index: {current_select_tab_index}")
    
    # access the selected rows
    current_select_row = selected_rows[current_select_tab_index]
    
    # return no update if the selected row is empty
    if current_select_row is None:
        message = fac.AntdMessage(content='Please select a row to delete', type='error')
        return no_update, message
    
    # get the selected row id
    
    delete_data(table_name=clicked_button_table, row_id_column='id', row_id_value=current_select_row[0]['id'])
    
    # # Re-query the updated table data
    _, updated_data = query_table_data(table_name=clicked_button_table)
    
    # Return the updated data for the table
    all_table_data = []
    for index, table_id in enumerate(table_ids):
        if table_id['index'] == valid_tables_dictions[clicked_button_table]:
            all_table_data.append(updated_data)
        else:
            all_table_data.append(table_values[index])
            
    message = fac.AntdMessage(content='Data Deleted', type='success')
    
    return all_table_data, message