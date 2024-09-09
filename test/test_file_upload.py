import dash
from dash import html
import feffery_antd_components as fac
from dash.dependencies import Input, Output, State
import base64
from flask import request, jsonify

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    fac.AntdPictureUpload(
        id='picture-upload-demo',
        apiUrl='/upload/',
        buttonContent='Select Image',
        uploadId='test-picture-upload',
        locale='en-us',
        fileMaxSize=5,
    ),
    html.Div(id='upload-output')
])


# Route to handle file upload
@app.server.route('/upload/', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Read and encode file content
    file_content = file.read()
    encoded_content = base64.b64encode(file_content).decode('utf-8')
    
    # Return success response
    return jsonify({
        'status': 'success',
        'fileName': file.filename,
        'fileContent': encoded_content
    })

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
