import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html

# Sample DataFrame (replace with your actual data)
data = {
    'department': ['CVD', 'CVD', 'CVD', 'CVD', 'PVD', 'PVD', 'PVD', 'PVD', 
                   'Photo', 'Photo', 'Photo', 'Photo', 'Metal', 'Metal', 'Metal', 'Metal'],
    'status': ['KIV', 'Closed', 'Open', 'New', 'KIV', 'Closed', 'Open', 'New', 
               'KIV', 'Closed', 'Open', 'New', 'KIV', 'Closed', 'Open', 'New'],
    'count': [2, 3, 4, 1, 4, 2, 2, 1, 4, 4, 2, 2, 4, 5, 2, 1]
}

df = pd.DataFrame(data)

# Calculate the total count per department and sort by this total
df_total = df.groupby('department')['count'].sum().reset_index()
df_total = df_total.sort_values(by='count', ascending=False)

# Sort the main DataFrame based on the sorted department order
df['department'] = pd.Categorical(df['department'], categories=df_total['department'], ordered=True)
df = df.sort_values('department')

# Create stacked bar chart traces
bar_traces = []
statuses = df['status'].unique()

for status in statuses:
    filtered_df = df[df['status'] == status]
    bar_traces.append(
        go.Bar(
            x=filtered_df['department'],
            y=filtered_df['count'],
            name=status,
            text=filtered_df['count'],  # Display value inside the bar
            textposition='auto',  # Automatically positions the text inside the bar
            hovertemplate='<b>Department:</b> %{x}<br><b>Status:</b> %{name}<br><b>Count:</b> %{y}<extra></extra>',
        )
    )

# Set up the layout
layout = go.Layout(
    title="Stacked Bar Chart by Department and Status (Sorted by Total Count)",
    xaxis=dict(title='Department'),
    yaxis=dict(title='Count'),
    barmode='stack',
    height=600,  # Increase the chart height for better visibility
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    )
)

# Create figure
fig = go.Figure(data=bar_traces, layout=layout)

# Set up Dash app
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
