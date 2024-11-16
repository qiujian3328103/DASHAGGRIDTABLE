import pandas as pd 
from config import TEST_WAFER_MAP_SAMPLE_DATA
import plotly.graph_objs as go
import numpy as np 
def create_wafer_data_for_plotly(root_lot_id):
    """similar to create_wafer_data, but more suitable for plotly plot data strcuture

    Args:
        root_lot_id (_type_): _description_
    """
    # TEST_WAFER_MAP_SAMPLE_DATA = r'/Users/JianQiu/Dropbox/pythonprojects/DashAggridTable/test/sample_wafermap_data.csv'
    df_raw = pd.read_csv(TEST_WAFER_MAP_SAMPLE_DATA, index_col=False)
    
    # filter out rows based on "sort_test_flag"
    df = df_raw[df_raw["sort_test_flag"] == "T"]
    width = 7270.96*0.001
    height = 6559.46*0.001
    
    df['x0'] = df['ucs_die_origin_x']*0.001 - width/2
    df['x1'] = df['ucs_die_origin_x']*0.001 + width/2
    df['y0'] = df['ucs_die_origin_y'] *0.001 - height/2
    df['y1'] = df['ucs_die_origin_y']*0.001 + height/2
    
    df["color"] = "green"
    
    return df[['x0', 'x1', 'y0', 'y1', 'color', 'bin_value', 'sort_die_x', 'sort_die_y']]

def create_wafer_data(root_lot_id):
    # TEST_WAFER_MAP_SAMPLE_DATA = r'/Users/JianQiu/Dropbox/pythonprojects/DashAggridTable/test/sample_wafermap_data.csv'
    df_raw = pd.read_csv(TEST_WAFER_MAP_SAMPLE_DATA, index_col=False)
    
    # Filter out rows based on "sort_test_flag"
    df = df_raw[df_raw["sort_test_flag"] == "T"]
    width = 7270.96*0.001
    height = 6559.46*0.001

    df['left'] = df['ucs_die_origin_x']*0.001 
    df['right'] = df['ucs_die_origin_x']*0.001
    df['bottom'] = df['ucs_die_origin_y'] *0.001
    df['top'] = df['ucs_die_origin_y']*0.001
    # Setting the width and height
    
    df["shot_bottom"] = df["ucs_die_y"]
    df["shot_left"] = df["ucs_die_x"]
    # shot_width = 5
    # shot_height = 12

    # Map the ucs_die_origin_x and ucs_die_origin_y to x and y, and set color
    # df["color"] = "green"
    
    # Generate a list of dictionaries to match the format needed for D3.js
    single_wafer_data = df.apply(lambda row: {
        "x": row["left"],
        "y": row["bottom"],
        "color": row["color"],
        "bin_value": row["bin_value"],
        "mouseover": f"Die_X: {int(row['sort_die_x'])}\nDie_Y: {int(row['sort_die_y'])}"
    }, axis=1).tolist()
    

    # print(df)
    # # Generate a list of dictionaries to match the format needed for D3.js
    single_shot_data = df.apply(lambda row: {
        "x": row["shot_left"],
        "y": row["shot_bottom"],
        "color": row["color"],
    }, axis=1).tolist()
    
    wafer_data = single_wafer_data
    shot_data = single_shot_data
    

    return wafer_data, shot_data, width, height


def create_wafer_data_as_dataframe(root_lot_id):
    # TEST_WAFER_MAP_SAMPLE_DATA = r'/Users/JianQiu/Dropbox/pythonprojects/DashAggridTable/test/sample_wafermap_data.csv'
    df_raw = pd.read_csv(TEST_WAFER_MAP_SAMPLE_DATA, index_col=False)
    
    # Filter out rows based on "sort_test_flag"
    df = df_raw[df_raw["sort_test_flag"] == "T"]
    width = 7270.96*0.001
    height = 6559.46*0.001

    df['left'] = df['ucs_die_origin_x']*0.001 - width/2
    df['right'] = df['ucs_die_origin_x']*0.001 + width/2
    df['bottom'] = df['ucs_die_origin_y'] *0.001 - height/2
    df['top'] = df['ucs_die_origin_y']*0.001 + height/2
    # Setting the width and height
    
    df["shot_bottom"] = df["ucs_die_y"]
    df["shot_left"] = df["ucs_die_x"]
    # shot_width = 5
    # shot_height = 12

    return df


def generate_square_coordinates(x0, x1, y0, y1):
    return ([x0, x0, x1, x1, x0], [y0, y1, y1, y0, y0])

def generate_plotly_wafermap(wafer_data=None, root_lot_id=None, wafer_id=None, shot_data=None, width=None, height=None):
    """Generate an optimized Plotly wafer map based on wafer_data."""
    
    # Create a dictionary for bin group colors
    color_discrete = wafer_data.groupby("bin_group")["color"].first().to_dict()

    # Calculate yield
    lot_wafer_info = f"Root Lot ID: {root_lot_id}<br>Wafer ID: {wafer_id}"
    yield_value = round((wafer_data["gross_bin_type"].value_counts().get("G", 0) / len(wafer_data)) * 100, 2)

    # Initialize the figure
    fig = go.Figure()

    # Add a circle shape for the wafer boundary
    fig.add_shape(type='circle', xref='x', yref='y', x0=-150, y0=-150, x1=150, y1=150, line=dict(color='black', width=1))

    # Add yield and wafer info annotations
    fig.add_annotation(x=-150, y=150, text=f"Yield: {yield_value}%", showarrow=False, font=dict(size=12, color='black'))
    fig.add_annotation(x=150, y=150, text=lot_wafer_info, showarrow=False, font=dict(size=12, color='black'))

    # Prepare data for vectorized processing
    wafer_data['x0'] = wafer_data['left']
    wafer_data['x1'] = wafer_data['right']
    wafer_data['y0'] = wafer_data['bottom']
    wafer_data['y1'] = wafer_data['top']
    wafer_data['hover_text'] = (
        "Die_X: " + wafer_data['sort_die_x'].astype(str) +
        "<br>Die_Y: " + wafer_data['sort_die_y'].astype(str) +
        "<br>Bin: " + wafer_data['bin_value']
    )

    # Vectorized shape generation using groupby
    traces = []
    for bin_group, group in wafer_data.groupby("bin_group"):
        color = color_discrete[bin_group]
        nan_array = np.full(len(group), np.nan)
        x_coords = np.vstack([group['x0'], group['x0'], group['x1'], group['x1'], group['x0'], nan_array]).T.flatten()
        y_coords = np.vstack([group['y0'], group['y1'], group['y1'], group['y0'], group['y0'], nan_array]).T.flatten()

        hover_texts = np.repeat(group['hover_text'].values, 6)

        # Add scatter trace for each bin group
        traces.append(go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='lines',
            line=dict(color=color, width=1),
            fill='toself',
            fillcolor=color,
            hoverinfo='text',
            hoveron='points+fills',
            text=hover_texts,
            name=bin_group
        ))

    # Add all traces to the figure at once
    fig.add_traces(traces)

    # Update layout
    fig.update_layout(
        xaxis=dict(range=[-151, 151], showgrid=False, zeroline=False, showline=False, showticklabels=False),
        yaxis=dict(range=[-151, 151], showgrid=False, zeroline=False, showline=False, ticks='', showticklabels=False),
        plot_bgcolor='white',
        scene=dict(aspectratio=dict(x=1, y=1, z=1)),
        margin=dict(l=0, r=0, b=0, t=0),
        height=280,
        showlegend=False
    )

    return fig

# def generate_plotly_wafermap(wafer_data=None, root_lot_id=None, wafer_id=None, shot_data=None, width=None, height=None):
#     """Generate a plotly wafermap based on the wafer_data and shot_data

#     Args:
#         wafer_data (list[dict]): A list of dictionaries containing the wafer data
#         root_lot_id (str): The root lot id
#         wafer_id (str): The wafer id
#         shot_data (list[dict]): A list of dictionaries containing the shot data
#         width (float): The width of the wafer
#         height (float): The height of the wafer

#     Returns:
#         plotly.graph_objs.Figure: A plotly figure object
#     """
#     import plotly.graph_objs as go
#     # print(wafer_data)
#     color_discrete = {}
#     for bin_group in wafer_data["bin_group"].unique():
#         COLOR = wafer_data[wafer_data["bin_group"] == bin_group]["color"].tolist()
#         color_discrete.update({bin_group: COLOR[0]})

#     # calcuate the yield for wafer, sum the GROSS_BIN_GROUp value equal to 'G'
#     lot_wafer_info = f"Root Lot ID: {root_lot_id}<br>Wafer ID: {wafer_id}"

#     # yield calculation 
#     yield_value = round((wafer_data['gross_bin_type'].value_counts()['G'] / len(wafer_data)) * 100, 2)

#     # Create a scatter plot for the wafer data
#     fig = go.Figure()
#     # add square shapes for each die in the fig 
#     fig.add_shape(type='circle', xref='x', yref='y', x0=-150, y0=-150, x1=150, y1=150, line=dict(color='black', width=1))
#     # add an annotation for yield number 
#     fig.add_annotation(x=-150, y=150, text=f"Yield: {yield_value}%", showarrow=False, font=dict(size=12, color='black'))
#     # add an annotation for lot and wafer info
#     fig.add_annotation(x=150, y=150, text=lot_wafer_info, showarrow=False, font=dict(size=12, color='black'))

#     # add th wafer-data using scatter to draw the wafermap 
#     for bin_group in color_discrete.keys():
#         filter_df = wafer_data[wafer_data["bin_group"] == bin_group]
#         color = filter_df["color"].tolist()[0]
#         all_x = []
#         all_y = []
#         text_data = []
#         for index, row in filter_df.iterrows():
#             x, y = generate_square_coordinates(row["left"], row["right"], row["bottom"], row["top"])
#             all_x.extend(x)
#             all_y.extend(y)
#             # add break on each die to make the die clear 
#             all_x.append(None)
#             all_y.append(None)
#             hover_text = f"Die_X: {row['sort_die_x']}<br>Die_Y: {row['sort_die_y']}<br>Bin: {row['bin_value']}"
#             text_data.extend([hover_text] * 5)
#             text_data.append(None)

#         fig.add_trace(go.Scatter(
#             x=all_x,
#             y=all_y,
#             mode='lines',
#             line=dict(color=color, width=1),
#             fill='toself',
#             fillcolor=color,
#             hoverinfo='text',
#             hoveron='points+fills',
#             text=text_data,
#             name=bin_group
#         ))

#         # update the layout 
#         fig.update_layout(
#             xaxis=dict(
#                 range=[-151, 151],
#                 showgrid=False,
#                 zeroline=False,
#                 showline=False,
#                 showticklabels=False
#             ),
#             yaxis=dict(
#                 range=[-151, 151],
#                 showgrid=False,
#                 zeroline=False,
#                 showline=False,
#                 ticks='',
#                 showticklabels=False
#             ),
#             plot_bgcolor='white',
#             scene=dict(aspectratio=dict(x=1, y=1, z=1)),
#             margin=dict(l=0, r=0, b=0, t=0),
#             height=280,
#             showlegend=False
#         )

#         return fig 


