import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import base64
import io
import plotly.graph_objects as go

# Create a sample Plotly plot
def create_plot():
    fig = px.scatter(x=[1, 2, 3, 4, 5], y=[10, 11, 12, 13, 14], labels={'x': 'X Axis', 'y': 'Y Axis'})
    return fig

# Convert the Plotly plot to a base64-encoded image
def fig_to_base64(fig):
    # Save the figure to a buffer
    buf = io.BytesIO()
    fig.write_image(buf, format="png")
    buf.seek(0)
    
    # Convert the image to base64
    encoded_image = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded_image}"

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='plot', figure=create_plot()),  # Display the plot
    html.Button("Convert to Image", id='convert-button', n_clicks=0),  # Button to convert plot
    html.Img(id='plot-image', style={'display': 'block', 'margin-top': '20px'})  # Display the converted image
])

@app.callback(
    Output('plot-image', 'src'),
    Input('convert-button', 'n_clicks'),
    State('plot', 'figure')
)
def convert_plot_to_image(n_clicks, figure):
    if n_clicks > 0:
        # Convert the Plotly figure to a base64 image
        fig = go.Figure(figure)
        base64_image = fig_to_base64(fig)
        return base64_image
    return None

if __name__ == '__main__':
    app.run_server(debug=True)