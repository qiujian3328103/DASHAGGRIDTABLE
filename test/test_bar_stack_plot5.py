import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html

# Sample DataFrame (replace with your actual data)
data = {
    'year-month': ['2024-01', '2024-01', '2024-01', '2024-01', '2024-02', '2024-02', '2024-02', '2024-02',
                   '2024-03', '2024-03', '2024-03', '2024-03', '2024-04', '2024-04', '2024-04', '2024-04'],
    'sba_type': ['EDS', 'FT', 'EDS Logic', 'EDS Sort', 'EDS', 'FT', 'EDS Logic', 'EDS Sort',
                 'EDS', 'FT', 'EDS Logic', 'EDS Sort', 'EDS', 'FT', 'EDS Logic', 'EDS Sort'],
    'tat': [1.22, 2.11, 2.1, 23.1, 3.1, 24.1, 32.1, 21.1, 43.1, 54.1, 23.1, 54.3, 23.1, 23, 42.2, 21.1]
}

df = pd.DataFrame(data)

# Treat year-month as categorical (string) values
df['year-month'] = df['year-month'].astype(str)

# Create stacked bar chart traces
bar_traces = []
sba_types = df['sba_type'].unique()

for sba in sba_types:
    filtered_df = df[df['sba_type'] == sba]
    bar_traces.append(
        go.Bar(
            x=filtered_df['year-month'],
            y=filtered_df['tat'],
            name=sba,
            text=filtered_df['tat'],  # Display the TAT value inside the bar
            textposition='auto',  # Automatically position the text inside the bar
            hovertemplate='<b>Year-Month:</b> %{x}<br><b>SBA Type:</b> %{name}<br><b>TAT:</b> %{y}<extra></extra>',
        )
    )

# Set up the layout
layout = go.Layout(
    title="Stacked Bar Chart of TAT by Year-Month and SBA Type",
    xaxis=dict(
        title='Year-Month',
        type='category',  # Ensure the x-axis treats 'year-month' as categorical
        tickangle=-45,  # Rotate the labels for better readability
        automargin=True  # Adjust margins for labels
    ),
    yaxis=dict(title='TAT (Sum)'),
    barmode='stack',  # Stack the bars
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
