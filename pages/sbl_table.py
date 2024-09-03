from components.table import create_table, query_data_by_date_range
from dash import html, callback, Output, Input, State
from dash.exceptions import PreventUpdate
import feffery_antd_components as fac
import datetime 
from utilities.data_process import query_row_by_id
from components.modal import create_edit_sbl_modal
def create_sbl_page():
    """create the SBL page layout
    """
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=10)
    return html.Div([
        html.Div(
            [
                fac.AntdRow(
                    [
                        fac.AntdCol([
                            fac.AntdDatePicker(id="sba-start-date", value=start_date.strftime("%Y-%m-%d"), placeholder="Start Date", style={"width": "200px"}),
                        ], span=5),
                        fac.AntdCol([
                            fac.AntdDatePicker(id="sba-end-date", value=today.strftime("%Y-%m-%d"),placeholder="End Date", style={"width": "200px"}),
                        ], span=5),
                        fac.AntdCol([
                            fac.AntdButton("Filter", id="sba-search", type="primary", className='search-sba-btn'),
                        ], span=1),
                    ]
                ),
            ],
        ),
        fac.AntdDivider(),
        html.Div(
            fac.AntdRow([
                fac.AntdCol([
                    fac.AntdSpace([
                        fac.AntdTag(content="FT", style={"color":"#8039d6"}),
                        fac.AntdTag(content="EDS", style={"color":"#8039d6"}),
                        fac.AntdTag(content="EDS logic", style={"color":"#8039d6"}),
                    ], style={"textAlign": "center"}),
                ], span=16),
                fac.AntdCol([
                    fac.AntdButton("Create New SBL", id="create-sbl", type="primary",),
                    fac.AntdButton("Download CSV", id="download-sba", type="primary", danger=True),
                ], span=8, style={"textAlign": "right"}),
                
            ]),
        ),
        html.Div(
            create_table(),
            style={'padding': '20px'}
        ), 
    ])


@callback(
    Output('sbl-table', 'rowData'),
    Input('sba-search', 'nClicks'),
    State('sba-start-date', 'value'),
    State('sba-end-date', 'value'),
    background=True,
    running=[
        (Output('sba-search', 'disabled'), True, False),  # Disable the button while running
    ],
    prevent_initial_call=True
)
def update_table_on_filter(nClicks, start_date, end_date):
    """Update the table based on the selected date range."""
    if nClicks:
        # Query the data based on the selected date range
        filtered_data = query_data_by_date_range(start_date, end_date)
        return filtered_data
    
    # Prevent the table from updating if no button click
    raise PreventUpdate
