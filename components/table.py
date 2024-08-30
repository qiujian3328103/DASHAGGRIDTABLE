import dash
from dash import html
import dash_ag_grid as dag
import feffery_antd_components as fac
import sqlite3

# Function to load data from SQLite database
def load_data_from_db():
    conn = sqlite3.connect(r'C:\Users\Jian Qiu\Dropbox\pythonprojects\DashAggridTable\test\test_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, sba_date, eval_date, product, bin, sba_cnt, hit_rate, sba_avg, sba_limit, status, pgm_process, comment, action_item, assigned_team, action_owner, pe_owner, fit, fit_status, follow_up, last_update FROM sbl_table')
    rows = cursor.fetchall()

    # Convert to list of dictionaries
    data = [
        {
            "Lot Id": row[0],
            "SBA Date": row[1],
            "Eval Date": row[2],
            "Product": row[3],
            "Bin": row[4],
            "SBA CNT": row[5],
            "Hit Rate": row[6],
            "SBA Avg": row[7],
            "SBA Limit": row[8],
            "Status": row[9],
            "PGM/Process": row[10],
            "Comment": row[11],
            "Action Item": row[12],
            "Assigned Team": row[13],
            "Action Owner": row[14],
            "PE Owner": row[15],
            "FIT": row[16],
            "FIT Status": row[17],
            "Follow Up": row[18],
            "Last Update": row[19],
        }
        for row in rows
    ]

    conn.close()
    return data

def create_table():
    """create a table component with the given data and column definitions

    Args:
        data (list[dict]): The data to be displayed in the table
        column_defs (list[dict]): The column definitions for the table
    """
    # Column definitions for AG Grid
    data = load_data_from_db()
    column_defs = [
        {"headerName": "Lot Id", "field": "Lot Id"},
        {"headerName": "SBA Date", "field": "SBA Date"},
        {"headerName": "Eval Date", "field": "Eval Date"},
        {"headerName": "Product", "field": "Product"},
        {"headerName": "Bin", "field": "Bin"},
        {"headerName": "SBA CNT", "field": "SBA CNT"},
        {"headerName": "Hit Rate", "field": "Hit Rate"},
        {"headerName": "SBA Avg", "field": "SBA Avg"},
        {"headerName": "SBA Limit", "field": "SBA Limit"},
        {"headerName": "Status", "field": "Status"},
        {"headerName": "PGM/Process", "field": "PGM/Process"},
        {"headerName": "Comment", "field": "Comment"},
        {"headerName": "Action Item", "field": "Action Item"},
        {"headerName": "Assigned Team", "field": "Assigned Team"},
        {"headerName": "Action Owner", "field": "Action Owner"},
        {"headerName": "PE Owner", "field": "PE Owner"},
        {"headerName": "FIT", "field": "FIT"},
        {"headerName": "FIT Status", "field": "FIT Status"},
        {"headerName": "Follow Up", "field": "Follow Up"},
        {"headerName": "Last Update", "field": "Last Update"},
    ]

    return dag.AgGrid(
        columnDefs=column_defs,
        rowData=data,
        defaultColDef={"filter": True, "floatingFilter": True,  "wrapHeaderText": True, "autoHeaderHeight": True, "initialWidth": 125 },
        dashGridOptions={"pagination": True},
        style={'height': '600px', 'width': '100%'}
    )