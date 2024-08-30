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
        ]),
        create_footer("My Application")
    ]), 

    create_new_sbl_record_modal(),
])

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

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
