import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
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

# Set layout properties
fig.update_layout(
    title="Heatmap by SBA Group",
    height=600,
    width=1200,
    showlegend=False
)

# Initialize Dash app
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
