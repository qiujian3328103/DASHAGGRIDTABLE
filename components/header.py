import dash
from dash import html
import dash_ag_grid as dag
import feffery_antd_components as fac

def create_header():
    """Generate a header component with a title, a menu, and a user avatar.

    Returns:
        _type_: _description_
    """
    return fac.AntdHeader([
        fac.AntdRow([
            fac.AntdCol([
                html.Div("My Application", style={"fontSize": "24px", "fontWeight": "bold", "color": "white"})
            ], span=16),
            
            fac.AntdCol([
                fac.AntdSpace([
                    fac.AntdAvatar(
                        src="https://example.com/avatar.png",
                        size=40
                    ),
                    html.Span("Username", style={"marginLeft": "10px", "color": "white", "fontSize": "16px"}),
                    fac.AntdSwitch(
                        id='theme-switch',
                        checkedChildren='Bright',
                        unCheckedChildren='Dark'
                    ),
                ],direction="horizontal", wrap=True)
            ], span=8, style={"textAlign": "right"})
        ])
    ])