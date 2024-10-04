import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
from plotly.subplots import make_subplots

# Sample DataFrame (replace this with your actual data)
data = {
    'chip_x_pos': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'chip_y_pos': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'BIN_COUNTS': [2, 3, 2, 41, 2, 3, 1, 1, 2, 1, 2, 3, 1, 3, 2, 4, 6, 7, 4, 3, 4, 5, 6, 3, 2, 4, 4, 3, 3, 2, 6, 7, 7, 5, 4, 3, 2, 4, 5, 7],
    'sba_group': ['POR', 'POR', 'POR', 'POR', 'POR', 'POR', 'POR', 'POR', 'POR', 'POR', 'POR', 'POR', 'POR', 'POR', 'POR', 'POR', 'POR', 'POR', 'POR', 'POR',
                  'SBA', 'SBA', 'SBA', 'SBA', 'SBA', 'SBA', 'SBA', 'SBA', 'SBA', 'SBA', 'SBA', 'SBA', 'SBA', 'SBA', 'SBA', 'SBA', 'SBA', 'SBA', 'SBA', 'SBA']
}

df = pd.DataFrame(data)

# Get unique sba_group values
sba_groups = df['sba_group'].unique()

# Create subplots: one subplot per sba_group
fig = make_subplots(
    rows=1, cols=len(sba_groups), 
    subplot_titles=sba_groups,
    horizontal_spacing=0.1
)

# Iterate through each sba_group and create a heatmap for it
for i, group in enumerate(sba_groups):
    # Filter data for each sba_group
    group_df = df[df['sba_group'] == group]
    
    # Aggregate BIN_COUNTS by summing up the values for duplicate positions
    group_df = group_df.groupby(['chip_x_pos', 'chip_y_pos'], as_index=False)['BIN_COUNTS'].sum()
    
    # Create a pivot table for heatmap data
    heatmap_data = group_df.pivot(index='chip_y_pos', columns='chip_x_pos', values='BIN_COUNTS').fillna(0)
    
    # Create heatmap
    heatmap = go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Viridis',
        colorbar=dict(title='BIN_COUNTS'),
        showscale=True if i == len(sba_groups) - 1 else False  # Show the color scale only on the last subplot
    )
    
    # Add heatmap to subplot
    fig.add_trace(heatmap, row=1, col=i+1)

# Reverse y-axis for all subplots
fig.update_yaxes(autorange='reversed')

# Set layout properties
fig.update_layout(
    title="Heatmap by SBA Group",
    showlegend=False,
    autosize=True  # Enable autosize for dynamic resizing
)

# Initialize Dash app
app = Dash(__name__)

# Main layout of the app with an AntdCard
app.layout = html.Div([
    fac.AntdCard(
        dcc.Graph(
            id='heatmap-graph',
            figure=fig,
            style={
                'backgroundColor': '#e0f7fa',  # Add background color to the graph for visibility
                'height': '100%',  # Make the graph height adapt to the card size
                'width': '100%'    # Make the graph width adapt to the card size
            }
        ),
        style={
            'width': '100%', 
            'height': '600px',  # Initial height for the card
            'minHeight': '400px',
            # 'resize': 'both',  # Enable resizing of the card
            # 'overflow': 'auto',  # Handle content overflow when resizing
            'border': '1px solid #ccc',  # Optional: for visual effect
            'backgroundColor': '#ffeb3b'  # Background color for the card for visibility
        }
    ),
    # Add a hidden div to store the window size
    html.Div(id="window-size", style={"display": "none"})
])



@app.callback(
    Output('heatmap-graph', 'figure'),
    [Input('window-size', 'children')],
    [State('heatmap-graph', 'figure')]
)
def resize_graph(window_size, current_fig):
    if window_size:
        width, height = window_size.split(',')
        # Dynamically adjust the width and height based on the window size
        current_fig['layout']['width'] = int(width) * 0.9
        current_fig['layout']['height'] = int(height) * 0.8
    return current_fig


if __name__ == '__main__':
    app.run_server(debug=True)
