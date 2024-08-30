from dash import Dash, dcc, html, Input, Output, callback_context
import base64
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Textarea(
        id='paste-area',
        placeholder="Paste your image here...",
        style={
            'width': '100%',
            'height': '100px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
        }
    ),
    html.Div(id='output-image-upload'),
    dcc.Store(id='image-content-store')
])

def save_file(name, content):
    """Decode and save the uploaded file."""
    data = content.split(',')[1]
    with open(os.path.join(os.getcwd(), name), "wb") as fp:
        fp.write(base64.b64decode(data))

@app.callback(
    Output('output-image-upload', 'children'),
    Input('image-content-store', 'data')
)
def update_output(data):
    if data is not None:
        filename = 'pasted_image.png'
        save_file(filename, data)
        return html.Div(['Image pasted and saved successfully!'])

# Custom script to handle paste event
app.clientside_callback(
    """
    function(n_clicks) {
        if (!window._dash_paste_listener) {
            window._dash_paste_listener = true;
            document.addEventListener('paste', function(event) {
                var items = event.clipboardData.items;
                for (var i = 0; i < items.length; i++) {
                    if (items[i].kind === 'file') {
                        var blob = items[i].getAsFile();
                        var reader = new FileReader();
                        reader.onload = function(event) {
                            var dataURL = event.target.result;
                            var contentStore = document.querySelector('#image-content-store');
                            var evt = new CustomEvent('dash-update', {
                                detail: {id: contentStore.id, prop: 'data', value: dataURL}
                            });
                            contentStore.dispatchEvent(evt);
                        };
                        reader.readAsDataURL(blob);
                    }
                }
            });
        }
        return '';
    }
    """,
    Output('paste-area', 'value'),
    Input('paste-area', 'n_clicks'),
)

if __name__ == '__main__':
    app.run(debug=True)
