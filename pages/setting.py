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
def insert_data(table_name, new_value):
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()

    # Check if the value already exists
    cursor.execute(f'SELECT * FROM {table_name} WHERE pgm_process = ?', (new_value,))
    existing_entry = cursor.fetchone()

    if not existing_entry:
        # Insert new value
        cursor.execute(f'INSERT INTO {table_name} (pgm_process) VALUES (?)', (new_value,))
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

# Callback to populate input when a row is selected
@callback(
    Output('db-input', 'value'),
    Input('table-pgm-process', 'selectedRows'),
    Input('table-status', 'selectedRows'),
    Input('table-fit-status', 'selectedRows'),
    State('tab-selection', 'selectedRowKeys'),
    prevent_initial_call=True
)
def populate_input(selected_rows_pgm, selected_rows_status, selected_rows_fit, active_tab):
    if active_tab == 'pgm-process-tab' and selected_rows_pgm:
        selected_row = selected_rows_pgm[0]  # Get the first selected row
        return selected_row.get('pgm_process')  # Return the value of the selected row for pgm_process_table

    elif active_tab == 'status-tab' and selected_rows_status:
        selected_row = selected_rows_status[0]  # Get the first selected row
        return selected_row.get('status')  # Return the value of the selected row for status_table

    elif active_tab == 'fit-tab' and selected_rows_fit:
        selected_row = selected_rows_fit[0]  # Get the first selected row
        return selected_row.get('fit_status')  # Return the value of the selected row for fit_status_table
    
    return ''

# Callback to handle adding a new record based on the active tab
@callback(
    Output('table-pgm-process', 'data'),
    Output('table-status', 'data'),
    Output('table-fit-status', 'data'),
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
        insert_data('pgm_process_table', new_value)
    elif active_tab == 'status-tab':
        insert_data('status_table', new_value)
    elif active_tab == 'fit-tab':
        insert_data('fit_status_table', new_value)

    # Re-query all tables to get updated data
    pgm_process_columns, pgm_process_data = query_table_data('pgm_process_table')
    status_columns, status_data = query_table_data('status_table')
    fit_status_columns, fit_status_data = query_table_data('fit_status_table')

    # Return the updated data for all tables
    return pgm_process_data, status_data, fit_status_data
