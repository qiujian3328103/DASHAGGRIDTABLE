import dash
from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc


def create_customized_image_card(image_url):
    return fac.AntdCard(
        [
            fac.AntdButton(
                fac.AntdIcon(icon="antd-close"),
                type="text",
                style={"position": "absolute", "top": "5px", "right": "5px"},
                id="close-button"
            ),
            fac.AntdImage(
                src=image_url,
                style={"width": "100%", "height": "auto"}
            )
        ],
        style={
            "width": "100px",
            "position": "relative"
        },
        headStyle={
            "padding": "5px 10px",  # Controls the padding inside the header
            "fontSize": "14px",  # Controls the font size of the title
            "lineHeight": "20px",  # Controls the line height of the title text
            "height": "30px",  # Set an explicit height for the header
            "overflow": "hidden"  # Ensures content fits within the specified height
        },
        bodyStyle={
            "padding": "0"  # Remove padding in the card body
        }, 
        size="small"
    )


# Example usage in a Dash layout
app = dash.Dash(__name__)

app.layout = html.Div(
    [
        create_customized_image_card(
            image_url="https://example.com/your-image.jpg",
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
