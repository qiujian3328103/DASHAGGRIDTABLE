from components.table import create_table, query_data_by_date_range
from dash import html, callback, Output, Input, State, clientside_callback
from dash.exceptions import PreventUpdate
import feffery_antd_components as fac
import feffery_utils_components as fuc 
import datetime 
import numpy as np
import json 
# from utilities.data_process import query_row_by_id
# from components.modal import create_edit_sbl_modal
from utilities.wafer_map import create_wafer_data, create_wafer_data_for_plotly
import plotly.graph_objects as go
from dash import dcc

def get_square_coordinates(x0, x1, y0, y1):
    """get the coordinates of a square
    """
    return ([x0, x0, x1, x1, x0], [y0, y1, y1, y0, y0])

def generate_plotly_wafermap(wafer_data=None, shot_data=None, width=None, height=None):
    """generate the wafer map plotly figure
    """
    fig = go.Figure()
    
    # Add square shapes for each die in the fig 
    fig.add_shape(type='circle', xref='x', yref='y', x0=-150, y0=-150, x1=150, y1=150, line_color='black')
    
    # add the wafer_data use the scattergl to draw the wafermap, each die has x0, x1, y0, y1, color, where x0, x1, y0, y1 are the coordinates of the die, color is the color of the die
    # Add the wafer_data using scattergl to draw the wafermap
    if wafer_data is not None:
        for color in wafer_data['color'].unique().tolist():
            filter_df = wafer_data[wafer_data['color'] == color]
            all_x = []
            all_y = []
            text_data = []
            for index, row in filter_df.iterrows():
                x, y = get_square_coordinates(row['x0'], row['x1'], row['y0'], row['y1'])
                all_x.extend(x)
                all_y.extend(y)
                # add break on each die to make the die clear
                all_x.append(None)
                all_y.append(None)
                hover_text = f"x:{row['sort_die_x']}<br>y:{row['sort_die_y']}<br>Bin Value: {row['bin_value']}"
                text_data.extend([hover_text] * 5)
                text_data.append(None)
        fig.add_trace(go.Scatter(
            x=all_x,
            y=all_y,
            mode='lines',
            line_color='white',
            line=dict(color=color, width=1),
            fill='toself',
            fillcolor=color,
            hoverinfo='text',
            text=text_data,
            name=color,
            hoverlabel=dict(bgcolor='white', font_size=16),
            showlegend=False,
        ))
                
        
    fig.update_layout(
        xaxis=dict(
            range=[-151, 151],
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        yaxis=dict(
            range=[-151, 151],
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            scaleanchor='x',
            scaleratio=1,
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        scene=dict(aspectratio=dict(x=1, y=1)),
        margin=dict(l=0, r=0, t=0, b=0),
        height=280,
        showlegend=False,
    )
    
    return fig 


def generate_plotly_heatmap(df=None, shot_data=None, width=None, height=None):
    """use the heatmap to draw the wafermap 

    Args:
        df (_type_, optional): _description_. Defaults to None.
        shot_data (_type_, optional): _description_. Defaults to None.
        width (_type_, optional): _description_. Defaults to None.
        height (_type_, optional): _description_. Defaults to None.
    """

    # Step 1: Get unique bin values and assign a unique numerical index
    unique_bins = df["bin_value"].dropna().unique()  # Drop NaN values
    bin_index_mapping = {bin_value: index for index, bin_value in enumerate(unique_bins, start=1)}

    # Step 2: Map bin values to numerical indices
    df["bin_index"] = df["bin_value"].map(bin_index_mapping)

    # Step 3: Create a pivot table using numerical indices for bin_value
    pivot_table = df.pivot(index="sort_die_y", columns="sort_die_x", values="bin_index")

    # Step 4: Create the z values (2D list) for the heatmap
    z = pivot_table.values.tolist()

    # Step 5: Get the unique values from the z matrix (excluding 0) and assign colors
    unique_z_values = sorted(set(val for row in z for val in row if val != 0))
    color_palette = ["#2ecc71", "#e74c3c", "#3498db", "#9b59b6", "#f1c40f", "#e67e22", "#1abc9c", "#34495e"]
    z_color_mapping = {z_val: color_palette[i % len(color_palette)] for i, z_val in enumerate(unique_z_values)}

    # Step 6: Create a custom colorscale based on z values
    colorscale = [(i / (len(unique_z_values) - 1), z_color_mapping[z_val]) for i, z_val in enumerate(unique_z_values)]
    colorscale.insert(0, (0, "#808080"))  # Add gray color for 0 (NaN values)

    # Step 7: Create hover text
    hover_text = [[f"x: {x}<br>y: {y}<br>bin: {bin_value}" for x, y, bin_value in zip(pivot_table.columns, pivot_table.index, row)] for row in pivot_table.values]

    min_value = min(df["sort_die_x"].min(), df["sort_die_y"].min())
    max_value = max(df["sort_die_x"].max(), df["sort_die_y"].max())

    # Step 2: Define the common axis range
    common_range = [min_value-2, max_value+2]

    # Step 8: Create the heatmap
    fig = go.Figure(
        go.Heatmap(
            x=pivot_table.columns,
            y=pivot_table.index,
            z=z,
            text=hover_text,
            hoverinfo="text",
            colorscale=colorscale,
            showscale=False,
            xgap=1,  # Add gap between x cells
            ygap=1,  # Add gap between y cells
        )
    )

    # Update layout to remove axis labels and ticks, and set aspect ratio to 1
    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=common_range,
            scaleanchor="y",
            scaleratio=1
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=common_range
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="white",  # Set the background color to white (edge color)
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return fig 

def create_wafermap_page():
    """create the SBL page layout
    """
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=10)
    wafer_data = create_wafer_data_for_plotly(root_lot_id='AAAAA')
    # print(wafer_data)
    # print(wafer_data)
    wafer_data, shot_data, width, height = create_wafer_data(root_lot_id='AAAAA')
    
    # Prepare the data for JavaScript
    wafer_map_data = {
        "wafer_data": wafer_data,
        "width": width,
        "height": height
    }

    # Store the wafer map data in dcc.Store
    # store_data = dcc.Store(id='wafer-data-store', data=json.dumps(wafer_map_data))

    wafer_maps_cards = []
    for i in range(1,2):
        wafer_maps_cards.append(
            fac.AntdCardGrid([
                fac.AntdSpace([
                    fac.AntdText(f'Wafer {i}', style={'fontSize': '10px', "width": "280px", "textAlign": "center", "height":"10px"}),
                    html.Div(
                        children=[],
                        id='wafer-map-{i}',
                        style={'height': '280px', 'width': '280px'},
                    )
                    # dcc.Graph(
                    #     id={'type': 'wafermap', 'index': i},
                    #     # figure=generate_plotly_wafermap(wafer_data=wafer_data),
                    #     figure=generate_plotly_heatmap(df=wafer_data),
                    #     config={'displaylogo': False, 'scrollZoom': False},
                    #     style={'width': '280px', 'height': '280px'}
                    # ),
                    # fac.AntdSpace([
                    #     fac.AntdProgress(percent=80, steps=10, size='small'),
                    #     fac.AntdProgress(percent=72, steps=10, size='small'),
                    #     fac.AntdProgress(percent=61, steps=10, size='small'),
                    #     fac.AntdProgress(percent=23, steps=10, size='small'),
                    #     fac.AntdProgress(percent=12, steps=10, size='small'),
                    # ], direction='vertical', style={'width': '280px', 'height': '50px'}),
                ], direction='vertical', style={'width': '280px', 'height': '100%'}),    
            ], style={'width': '300px', 'height': '350px', 'padding': '10px'})
        )
    
    wafer_maps = fac.AntdCard(
            wafer_maps_cards,
            title='Root Lot ID: AAAAA',
            style={'height': '100%', 'overflow': 'auto', 'width': '100%'},
        )
    
    return html.Div([
        fac.AntdSplitter(
            items=[
                {
                    'children': fuc.FefferyLazyLoad(
                            fac.AntdCenter(
                                wafer_maps, style={'height': '600px'}
                            )
                        ),
                    'defaultSize': '80%',
                },
                {
                    'children': fac.AntdCenter(
                        'Color Bar Setting', style={'height': '100%'}
                    ),
                    'min': 0,
                    'max': '30%',
                    'defaultSize': '10%',
                },
            ],
            style={
                'height': '100%',
                'boxShadow': '0 0 10px rgba(0, 0, 0, 0.1)',
            },
        ),
    ])
    

clientside_callback(
    """
    function(waferData) {
        console.log(waferData);
    }
    """,
    Output('wafer-data-store', 'data'),
    Input('wafer-data-store', 'data')
)