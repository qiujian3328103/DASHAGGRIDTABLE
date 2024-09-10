from dash import Dash, dcc, html, Input, Output, callback_context, State, ALL
import base64
import os
from dash.exceptions import PreventUpdate
import feffery_antd_components as fac
import feffery_utils_components as fuc
import uuid
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

def create_image_div(image_url, card_id):
    return html.Div(
        id=card_id,
        style={'position': 'relative', 'display': 'inline-block', 'margin': '10px'},
        children=[
            fac.AntdImage(
                src=image_url,
                style={'width': '100px', 'height': '100px'}
            ),
            fac.AntdIcon(
                icon='antd-close-circle-two-tone',
                style={'position': 'absolute', 'top': '5px', 'right': '5px', 'fontSize': '20px', 'color': 'red', 'cursor': 'pointer'},
                id={"type": "close-button", "index": card_id}  # Dynamic ID
            )
        ]
    )

def create_paste_div(div_id, label):
    return html.Div(
        style={'position': 'relative', 'display': 'inline-block', 'margin': '10px'},
        children=[
            fuc.FefferyDiv(
                label,
                id=f'{div_id}-container',
                shadow='hover-shadow',
                style={
                    'height': '120px',
                    'width': '100%',
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'borderRadius': '6px',
                    'border': '3px dashed #FFBF00',
                    'fontSize': '10px',
                },
            ),
            fuc.FefferyImagePaste(
                id=f'{div_id}-paste-demo',
                disabled=True
            ),
            html.Div(id=f'{div_id}-output-group', style={'marginTop': '10px'})
        ]
    )

app.layout = html.Div([
    create_paste_div('image', 'Hover Ctrl + V Map Image'),
    create_paste_div('trend-image', 'Hover Ctrl + V Trend Image'),
    dcc.Store(id='map-image-store',data=[])
])

# Clientside callback to enable pasting when hovering over the FefferyDiv
app.clientside_callback(
    '''(isHovering) => !isHovering;''',
    Output({'type': 'paste-demo', 'index': ALL}, 'disabled'),
    Input({'type': 'container', 'index': ALL}, 'isHovering')
)

# Server side callback to handle the pasted image and add it to the image group
@app.clientside_callback(
    '''(imageInfo) => imageInfo.base64;''',
    Input({'type': 'paste-demo', 'index': ALL}, 'imageInfo'),
    prevent_initial_call=True
)

# Callback to update the image group
@app.callback(
    Output({'type': 'output-group', 'index': ALL}, 'children', allow_duplicate=True),
    Output('map-image-store', 'data', allow_duplicate=True),
    Input({'type': 'paste-demo', 'index': ALL}, 'imageInfo'),
    State({'type': 'output-group', 'index': ALL}, 'children'),
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
    if image_info:
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
    Output({'type': 'output-group', 'index': ALL}, 'children', allow_duplicate=True),
    Output('map-image-store', 'data', allow_duplicate=True),
    Input({'type': 'close-button', 'index': ALL}, 'nClicks'),
    State({'type': 'output-group', 'index': ALL}, 'children'),
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

if __name__ == '__main__':
    app.run(debug=True)
