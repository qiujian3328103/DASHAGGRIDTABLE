import dash
import feffery_antd_components as fac
from dash import dcc, html
import dash_ag_grid as dag

app = dash.Dash(__name__)

# Function to generate the Ag-Grid table with dropdown
def caret_ag_grid_table():
    column_defs = [
        {
            "headerName": "Color",
            "field": "color",
            "sortable": True,
            "editable": True,  # Enable editing for the dropdown
            "cellEditor": "agSelectCellEditor",
            "cellEditorParams": {"values": ["red", "green", "blue"]},
            "singleClickEdit": True,  # Enable single-click for dropdown activation
            "cellStyle": {
                "styleConditions": [
                    {"condition": "params.value === 'red'", "style": {"backgroundColor": "red", "color": "white"}},
                    {"condition": "params.value === 'green'", "style": {"backgroundColor": "green", "color": "white"}},
                    {"condition": "params.value === 'blue'", "style": {"backgroundColor": "blue", "color": "white"}},
                ]
            },
        },
        {"headerName": "Value", "field": "value", "sortable": True},
        {"headerName": "Group", "field": "date", "sortable": True},
    ]
    data = [
        {"color": "red", "value": 1, "date": "group1"},
        {"color": "green", "value": 2, "date": "group1"},
        {"color": "blue", "value": 3, "date": "group1"},
        {"color": "red", "value": 4, "date": "group2"},
        {"color": "green", "value": 5, "date": "group2"},
        {"color": "blue", "value": 6, "date": "group2"},
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
    )

app.layout = fac.AntdLayout(
    [
        fac.AntdHeader(
            fac.AntdTitle("Color Dropdown with Single Click Edit", level=2, style={"color": "white", "margin": "0"}),
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
