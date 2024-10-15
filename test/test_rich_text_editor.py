import os
import dash
from dash import html
from flask import request, send_file
import feffery_antd_components as fac
import feffery_utils_components as fuc
import feffery_markdown_components as fmc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        fuc.FefferyRichTextEditor(
            id='rich-text-editor',
            locale='en',
            mode='simple',
            style={
                'width': '50%',
                'margin': '25px auto'
            },
            editorStyle={
                'height': '500px'
            },
            # uploadImage={
            #     'server': '/upload/',
            #     'fieldName': 'file'
            # },
            # uploadVideo={
            #     'server': '/upload/',
            #     'fieldName': 'file'
            # }
        ),
        html.Div(
            [
                fac.AntdDivider('html渲染效果', innerTextOrientation='left'),
                fmc.FefferyMarkdown(
                    id='output-html',
                    renderHtml=True
                )
            ],
            style={
                'width': '50%',
                'margin': '25px auto'
            }
        ),
    ],
    id='app-container'
)


@app.callback(
    Output('output-html', 'markdownStr'),
    Input('rich-text-editor', 'htmlValue'),
    prevent_initial_call=True
)
def callback_output(htmlValue):
    return htmlValue


@app.server.route('/upload/', methods=['POST'])
def upload():
    '''
    构建文件上传服务
    :return:
    '''

    # 获取上传的文件名称
    filename = request.files['file'].filename

    # 基于上传id，若本地不存在则会自动创建目录
    try:
        os.mkdir(os.path.join('cache'))
    except FileExistsError:
        pass
    try:
        # 流式写出文件到指定目录
        with open(os.path.join('cache', filename), 'wb') as f:
            # 流式写出大型文件，这里的10代表10MB
            for chunk in iter(lambda: request.files['file'].read(1024 * 1024 * 10), b''):
                f.write(chunk)

        return {
            "errno": 0,
            "data": {
                "url": "http://127.0.0.1:8050/get?filename=" + filename,
                "alt": "yyy",
                "href": "zzz"
            }
        }
    except Exception as e:
        return {
            "errno": 1,
            "message": str(e)
        }


@app.server.route('/get', methods=['GET'])
def get_file():
    filename = request.args.get('filename')  # 从查询字符串中获取文件名
    # 检查文件是否存在，这里省略相关逻辑

    # 返回文件
    return send_file(os.path.join('cache', filename), as_attachment=True)


if __name__ == '__main__':
    app.run_server(debug=True)
