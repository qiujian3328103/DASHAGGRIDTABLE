from dash import html

def create_summary_page():
    return html.Div([
        html.H1("Summary Page"),
        # Add your summary page components here
        html.P("This is the summary page content.")
    ])