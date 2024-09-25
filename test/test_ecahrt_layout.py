import dash
from dash import html, Input, Output
# from dash.dependencies import Input, Output
import feffery_antd_components as fac
import dash_echarts

app = dash.Dash(__name__)



# Sample ECharts options for the plots
chart_options1 = {
    'title': {'text': 'EChart 1', 'left': 'center'},
    'tooltip': {},
    'xAxis': {'data': ['Category A', 'Category B', 'Category C']},
    'yAxis': {},
    'series': [{'type': 'bar', 'data': [5, 20, 36]}],
    'grid': {'left': '3%', 'right': '3%', 'top': '10%', 'bottom': '10%', 'containLabel': True},
    'responsive': True  # Ensures chart resizes properly
}

chart_options2 = {
    'title': {'text': 'EChart 2', 'left': 'center'},
    'tooltip': {},
    'xAxis': {'data': ['Category X', 'Category Y', 'Category Z']},
    'yAxis': {},
    'series': [{'type': 'line', 'data': [15, 30, 20]}],
    'grid': {'left': '3%', 'right': '3%', 'top': '10%', 'bottom': '10%', 'containLabel': True},
    'responsive': True  # Ensures chart resizes properly
}

app.layout = fac.AntdLayout(
    fac.AntdRow(
        [
            fac.AntdCol(
                fac.AntdCard(
                    dash_echarts.DashECharts(
                        option=chart_options1,
                        style={"width": "100%", "height": "400px"},
                    ),
                    title="Chart 1",
                    bodyStyle={'padding': '0', 'width': '100%', 'height': '100%'} 
                ),
                span=12
            ),
            fac.AntdCol(
                fac.AntdCard(
                    dash_echarts.DashECharts(
                        option=chart_options2,
                        style={"width": "100%", "height": "400px"},
                    ),
                    title="Chart 2",
                    bodyStyle={'padding': '0', 'width': '100%', 'height': '100%'} 
                ),
                span=12
            )
        ]
    ),
    style={"width": "100%"}  # Ensures row takes full width of the page
)

if __name__ == '__main__':
    app.run_server(debug=True)