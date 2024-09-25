import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html

# Sample DataFrame (replace with your actual data)
data = {
    'sba_type': ['EDS', 'EDS', 'EDS', 'EDS', 'EDS', 'EDS', 'EDS', 'EDS', 'EDS', 'EDS', 'EDS', 'FT', 'FT', 'FT', 'FT', 'FT', 'FT', 'FT', 'FT', 'FT', 'FT', 'FT', 'EDS Logic', 'EDS Logic', 'EDS Logic', 'EDS Logic', 'EDS Logic', 'EDS Logic', 'EDS Logic', 'EDS Logic', 'EDS Logic', 'EDS Logic', 'EDS Logic'],
    'product': ['product1', 'product2', 'product3', 'product4', 'product5', 'product6', 'product7', 'product8', 'product9', 'product10', 'product11', 'product1', 'product2', 'product3', 'product4', 'product5', 'product6', 'product7', 'product8', 'product9', 'product10', 'product11', 'product1', 'product2', 'product3', 'product4', 'product5', 'product6', 'product7', 'product8', 'product9', 'product10', 'product11'],
    'count': [2, 12, 4, 2, 1, 1, 4, 32, 2, 3, 4, 1, 2, 3, 3, 4, 5, 4, 3, 4, 6, 3, 2, 3, 4, 2, 2, 5, 4, 6, 4, 3, 2]
}

df = pd.DataFrame(data)

# Calculate total count per product
df_total = df.groupby('product')['count'].sum().reset_index()
df_total = df_total.sort_values(by='count', ascending=False)

# Sort the main DataFrame based on the sorted products
df['product'] = pd.Categorical(df['product'], categories=df_total['product'], ordered=True)
df = df.sort_values('product')

# Create stacked bar chart traces
bar_traces = []
sba_types = df['sba_type'].unique()

for sba in sba_types:
    filtered_df = df[df['sba_type'] == sba]
    bar_traces.append(
        go.Bar(
            x=filtered_df['product'],
            y=filtered_df['count'],
            name=sba,
            text=filtered_df['count'],  # Display value inside the bar
            textposition='auto',  # Automatically positions the text inside the bar
            hovertemplate='<b>Product:</b> %{x}<br><b>Type:</b> %{name}<br><b>Count:</b> %{y}<extra></extra>',
        )
    )

# Set up the layout
layout = go.Layout(
    title="Stacked Bar Chart by Product and SBA Type",
    xaxis=dict(title='Product'),
    yaxis=dict(title='Count'),
    barmode='stack',
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
