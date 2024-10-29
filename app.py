import dash 
from dash import dcc, html, Dash, clientside_callback, callback_context, DiskcacheManager, CeleryManager
from dash.exceptions import PreventUpdate
import feffery_antd_components as fac
from dash.dependencies import Input, Output, State
from components.header import create_header
from components.footer import create_footer
from components.sidebar import create_sidebar
from components.modal import create_new_sbl_record_modal, create_image_display_modal, create_edit_sbl_modal
from components.customized_image_card import create_image_div
from pages.summary import create_summary_page
from pages.setting import create_settings_page
from pages.sbl_table import create_sbl_page
from utilities.data_process import query_row_by_id
# from test.test_file_b64 import b64data
from flask_caching import Cache
from utilities.data_process import query_and_group_tat_time
import uuid 
import os 
import flask
import base64
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize the background callback manager
if 'REDIS_URL' in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    from celery import Celery
    celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
    background_callback_manager = CeleryManager(celery_app)

else:
    # Diskcache for non-production apps when developing locally
    import diskcache
    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache)


# Initialize Dash app
app = Dash(__name__, 
           title="SBL Tracker",
           suppress_callback_exceptions=True, 
           background_callback_manager=background_callback_manager)

# Configure cache
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',  # Use filesystem cache
    'CACHE_DIR': 'cache-directory',  # Directory to store cached files
    'CACHE_DEFAULT_TIMEOUT': 3000  # Cache timeout in seconds (50 minutes)
})

# Cache the query_and_group_tat_time function
@cache.memoize()
def get_cached_data():
    return query_and_group_tat_time()


# Define the layout
app.layout = fac.AntdConfigProvider(
    id='config-provider-algorithm-demo',
    algorithm='default',
    children=[
                html.Div([
                    # Store for tracking all pasted map images and their data
                    dcc.Store(id='map-image-store', data=[]),
                    fac.Fragment(id='fragment-demo'),
                    fac.AntdLayout([
                        # create a header
                        create_header(),
                        # create a side bar
                        fac.AntdLayout(
                            [
                                create_sidebar(),
                                fac.AntdDrawer('UserSetting', title='User Settings', id='drawer-basic'),
                                fac.AntdLayout([
                                    fac.AntdContent(id='page-content', style={"height": "100%", "overflowY": "auto"}, children=[]),
                                    create_footer("My Application"), 
                                ], style={"height": "100%", "overflow": "hidden auto"}),
                            ]),
                        
                        ]),
                        # Modal for creating a new SBL record
                        create_new_sbl_record_modal(),
                        # Modal for editing an existing SBL record
                        create_edit_sbl_modal(),
                        # Modal for displaying the images in a grid layout
                        create_image_display_modal(),
                        # Test Modal
                        # html.Div(id='custom-component-btn-value-changed'),
                ]), 
            ]
    )

# change the theme of the app
# app.clientside_callback(
#     '''
#     function(checked) {
#         const theme = checked ? 'dark' : 'default';
#         const agGridTheme = checked ? 'ag-theme-alpine-dark' : 'ag-theme-alpine';
#         return [theme, agGridTheme];
#     }
#     ''',
#     [Output('config-provider-algorithm-demo', 'algorithm'),
#      Output('sbl-table', 'className', allow_duplicate=True)],
#     Input('theme-switch', 'checked'), 
#     prevent_initial_call=True
# )

@app.callback(
    Output('drawer-basic', 'visible'),
    Input('download-sba', 'nClicks'),
    prevent_initial_call=True,
)
def drawer_basic_demo(nCLicks):
    if nCLicks:
        return True
    return False

# Define the callback to update page content based on URL
@app.callback(
    Output('page-content', 'children'),
    Input('menu', 'currentKey')
)
def display_page(currentKey):
    if currentKey == 'Summary':
        return create_summary_page(get_cached_data)  # Render the summary page
    elif currentKey == 'Setting':
        return create_settings_page()  # Render the settings page
    else:
        return create_sbl_page()  # Default to home page (your main table)


# Callback to open the modal
@app.callback(
    Output('modal-create-sbl', 'visible'),
    Output({'type': 'create-input', 'key': 'sba-avg'}, 'options'),
    Input('create-sbl', 'nClicks'),
    prevent_initial_call=True
)
def open_create_sbl_modal(nClicks):
    if nClicks:
        return True, ["value5", "value4"]  # Open modal only when the button is clicked
    return False, ["value1", "value2"] # Ensure it stays closed otherwise


# Callback to display images in the modal when an image thumbnail is clicked
@app.callback(
    Output("image-modal", "visible"),
    Output("modal-image-container", "children"),
    Input("sbl-table", "cellRendererData"),
    prevent_initial_call=True
)
def show_image_modal(data):
    if not data:
        raise PreventUpdate
    print(data)
    # Check if the data exists and if it was triggered by the correct columns
    if isinstance(data, dict) and data.get("value") and data.get("colId") in ["Map Images", "Trend Images"]:
            images = data['value']
            image_components = [
                fac.AntdImage(
                    src=f"data:image/jpeg;base64,{img}",
                    height=200,
                    preview=True,
                    locale="en-us",
                ) for img in images
            ]
            return True, image_components

    raise PreventUpdate


# handle edit button click in ag-grid to display current row data in modal
@app.callback(
    Output('modal-edit-sbl', 'visible'),
    Output('edit-sba-date', 'value'),
    Output('edit-eval-date', 'value'),
    Output('edit-product', 'value'),
    Output('edit-bin', 'value'),
    Output('edit-sba-cnt', 'value'),
    Output('edit-hit-rate', 'value'),
    Output('edit-sba-avg', 'value'),
    Output('edit-sba-limit', 'value'),
    Output('edit-status', 'value'),
    Input('sbl-table', 'cellRendererData'),
    prevent_initial_call=True
)
def handle_edit_button_click(cell_renderer_data):
    if cell_renderer_data:
        
        if isinstance(cell_renderer_data.get('value', {}), list):
            # if the cell_renderer_data is a list, it means the data is from the image columns
            # so we need to prevent the update  
            raise PreventUpdate
        action = cell_renderer_data.get('value', {}).get('action')
        row_id = cell_renderer_data.get('value', {}).get('rowId')
        
        if action == 'edit':
            # Fetch the row data using the new function
            row_data = query_row_by_id(row_id)

            if row_data:
                return (
                    True,  # Open modal
                    row_data['SBA Date'],
                    row_data['Eval Date'],
                    row_data['Product'],
                    str(row_data['Bin']),
                    row_data['SBA CNT'],
                    row_data['Hit Rate'],
                    row_data['SBA Avg'],
                    row_data['SBA Limit'],
                    row_data['Status']
                )
        else:
            raise PreventUpdate
    raise PreventUpdate


# Clientside callback to enable pasting when hovering over the FefferyDiv
app.clientside_callback(
    '''(isHovering) => !isHovering;''',
    Output('image-paste-demo', 'disabled'),
    Input('image-paste-container', 'isHovering')
)


# Server side callback to handle the pasted image and add it to the image group
app.clientside_callback(
    '''(imageInfo) => imageInfo.base64;''',
    Output('temporary-store-image-base64', 'data'),
    Input('image-paste-demo', 'imageInfo'),
    prevent_initial_call=True
)


# listen to dcc.store temporary-store-image-base64 and update the image group
@app.callback(
    Output('image-paste-output-group', 'children', allow_duplicate=True),
    Output('map-image-store', 'data'),
    Input('image-paste-demo', 'imageInfo'),
    State('image-paste-output-group', 'children'),
    State('map-image-store', 'data'),
    prevent_initial_call=True
)
def update_image_group(image_info, current_children, image_store_data):
    """the image_info is a dictionary with "base64" key and the value head already has data:image/png;base64
    no need to add it again. 

    Args:
        image_info (_type_): The dictionary containing the base64 image data
        current_children (_type_): The current children of the image group

    Raises:
        PreventUpdate: Prevents the callback from firing if no image is pasted

    Returns:
        _type_: The updated list of image cards and image store data
    """
    image_base64 = image_info["base64"]
    if image_base64:
        # Generate a unique ID for the new image
        image_id = str(uuid.uuid4())
        
        # Create a new image card using the base64 image data and assign it the unique ID
        new_image_card = create_image_div(
            image_url=image_base64,
            card_id=image_id
        )
        
        # Update the image store with the new image data
        image_store_data.append({
            "id": image_id,
            "base64": image_base64
        })

        # Append the new image card to the existing children
        return current_children + [new_image_card], image_store_data
    raise PreventUpdate


@app.callback(
    Output('image-paste-output-group', 'children', allow_duplicate=True),
    Output('map-image-store', 'data', allow_duplicate=True),
    Input({'type': 'close-button', 'index': dash.ALL}, 'nClicks'),
    State('image-paste-output-group', 'children'),
    State('map-image-store', 'data'),
    prevent_initial_call=True
)
def remove_image_card(n_clicks, current_children, image_store_data):
    """Remove the image card and its data from the image group and store when the close button is clicked"""
    if not any(n_clicks):
        raise PreventUpdate

    # Identify which button was clicked based on n_clicks
    button_indices_to_remove = [
        i for i, clicks in enumerate(n_clicks) if clicks
    ]
    
    # Remove the card and image data corresponding to the clicked button(s)
    updated_children = [
        child for i, child in enumerate(current_children)
        if i not in button_indices_to_remove
    ]

    updated_image_store_data = [
        image for i, image in enumerate(image_store_data)
        if i not in button_indices_to_remove
    ]

    return updated_children, updated_image_store_data


# Add this route to your app
@app.server.route('/upload/', methods=['POST'])
def upload():
    if 'file' not in flask.request.files:
        return flask.jsonify({'error': 'No file part'}), 400
    file = flask.request.files['file']
    if file.filename == '':
        return flask.jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.server.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        with open(file_path, 'rb') as f:
            encoded_content = base64.b64encode(f.read()).decode('utf-8')
        return flask.jsonify({
            'status': 'success',
            'fileName': filename,
            'fileContent': encoded_content
        })
    return flask.jsonify({'error': 'File type not allowed'}), 400


if __name__ == '__main__':
    app.run_server(debug=True)
