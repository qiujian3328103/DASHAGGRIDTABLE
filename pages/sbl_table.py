from components.table import create_table
from dash import html, callback, Output, Input
import feffery_antd_components as fac

def create_sbl_page():
    """create the SBL page layout
    """
    return html.Div([
        html.Div(
            create_table(),
            style={'padding': '20px'}
        ), 
        html.Div(
            [
                fac.AntdButton("Create New SBL", id="create-sbl", type="primary", className='create-sbl-btn'),
                fac.AntdButton("Update SBL Table", id="update-sbl",type="primary", className='update-sbl-btn'),
                fac.AntdButton("Delete SBL Item", id="delete-sbl", type="primary", className='delete-sbl-btn', danger=True),
            ],
            style={"textAlign": "right", "marginTop": "20px"}  # Align buttons to the right and add margin to the top
        ),
    ])

# callback(
#     Output("custom-component-btn-value-changed", "children"),
#     Input("sbl-table", "cellRendererData"),
#     suppress_callback_exceptions=True
# )
# def handle_button_click(cell_renderer_data):
#     if cell_renderer_data:
#         action = cell_renderer_data.get('value', {}).get('action')
#         row_id = cell_renderer_data.get('value', {}).get('rowId')
#         print(action)
#         if action == 'edit':
#             return f'Edit button clicked for row {row_id}'
#         elif action == 'delete':
#             return f'Delete button clicked for row {row_id}'
#         print("no action taken")
#     return "No action taken"
