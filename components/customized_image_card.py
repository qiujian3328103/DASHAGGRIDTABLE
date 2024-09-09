import dash
from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc


def create_customized_image_card(image_url, card_id):
    return fac.AntdCard(
        [
            fac.AntdButton(
                fac.AntdIcon(icon="antd-close"),
                type="text",
                style={"position": "absolute", "top": "5px", "right": "5px"},
                id={"type": "close-button", "index": card_id}  # Dynamic ID
            ),
            fac.AntdImage(
                src=image_url,
                style={"width": "100%", "height": "auto"}
            )
        ],
        id={"type": "image-card", "index": card_id},  # Dynamic ID for the card
        style={
            "width": "120px",
            "position": "relative"
        },
        headStyle={
            "padding": "0px",  # Controls the padding inside the header
            "fontSize": "10px",  # Controls the font size of the title
        },
        bodyStyle={
            "padding": "0",  # Remove padding in the card body
            "height": "100px",
        },
        size="small"
    )
    
    
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