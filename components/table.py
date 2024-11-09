
import dash_ag_grid as dag
import feffery_antd_components as fac
import sqlite3
import base64
from dash import html
from config import DB_URL
# Function to load data from SQLite database
def load_data_from_db():
    """Function to load data from SQLite database
    """
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()

    # Fetch data from sbl_table
    cursor.execute('''
        SELECT id, sba_date, eval_date, product, bin, sba_cnt, hit_rate, sba_avg, sba_limit, status, pgm_process, comment, action_item, assigned_team, action_owner, pe_owner, fit, fit_status, follow_up, last_update, foreigner_key
        FROM sbl_table
    ''')
    rows = cursor.fetchall()

    # Convert to list of dictionaries
    data = []
    for row in rows:
        foreigner_key = row[20]

        # Fetch map images for the foreigner_key
        cursor.execute('SELECT map_image FROM map_image WHERE foreigner_key = ?', (foreigner_key,))
        map_images = cursor.fetchall()
        map_image_b64 = [base64.b64encode(img[0]).decode('utf-8') for img in map_images]

        # Fetch trend images for the foreigner_key
        cursor.execute('SELECT trend_image FROM trend_image WHERE foreigner_key = ?', (foreigner_key,))
        trend_images = cursor.fetchall()
        trend_image_b64 = [base64.b64encode(img[0]).decode('utf-8') for img in trend_images]

        # Add the images and other data to the row
        data.append({
            "Id": row[0],
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
            "Map Images": map_image_b64,
            "Trend Images": trend_image_b64,
        })

    conn.close()
    return data

def query_data_by_date_range(start_date, end_date):
    print(start_date, end_date)
    """Query data from the database based on the SBA Date range."""
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, sba_date, eval_date, product, bin, sba_cnt, hit_rate, sba_avg, sba_limit, status, pgm_process, comment, action_item, assigned_team, action_owner, pe_owner, fit, fit_status, follow_up, last_update, foreigner_key
        FROM sbl_table
        WHERE sba_date BETWEEN ? AND ?
    ''', (start_date, end_date))
    rows = cursor.fetchall()

    data = []
    for row in rows:
        foreigner_key = row[20]

        cursor.execute('SELECT map_image FROM map_image WHERE foreigner_key = ?', (foreigner_key,))
        map_images = cursor.fetchall()
        map_image_b64 = [base64.b64encode(img[0]).decode('utf-8') for img in map_images]

        cursor.execute('SELECT trend_image FROM trend_image WHERE foreigner_key = ?', (foreigner_key,))
        trend_images = cursor.fetchall()
        trend_image_b64 = [base64.b64encode(img[0]).decode('utf-8') for img in trend_images]

        data.append({
            "Id": row[0],
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
            "Map Images": map_image_b64,
            "Trend Images": trend_image_b64,
        })

    conn.close()
    return data

def create_table(data=None):
    """create a table component with the given data and column definitions

    Args:
        data (list[dict]): The data to be displayed in the table
        column_defs (list[dict]): The column definitions for the table
    """
    # Column definitions for AG Grid
    if data is None:
        data = load_data_from_db()
        
    column_defs = [
        {"headerName": "Id", "field": "Id", "initialWidth": 80},
        {"headerName": "SBA Date", "field": "SBA Date", "initialWidth": 90, "cellStyle": {"padding": "2px"},},
        {"headerName": "Eval Date", "field": "Eval Date", "initialWidth": 90, "cellStyle": {"padding": "2px"},},
        {"headerName": "Product", "field": "Product", "cellStyle": {"padding": "2px"}},
        {"headerName": "Bin", "field": "Bin", "cellStyle": {"padding": "2px"}},
        {
            "headerName": "Status", 
            "field": "Status", 
            "cellStyle": {
                "padding": "2px",
                "defaultStyle": {"backgroundColor": "white"}, 
                "styleConditions": [
                    {
                        "condition": "params.value === 'Open'",
                        "style": {"backgroundColor": "#bee4a3"},
                    },
                    {
                        "condition": "params.value === 'Close'",
                        "style": {"backgroundColor": "#bee4a3"},
                    },
                    {
                        "condition": "params.value === 'KIV'",
                        "style": {"backgroundColor": "#a3bee4"},
                    },
                                        {
                        "condition": "params.value === 'New'",
                        "style": {"backgroundColor": "#e4a3be"},
                    },
                ],
            }
        },
        {
            "headerName": "Map Images",
            "field": "Map Images",
            "cellRenderer": "ImgThumbnail",
            "initialWidth": 120,
            "cellStyle": {"padding": "2px"}, 
        },
        {
            "headerName": "Trend Images",
            "field": "Trend Images",
            "cellRenderer": "ImgThumbnail",
            "initialWidth": 300,
            "cellStyle": {"padding": "2px"}, 
        },
        {"headerName": "SBA CNT", "field": "SBA CNT", "cellStyle": {"padding": "2px"}},
        {"headerName": "Hit Rate", "field": "Hit Rate", "cellStyle": {"padding": "2px"}},
        {"headerName": "SBA Avg", "field": "SBA Avg", "cellStyle": {"padding": "2px"}},
        {"headerName": "SBA Limit", "field": "SBA Limit", "cellStyle": {"padding": "2px"}},
        {"headerName": "PGM/Process", "field": "PGM/Process", "cellStyle": {"padding": "2px"}},
        {"headerName": "Comment", "field": "Comment", "cellStyle": {"padding": "2px"}, "cellRenderer": "CommentRenderer",},
        {"headerName": "Action Item", "field": "Action Item", "cellStyle": {"padding": "2px"}},
        {"headerName": "Assigned Team", "field": "Assigned Team", "cellStyle": {"padding": "2px"}},
        {"headerName": "Action Owner", "field": "Action Owner", "cellStyle": {"padding": "2px"}},
        {"headerName": "PE Owner", "field": "PE Owner", "cellStyle": {"padding": "2px"}},
        {"headerName": "FIT", "field": "FIT", "cellStyle": {"padding": "2px"}},
        {"headerName": "FIT Status", "field": "FIT Status", "cellStyle": {"padding": "2px"}},
        {"headerName": "Follow Up", "field": "Follow Up", "cellStyle": {"padding": "2px"}},
        {"headerName": "Last Update", "field": "Last Update", "cellStyle": {"padding": "2px"}},
        {
            "headerName": "Edit Item",
            "field": "Edit Item",
            "cellRenderer": "EditDeleteButton",
            "cellRendererParams": {"className": "btn"},
            "pinned": "right",
            "floatingFilter": False,
            "initialWidth": 200,
            "cellStyle": {"padding": "2px"}
        },
    ]

    return dag.AgGrid(
        id='sbl-table',
        className='ag-theme-alpine',
        columnDefs=column_defs,
        rowData=data,
        defaultColDef={"filter": True, "floatingFilter": True,  "wrapHeaderText": True, "autoHeaderHeight": True, "initialWidth": 125 },
        dashGridOptions={"pagination": True, "rowHeight": 90,
                        "loadingOverlayComponent": "CustomLoadingOverlay",
                        "loadingOverlayComponentParams": {
                        "loadingMessage": "One moment please...",
                        "color": "red",
                        },},
        style={'height': '650px', 'width': '100%'},
    )
