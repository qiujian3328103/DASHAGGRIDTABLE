import dash
from dash import html
import feffery_antd_components as fac

def create_new_sbl_record_modal():
    # Modal for Creating New SBL
    return fac.AntdModal(
        [
            fac.AntdRow([
                fac.AntdCol(html.Label('SBA Date:', style={'marginRight': '10px'}), span=4),
                fac.AntdCol(fac.AntdInput(id='sba-date', placeholder='Enter SBA Date (e.g., 8/21/2024)'), span=20),
            ], style={'marginBottom': '10px'}),

            fac.AntdRow([
                fac.AntdCol(html.Label('Eval Date:', style={'marginRight': '10px'}), span=4),
                fac.AntdCol(fac.AntdInput(id='eval-date', placeholder='Enter Eval Date (e.g., 8/29/2024)'), span=20),
            ], style={'marginBottom': '10px'}),

            fac.AntdRow([
                fac.AntdCol(html.Label('Product:', style={'marginRight': '10px'}), span=4),
                fac.AntdCol(fac.AntdInput(id='product', placeholder='Enter Product (e.g., Electron)'), span=20),
            ], style={'marginBottom': '10px'}),

            fac.AntdRow([
                fac.AntdCol(html.Label('Bin:', style={'marginRight': '10px'}), span=4),
                fac.AntdCol(fac.AntdInput(id='bin', placeholder='Enter Bin (e.g., 5999)'), span=20),
            ], style={'marginBottom': '10px'}),

            fac.AntdRow([
                fac.AntdCol(html.Label('SBA CNT:', style={'marginRight': '10px'}), span=4),
                fac.AntdCol(fac.AntdInput(id='sba-cnt', placeholder='Enter SBA CNT (e.g., 27)'), span=20),
            ], style={'marginBottom': '10px'}),

            fac.AntdRow([
                fac.AntdCol(html.Label('Hit Rate:', style={'marginRight': '10px'}), span=4),
                fac.AntdCol(fac.AntdInput(id='hit-rate', placeholder='Enter Hit Rate (e.g., 7.52%)'), span=20),
            ], style={'marginBottom': '10px'}),

            fac.AntdRow([
                fac.AntdCol(html.Label('SBA Avg:', style={'marginRight': '10px'}), span=4),
                fac.AntdCol(fac.AntdInput(id='sba-avg', placeholder='Enter SBA Avg (e.g., 0.46%)'), span=20),
            ], style={'marginBottom': '10px'}),

            fac.AntdRow([
                fac.AntdCol(html.Label('SBA Limit:', style={'marginRight': '10px'}), span=4),
                fac.AntdCol(fac.AntdInput(id='sba-limit', placeholder='Enter SBA Limit (e.g., 0.15%)'), span=20),
            ], style={'marginBottom': '10px'}),

            fac.AntdRow([
                fac.AntdCol(html.Label('Status:', style={'marginRight': '10px'}), span=4),
                fac.AntdCol(fac.AntdInput(id='status', placeholder='Enter Status (e.g., Open)'), span=20),
            ], style={'marginBottom': '10px'}),

            # Text area for Comment
            fac.AntdRow([
                fac.AntdCol(html.Label('Comment:', style={'marginRight': '10px'}), span=4),
                fac.AntdCol(fac.AntdInput(id='comment', placeholder='Enter Comment', mode='text-area'), span=20),
            ], style={'marginBottom': '10px'}),

            # Text area for Follow Up
            fac.AntdRow([
                fac.AntdCol(html.Label('Follow Up:', style={'marginRight': '10px'}), span=4),
                fac.AntdCol(fac.AntdInput(id='follow-up', placeholder='Enter Follow Up', mode='text-area'), span=20),
            ], style={'marginBottom': '10px'}),
        ],
        id='modal-create-sbl',
        title='Create New SBL Record',
        renderFooter=True,
        okText='Ok',
        cancelText='Cancel',
    )
