from dash import html
import feffery_antd_components as fac
from components.customized_indicator import create_indicator_card
from dash import dcc
import plotly.express as px

def create_summary_page(get_cached_data):
    """_summary_

    Args:
        get_cached_data (_type_): _description_

    Returns:
        _type_: _description_
    """
    df = px.data.iris()  # iris is a pandas DataFrame
    fig = px.scatter(df, x="sepal_width", y="sepal_length")
    # Set default layout with adaptive theming
    fig.update_layout(
        template='plotly',  # Use the light theme by default
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="#000",  # Default to black text for light mode
    )
    graph = dcc.Graph(figure=fig)
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
            ]),
            fac.AntdRow([
                fac.AntdCol([
                    fac.AntdCard(
                        graph,
                        title ='卡片示例',
                        id='graph-card',
                    )
                ]),
            ]),
            
        ]),
    ])
    
