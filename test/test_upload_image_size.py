
import dash_ag_grid as dag
import feffery_antd_components as fac
import sqlite3
import base64
from dash import html

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