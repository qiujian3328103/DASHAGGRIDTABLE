import dash
from dash import html
import feffery_antd_components as fac

def create_new_sbl_record_modal():
    # Modal for Creating New SBL
    return fac.AntdModal(
        [
            # SBA Date and Eval Date on the same row
            fac.AntdRow([
                fac.AntdCol(html.Label('SBA Date:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdDatePicker(id='sba-date', placeholder='Select SBA Date', locale='en-us'), span=10),
                fac.AntdCol(html.Label('Eval Date:', style={'marginRight': '10px', 'marginLeft': '20px'}), span=2),
                fac.AntdCol(fac.AntdDatePicker(id='eval-date', placeholder='Select Eval Date', locale='en-us'), span=10),
            ], style={'marginBottom': '10px'}),

            # Product as Text Input
            fac.AntdRow([
                fac.AntdCol(html.Label('Product:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInput(id='product', placeholder='Enter Product (e.g., Electron)'), span=20),
            ], style={'marginBottom': '10px'}),

            # Bin as Text Input
            fac.AntdRow([
                fac.AntdCol(html.Label('Bin:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInput(id='bin', placeholder='Enter Bin'), span=20),
            ], style={'marginBottom': '10px'}),

            # SBA CNT and Hit Rate on the same row
            fac.AntdRow([
                fac.AntdCol(html.Label('SBA CNT:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInputNumber(id='sba-cnt', placeholder='Enter SBA CNT', addonAfter='%', style={'width': '100%'}), span=5),
                fac.AntdCol(html.Label('Hit Rate:', style={'marginRight': '10px', 'marginLeft': '20px'}), span=2),
                fac.AntdCol(fac.AntdInputNumber(id='hit-rate', placeholder='Enter Hit Rate', addonAfter='%', style={'width': '100%'}), span=5),
            ], style={'marginBottom': '10px'}),

            # SBA Avg as Number Input with Percentage Addon
            fac.AntdRow([
                fac.AntdCol(html.Label('SBA Avg:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInputNumber(id='sba-avg', placeholder='Enter SBA Avg', addonAfter='%', style={'width': '100%'}), span=20),
            ], style={'marginBottom': '10px'}),

            # SBA Limit as Number Input with Percentage Addon
            fac.AntdRow([
                fac.AntdCol(html.Label('SBA Limit:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInputNumber(id='sba-limit', placeholder='Enter SBA Limit', addonAfter='%', style={'width': '100%'}), span=20),
            ], style={'marginBottom': '10px'}),

            # Status as Text Input
            fac.AntdRow([
                fac.AntdCol(html.Label('Status:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInput(id='status', placeholder='Enter Status'), span=20),
            ], style={'marginBottom': '10px'}),

            # Text area for Comment
            fac.AntdRow([
                fac.AntdCol(html.Label('Comment:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInput(id='comment', placeholder='Enter Comment', mode='text-area'), span=20),
            ], style={'marginBottom': '10px'}),

            # Text area for Follow Up
            fac.AntdRow([
                fac.AntdCol(html.Label('Follow Up:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInput(id='follow-up', placeholder='Enter Follow Up', mode='text-area'), span=20),
            ], style={'marginBottom': '10px'}),

            # Upload input for Map Image
            fac.AntdRow([
                fac.AntdCol(html.Label('Map Image:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(
                    fac.AntdPictureUpload(
                        id='map-image-upload',
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
                        id='trend-image-upload',
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
        id='modal-create-sbl',
        title='Create New SBL Record',
        renderFooter=True,
        okText='Ok',
        cancelText='Cancel',
        width='75vw',
    )
