import dash
from dash import html
import dash_ag_grid as dag
import feffery_antd_components as fac

def create_footer(title):
    """create a footer component with a title

    Args:
        title (_type_): _description_
    """
    return fac.AntdFooter(title)