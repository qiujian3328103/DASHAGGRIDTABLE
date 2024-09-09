import dash
from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc

import dash
from dash import html, Output, Input, State
import feffery_antd_components as fac
import feffery_utils_components as fuc
from components.customized_image_card import create_customized_image_card, create_image_div

def create_new_sbl_record_modal():
    return fac.AntdModal(
        [
            fac.AntdRow([
                fac.AntdCol(
                    [
                        fuc.FefferyDiv(
                            'Hover Ctrl + V Map Image',
                            id='image-paste-container',
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
                            id='image-paste-demo',
                            disabled=True
                        ),
                    ],
                    span=3
                ),
                fac.AntdCol(
                    [
                        fuc.FefferyDiv(
                            [
                                fac.AntdImageGroup(
                                    id='image-paste-output-group',
                                    children=[]  # Initially empty
                                ),
                            ], 
                            style={
                                'height': '120px',
                                'width': '100%',
                                'display': 'flex',
                                'justifyContent': 'center',
                                'alignItems': 'left',
                                'borderRadius': '6px',
                                'border': '1px solid #f0f0f0',
                            }),
                    ],
                    span=21
                ),
            ], style={'marginBottom': '10px'}),
        ],
        id='modal-create-sbl',
        visible=False,
        title='Create New SBL Record',
        renderFooter=True,
        okText='Ok',
        cancelText='Cancel',
        width='75vw',
    )

def create_image_display_modal():
    """Modal for displaying the images in a grid layout

    Returns:
        _type_: _description_
    """
    return fac.AntdModal(
            id="image-modal",
            title="Images",
            visible=False,  # Initially hidden
            width="55vw",  # Adjust the width as needed
            children=[
                html.Div(
                    id="modal-image-container", 
                    style={
                        "display": "grid", 
                        "gridTemplateColumns": "repeat(auto-fill, minmax(200px, 1fr))", 
                        "gap": "10px"
                    }),
            ]
        )

def create_edit_sbl_modal():
    """edit the SBL record modal

    Returns:
        _type_: _description_
    """
    # Modal for Creating New SBL
    return fac.AntdModal(
        [
            # SBA Date and Eval Date on the same row
            fac.AntdRow([
                fac.AntdCol(html.Label('SBA Date:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdDatePicker(id='edit-sba-date', placeholder='Select SBA Date', locale='en-us'), span=10),
                fac.AntdCol(html.Label('Eval Date:', style={'marginRight': '10px', 'marginLeft': '20px'}), span=2),
                fac.AntdCol(fac.AntdDatePicker(id='edit-eval-date', placeholder='Select Eval Date', locale='en-us'), span=10),
            ], style={'marginBottom': '10px'}),

            # Product as Text Input
            fac.AntdRow([
                fac.AntdCol(html.Label('Product:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInput(id='edit-product', placeholder='Enter Product (e.g., Electron)'), span=20),
            ], style={'marginBottom': '10px'}),

            # Bin as Text Input
            fac.AntdRow([
                fac.AntdCol(html.Label('Bin:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInput(id='edit-bin', placeholder='Enter Bin'), span=20),
            ], style={'marginBottom': '10px'}),

            # SBA CNT and Hit Rate on the same row
            fac.AntdRow([
                fac.AntdCol(html.Label('SBA CNT:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInputNumber(id='edit-sba-cnt', placeholder='Enter SBA CNT', addonAfter='%', style={'width': '100%'}), span=5),
                fac.AntdCol(html.Label('Hit Rate:', style={'marginRight': '10px', 'marginLeft': '20px'}), span=2),
                fac.AntdCol(fac.AntdInputNumber(id='edit-hit-rate', placeholder='Enter Hit Rate', addonAfter='%', style={'width': '100%'}), span=5),
            ], style={'marginBottom': '10px'}),

            # SBA Avg as Number Input with Percentage Addon
            fac.AntdRow([
                fac.AntdCol(html.Label('SBA Avg:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInputNumber(id='edit-sba-avg', placeholder='Enter SBA Avg', addonAfter='%', style={'width': '100%'}), span=20),
            ], style={'marginBottom': '10px'}),

            # SBA Limit as Number Input with Percentage Addon
            fac.AntdRow([
                fac.AntdCol(html.Label('SBA Limit:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInputNumber(id='edit-sba-limit', placeholder='Enter SBA Limit', addonAfter='%', style={'width': '100%'}), span=20),
            ], style={'marginBottom': '10px'}),

            # Status as Text Input
            fac.AntdRow([
                fac.AntdCol(html.Label('Status:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInput(id='edit-status', placeholder='Enter Status'), span=20),
            ], style={'marginBottom': '10px'}),

            # Text area for Comment
            fac.AntdRow([
                fac.AntdCol(html.Label('Comment:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInput(id='edit-comment', placeholder='Enter Comment', mode='text-area', style={'autoSize': True, 'height': '10px'}), span=20),
            ], style={'marginBottom': '10px'}),

            # Text area for Follow Up
            fac.AntdRow([
                fac.AntdCol(html.Label('Follow Up:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInput(id='edit-follow-up', placeholder='Enter Follow Up', mode='text-area', style={'autoSize': True, 'height': '10px'}), span=20),
            ], style={'marginBottom': '10px'}),

            # Upload input for Map Image
            fac.AntdRow([
                fac.AntdCol(html.Label('Map Image:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(
                    fac.AntdPictureUpload(
                        id='edit-map-image-upload',
                        apiUrl='/upload/',
                        fileMaxSize=5,  # Max file size in MB
                        buttonContent='Click to upload map image',
                        confirmBeforeDelete=True,
                        locale='en-us',
                    ),
                    span=20
                ),
            ], style={'marginBottom': '10px'}),

            # Upload input for Trend Image
            fac.AntdRow([
                fac.AntdCol(html.Label('Trend Image:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(
                    fac.AntdPictureUpload(
                        id='edit-trend-image-upload',
                        apiUrl='/upload/',
                        fileMaxSize=5,  # Max file size in MB
                        buttonContent='Click to upload trend image',
                        confirmBeforeDelete=True,
                        locale='en-us',
                    ),
                    span=20
                ),
            ], style={'marginBottom': '10px'}),
        ],
        id='modal-edit-sbl',
        visible=False,
        title='Edit SBL Record',
        renderFooter=True,
        okText='Ok',
        cancelText='Cancel',
        width='75vw',
    )