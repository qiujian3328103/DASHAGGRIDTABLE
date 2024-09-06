from dash import html, callback, Input, Output, State
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
            'editable': True,
            'editOptions': {
                'mode': 'text-area', 
                'autoSize': {'minRows': 1, 'maxRows': 3},
            },
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

# Function to insert a new value into the table
def insert_data(table_name, column_name, new_value):
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()

    # Check if the value already exists
    cursor.execute(f'SELECT * FROM {table_name} WHERE {column_name} = ?', (new_value,))
    existing_entry = cursor.fetchone()

    if not existing_entry:
        # Insert new value
        cursor.execute(f'INSERT INTO {table_name} ({column_name}) VALUES (?)', (new_value,))
        conn.commit()
    
    conn.close()

# Function to delete a row from the table
def delete_data(table_name, row_id, column_name):
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()

    # Delete the row based on the provided ID
    cursor.execute(f'DELETE FROM {table_name} WHERE {column_name} = ?', (row_id,))
    conn.commit()
    conn.close()

# Function to create the settings page
def create_settings_page():
    
    # Query data for each table
    pgm_process_columns, pgm_process_data = query_table_data('pgm_process_table')
    status_columns, status_data = query_table_data('status_table')
    fit_status_columns, fit_status_data = query_table_data('fit_status_table')
    
    return html.Div([
        fac.AntdSpace([
            fac.AntdText("Input Data to DB:", style={"textAlign": "center"}),
            fac.AntdInput(variant='filled', placeholder='Input Data and Click Add Button', style={"width": "200px"}, id="db-input"),
            fac.AntdButton("Add", id="db-add-btn", type="primary"),
            fac.AntdButton("Delete", id="db-delete-btn", type="primary", danger=True),  
        ]),
        fac.AntdTabs(
            id='tab-selection',
            activeKey='pgm-process-tab',
            items=[
                {
                    'key': 'pgm-process-tab',
                    'label': 'pgm-process-tab',
                    'children': fac.AntdTable(
                        id='table-pgm-process', 
                        columns=pgm_process_columns, 
                        data=pgm_process_data, 
                        locale="en-us",
                        bordered=True,
                        maxHeight=300,
                        rowSelectionType='radio',  # Radio selection
                    ),
                },
                {
                    'key': 'status-tab',
                    'label': 'status-tab',
                    'children': fac.AntdTable(
                        id='table-status', 
                        columns=status_columns, 
                        data=status_data, 
                        locale="en-us",
                        bordered=True,
                        rowSelectionType='radio',
                    ),
                },
                {
                    'key': 'fit-tab',
                    'label': 'fit-tab',
                    'children': fac.AntdTable(
                        id='table-fit-status', 
                        columns=fit_status_columns, 
                        data=fit_status_data, 
                        locale="en-us",
                        bordered=True,
                        rowSelectionType='radio',
                    ),
                },
            ]
        ),
    ])

# Callback to handle adding a new record based on the active tab
@callback(
    Output('table-pgm-process', 'data', allow_duplicate=True),
    Output('table-status', 'data', allow_duplicate=True),
    Output('table-fit-status', 'data', allow_duplicate=True),
    Input('db-add-btn', 'nClicks'),
    State('db-input', 'value'),
    State('tab-selection', 'activeKey'),  # Corrected to match the tab id
    prevent_initial_call=True
)
def add_data_to_table(nClicks, new_value, active_tab):
    if not new_value:
        raise PreventUpdate

    # Determine which table to insert the data into based on the active tab
    if active_tab == 'pgm-process-tab':
        insert_data('pgm_process_table', 'pgm_process', new_value)
    elif active_tab == 'status-tab':
        insert_data('status_table','status', new_value)
    elif active_tab == 'fit-tab':
        insert_data('fit_status_table','fit_status', new_value)

    # Re-query all tables to get updated data
    pgm_process_columns, pgm_process_data = query_table_data('pgm_process_table')
    status_columns, status_data = query_table_data('status_table')
    fit_status_columns, fit_status_data = query_table_data('fit_status_table')

    # Return the updated data for all tables
    return pgm_process_data, status_data, fit_status_data

# Callback to handle deleting a selected record based on the active tab
@callback(
    Output('table-pgm-process', 'data', allow_duplicate=True),
    Output('table-status', 'data', allow_duplicate=True),
    Output('table-fit-status', 'data', allow_duplicate=True),
    Input('db-delete-btn', 'nClicks'),
    State('tab-selection', 'activeKey'),
    State('table-pgm-process', 'selectedRows'),
    State('table-status', 'selectedRows'),
    State('table-fit-status', 'selectedRows'),
    prevent_initial_call=True
)
def delete_data_from_table(nClicks, active_tab, pgm_selected, status_selected, fit_selected):
    if not nClicks:
        raise PreventUpdate

    # Determine which table and selected row to delete based on the active tab
    if active_tab == 'pgm-process-tab' and pgm_selected:
        row_id = pgm_selected[0]['pgm_process']
        delete_data('pgm_process_table', row_id, 'pgm_process')
    elif active_tab == 'status-tab' and status_selected:
        row_id = status_selected[0]['status']
        delete_data('status_table', row_id, 'status')
    elif active_tab == 'fit-tab' and fit_selected:
        row_id = fit_selected[0]['fit_status']
        delete_data('fit_status_table', row_id, 'fit_status')

    # Re-query all tables to get updated data
    pgm_process_columns, pgm_process_data = query_table_data('pgm_process_table')
    status_columns, status_data = query_table_data('status_table')
    fit_status_columns, fit_status_data = query_table_data('fit_status_table')

    # Return the updated data for all tables
    return pgm_process_data, status_data, fit_status_data
