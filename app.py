import dash
from dash import html
import dash_ag_grid as dag
import feffery_antd_components as fac
from dash.dependencies import Input, Output, State
from components.header import create_header
from components.footer import create_footer
from components.table import create_table
from components.modal import create_new_sbl_record_modal
from utilities.data_process import insert_data_to_db
# Initialize Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    fac.AntdLayout([
        create_header(),
        fac.AntdLayout(
            [
                fac.AntdSider([
                    fac.AntdMenu(
                        menuItems=[
                            {'component':'Item', 'props':{'key':'Home', 'title':'Home', 'icon':'antd-home'}},
                            {'component':'Item', 'props':{'key':'Summary', 'title':'Summary', 'icon':'antd-bar-chart'}},
                            {'component':'Item', 'props':{'key':'Setting', 'title':'Setting', 'icon':'antd-setting'}},
                        ], 
                        mode='inline',
                        style={"height": "100%", "overflow": "hidden auto"}
                    ),
                ], 
                collapsible=True,
                collapsed=True,
                collapsedWidth=60,
                style={"backgroundColor": "rgb(240,242,245)"}
                ),

                fac.AntdLayout([
                    fac.AntdContent([
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
                        create_footer("My Application")
                    ]),
                ]),
            ]
            ),
        ]),
        create_new_sbl_record_modal(),
        html.Div(id='custom-component-btn-value-changed'),
    ]), 

# Callback to open the modal
@app.callback(
    Output('modal-create-sbl', 'visible'),
    Input('create-sbl', 'nClicks'),
    prevent_initial_call=True,
)
def open_create_sbl_modal(nClicks):
    return True


# Callback to insert data into the database when the "Ok" button is clicked, and close the modal
@app.callback(
    Output('modal-create-sbl', 'visible', allow_duplicate=True),
    Input('modal-create-sbl', 'okCounts'),
    Input('modal-create-sbl', 'cancelCounts'),
    State('sba-date', 'value'),
    State('eval-date', 'value'),
    State('product', 'value'),
    State('bin', 'value'),
    State('sba-cnt', 'value'),
    State('hit-rate', 'value'),
    State('sba-avg', 'value'),
    State('sba-limit', 'value'),
    State('status', 'value'),
    prevent_initial_call=True
)
def create_sbl_record(okClicks, cancelClicks, sba_date, eval_date, product, bin_value, sba_cnt, hit_rate, sba_avg, sba_limit, status):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'modal-create-sbl-ok':
        insert_data_to_db(sba_date, eval_date, product, bin_value, sba_cnt, hit_rate, sba_avg, sba_limit, status)
    
    # Close the modal after either action, but only insert data if "Ok" was clicked
    return False


# Callback to update or delete current SBL record
@app.callback(
    Output("custom-component-btn-value-changed", "children"),
    Input("sbl-table", "cellRendererData"),
)
def handle_button_click(cell_renderer_data):
    if cell_renderer_data:
        action = cell_renderer_data.get('value', {}).get('action')
        row_id = cell_renderer_data.get('value', {}).get('rowId')
        print(action)
        if action == 'edit':
            return f'Edit button clicked for row {row_id}'
        elif action == 'delete':
            return f'Delete button clicked for row {row_id}'
        print("no action taken")
    return "No action taken"
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
