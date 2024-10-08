import dash
import feffery_antd_components as fac
from dash import html, dcc
import feffery_utils_components as fuc

def create_edit_sbl_modal():
    """edit the SBL record modal

    Returns:
        _type_: _description_
    """
    # Modal for Creating New SBL
    status = ["Open", "KIV", "NEW", "CLOSE"]
    sbl_status_options = [{'label': status, 'value': status} for status in status]
    fit_status = ["Open", "Close"]
    fit_status_options = [{'label': status, 'value': status} for status in fit_status]
    sba_type = ["EDS", "EDS Logic", "FT"]
    process_options = ["TEST", "Process", "Equipment", "Device"]
    return fac.AntdModal(
        [
            # SBA type 
            fac.AntdRow([
                fac.AntdCol([fac.AntdText('SBA Type:')], span=2),
                fac.AntdCol([fac.AntdSelect(id="edit-sba-type", placeholder="", options=sba_type, style={'width': '100%'})], span=10),
                fac.AntdCol([fac.AntdText('Status:', style={'marginLeft': '10px'})], span=2),
                fac.AntdCol([fac.AntdSelect(id="edit-status", placeholder="Select SBA Status", options=status, style={'width': '100%'})], span=10)
            ], style={'marginBottom': '10px'}),
            # SBA Date and Eval Date on the same row
            fac.AntdRow([
                fac.AntdCol([fac.AntdText('SBA Date:')], span=2),
                fac.AntdCol([fac.AntdDatePicker(id='edit-sba-date', placeholder='Select SBA Date', locale='en-us', style={'width': '100%'},)], span=10),
                fac.AntdCol([fac.AntdText('Eval Date:', style={'marginLeft': '10px'})], span=2),
                fac.AntdCol(fac.AntdDatePicker(id='edit-eval-date', placeholder='Select Eval Date', locale='en-us', style={'width': '100%'},), span=10),
            ], style={'marginBottom': '10px'}),

            # Product as Text Input
            # Bin as Text Input
            fac.AntdRow([
                fac.AntdCol([fac.AntdText('Product:')], span=2),
                fac.AntdCol(fac.AntdInput(id='edit-product', placeholder='Enter Product (e.g., Electron)'), span=4),
                fac.AntdCol([fac.AntdText('BIN:', style={'marginLeft': '10px'})], span=2),
                fac.AntdCol(fac.AntdInput(id='edit-bin', placeholder='Enter Bin', style={'width': '100%'}), span=4),
                fac.AntdCol([fac.AntdText('BIN Group:', style={'marginLeft': '10px'})], span=2),
                fac.AntdCol(fac.AntdInput(id='edit-bin-group', placeholder='Enter Bin Group'), span=4),
                fac.AntdCol([fac.AntdText('PGM/Process:', style={'marginLeft': '10px', 'fontSize':'12px'})], span=2),
                fac.AntdCol([fac.AntdSelect(id="edit-pgm-process", placeholder="", options=process_options, style={'width': '100%'})], span=4)
            ], style={'marginBottom': '10px'}),

            # SBA CNT and Hit Rate on the same row
            fac.AntdRow([
                fac.AntdCol([fac.AntdText('SBA Qty:')],  span=2),
                fac.AntdCol(fac.AntdInputNumber(id='edit-sba-qty', placeholder='Enter SBA CNT', addonAfter='cnt', style={'width': '100%'}), span=4),
                fac.AntdCol([fac.AntdText('SBA Avg:', style={'marginLeft': '10px'})], span=2),
                fac.AntdCol(fac.AntdInputNumber(id='edit-sba-avg', placeholder='Enter SBA Avg', addonAfter='%', style={'width': '100%'}), span=4),
                fac.AntdCol([fac.AntdText('Hit Rate:', style={'marginLeft': '10px'})], span=2),
                fac.AntdCol(fac.AntdInputNumber(id='edit-hit-rate', placeholder='Enter Hit Rate', addonAfter='%', style={'width': '100%'}), span=4),
                fac.AntdCol([fac.AntdText('SBA Limit:', style={'marginLeft': '10px'})], span=2),
                fac.AntdCol(fac.AntdInputNumber(id='edit-sba-limit', placeholder='Enter SBA Limit', addonAfter='%', style={'width': '100%'}), span=4),
            ], style={'marginBottom': '10px'}),

            # assigned team, action owner, PE owner. 
            fac.AntdRow([
                fac.AntdCol([fac.AntdText('Assign Team')], span=2),
                fac.AntdCol(fac.AntdInput(id='edit-assigned-team', placeholder='Enter Team (e.g., PE,YA)'), span=4),
                fac.AntdCol([fac.AntdText('Action Owner:', style={'marginLeft': '10px', 'fontSize':'12px'})], span=2),
                fac.AntdCol(fac.AntdInput(id='edit-action-owner', placeholder='Enter Owner (e.g., Jian Qiu)'), span=4),
                fac.AntdCol([fac.AntdText('YA Rep:', style={'marginLeft': '10px'})], span=2),
                fac.AntdCol(fac.AntdInput(id='edit-ya-rep', placeholder='Enter Owner (e.g., Jian Qiu)'), span=4),
                fac.AntdCol(html.Label('PE Owner:', style={'marginRight': '10px', 'marginLeft': '10px'}), span=2),
                fac.AntdCol(fac.AntdInput(id='edit-pe-owner', placeholder='Enter PE Owner (e.g., Jian Qiu)'), span=4),
            ], style={'marginBottom': '10px'}),

            # FT item and owner 
            fac.AntdRow([
                fac.AntdCol([fac.AntdText('Follow Up:')], span=2),
                fac.AntdCol(fac.AntdInput(id='edit-follow-up', placeholder='Enter MRB/Fit/Yield Meeting...'), span=6),
                fac.AntdCol([fac.AntdText('Fit:', style={'marginLeft': '10px'})], span=2),
                fac.AntdCol(fac.AntdInput(id='edit-fit-link', placeholder='Enter Fit (e.g., Electron)'), span=6),
                fac.AntdCol([fac.AntdText('Fit Status:', style={'marginLeft': '10px'})], span=2),
                fac.AntdCol([fac.AntdSelect(id="edit-fit-status", placeholder="Fit Status", options=fit_status_options, style={'width': '100%'},)], span=6)
            ], style={'marginBottom': '10px'}), 

            fac.AntdRow([
                fac.AntdCol(html.Label('Cause:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInput(id='edit-root-cause', placeholder='Enter Root Cause', mode='text-area'), span=22),
            ], style={'marginBottom': '10px'}),

            # Test area for actions
            fac.AntdRow([
                fac.AntdCol(html.Label('Action Item:', style={'marginRight': '10px'}), span=2),
                fac.AntdCol(fac.AntdInput(id='edit-action-item', placeholder='Enter Action', mode='text-area'), span=22),
            ], style={'marginBottom': '10px'}),

            # Text area for Comment
            fac.AntdRow([
                fac.AntdCol([fac.AntdText('Comment:')], span=2),
                fac.AntdCol(fac.AntdInput(id='edit-comment', placeholder='Enter Comment'), span=22),
            ], style={'marginBottom': '10px'}),

            # Upload input for Map Image
            fac.AntdRow([
                fac.AntdCol(
                    [
                        fuc.FefferyDiv(
                            'Hover Ctrl + V Map Image',
                            id='edit-image-paste-container',
                            shadow='hover-shadow',
                            style={
                                'height': '140px',
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
                            id='edit-image-paste-demo',
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
                                    id='edit-image-paste-output-group',
                                    children=[]  # Initially empty
                                ),
                            ], 
                            style={
                                'height': '140px',
                                'width': '100%',
                                'display': 'flex',
                                'justifyContent': 'center',
                                'alignItems': 'left',
                                'borderRadius': '6px',
                                'border': '1px solid #f0f0f0',
                                'marginLeft': '10px',
                                'marginRight': '20px'
                            })
                    ],span=9),
                fac.AntdCol(
                    [
                        fuc.FefferyDiv(
                            'Hover Ctrl + V Trend Image',
                            id='edit-trend-image-paste-container',
                            shadow='hover-shadow',
                            style={
                                'height': '140px',
                                'display': 'flex',
                                'justifyContent': 'center',
                                'alignItems': 'center',
                                'borderRadius': '6px',
                                'border': '3px dashed #FF4500',
                                'fontSize': '10px',
                            },
                        ),
                        fuc.FefferyImagePaste(
                            id='edit-trend-image-paste-demo',
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
                                    id='edit-trend-image-paste-output-group',
                                    children=[]  # Initially empty
                                ),
                            ], 
                            style={
                                'height': '140px',
                                'display': 'flex',
                                'justifyContent': 'center',
                                'alignItems': 'left',
                                'borderRadius': '6px',
                                'border': '1px solid #f0f0f0',
                                'marginLeft': '10px',
                                'marginRight': '20px'
                            }),
                    ],span=9
                ),
            ], style={'marginBottom': '10px'}),
        ],
        id='modal-edit-sbl',
        title='Edit SBA Record',
        renderFooter=False,
        okText='Ok',
        cancelText='Cancel',
        width='80vw',
    )