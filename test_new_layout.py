import dash
import feffery_antd_components as fac
from dash import dcc, html
import dash_ag_grid as dag

# Create the Dash app
app = dash.Dash(__name__)

# Function to generate the Ag-Grid table with a color bar renderer
def caret_ag_grid_table():
    data = [
        {"color": "red", "value": 0.1, "date": "group1"},
        {"color": "green", "value": -20, "date": "group1"},
        {"color": "blue", "value": -0.9, "date": "group1"},
        {"color": "red", "value": 11.2, "date": "group2"},
        {"color": "green", "value": 0.7, "date": "group2"},
        {"color": "blue", "value": 0.9, "date": "group2"},
    ]

    # Calculate max positive and max negative values
    max_positive = max(d['value'] for d in data if d['value'] > 0)
    max_negative = abs(min(d['value'] for d in data if d['value'] < 0))

    column_defs = [
        {
            "headerName": "Color",
            "field": "color",
            "sortable": True,
            "editable": True,  # Enable editing for the dropdown
            "cellEditor": "agSelectCellEditor",
            "cellEditorParams": {"values": ["red", "green", "blue"]},
            "singleClickEdit": True,  # Enable single-click for dropdown activation
        },
        {
            "headerName": "Value",
            "field": "value",
            "sortable": True,
            "editable": False,
            # Use custom JavaScript cell renderer defined in dashAgGridComponentFunctions.js
            "cellRenderer": "ColorBarRenderer",  # Ensure this matches the correct function name
            # Pass max and min values as params
            "cellRendererParams": {
                "maxPositive": max_positive,
                "maxNegative": max_negative
            },
        },
        {"headerName": "Group", "field": "date", "sortable": True},
    ]

    return dag.AgGrid(
        id='ag-grid-table',
        className='ag-theme-alpine',
        columnDefs=column_defs,
        rowData=data,
        defaultColDef={
            "sortable": True,
            "resizable": True,
            "editable": True,
        },
        dashGridOptions={}
    )

app.layout = fac.AntdLayout(
    [
        fac.AntdHeader(
            fac.AntdTitle("Dynamic Range Color Bar Renderer", level=2, style={"color": "white", "margin": "0"}),
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
            },
        ),
        fac.AntdLayout(
            [
                fac.AntdSider(
                    fac.AntdAccordion(
                        items=[
                            {
                                "title": "Select",
                                "key": "Select",
                                "children": [
                                    fac.AntdText('Root Lot Id'),
                                    fac.AntdInput(id='root-lot-id', placeholder='Root Lot Id'),
                                    fac.AntdText('Step Seq:'),
                                    fac.AntdSelect(options=['1', '2', '3'], id='step-seq', placeholder='Step Seq'),
                                ],
                            }
                        ],
                        defaultActiveKey=["3"],
                    ),
                    width=300,
                    style={
                        "backgroundColor": "rgb(240, 242, 245)",
                    },
                ),
                fac.AntdLayout(
                    [
                        fac.AntdContent(
                            [
                                fac.AntdCenter(
                                    [
                                        caret_ag_grid_table()
                                    ],
                                    style={
                                        "height": "100%",
                                    },
                                ),
                            ],
                            style={"backgroundColor": "white"},
                        ),
                        fac.AntdFooter(
                            [
                                fac.AntdText("页脚示例", style={"color": "white"}),
                            ],
                            style={
                                "backgroundColor": "rgb(193, 193, 193)",
                                "height": "5px",
                            },
                        ),
                    ]
                ),
            ],
            style={"height": "100%"},
        ),
    ],
    style={"height": "100vh"},
)

if __name__ == "__main__":
    app.run(debug=True)
