from dash import html
import feffery_antd_components as fac
from components.customized_indicator import create_indicator_card
def create_summary_page(get_cached_data):
    """_summary_

    Args:
        get_cached_data (_type_): _description_

    Returns:
        _type_: _description_
    """
    return html.Div([
        html.Div([
            fac.AntdRow([
                fac.AntdCol([
                    create_indicator_card("SBA FT", get_cached_data)
                ], span=8),
                fac.AntdCol([
                    create_indicator_card("SBA EDS", get_cached_data)
                ], span=8),
                fac.AntdCol([
                    create_indicator_card("SBA EDS logic", get_cached_data)
                ], span=8)
            ])
        ]),
    ])