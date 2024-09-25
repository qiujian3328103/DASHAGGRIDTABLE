import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html

# Sample DataFrame (replace with your actual data)
data = {
    'year-month': ['2024-01', '2024-01', '2024-01', '2024-01', '2024-02', '2024-02', '2024-02', '2024-02', 
                   '2024-03', '2024-03', '2024-03', '2024-03', '2024-04', '2024-05', '2024-06', '2024-07'],
    'status': ['KIV', 'CLose', 'Open', 'New', 'KIV', 'CLose', 'Open', 'New', 'KIV', 'CLose', 'Open', 'New', 
               'KIV', 'CLose', 'Open', 'New'],
    'count': [0, 2, 1, 4, 2, 2, 14, 2, 1, 24, 5, 2, 12, 2, 1, 3]
}

df = pd.DataFrame(data)

# Calculate closed ratio for each year-month
df_grouped = df.groupby('year-month').agg(total_count=('count', 'sum'), close_count=('count', lambda x: x[df['status'] == 'CLose'].sum()))
df_grouped['closed_ratio'] = df_grouped['close_count'] / df_grouped['total_count']

# Create stacked bar traces for each status
statuses = df['status'].unique()
bar_traces = []

for status in statuses:
    bar_traces.append(
        go.Bar(
            x=df[df['status'] == status]['year-month'],
            y=df[df['status'] == status]['count'],
            name=status,
            hovertemplate=
            '<b>Year-Month:</b> %{x}<br>' +
            '<b>Status:</b> %{name}<br>' +
            '<b>Count:</b> %{y}<extra></extra>',  # Custom hovertemplate
        )
    )

# Create the line trace for the closed ratio, showing text for each point
line_trace = go.Scatter(
    x=df_grouped.index,
    y=df_grouped['closed_ratio'],
    mode='lines+markers+text',
    name='Closed Ratio',
    yaxis='y2',
    hovertemplate=
    '<b>Year-Month:</b> %{x}<br>' +
    '<b>Closed Ratio:</b> %{y:.2f}<extra></extra>',  # Custom hovertemplate for the line
    text=df_grouped['closed_ratio'].round(2),  # Display the rounded closed ratio as text
    textposition='top center'  # Position the text above the data points
)

# Set up the layout for secondary y-axis and legend position
layout = go.Layout(
    title="Status Stacked Bar with Closed Ratio Line",
    xaxis=dict(title='Year-Month'),
    yaxis=dict(title='Count'),
    yaxis2=dict(
        title='Closed Ratio',
        overlaying='y',
        side='right'
    ),
    barmode='stack',
    legend=dict(
        orientation="h",  # Horizontal orientation for the legend
        yanchor="bottom",  # Anchor the legend at the bottom
        y=1.02,  # Position it slightly above the plot area
        xanchor="center",  # Center the legend horizontally
        x=0.5  # Horizontal centering
    )
)

# Create figure
fig = go.Figure(data=bar_traces + [line_trace], layout=layout)

# Set up Dash app
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
